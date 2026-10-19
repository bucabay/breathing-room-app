import { execFileSync } from "node:child_process";
import { existsSync, mkdtempSync, renameSync, rmSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { pathToFileURL } from "node:url";
import { ensureStableDesktopSigning } from "./desktop-signing.mjs";

const applicationId = "app.breathingroom.mac";
const defaultDestination = "/Applications/Breathing Room.app";
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));

export function bundleId(bundle) {
  return execFileSync("/usr/libexec/PlistBuddy", ["-c", "Print :CFBundleIdentifier", join(bundle, "Contents/Info.plist")], {encoding:"utf8"}).trim();
}

function runningPids(paths) {
  const executables = new Set(paths.map(path => join(path, "Contents/MacOS/breathing-room")));
  return execFileSync("/bin/ps", ["-axo", "pid=,comm="], {encoding:"utf8"}).split("\n").flatMap(line => {
    const match = line.match(/^\s*(\d+)\s+(.+)$/);
    return match && executables.has(match[2].trim()) ? [Number(match[1])] : [];
  });
}

export async function installDesktop(source, {destination=defaultDestination, launch=false}={}) {
  if (process.platform !== "darwin") throw new Error("Desktop installation requires macOS.");
  source=resolve(source);destination=resolve(destination);
  if (source===destination) throw new Error("Build source and installation destination must differ.");
  if (bundleId(source)!==applicationId) throw new Error("Build bundle is not Breathing Room.");
  if (existsSync(destination) && bundleId(destination)!==applicationId) throw new Error("Installation destination belongs to another application.");
  ensureStableDesktopSigning(source);
  const parent=dirname(destination);
  // Stage a complete bundle on the same filesystem before stopping the running app.
  const staging=mkdtempSync(join(parent,".breathing-room-install-"));
  const next=join(staging,"Breathing Room.app");const backup=join(staging,"previous.app");
  let installed=false;
  try {
    execFileSync("/usr/bin/ditto",[source,next],{stdio:"inherit"});
    const pids=runningPids([destination,source]);
    for (const pid of pids) {try{process.kill(pid,"SIGTERM");}catch(error){if(error.code!=="ESRCH")throw error;}}
    for(let attempt=0;attempt<80 && runningPids([destination,source]).length;attempt++)await sleep(100);
    if(runningPids([destination,source]).length)throw new Error("Breathing Room did not exit. Quit it and rebuild to complete installation.");
    if(existsSync(destination))renameSync(destination,backup);
    try{renameSync(next,destination);installed=true;}catch(error){if(existsSync(backup))renameSync(backup,destination);throw error;}
    // Register the Applications copy so Spotlight / Launch Services use this bundle.
    const register="/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister";
    try{execFileSync(register,["-u",source],{stdio:"pipe"});}
    catch(error){
      // Launch Services returns -10814 when this build copy is already unregistered.
      if(!String(error.stderr??error.message).includes("-10814"))throw error;
    }
    execFileSync(register,["-f",destination]);
    if(pids.length||launch)execFileSync("/usr/bin/open",[destination]);
    console.log(`Updated ${destination}${pids.length||launch?" and launched the installed app":""}.`);
    return destination;
  } finally {
    // Never delete the previous app if restoring it failed.
    if(installed||!existsSync(backup))rmSync(staging,{recursive:true,force:true});
  }
}

if(process.argv[1] && import.meta.url===pathToFileURL(resolve(process.argv[1])).href) {
  const source=process.argv[2];
  if(!source)throw new Error("Usage: node scripts/install-desktop.mjs <built-app-path> [--launch]");
  await installDesktop(source,{launch:process.argv.includes("--launch")});
}
