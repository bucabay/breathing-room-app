// Stable local-development signing. Certificate fingerprints are public metadata;
// private keys stay in Keychain and are accessed only by Apple's codesign tool.
import {execFileSync,spawnSync} from "node:child_process";
import {existsSync,readFileSync,writeFileSync} from "node:fs";
import {fileURLToPath} from "node:url";

const applicationId="app.breathingroom.mac";
const localConfig=fileURLToPath(new URL("../.desktop-signing.local.json",import.meta.url));
function run(program,args){return execFileSync(program,args,{encoding:"utf8",stdio:["ignore","pipe","pipe"]});}
export function parseSigningIdentities(text){return [...text.matchAll(/^\s*\d+\) ([A-Fa-f0-9]{40}) "([^"]+)"\s*$/gm)].map(([,hash,name])=>({hash:hash.toUpperCase(),name}));}
export function chooseSigningIdentity(identities,configured){
  if(configured){const selected=identities.find(identity=>identity.hash===configured.toUpperCase()||identity.name===configured);if(!selected)throw new Error("The configured desktop signing identity is unavailable. Restore it in Keychain or explicitly choose a replacement; the app will not silently change identity.");return selected;}
  const selected=identities.find(identity=>identity.name.startsWith("Apple Development:"));
  if(!selected)throw new Error("No Apple Development signing identity is available. Configure APPLE_SIGNING_IDENTITY or create a development certificate in Xcode. Repeated ad-hoc installs can reset macOS folder-access decisions.");
  return selected;
}
export function stableSignature(details){return /^Identifier=app\.breathingroom\.mac$/m.test(details)&&/^TeamIdentifier=(?!not set$)\S+$/m.test(details)&&details.includes("anchor apple")&&!/^Signature=adhoc$/m.test(details)&&!/designated => cdhash /m.test(details);}
export function ensureStableDesktopSigning(bundle){
  if(process.platform!=="darwin")return;
  // spawnSync keeps successful stderr without printing any certificate/key data.
  const details=signingDetails(bundle);
  if(stableSignature(details)){run("/usr/bin/codesign",["--verify","--deep","--strict",bundle]);return;}
  if(process.env.BREATHING_ROOM_ALLOW_ADHOC_INSTALL==="1"){
    console.warn("Explicit ad-hoc installation: macOS access prompts may repeat after every rebuild.");return;
  }
  const stored=existsSync(localConfig)?JSON.parse(readFileSync(localConfig,"utf8")):{};
  const configured=process.env.APPLE_SIGNING_IDENTITY||stored.identity;
  const identities=parseSigningIdentities(run("/usr/bin/security",["find-identity","-v","-p","codesigning"]));
  const identity=chooseSigningIdentity(identities,configured);
  run("/usr/bin/codesign",["--force","--sign",identity.hash,"--identifier",applicationId,"--preserve-metadata=entitlements","--timestamp=none",bundle]);
  run("/usr/bin/codesign",["--verify","--deep","--strict",bundle]);
  if(!stableSignature(signingDetails(bundle)))throw new Error("Desktop signing did not produce a stable app/team requirement. Installation stopped.");
  if(!configured)writeFileSync(localConfig,JSON.stringify({identity:identity.hash},null,2)+"\n",{mode:0o600});
  console.log("Verified stable Apple-signed desktop identity; private key remains in Keychain.");
}

export function signingDetails(bundle){const result=spawnSync("/usr/bin/codesign",["-d","-r-","--verbose=4",bundle],{encoding:"utf8"});return result.status===0?result.stdout+result.stderr:"";}
