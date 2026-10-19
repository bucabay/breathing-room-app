//! Learned discovery leads are data, never executable cleanup policy.
use crate::{cleanup_session as session, model::now, runtime_store};
use rusqlite::params;
use serde::{Deserialize,Serialize};
use serde_json::{json,Value};
use sha2::{Digest,Sha256};
use std::{fs,path::{Path,PathBuf},time::Instant};

#[derive(Clone,Serialize,Deserialize)]
#[serde(rename_all="camelCase",deny_unknown_fields)]
pub struct RuleInput{pub title:String,pub relative_path:String,pub profiles:Vec<String>,pub evidence_path:String,pub reason:String}
#[derive(Clone,Serialize,Deserialize)]
#[serde(rename_all="camelCase")]
pub struct Rule{pub id:String,pub title:String,pub relative_path:String,pub profiles:Vec<String>,pub reason:String,pub evidence_path:String,pub source_run:String,pub learned_at:u64}

fn pattern(input:&RuleInput)->Result<Vec<&str>,String>{
    if input.title.is_empty()||input.title.len()>160||input.reason.is_empty()||input.reason.len()>1200||input.relative_path.len()>1000||input.profiles.is_empty()||input.profiles.iter().any(|p|!["everyday","developer","builder","creator"].contains(&p.as_str())){return Err("Invalid discovery rule metadata".into());}
    let parts=input.relative_path.split('/').collect::<Vec<_>>();
    if parts.len()<2||parts.len()>12||parts.iter().any(|p|p.is_empty()||*p=="."||*p==".."||p.contains('\\')||p.contains('\0')||p.contains('\n')||(p.contains('*')&&*p!="*")||p.contains('?')||p.contains('['))||parts.iter().filter(|p|**p=="*").count()>3||parts[0]=="*"{return Err("Use a bounded home-relative discovery path; only whole-segment * wildcards are supported".into());}
    Ok(parts)
}
pub fn save(home:&Path,run_id:&str,input:RuleInput)->Result<Value,String>{
    let parts=pattern(&input)?;let evidence=session::tool_path(home,&input.evidence_path)?;
    let relative=evidence.strip_prefix(home).map_err(|_|"Learned rules must be portable home-relative paths")?;
    let observed=relative.components().map(|c|c.as_os_str().to_string_lossy().into_owned()).collect::<Vec<_>>();
    if observed.len()!=parts.len()||observed.iter().zip(parts).any(|(observed,part)|part!="*"&&part!=observed){return Err("The rule does not match its inspected evidence location".into());}
    let run=session::tool_run(home,run_id)?;
    if run.status!="inspecting"{return Err("Discovery rules can only be learned during inspection".into());}
    if !run.measurements.contains_key(&evidence.to_string_lossy().into_owned()){return Err("Inspect and measure the evidence location before saving a rule".into());}
    if !run.scope.is_empty()&&!evidence.starts_with(session::tool_path(home,&run.scope)?){return Err("Rule evidence is outside the requested scope".into());}
    let id=format!("rule-{:x}",Sha256::digest(input.relative_path.as_bytes()));
    let rule=Rule{id:id.clone(),title:input.title,relative_path:input.relative_path,profiles:input.profiles,reason:input.reason,evidence_path:evidence.to_string_lossy().into_owned(),source_run:run_id.into(),learned_at:now()};
    runtime_store::open(home)?.execute("INSERT INTO discovery_rules VALUES(?,?,1,?) ON CONFLICT(id) DO UPDATE SET payload=excluded.payload,updated_at=excluded.updated_at",params![id,serde_json::to_string(&rule).map_err(|e|e.to_string())?,now()]).map_err(|e|e.to_string())?;
    session::learned_rule(home,run_id)?;
    Ok(json!({"saved":true,"rule":rule,"discoveryOnly":true,"note":"Future scans inspect matching locations. This grants no deletion authority or automatic eligibility."}))
}
pub fn list(home:&Path)->Result<Vec<Rule>,String>{
    let db=runtime_store::open(home)?;let mut query=db.prepare("SELECT payload FROM discovery_rules WHERE enabled=1 ORDER BY updated_at DESC,id").map_err(|e|e.to_string())?;
    let rows=query.query_map([],|r|r.get::<_,String>(0)).map_err(|e|e.to_string())?;
    rows.map(|row|serde_json::from_str(&row.map_err(|e|e.to_string())?).map_err(|_|"Invalid learned discovery rule".into())).collect()
}
pub fn matching(home:&Path,rule:&Rule,deadline:Instant)->Vec<PathBuf>{
    let mut paths=vec![home.to_path_buf()];
    for segment in rule.relative_path.split('/'){
        if Instant::now()>=deadline{return vec![];}
        let mut next=vec![];
        for path in paths{
            if segment=="*"{if let Ok(entries)=fs::read_dir(&path){for entry in entries.flatten(){if Instant::now()>=deadline||next.len()>=250{break;}let candidate=entry.path();if session::tool_path(home,&candidate.to_string_lossy()).is_ok(){next.push(candidate);}}}}
            else{let candidate=path.join(segment);if session::tool_path(home,&candidate.to_string_lossy()).is_ok(){next.push(candidate);}}
            if next.len()>=250{break;}
        }
        paths=next;
    }paths
}
#[cfg(test)]mod tests{
    use super::*;
    #[test]fn learned_rules_are_bounded_data_not_commands(){let mut rule=RuleInput{title:"App cache".into(),relative_path:"Library/Application Support/*/Cache".into(),profiles:vec!["everyday".into()],evidence_path:String::new(),reason:"Observed cache".into()};assert!(pattern(&rule).is_ok());for invalid in ["../../Documents","/*","Library/**/Cache","Library/*/*/*/*/Cache"]{rule.relative_path=invalid.into();assert!(pattern(&rule).is_err());}assert!(serde_json::from_value::<RuleInput>(json!({"title":"x","relativePath":"Library/Caches/x","profiles":["everyday"],"evidencePath":"/x","reason":"x","command":["rm","-rf"]})).is_err());}
}
