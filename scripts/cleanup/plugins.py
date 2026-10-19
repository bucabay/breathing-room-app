#!/usr/bin/env python3
"""Shipped cleanup plugin interface and isolated, bounded parallel runner."""
import abc
from collections import deque
from dataclasses import dataclass
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import signal
import subprocess
import sys
import tempfile
import time
import cleanup as core

HANDLERS = {"paths", "tool-cache", "app-data", "simulator-runtimes"}


@dataclass
class Context:
    home: Path
    rule: dict
    definition: dict
    deadline: float
    roots: list


def definition(rule):
    value = {"handler": "paths", "root": "home", "timeoutSeconds": 12, "maxItems": 12, **rule.get("plugin", {})}
    if rule["id"] in core.TOOLS:
        value["handler"] = "tool-cache"
    return value


def bounded_command(argv, context, seconds=8):
    remaining = min(seconds, context.deadline - time.monotonic())
    if remaining <= 0:
        raise TimeoutError("Plugin deadline reached")
    result = subprocess.run(argv, capture_output=True, timeout=remaining)
    return result


def expand(pattern, context):
    base = Path("/") if context.definition["root"] == "system" else context.home
    parts = pattern.split("/")
    pending, found, visited = deque([(base, 0, 0)]), [], 0
    while pending and len(found) < context.definition["maxItems"]:
        if time.monotonic() >= context.deadline or visited >= 12000:
            break
        path, index, depth = pending.popleft()
        visited += 1
        try:
            if path.is_symlink():
                continue
            if index == len(parts):
                if path.exists(): found.append(path)
                continue
            part = parts[index]
            if part == "**":
                pending.append((path, index + 1, depth))
                if depth < 6 and path.is_dir():
                    with os.scandir(path) as entries:
                        for entry in entries:
                            if entry.is_dir(follow_symlinks=False) and entry.name not in (".git", "node_modules", "target", "vendor") and not entry.name.endswith(core.PACKAGES):
                                pending.append((Path(entry.path), index, depth + 1))
            elif any(c in part for c in "*?["):
                if path.is_dir():
                    with os.scandir(path) as entries:
                        for entry in entries:
                            if fnmatch.fnmatchcase(entry.name, part) and not entry.is_symlink():
                                pending.append((Path(entry.path), index + 1, depth))
            else:
                pending.append((path / part, index + 1, depth))
        except OSError:
            continue
    return found


class CleanupPlugin(abc.ABC):
    @abc.abstractmethod
    def discover(self, context): pass
    @abc.abstractmethod
    def list(self, location, context): pass
    def delete(self, finding, context):
        if finding.get("pluginId") != context.rule["id"]:
            raise ValueError("Finding does not belong to this plugin")
        if not finding.get("judgment") and not finding.get("userApproved") and not finding.get("explicitSelected"):
            raise ValueError("JEV AI assessment is required before deletion")
        return core.execute_item(finding, context.home)


class PathsPlugin(CleanupPlugin):
    def discover(self, context):
        paths = []
        for pattern in context.rule["patterns"]:
            paths.extend(expand(pattern, context))
        # Custom project roots participate without requiring their names in code.
        for root in context.roots:
            if not Path(root).is_relative_to(context.home): continue
            for pattern in context.rule["patterns"]:
                if "/**/" in pattern and pattern.split("/", 1)[0] in ("code", "Projects", "workspace"):
                    relative = str(Path(root).relative_to(context.home)) + "/**/" + pattern.split("/**/", 1)[1]
                    paths.extend(expand(relative, context))
        return list(dict.fromkeys(paths))[:context.definition["maxItems"]]

    def list(self, location, context):
        preset = location if isinstance(location,dict) else None
        path = Path(preset["path"] if preset else location)
        rule = context.rule
        metadata = path.lstat()
        if preset:
            size,size_complete=preset["bytes"],preset["sizeComplete"]
        elif path.is_file():
            size, size_complete = metadata.st_blocks * 512, True
        else:
            result = bounded_command(["/usr/bin/du", "-s", "-k", "-x", str(path)], context, 8)
            lines = result.stdout.decode(errors="replace").splitlines()
            size = int(lines[-1].split("\t", 1)[0]) * 1024 if lines and lines[-1].split("\t", 1)[0].isdigit() else 0
            size_complete = result.returncode == 0
            if not size and result.returncode:
                raise ValueError("Location exists but sizing was denied or unavailable")
        if not size: return None
        snap = {"complete": False, "blocked": True, "digest": "", "newest": metadata.st_mtime, "files": 0}
        if rule["kind"] != "review" and path.is_relative_to(context.home):
            with core.filesystem_timeout(min(3, max(.1, context.deadline-time.monotonic()))):
                snap = core.snapshot(path, context.home, seconds=2, allow_artifacts=rule["id"] in ("cypress","xcode-derived","electron"))
        executable = rule["kind"] != "review" and snap["complete"] and not snap["blocked"]
        reason = ""
        if executable:
            try:
                core.valid_path(path, context.home)
                if core.tracked(path, context.home): raise ValueError("Contains Git-tracked files")
                if rule["minAgeDays"] and snap["newest"] > time.time()-rule["minAgeDays"]*86400:
                    raise ValueError("Recently changed; review activity before cleanup")
            except (ValueError, OSError) as error:
                executable, reason = False, str(error)
        if not executable and not reason:
            reason = "Owning-app inspection required" if rule["kind"] == "review" else "Full identity validation required before cleanup"
        title = rule["name"]
        if rule["id"] in ("app-cache", "app-support", "container-cache"):
            owner=path.name
            if owner.startswith(("com.","org.","net.","io.","so.")):
                owner=owner.split(".")[1].replace("-"," ").title()
            title = owner + (" cache" if rule["id"] != "app-support" else " app data")
        if "ms-playwright" in str(path): title = "Playwright browsers"
        if "puppeteer" in str(path).lower(): title = "Puppeteer browsers"
        return {"id": hashlib.sha256(f"{rule['id']}:{path}".encode()).hexdigest()[:24], "pluginId": rule["id"], "ruleId": rule["id"],
                "name": title, "path": str(path), "bytes": size, "sizeComplete": size_complete, "sizeBasis": "Allocated filesystem bytes (du)",
                "complete": snap["complete"], "digest": snap["digest"], "files": snap["files"], "newestAt": int(snap["newest"]),
                "kind": rule["kind"], "adapter": rule["adapter"], "executable": executable, "reason": reason,
                "type": rule["type"], "category": rule["category"], "profiles": rule["profiles"], "impactLevel": rule["impactLevel"],
                "minAgeDays": rule["minAgeDays"], "description": rule["description"], "impact": rule["impact"], "source": rule["source"],
                "evidence": "Catalog plugin + measured actual location", "patterns": rule["patterns"], "judgment": None,
                "method": "Move exact selected location to Trash" if rule["kind"] == "trash" else "Owning-app inspection",
                "actions": {"review": True, "delete": executable, "deleteMode": rule["kind"]}, "icon": rule["category"]}


class ToolCachePlugin(PathsPlugin):
    def discover(self, context):
        try: return [core.tool_path(context.rule, context.home)]
        except (ValueError, OSError): return super().discover(context)
    def list(self, location, context):
        item = super().list(location, context)
        if not item: return None
        tool = core.TOOLS[context.rule["id"]]
        item["method"] = " ".join([tool["tool"], *tool["action"]])
        try:
            if core.tool_path(context.rule, context.home) != location: item["executable"] = False
        except (ValueError, OSError):
            item["executable"] = False
            item["reason"] = "The installed tool could not verify its cache location"
        item["actions"]["delete"] = item["executable"]
        return item


class AppDataPlugin(PathsPlugin):
    def discover(self, context):
        paths=[]
        for pattern in context.rule["patterns"]:
            for parent in expand(pattern, context):
                result=bounded_command(["/usr/bin/du","-k","-d","1",str(parent)],context,15)
                entries=[]
                for line in result.stdout.decode(errors="replace").splitlines():
                    value,sep,raw=line.partition("\t")
                    if sep and value.isdigit() and raw!=str(parent) and Path(raw).parent==parent:
                        entries.append((int(value),Path(raw)))
                paths.extend({"path":str(path),"bytes":size*1024,"sizeComplete":result.returncode==0} for size,path in sorted(entries,reverse=True)[:context.definition["maxItems"]])
        return paths


class SimulatorPlugin(CleanupPlugin):
    def discover(self, context):
        result=bounded_command(["/usr/bin/xcrun","simctl","runtime","list","-j"],context,10)
        if result.returncode: return []
        data=json.loads(result.stdout)
        return [item for key,item in data.items() if re.fullmatch(r"[0-9A-Fa-f-]{36}",key) and isinstance(item,dict)][:context.definition["maxItems"]]
    def list(self, location, context):
        rule=context.rule; runtime=location
        bundle=runtime.get("runtimeBundlePath",runtime.get("mountPath",""))
        if not bundle.startswith("/Library/Developer/CoreSimulator/"): return None
        mount=runtime.get("mountPath","")
        mounted_bytes=None
        if mount:
            result=bounded_command(["/bin/df","-k",mount],context,3)
            fields=result.stdout.decode(errors="replace").splitlines()[-1].split()
            if len(fields)>3 and fields[2].isdigit(): mounted_bytes=int(fields[2])*1024
        uuid=runtime["identifier"]
        platform=runtime.get("runtimeIdentifier","Simulator").split(".")[-1].split("-")[0]
        return {"id":uuid,"pluginId":rule["id"],"ruleId":rule["id"],"name":f"{platform} {runtime.get('version','')} Simulator runtime",
                "path":bundle,"bytes":runtime.get("sizeBytes",0),"mountedBytes":mounted_bytes,"sizeComplete":True,"sizeBasis":"simctl runtime image size; mounted usage shown separately",
                "runtimeUuid":uuid,"runtimeIdentity":runtime.get("runtimeIdentifier",""),"runtimeVersion":runtime.get("version",""),"runtimeImagePath":runtime.get("path",""),
                "complete":True,"digest":hashlib.sha256(json.dumps(runtime,sort_keys=True).encode()).hexdigest(),"files":0,"newestAt":0,
                "kind":"tool","adapter":"simulator-runtime plugin","executable":bool(runtime.get("deletable") and runtime.get("state")=="Ready"),"reason":"",
                "type":rule["type"],"category":rule["category"],"profiles":rule["profiles"],"impactLevel":rule["impactLevel"],"minAgeDays":0,
                "description":rule["description"],"impact":rule["impact"],"source":rule["source"],"evidence":"Installed runtime reported by simctl; not a guessed folder",
                "patterns":rule["patterns"],"judgment":None,"method":"xcrun simctl runtime delete <verified UUID>","actions":{"review":True,"delete":bool(runtime.get("deletable")),"deleteMode":"supported tool"},"icon":"development"}
    def delete(self, finding, context):
        if not (finding.get("judgment") or finding.get("explicitSelected")) or finding.get("pluginId")!="simulator-runtimes": raise ValueError("Assess and select this runtime first")
        uuid=finding.get("runtimeUuid","")
        if not re.fullmatch(r"[0-9A-Fa-f-]{36}",uuid): raise ValueError("Invalid runtime UUID")
        current=next((r for r in self.discover(context) if r.get("identifier")==uuid),None)
        if not current or not current.get("deletable") or current.get("state")!="Ready" or current.get("path")!=finding.get("runtimeImagePath") or current.get("runtimeIdentifier")!=finding.get("runtimeIdentity"):
            raise ValueError("Runtime changed or cannot be deleted")
        devices=bounded_command(["/usr/bin/xcrun","simctl","list","devices","booted","-j"],context,8)
        if devices.returncode: raise ValueError("Cannot verify running simulator devices")
        if any(d.get("state")=="Booted" for d in json.loads(devices.stdout).get("devices",{}).get(current.get("runtimeIdentifier"),[])):
            raise ValueError("This runtime has a booted device; shut it down first")
        result=bounded_command(["/usr/bin/xcrun","simctl","runtime","delete",uuid],context,30)
        if result.returncode: raise ValueError("simctl could not remove the runtime; use Xcode runtime management")
        return "Selected runtime removed by simctl. Reinstall it before using its simulator devices."


REGISTRY={"paths":PathsPlugin,"tool-cache":ToolCachePlugin,"app-data":AppDataPlugin,"simulator-runtimes":SimulatorPlugin}


def worker(request):
    rule=request["rule"]; spec=definition(rule)
    context=Context(Path(request["home"]),rule,spec,time.monotonic()+spec["timeoutSeconds"]-.2,request.get("roots",[]))
    plugin=REGISTRY[spec["handler"]]()
    findings=[];errors=[]
    for location in plugin.discover(context):
        if time.monotonic()>context.deadline: break
        try:
            item=plugin.list(location,context)
            if item:findings.append(item)
        except (OSError,ValueError,TimeoutError,subprocess.SubprocessError) as error:
            errors.append(str(error))
    return {"id":rule["id"],"name":rule["name"],"status":"partial" if errors else "complete" if findings else "not-found", "findings":findings,"errors":errors[:3]}


def terminate(process):
    try: os.killpg(process.pid,signal.SIGKILL)
    except ProcessLookupError: pass
    process.wait()


def deduplicate(findings):
    # Keep parent app-data summaries visible, but label nested overlap rather than hide them.
    by_path={}
    for finding in findings:
        old=by_path.get(finding["path"])
        if old is None or (old["pluginId"] in ("app-cache","app-support") and finding["pluginId"] not in ("app-cache","app-support")):
            by_path[finding["path"]]=finding
    items=sorted(by_path.values(),key=lambda c:c["bytes"],reverse=True)[:1000]
    locations={item["path"]:item for item in items}
    for item in items:
        item["overlaps"]=False
    for item in items:
        for parent in Path(item["path"]).parents:
            if str(parent) in locations:
                item["overlaps"]=True;locations[str(parent)]["overlaps"]=True
    return items


def atomic(path,value):
    temp=path.with_name(path.name+"-"+secrets.token_hex(4)+".tmp")
    with temp.open("x") as f:
        os.chmod(temp,0o600);json.dump(value,f)
    temp.replace(path)


def run(home,catalog,roots=(),profiles=(),workers=4,budget=120,progress=None,cancel=None):
    waiting=deque(r for r in catalog["rules"] if not profiles or set(r["profiles"]).intersection(profiles))
    total=len(waiting); active=[]; results=[]; findings=[]; start=time.monotonic(); stopped=False
    def publish():
        data={"running":bool(waiting or active),"total":total,"completed":len(results),"active":[v["rule"]["name"] for v in active],
              "elapsedSeconds":round(time.monotonic()-start,1),"plugins":results,"candidates":deduplicate(findings),"cancelled":stopped,"catalogVersion":catalog["version"]}
        if progress:atomic(progress,data)
        return data
    try:
        publish()
        while waiting or active:
            if (cancel and cancel.exists()) or time.monotonic()-start>=budget:
                stopped=True
                for job in active:
                    terminate(job["process"]);job["output"].close();results.append({"id":job["rule"]["id"],"name":job["rule"]["name"],"status":"cancelled","errors":[]})
                active.clear()
                while waiting:
                    rule=waiting.popleft();results.append({"id":rule["id"],"name":rule["name"],"status":"cancelled","errors":[]})
                publish();break
            while waiting and len(active)<workers:
                rule=waiting.popleft();out=tempfile.TemporaryFile()
                process=subprocess.Popen([sys.executable,"-B",str(Path(__file__)),"worker"],stdin=subprocess.PIPE,stdout=out,stderr=subprocess.DEVNULL,start_new_session=True)
                process.stdin.write(json.dumps({"rule":rule,"home":str(home),"roots":list(roots)}).encode());process.stdin.close()
                active.append({"process":process,"output":out,"rule":rule,"start":time.monotonic()})
            for job in active[:]:
                timeout=time.monotonic()-job["start"]>definition(job["rule"])["timeoutSeconds"]
                if job["process"].poll() is None and not timeout: continue
                if timeout: terminate(job["process"])
                out=job["output"];out.seek(0);raw=out.read(512*1024+1);out.close()
                result={"id":job["rule"]["id"],"name":job["rule"]["name"],"status":"timeout" if timeout else "error","errors":["Per-plugin timeout" if timeout else "Plugin failed or returned invalid data"]}
                if not timeout:
                    try:
                        value=json.loads(raw)
                        if len(raw)>512*1024 or value.get("id")!=job["rule"]["id"]:raise ValueError("Invalid plugin result")
                        findings.extend(value.pop("findings",[]));result=value
                    except (ValueError,KeyError):pass
                result["durationMs"]=round((time.monotonic()-job["start"])*1000)
                results.append(result);active.remove(job);publish()
            time.sleep(.1)
    finally:
        for job in active:
            terminate(job["process"]);job["output"].close()
    data=publish()
    return {"version":1,"createdAt":int(time.time()),"expiresAt":int(time.time())+1800,"catalogVersion":catalog["version"],"catalogFingerprint":core.fingerprint(catalog),
            "candidates":data["candidates"],"plugins":results,"cancelled":stopped,"partial":stopped or any(r["status"] in ("error","timeout","partial") for r in results),
            "warnings":[f"{r['name']}: {r['status']}" for r in results if r["status"] not in ("complete","not-found")],"mode":"offline",
            "message":f"{len(data['candidates'])} measured locations from {total} plugins. Nested totals may overlap; no files deleted."}


def delete(finding,home):
    rule=core.RULES.get(finding.get("pluginId",finding["ruleId"]))
    if not rule:
        if finding.get("userApproved"):return core.execute_item(finding,home)
        raise ValueError("Unknown plugin")
    spec=definition(rule);context=Context(home,rule,spec,time.monotonic()+45,[])
    return REGISTRY[spec["handler"]]().delete(finding,context)


def exact(home,catalog,scope):
    path=Path(scope) if scope.startswith("/") else home/scope.removeprefix("~/")
    if ".." in path.parts or not path.exists() or path.resolve()!=path:
        raise ValueError("Exact location unavailable or contains a symlink")
    if not path.is_relative_to(home) and not any(str(path).startswith(prefix) for prefix in ("/Library/","/Applications/","/opt/","/private/","/usr/local/")):
        raise ValueError("Outside supported inspection roots")
    if str(path).startswith("/Library/Developer/CoreSimulator/Volumes/"):
        rule=core.RULES["simulator-runtimes"];spec=definition(rule);ctx=Context(home,rule,spec,time.monotonic()+20,[]);plugin=SimulatorPlugin()
        matches_runtime=[r for r in plugin.discover(ctx) if r.get("runtimeBundlePath")==str(path) or r.get("mountPath")==str(path)]
        items=[plugin.list(r,ctx) for r in matches_runtime]
    else:
        rule=core.rule_for(path,home,catalog) if path.is_relative_to(home) else None
        if rule is None:
            rule={"id":"unknown","name":path.name,"type":"exact-location","category":"app-data","profiles":[],"patterns":[],"kind":"review","adapter":"inspect-only.py","impactLevel":4 if path.is_relative_to(home) else 5,"minAgeDays":0,"description":"Exact user-selected location, not an inferred disposable folder","impact":"May contain originals or mixed data; review before cleanup.","source":"https://support.apple.com/en-us/102624"}
        spec=definition(rule);ctx=Context(home,rule,spec,time.monotonic()+20,[]);items=[PathsPlugin().list(path,ctx)]
    return {"version":1,"createdAt":int(time.time()),"expiresAt":int(time.time())+1800,"catalogVersion":catalog["version"],"catalogFingerprint":core.fingerprint(catalog),"candidates":[i for i in items if i],"plugins":[],"partial":False,"warnings":[],"mode":"offline","message":"Exact location measured for JEV AI review."}


if __name__=="__main__":
    try:print(json.dumps(worker(json.load(sys.stdin))))
    except (ValueError,OSError,KeyError,TimeoutError,subprocess.SubprocessError):print(json.dumps({"error":"Plugin could not complete"}))
