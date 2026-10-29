#!/usr/bin/env python3
"""Read-only Git-tree binding of current main65; never fetch Git packs or compile."""
from pathlib import Path
import base64,hashlib,json,subprocess,tarfile
P=Path(__file__).resolve().parent;REV='5634890b9b7aa03dccb82b22ec0e1dc9f2e1eaa1';OWNER='lalalune/pumpfun-source';BASEPROOF=Path('/workspace/pumpfun-source-workers/pump-creation/work/pump-creation/resume-1285b5e9/perhop-clock-snapshot/MAIN-65-BOUND.json')
sha=lambda b:hashlib.sha256(b).hexdigest()
def api(path):return json.loads(subprocess.check_output(['gh','api',f'repos/{OWNER}/{path}']))
def dump(name,data):(P/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
root=api('git/trees/'+REV);dump('main-root-tree.json',root);programs=next(r['sha']for r in root['tree']if r['path']=='programs');middle=api('git/trees/'+programs);dump('main-programs-tree.json',middle);pump=next(r['sha']for r in middle['tree']if r['path']=='pump');tree=api('git/trees/'+pump+'?recursive=1');assert not tree.get('truncated');dump('main-pump-tree.json',tree)
proof=json.loads(BASEPROOF.read_text());print('proof_file_type',type(proof['files']).__name__);print('proof_example',str(proof['files'])[:650])
readme=api(f'contents/programs/pump/README.md?ref={REV}');raw=base64.b64decode(readme['content']);assert hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==readme['sha'];(P/'main-pump-README.md').write_bytes(raw);print(raw.decode()[:10500])
