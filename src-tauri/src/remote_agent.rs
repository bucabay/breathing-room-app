//! Authenticated remote reasoning. All filesystem tools remain native.
use crate::{cleanup_session as session, model::now, runtime_store as store, system};
use base64::{engine::general_purpose::URL_SAFE_NO_PAD,Engine};
use reqwest::blocking::Client;
use serde::{Deserialize,Serialize};
use serde_json::{json,Value};
use sha2::{Digest,Sha256};
use std::{io::{Read,Write},net::{TcpListener,TcpStream},path::Path,sync::Mutex,thread,time::{Duration,Instant}};

static AUTH_LOCK:Mutex<()>=Mutex::new(());
const DEFAULT_CONFIG:&str=include_str!("../../src/agent-config.json");
#[derive(Default,Clone,Serialize,Deserialize)]
#[serde(rename_all="camelCase")]
struct Credentials{
    #[serde(default)]access_token:String,#[serde(default)]refresh_token:String,#[serde(default)]expires_at:u64,
    #[serde(default)]account:Value,#[serde(default)]pending:Option<Pending>,
    #[serde(default)]last_login_id:Option<String>,
}
#[derive(Clone,Serialize,Deserialize)]struct Pending{id:String,verifier:String,expires_at:u64,#[serde(default)]callback_code:Option<String>,#[serde(default)]error:Option<String>}
fn digest(text:&str)->String{URL_SAFE_NO_PAD.encode(Sha256::digest(text.as_bytes()))}
fn random()->Result<String,String>{let mut b=[0u8;32];std::fs::File::open("/dev/urandom").and_then(|mut f|f.read_exact(&mut b)).map_err(|e|e.to_string())?;Ok(URL_SAFE_NO_PAD.encode(b))}
fn client()->Result<Client,String>{Client::builder().timeout(Duration::from_secs(90)).connect_timeout(Duration::from_secs(10)).redirect(reqwest::redirect::Policy::none()).build().map_err(|_|"Could not initialize API connection".into())}
fn valid_url(raw:&str)->Result<String,String>{
    let url=reqwest::Url::parse(raw).map_err(|_|"Use an HTTPS API origin")?;
    let loopback=matches!(url.host_str(),Some("127.0.0.1"|"localhost"|"[::1]"));
    if (url.scheme()!="https"&&!(url.scheme()=="http"&&loopback))||!url.username().is_empty()||url.password().is_some()||url.query().is_some()||url.fragment().is_some()||url.path()!="/"{return Err("Use an exact HTTPS API origin, or HTTP loopback for development".into());}
    Ok(url.as_str().trim_end_matches('/').into())
}
pub fn base_url()->Result<String,String>{
    if let Ok(url)=std::env::var("BREATHING_ROOM_API_URL"){return valid_url(&url);}
    let h=system::user_home()?;
    let saved=store::cache_get(&h,"api-config")?;
    let config=saved.unwrap_or_else(||serde_json::from_str(DEFAULT_CONFIG).unwrap());
    valid_url(config["baseUrl"].as_str().ok_or("API origin is missing")?)
}
pub fn configure(url:String)->Result<(),String>{let base=valid_url(&url)?;store::cache_put(&system::user_home()?,"api-config",&json!({"baseUrl":base}),None)}
fn load_credentials(base:&str)->Result<Credentials,String>{
    load_credentials_at(&system::user_home()?,base)
}
fn load_credentials_at(home:&Path,base:&str)->Result<Credentials,String>{match store::auth_load(home,base)?{Some(value)=>serde_json::from_value(value).map_err(|_|"Saved app session is invalid; sign in again".into()),None=>Ok(Credentials::default())}}
fn save_credentials(base:&str,value:&Credentials)->Result<(),String>{save_credentials_at(&system::user_home()?,base,value)}
fn save_credentials_at(home:&Path,base:&str,value:&Credentials)->Result<(),String>{store::auth_save(home,base,&serde_json::to_value(value).map_err(|_|"Could not save app sign-in")?)}
fn response(response:reqwest::blocking::Response)->Result<(u16,Value),String>{
    let status=response.status().as_u16();let mut bytes=vec![];
    response.take(1_048_577).read_to_end(&mut bytes).map_err(|_|"API response was interrupted")?;
    if bytes.len()>1_048_576{return Err("API response exceeded the size limit".into());}
    let value:Value=serde_json::from_slice(&bytes).map_err(|_|"API returned an invalid response")?;
    Ok((status,value))
}
fn error(status:u16,value:&Value)->String{
    match value["error"].as_str().unwrap_or(""){
        "sign_in_required"|"session_expired"=>"Sign in to Breathing Room to use the remote agent".into(),
        "auth_not_configured"=>"The API's AnyOAuth login is not configured yet".into(),
        "login_expired"|"login_failed"=>"Sign-in expired or failed. Start sign-in again".into(),
        "daily_usage_limit"|"step_limit"=>"Agent usage limit reached; cached results remain available".into(),
        "inference_unavailable"=>"Workers AI is temporarily unavailable or its allowance is exhausted".into(),
        "invalid_model_response"|"incomplete_model_response"|"invalid_candidate_selection"=>"The model could not complete its review. Start a new inspection; your files have not been changed.".into(),
        "step_failed_start_new_run"=>"The previous inference step failed. Start a new inspection".into(),
        "billing_not_ready"=>"AI Care checkout is temporarily unavailable. Please try again later.".into(),
        "subscription_already_exists"=>"You already have an AI Care subscription. Choose Manage subscription to make changes.".into(),
        "checkout_already_starting"=>"Checkout is already opening. Please wait a moment and try again.".into(),
        "billing_customer_missing"=>"No AI Care billing account was found for this sign-in.".into(),
        _=>format!("Agent API could not complete this request (HTTP {status})"),
    }
}
fn public_post(base:&str,path:&str,input:&Value)->Result<(u16,Value),String>{response(client()?.post(format!("{base}{path}")).json(input).send().map_err(|_|"Could not reach the Breathing Room API")?)}
fn authenticated(base:&str,force_refresh:bool)->Result<Credentials,String>{
    let _lock=AUTH_LOCK.lock().map_err(|_|"Sign-in state is busy")?;
    let mut value=load_credentials(base)?;
    if value.access_token.is_empty(){return Err("Sign in to Breathing Room to use the remote agent".into());}
    if force_refresh||value.expires_at<=now()+30{
        let pending=value.pending.take();
        let last_login=value.last_login_id.take();
        let(status,data)=public_post(base,"/v1/auth/refresh",&json!({"refreshToken":value.refresh_token}))?;
        if status!=200{return Err(error(status,&data));}
        value=serde_json::from_value(data).map_err(|_|"API returned invalid sign-in state")?;value.pending=pending;value.last_login_id=last_login;save_credentials(base,&value)?;
    }
    Ok(value)
}
pub(crate) fn account_id()->Result<String,String>{authenticated(&base_url()?,false)?.account["subject"].as_str().map(str::to_owned).ok_or("Account identity missing".into())}
pub fn billing_checkout(plan:&str)->Result<String,String>{
    if !matches!(plan,"monthly"|"annual"){return Err("Choose monthly or yearly AI Care".into());}
    let (_,value)=post(&base_url()?,"/v1/billing/checkout",&json!({"plan":plan,"mode":"live"}))?;
    let url=value["url"].as_str().ok_or("Checkout URL missing")?;
    let parsed=reqwest::Url::parse(url).map_err(|_|"Invalid checkout URL")?;
    if parsed.scheme()!="https"||parsed.host_str()!=Some("checkout.stripe.com")||!parsed.username().is_empty()||parsed.password().is_some()||parsed.port().is_some(){return Err("Invalid Stripe checkout destination".into());}
    Ok(parsed.to_string())
}
pub fn billing_status()->Result<Value,String>{
    let base=base_url()?;let mut creds=authenticated(&base,false)?;
    for attempt in 0..2{
        let(status,value)=response(client()?.get(format!("{base}/v1/billing/status")).bearer_auth(&creds.access_token).send().map_err(|_|"Could not check your AI Care subscription")?)?;
        if status==401&&attempt==0{creds=authenticated(&base,true)?;continue;}
        if status>=400{return Err(error(status,&value));}return Ok(value);
    }Err("Sign in again to check your subscription".into())
}
pub fn billing_portal()->Result<String,String>{
    let(_,value)=post(&base_url()?,"/v1/billing/portal",&json!({"mode":"live"}))?;
    let parsed=reqwest::Url::parse(value["url"].as_str().ok_or("Billing portal URL missing")?).map_err(|_|"Invalid billing portal URL")?;
    if parsed.scheme()!="https"||parsed.host_str()!=Some("billing.stripe.com")||!parsed.username().is_empty()||parsed.password().is_some()||parsed.port().is_some(){return Err("Invalid Stripe billing destination".into());}
    Ok(parsed.to_string())
}
pub(crate) fn local_account_id()->Result<String,String>{
    let base=base_url()?;let _lock=AUTH_LOCK.lock().map_err(|_|"Sign-in state is busy")?;
    load_credentials(&base)?.account["subject"].as_str().map(str::to_owned).ok_or("Use the account that inspected these locations".into())
}
fn post(base:&str,path:&str,input:&Value)->Result<(u16,Value),String>{
    let mut creds=authenticated(base,false)?;
    for attempt in 0..2{
        let(status,value)=response(client()?.post(format!("{base}{path}")).bearer_auth(&creds.access_token).json(input).send().map_err(|_|"Agent connection interrupted. Resume this inspection to retrieve saved steps")?)?;
        if status==401&&attempt==0{creds=authenticated(base,true)?;continue;}
        if status>=400{return Err(error(status,&value));}return Ok((status,value));
    }Err("Sign in again to continue".into())
}
pub fn connection()->Value{
    let default:Value=serde_json::from_str(DEFAULT_CONFIG).unwrap();
    let model=default["model"].as_str().unwrap_or("@cf/qwen/qwen3-30b-a3b-fp8");
    let result=(||->Result<Value,String>{
        let base=base_url()?;
        let(status,health)=response(client()?.get(format!("{base}/health")).send().map_err(|_|"Could not reach the Breathing Room API")?)?;
        if status!=200{return Err("The API is unavailable".into());}
        let mut signed_in=false;let mut account=Value::Null;
        if let Ok(creds)=authenticated(&base,false){
            let(status,me)=response(client()?.get(format!("{base}/v1/me")).bearer_auth(&creds.access_token).send().map_err(|_|"Could not check sign-in")?)?;
            if status==200{signed_in=true;account=me["account"].clone();let _=store::account(&system::user_home()?,&account);}
        }
        let configured=health["authConfigured"].as_bool().unwrap_or(false);
        Ok(json!({"available":signed_in&&configured,"reachable":true,"authenticated":signed_in,"authConfigured":configured,"account":account,"models":[health["model"]],"defaultModel":health["model"],"baseUrl":base,"message":if signed_in{"Cloudflare Workers AI · authenticated"}else if configured{"Sign in to use Cloudflare Workers AI"}else{"AnyOAuth login has not been configured on the API"},"usage":store::stats().ok()}))
    })();
    result.unwrap_or_else(|message|json!({"available":false,"reachable":false,"authenticated":false,"authConfigured":false,"models":[model],"defaultModel":model,"baseUrl":base_url().ok(),"message":message}))
}
/// The Worker chooses tools. Native code supplies only the advertised read-only
/// capabilities and an explicit disk-discovery operation, never a general mutation.
pub(crate) fn message(message:String,history:Value,mut perform:impl FnMut(&str,&Value)->Result<Value,String>)->Result<Value,String>{
    if message.trim().is_empty()||message.len()>2000{return Err("Ask a question of at most 2000 bytes".into());}
    let base=base_url()?;let account=account_id()?;
    let mut bytes=[0u8;16];std::fs::File::open("/dev/urandom").and_then(|mut f|f.read_exact(&mut bytes)).map_err(|_|"Could not create conversation ID")?;bytes[6]=(bytes[6]&15)|64;bytes[8]=(bytes[8]&63)|128;
    let hex=bytes.iter().map(|b|format!("{b:02x}")).collect::<String>();let id=format!("{}-{}-{}-{}-{}",&hex[..8],&hex[8..12],&hex[12..16],&hex[16..20],&hex[20..]);
    let mut outputs=vec![];let mut disk_run:Option<String>=None;
    for step in 0..=12{
        if base_url()?!=base||account_id()?!=account{return Err("Agent account or API origin changed during this conversation".into());}
        let input=json!({"id":id,"step":step,"message":message,"history":history,"outputs":outputs});
        let reply=match post(&base,"/v1/assistant/message",&input){
            Ok((_,reply))=>reply,
            Err(error)=>{if let Some(run)=disk_run{return Ok(json!({"answer":format!("Disk investigation started, but the follow-up answer was interrupted: {error}. Review the findings below; no cleanup was approved."),"features":[],"sources":[],"runId":run}));}return Err(error);}
        };
        let journal=format!("assistant-{id}");let home=system::user_home()?;
        store::save_step(&home,&journal,step,&digest(&input.to_string()),&reply)?;
        if reply["type"]=="answer"{let mut result=reply;if let Some(run)=disk_run{result["runId"]=json!(run);}return Ok(result);}
        let calls=reply["calls"].as_array().filter(|calls|calls.len()<=4).ok_or("Invalid conversational tool requests")?;
        outputs.clear();
        for call in calls{
            let name=call["name"].as_str().ok_or("Tool name missing")?;let args=&call["arguments"];
            let result=if name=="start_disk_discovery"&&disk_run.is_some(){Ok(json!({"runId":disk_run,"alreadyStarted":true}))}else{perform(name,args)};
            let result=result.unwrap_or_else(|error|json!({"error":error}));
            if name=="start_disk_discovery"{if let Some(run)=result["runId"].as_str(){disk_run=Some(run.into());}}
            let result=compact(result);store::save_tool(&home,&journal,call["id"].as_str().ok_or("Tool ID missing")?,&digest(&args.to_string()),&result)?;
            outputs.push(json!({"id":call["id"],"name":name,"result":result}));
        }
    }
    Err("Conversation reached its investigation limit; no further tools were run".into())
}
/// CLI diagnostics use the same authenticated conversation and tool contract as
/// the desktop. No approval/execute capability is exposed by this entry point.
pub fn ask(request:String)->Result<Value,String>{
    let home=system::user_home()?;let disk_request=request.clone();
    message(request,json!([]),|name,args|match name{
        "start_disk_discovery"=>session::inspect_configured(disk_request.clone(),args["scope"].as_str().unwrap_or("").into(),false,Default::default()).map(|id|json!({"runId":id,"status":"inspecting","note":"No cleanup approved"})),
        "inspect_activity"=>Err("Recorded monitor activity is available through the desktop app, not this CLI diagnostic. Recent-file and current CPU/memory tools remain available.".into()),
        _=>crate::system_tools::inspect(&home,name,args)
    })
}
pub fn auth_start(provider:String)->Result<Value,String>{
    if !["google","github","email"].contains(&provider.as_str()){return Err("Choose Google, GitHub, or email".into());}
    let base=base_url()?;let code=random()?;let nonce=random()?;
    let listener=TcpListener::bind("127.0.0.1:0").map_err(|_|"Could not open the local sign-in return address")?;
    listener.set_nonblocking(true).map_err(|_|"Could not initialize browser sign-in")?;
    let port=listener.local_addr().map_err(|_|"Local sign-in address unavailable")?.port();
    let redirect=format!("http://127.0.0.1:{port}/auth/return/{nonce}");
    let(status,result)=public_post(&base,"/v1/auth/desktop/start",&json!({"provider":provider,"codeChallenge":digest(&code),"redirectUri":redirect}))?;
    if status!=200{return Err(error(status,&result));}
    let id=result["id"].as_str().ok_or("Login response was incomplete")?;
    let url=result["loginUrl"].as_str().ok_or("Login response was incomplete")?;
    let parsed=reqwest::Url::parse(url).map_err(|_|"Invalid login URL")?;
    if parsed.origin().ascii_serialization()!=base{return Err("Login URL does not belong to the configured API".into());}
    {let _lock=AUTH_LOCK.lock().map_err(|_|"Sign-in state is busy")?;let mut creds=load_credentials(&base)?;creds.pending=Some(Pending{id:id.into(),verifier:code,expires_at:now()+600,callback_code:None,error:None});save_credentials(&base,&creds)?;}
    let origin=base.clone();let attempt=id.to_owned();thread::spawn(move||listen_for_login(listener,&origin,&attempt,&nonce));
    std::process::Command::new("/usr/bin/open").arg(url).spawn().map_err(|_|"Could not open the browser")?;
    Ok(json!({"id":id,"expiresAt":now()+600}))
}
pub fn auth_poll(id:String)->Result<Value,String>{
    let base=base_url()?;let _lock=AUTH_LOCK.lock().map_err(|_|"Sign-in state is busy")?;
    let creds=load_credentials(&base)?;
    if creds.last_login_id.as_deref()==Some(id.as_str())&&!creds.access_token.is_empty(){return Ok(json!({"status":"succeeded","account":creds.account}));}
    let pending=creds.pending.as_ref().ok_or("Start sign-in again")?;
    if pending.id!=id||pending.expires_at<=now(){return Err("Sign-in expired. Start again".into());}
    if let Some(error)=&pending.error{return Err(error.clone());}
    Ok(json!({"status":"pending"}))
}
fn callback_code(target:&str,host:&str,port:u16,id:&str,nonce:&str)->Option<String>{
    if host!=format!("127.0.0.1:{port}")||!target.starts_with('/')||target.len()>4096{return None;}
    let url=reqwest::Url::parse(&format!("http://127.0.0.1:{port}{target}")).ok()?;
    if url.path()!=format!("/auth/return/{nonce}")||url.fragment().is_some(){return None;}
    let pairs=url.query_pairs().collect::<Vec<_>>();if pairs.len()!=2{return None;}
    if !pairs.iter().any(|(key,value)|key=="state"&&value==id){return None;}
    let code=pairs.iter().find(|(key,_)|key=="code")?.1.to_string();
    (code.len()==43&&code.bytes().all(|byte|byte.is_ascii_alphanumeric()||byte==b'_'||byte==b'-')).then_some(code)
}
fn browser_reply(stream:&mut TcpStream,status:u16,message:&str){
    let html=auth_return_page(status,message);
    let reply=format!("HTTP/1.1 {status} {}\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: {}\r\nCache-Control: no-store\r\nReferrer-Policy: no-referrer\r\nContent-Security-Policy: default-src 'none'; style-src 'unsafe-inline'; font-src data:; frame-ancestors 'none'\r\nConnection: close\r\n\r\n{html}",if status==200{"OK"}else{"Bad Request"},html.len());
    let _=stream.write_all(reply.as_bytes());
}
fn auth_return_page(status:u16,message:&str)->String{
    let html=include_str!(concat!(env!("OUT_DIR"),"/auth-return.html")).to_owned();
    if status==200{return html;}
    let escaped=message.replace('&',"&amp;").replace('<',"&lt;").replace('>',"&gt;").replace('"',"&quot;").replace('\'',"&#39;");
    html.replace("Signed in — Breathing Room","Sign-in interrupted — Breathing Room")
        .replace("data-status=\"success\"","data-status=\"error\"")
        .replace("Sign-in complete","Sign-in interrupted")
        .replace("You’re signed in.","Let’s try that again.")
        .replace("Your cleanup agent is ready. Head back to Breathing Room to find a little more space.",&escaped)
        .replace("m5 12 4 4 10-10","M12 7v6m0 4h.01")
}
fn listen_for_login(listener:TcpListener,base:&str,id:&str,nonce:&str){
    let deadline=Instant::now()+Duration::from_secs(600);let port=listener.local_addr().map(|address|address.port()).unwrap_or(0);
    while Instant::now()<deadline{
        if !load_credentials(base).ok().and_then(|creds|creds.pending).is_some_and(|pending|pending.id==id&&pending.expires_at>now()){return;}
        match listener.accept(){
            Ok((mut stream,_))=>{
                let _=stream.set_read_timeout(Some(Duration::from_secs(2)));let _=stream.set_write_timeout(Some(Duration::from_secs(2)));
                let mut bytes=vec![];let mut chunk=[0u8;1024];
                while bytes.len()<8192{match stream.read(&mut chunk){Ok(0)|Err(_)=>break,Ok(count)=>{bytes.extend_from_slice(&chunk[..count]);if bytes.windows(4).any(|part|part==b"\r\n\r\n"){break;}}}}
                let request=String::from_utf8_lossy(&bytes);let mut lines=request.lines();let first=lines.next().unwrap_or("").split_whitespace().collect::<Vec<_>>();
                let host=lines.find_map(|line|line.split_once(':').filter(|(name,_)|name.eq_ignore_ascii_case("host")).map(|(_,value)|value.trim())).unwrap_or("");
                let returned=if first.len()==3&&first[0]=="GET"{callback_code(first[1],host,port,id,nonce)}else{None};
                let Some(code)=returned else{browser_reply(&mut stream,400,"This is not a valid sign-in return. Continue in Breathing Room.");continue;};
                let result=(||->Result<(),String>{
                    let _lock=AUTH_LOCK.lock().map_err(|_|"Sign-in state is busy")?;let mut creds=load_credentials(base)?;
                    let pending=creds.pending.as_mut().filter(|pending|pending.id==id&&pending.expires_at>now()).ok_or("Sign-in expired. Start again")?;
                    pending.callback_code=Some(code.clone());
                    let(status,response)=public_post(base,"/v1/auth/desktop/exchange",&json!({"id":id,"codeVerifier":pending.verifier,"code":code}))?;
                    if status!=200{return Err(error(status,&response));}
                    let mut signed:Credentials=serde_json::from_value(response).map_err(|_|"Invalid sign-in response")?;
                    if signed.access_token.is_empty()||signed.refresh_token.is_empty(){return Err("Sign-in response was incomplete".into());}
                    signed.last_login_id=Some(id.into());save_credentials(base,&signed)?;store::account(&system::user_home()?,&signed.account)?;Ok(())
                })();
                if result.is_ok(){browser_reply(&mut stream,200,"Signed in. Return to Breathing Room; you can close this window.");}
                else{if let Ok(_lock)=AUTH_LOCK.lock(){if let Ok(mut creds)=load_credentials(base){if let Some(pending)=creds.pending.as_mut().filter(|pending|pending.id==id){pending.error=Some("Sign-in could not complete. Start again in Breathing Room.".into());let _=save_credentials(base,&creds);}}}browser_reply(&mut stream,400,"Sign-in could not complete. Start again in Breathing Room.");}return;
            },
            Err(error)if error.kind()==std::io::ErrorKind::WouldBlock=>thread::sleep(Duration::from_millis(100)),
            Err(_)=>return,
        }
    }
}
pub fn logout()->Result<(),String>{
    let base=base_url()?;
    let creds={let _lock=AUTH_LOCK.lock().map_err(|_|"Sign-in state is busy")?;let creds=load_credentials(&base)?;store::auth_clear(&system::user_home()?,&base)?;creds};
    // Clear local sign-in immediately; revoke only the old session in the background.
    thread::spawn(move||{
        let mut token=creds.access_token;
        if creds.expires_at<=now()+30&&!creds.refresh_token.is_empty(){if let Ok((200,response))=public_post(&base,"/v1/auth/refresh",&json!({"refreshToken":creds.refresh_token})){token=response["accessToken"].as_str().unwrap_or("").into();}}
        if !token.is_empty(){if let Ok(client)=client(){let _=client.post(format!("{base}/v1/auth/logout")).bearer_auth(token).json(&json!({})).send();}}
    });Ok(())
}
fn compact(mut value:Value)->Value{
    for key in ["output","stderr","sample"]{
        if let Some(text)=value[key].as_str(){if text.len()>7000{let mut end=7000;while !text.is_char_boundary(end){end-=1;}value[key]=json!(format!("{}\n[output truncated; narrow the query to continue]",&text[..end]));value["truncated"]=json!(true);}}
    }
    let mut omitted=0;
    let mut recent_omitted=serde_json::Map::new();
    if let Some(entries)=value["entries"].as_array_mut(){let before=entries.len();entries.truncate(48);omitted=before-entries.len();}
    while value.to_string().len()>13000{
        if let Some(rows)=value["recentFindings"].as_array_mut(){if !rows.is_empty(){rows.pop();value["recentFindingsCompacted"]=json!(true);continue;}}
        let history_key=["events","diskHistory"].into_iter().find(|key|value["history"][*key].as_array().is_some_and(|rows|rows.len()>1));
        if let Some(key)=history_key{value["history"][key].as_array_mut().unwrap().pop();value["historyCompacted"]=json!(true);continue;}
        if let Some(entries)=value["entries"].as_array_mut(){if entries.len()>1{entries.pop();omitted+=1;continue;}}
        if let Some(entries)=value.get_mut("reviewLocations").and_then(Value::as_array_mut){if entries.len()>1{entries.pop();let next=value["reviewOffset"].as_u64().unwrap_or(0)+value["reviewLocations"].as_array().unwrap().len() as u64;value["reviewNextOffset"]=json!(next);value["reviewPageCompacted"]=json!(true);continue;}}
        let key=["groups","largestRecentFiles","latestCreatedFiles"].into_iter().filter(|key|value[*key].as_array().is_some_and(|rows|rows.len()>1)).max_by_key(|key|value[*key].as_array().map(Vec::len).unwrap_or(0));
        if let Some(key)=key{value[key].as_array_mut().unwrap().pop();let count=recent_omitted.get(key).and_then(Value::as_u64).unwrap_or(0)+1;recent_omitted.insert(key.into(),json!(count));continue;}break;
    }
    if omitted>0{
        value["clientRowsOmitted"]=json!(omitted);
        if value.get("nextOffset").is_some(){let count=value["entries"].as_array().map(Vec::len).unwrap_or(0);value["nextOffset"]=json!(value["offset"].as_u64().unwrap_or(0)+count as u64);}
    }
    if !recent_omitted.is_empty(){value["clientRecentRowsOmitted"]=Value::Object(recent_omitted);}
    if value.to_string().len()>14000{return json!({"truncated":true,"note":"Tool output exceeded the response budget; ask for a narrower query"});}
    value
}
pub(crate) fn turn(home:&Path,id:&str)->Result<String,String>{
    let base=base_url()?;let run=session::tool_run(home,id)?;
    if run.api_origin.as_deref()!=Some(base.as_str()){return Err("API origin changed. Start a new inspection rather than mixing cached runs from different servers".into());}
    if run.account_id.as_deref()!=Some(&account_id()?){return Err("Sign in with the account that started this inspection".into());}
    let creation_key=format!("run-create:{id}");
    let creation=if let Some(frozen)=store::cache_get(home,&creation_key)?{frozen}else{
        let assisted=run.discovery.as_ref().and_then(|d|d.agent.as_ref()).is_some_and(|a|a.triggered);
        let tools=if run.discovery.is_some()&&!assisted{crate::cleanup_tools::review_manifest()}else{crate::cleanup_tools::manifest()};
        let mut creation=json!({"clientRunId":id,"request":run.request,"scope":run.scope,"tools":tools});
        if let Some(discovery)=&run.discovery{
            // Context batching is independent of retained discoveries. All candidates
            // remain native and page through list_candidates during assisted discovery.
            let legacy=discovery.inventory.is_none()&&discovery.agent.is_none();
            let candidate_window=if legacy{discovery.candidates.len()}else{32};
            let mut manual=discovery.manual.iter().take(if discovery.inventory.is_some(){148}else{160}).map(|item|json!(item)).collect::<Vec<_>>();
            manual.truncate(120);
            manual.extend(discovery.review_locations.iter().take(28).map(|item|json!({"path":item.path,"reason":format!("{} allocated bytes; severity {}; recoverability {}; partial {}. Review-only, never a cleanup candidate. {}",item.bytes,item.risk.severity,item.risk.recoverability,item.partial,item.risk.warning)})));
            if let Some(inventory)=&discovery.inventory{manual.extend(inventory.largest.iter().take(12).map(|item|json!({"path":item["path"],"reason":format!("General inventory: {} allocated bytes, category {}. Review-only personal/app-managed data; size alone does not authorize deletion.",item["bytes"],item["category"])})));}
            creation["discovery"]=json!({"candidates":discovery.candidates.iter().take(candidate_window).collect::<Vec<_>>(),"manual":manual,"coverage":discovery.coverage,"errors":discovery.errors.iter().take(100).collect::<Vec<_>>(),"discoveredAt":discovery.discovered_at,"snapshotHash":discovery.snapshot_hash});
            if assisted{let agent=discovery.agent.as_ref().unwrap();creation["agentDiscovery"]=json!(true);creation["maxDiscoveryTurns"]=json!(agent.policy.max_turns);creation["maxDiscoveryToolCalls"]=json!(agent.policy.max_tool_calls);creation["inventory"]=json!(discovery.inventory);creation["triggerReason"]=json!(agent.reason);}
        }
        while creation.to_string().len()>110_000{let candidates=creation["discovery"]["candidates"].as_array_mut().ok_or("Discovery context is too large")?;if candidates.len()<=1{return Err("Discovery context is too large".into());}candidates.pop();}
        store::cache_put(home,&creation_key,&creation,None)?;creation
    };
    let(_,remote)=post(&base,"/v1/agent/runs",&creation)?;
    let remote_id=remote["id"].as_str().ok_or("Agent API did not return a run ID")?;
    session::remote_session(home,id,remote_id.to_owned(),remote["model"].as_str().ok_or("Agent model is missing")?.into())?;
    let key=format!("run-next:{id}");
    let mut input=store::cache_get(home,&key)?.unwrap_or(json!({"index":0,"outputs":[]}));
    let deadline=Instant::now()+Duration::from_secs(600);
    loop{
        if session::tool_run(home,id)?.status=="cancelled"{let _=post(&base,&format!("/v1/agent/runs/{remote_id}/cancel"),&json!({}));return Err("Inspection cancelled".into());}
        if Instant::now()>deadline{return Err("Inspection reached its time limit. Resume to retrieve completed steps".into());}
        let index=input["index"].as_u64().ok_or("Invalid saved step")?;let fingerprint=digest(&input.to_string());
        store::cache_put(home,&key,&input,None)?;
        let reply=if let Some(saved)=store::step(home,id,index,&fingerprint)?{saved}else{
            let(status,reply)=post(&base,&format!("/v1/agent/runs/{remote_id}/steps"),&input)?;
            if status==202{thread::sleep(Duration::from_secs(2));continue;}
            store::save_step(home,id,index,&fingerprint,&reply)?;reply
        };
        match reply["type"].as_str(){
            Some("plan")=>return Ok(reply.to_string()),
            Some("tools")=>{
                let calls=reply["calls"].as_array().filter(|calls|calls.len()<=8).ok_or("Invalid remote tool requests")?;
                let mut outputs=vec![];
                for call in calls{
                    if Instant::now()>deadline{return Err("Inspection reached its time limit. Resume to retrieve completed steps".into());}
                    let cid=call["id"].as_str().ok_or("Tool call ID missing")?;let name=call["name"].as_str().ok_or("Tool name missing")?;let args=&call["arguments"];
                    if !crate::cleanup_tools::inspection_tool(name){return Err("Remote agent requested an unsupported or mutation tool".into());}
                    let input_hash=digest(&json!({"name":name,"arguments":args}).to_string());
                    let result=if let Some(saved)=store::tool_result(home,id,cid,&input_hash)?{saved}else{
                        session::activity(home,id,format!("Agent: {name}"));
                        let value=crate::cleanup_tools::inspect(home,id,name,args).unwrap_or_else(|error|json!({"error":error}));
                        let value=compact(value);store::save_tool(home,id,cid,&input_hash,&value)?;value
                    };
                    outputs.push(json!({"id":cid,"name":name,"result":result}));
                }
                input=json!({"index":index+1,"outputs":outputs});
            },_=>return Err("Agent API returned an invalid step".into()),
        }
    }
}
#[cfg(test)]mod tests{
    use super::*;
    #[test]fn branded_return_page_is_self_contained_and_escapes_errors(){let success=auth_return_page(200,"ignored");assert!(success.contains("You’re signed in."));assert!(success.contains("class=\"brand\""));assert!(!success.contains("{{font_faces}}"));assert!(!success.contains("<script"));let error=auth_return_page(400,"<script>bad & unsafe</script>");assert!(error.contains("data-status=\"error\""));assert!(error.contains("&lt;script&gt;bad &amp; unsafe&lt;/script&gt;"));assert!(!error.contains("<script>"));}
    #[test]fn origins_cannot_carry_credentials_or_redirect_paths(){assert!(valid_url("https://user:pass@api.example.com").is_err());assert!(valid_url("http://api.example.com").is_err());assert!(valid_url("https://api.example.com/auth?key=secret").is_err());assert_eq!(valid_url("http://127.0.0.1:8797").unwrap(),"http://127.0.0.1:8797");}
    #[test]fn editor_review_compaction_preserves_warnings_and_resumable_pagination(){
        let value=compact(json!({"reviewLocations":(0..8).map(|i|json!({"path":format!("/fixture/{i}.cap"),"severity":"critical","recoverability":"not-rebuildable","warning":"Original footage. ".repeat(200)})).collect::<Vec<_>>(),"reviewOffset":8,"reviewNextOffset":16,"reviewLocationCount":24}));
        let rows=value["reviewLocations"].as_array().unwrap();assert!(!rows.is_empty());assert!(rows.len()<8);assert_eq!(value["reviewNextOffset"],8+rows.len());assert_eq!(value["reviewLocationCount"],24);assert_eq!(rows[0]["recoverability"],"not-rebuildable");assert!(value.to_string().len()<14000);
    }
    #[test]fn bounded_tool_output_keeps_omissions_explicit(){let value=compact(json!({"entries":(0..100).map(|i|json!({"path":format!("/fixture/{i}"),"bytes":i})).collect::<Vec<_>>() }));assert_eq!(value["entries"].as_array().unwrap().len(),48);assert_eq!(value["clientRowsOmitted"],52);}
    #[test]fn recent_output_compaction_keeps_temporal_totals_and_coverage(){
        let rows=(0..100).map(|i|json!({"path":format!("/fixture/{i}/{}","long-path/".repeat(30)),"allocatedBytes":8192})).collect::<Vec<_>>();
        let result=compact(json!({"groups":rows,"largestRecentFiles":rows,"latestCreatedFiles":rows,"recentlyCreatedBytes":900000,"coverage":{"partial":true},"reviewOnly":true}));
        assert_eq!(result["recentlyCreatedBytes"],900000);assert_eq!(result["coverage"]["partial"],true);assert!(result["clientRecentRowsOmitted"].is_object());assert!(result.to_string().len()<14000);
    }
    #[test]fn compacted_listings_do_not_skip_unseen_rows(){let value=compact(json!({"entries":(0..100).map(|i|json!({"path":format!("/fixture/{i}")})).collect::<Vec<_>>(),"offset":100,"nextOffset":200}));assert_eq!(value["nextOffset"],148);}
    #[test]fn return_requires_loopback_host_nonce_state_and_code(){let nonce="n".repeat(43);let code="c".repeat(43);let target=format!("/auth/return/{nonce}?code={code}&state=attempt");assert_eq!(callback_code(&target,"127.0.0.1:12345",12345,"attempt",&nonce),Some(code));assert!(callback_code(&target,"evil.test",12345,"attempt",&nonce).is_none());assert!(callback_code(&target,"127.0.0.1:12345",12345,"other",&nonce).is_none());assert!(callback_code(&target,"127.0.0.1:12345",12345,"attempt","other").is_none());}
    #[test]fn session_round_trip_uses_only_the_private_database(){let home=std::fs::canonicalize(std::env::temp_dir()).unwrap().join(format!("br-session-{}",std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos()));let creds=Credentials{access_token:"fixture-access".into(),refresh_token:"fixture-refresh".into(),account:json!({"subject":"fixture"}),..Default::default()};save_credentials_at(&home,"https://api.test",&creds).unwrap();assert_eq!(load_credentials_at(&home,"https://api.test").unwrap().access_token,"fixture-access");assert!(load_credentials_at(&home,"https://different.test").unwrap().access_token.is_empty());store::auth_clear(&home,"https://api.test").unwrap();assert!(load_credentials_at(&home,"https://api.test").unwrap().access_token.is_empty());std::fs::remove_dir_all(home).unwrap();}
}
