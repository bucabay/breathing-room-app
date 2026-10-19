import { spawn, execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { installDesktop } from "./install-desktop.mjs";

const require=createRequire(import.meta.url);
const root=resolve(dirname(fileURLToPath(import.meta.url)),"..");
const args=process.argv.slice(2);
const cli=join(dirname(require.resolve("@tauri-apps/cli/package.json")),"tauri.js");
const child=spawn(process.execPath,[cli,...args],{cwd:root,stdio:"inherit"});
for(const signal of ["SIGINT","SIGTERM"])process.on(signal,()=>child.kill(signal));
const code=await new Promise((resolve,reject)=>{child.on("error",reject);child.on("exit",code=>resolve(code??1));});
if(code!==0)process.exit(code);

if(process.platform==="darwin" && ["build","bundle"].includes(args[0])) {
  if(args.includes("--no-bundle")) {
    console.log("No app bundle requested; Applications installation skipped.");
  } else {
    const metadata=JSON.parse(execFileSync("cargo",["metadata","--no-deps","--format-version","1"],{cwd:join(root,"src-tauri"),encoding:"utf8"}));
    const option=(long,short)=>{
      const inline=args.find(arg=>arg.startsWith(`${long}=`));
      if(inline)return inline.slice(long.length+1);
      const index=args.findIndex(arg=>arg===long||arg===short);return index<0?undefined:args[index+1];
    };
    const target=option("--target","-t")??process.env.CARGO_BUILD_TARGET;
    const profile=args.includes("--debug")?"debug":"release";
    const bundle=join(metadata.target_directory,...(target?[target]:[]),profile,"bundle/macos/Breathing Room.app");
    await installDesktop(bundle);
  }
}
