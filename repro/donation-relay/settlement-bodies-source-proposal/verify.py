#!/usr/bin/env python3
"""Source-only integrity/materialization; local ELF comparison is explicit opt-in."""
import argparse, difflib, hashlib, importlib.util, json, subprocess
from pathlib import Path, PurePosixPath
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if(p/'.git').exists())
ORDER=['baseline','recovered']
def sha(data):return hashlib.sha256(data).hexdigest()
def read(path):return json.loads(path.read_bytes())
def safe(name):
 p=PurePosixPath(name);assert name and not p.is_absolute() and str(p)==name and '..'not in p.parts and '\\'not in name;return p
def file(folder,name):
 p=folder
 for part in safe(name).parts:p=p/part;assert not p.is_symlink()
 assert p.resolve().is_relative_to(folder.resolve());return p
def manifest(folder=HERE):
 assert not any(p.is_symlink()for p in folder.rglob('*'))
 expected=read(folder/'manifest.json');actual={str(p.relative_to(folder))for p in folder.rglob('*')if p.is_file()and p.name!='manifest.json'and'__pycache__'not in p.parts};assert actual==set(expected)
 for name,digest in expected.items():
  data=file(folder,name).read_bytes();assert sha(data)==digest,name;assert b'\0'not in data;data.decode('utf8');assert not name.endswith(('.so','.gz','.bz2','.zip','.tar'))
def public_blob(revision,name):
 safe(name);assert len(revision)==40 and all(c in '0123456789abcdef'for c in revision)
 return subprocess.check_output(['git','--no-optional-locks','show',revision+':'+name],cwd=ROOT)
def patch(before,after):
 return ''.join(''.join(difflib.unified_diff(before[n].decode().splitlines(True),after[n].decode().splitlines(True),fromfile='a/'+n,tofile='b/'+n))for n in sorted(after)if before[n]!=after[n])
def sources(folder=HERE):
 spec=read(folder/'baseline-sources.json');before={}
 for name,row in spec['files'].items():
  safe(name);data=public_blob(row['revision'],row['path']);assert sha(data)==row['sha256'];before[name]=data
 after=dict(before);override=folder/'source'
 for p in override.rglob('*'):
  if p.is_file():name=str(p.relative_to(override));after[name]=file(override,name).read_bytes()
 assert set(before)==set(after) and len(before)==60
 assert {n:sha(b)for n,b in before.items()}==read(folder/'source-inputs.json')['baseline']
 assert {n:sha(b)for n,b in after.items()}==read(folder/'source-inputs.json')['recovered']
 assert sorted(n for n in after if before[n]!=after[n])==['src/settlement_handlers.rs','src/tools/checks.rs','src/tools/distribution/shared.rs']
 assert patch(before,after).encode()==(folder/'source.patch').read_bytes()
 return {'baseline':before,'recovered':after}
def reports(folder=HERE):
 r=read(folder/'expected.json');assert r['gains']==[97,98,100] and r['losses']==[] and r['raw_gains']==[] and r['raw_losses']==[]
 assert r['baseline']['summary']['original_normalized_match_windows']==485
 assert r['recovered']['summary']['original_normalized_match_windows']==488
 assert r['recovered']['summary']['original_raw_match_windows']==142
 assert not r['recovered']['summary']['whole_file_equal']
 return {'source_variants':2,'inputs_per_variant':60,'compiler_executed':False,'runtime_verified':False,'elf_comparison':'not requested'}
def materialize(destination,source):
 assert not destination.exists() and not destination.is_symlink();assert not any(p.is_symlink()for p in destination.parents);destination.mkdir(parents=True)
 for name,data in source.items():p=file(destination,name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 assert {str(p.relative_to(destination)):sha(p.read_bytes())for p in destination.rglob('*')if p.is_file()}=={n:sha(b)for n,b in source.items()}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--materialize',type=Path);p.add_argument('--variant',choices=ORDER,default=ORDER[-1]);p.add_argument('--baseline-build',type=Path);p.add_argument('--candidate-build',type=Path);args=p.parse_args();manifest();s=sources();r=reports()
 if args.materialize:materialize(args.materialize,s[args.variant])
 assert (args.baseline_build is None)==(args.candidate_build is None)
 if args.candidate_build:
  spec=importlib.util.spec_from_file_location('tight_optional_comparison',HERE/'compare.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);r['elf_comparison']=m.compare(args.baseline_build,args.candidate_build)
 print(json.dumps(r,sort_keys=True))
if __name__=='__main__':main()
