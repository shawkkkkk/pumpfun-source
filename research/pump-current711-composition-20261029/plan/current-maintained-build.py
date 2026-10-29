#!/usr/bin/env python3
"""Portable empty-target Pump build with explicit SDK, libraries and registry inputs."""
from pathlib import Path
import argparse,gzip,hashlib,json,os,shutil,subprocess,sys,tarfile,time,tomllib
if not __debug__:raise SystemExit('Optimized Python is unsupported; run without -O.')
P=Path(__file__).resolve().parent;R=P.parents[1];sys.path.insert(0,str(P/'tools'))
from build_source_manifest import source_manifest
from compare import compare
import pump_target_library_profile as profile
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-directory',type=Path,default=P/'source');p.add_argument('--sdk',type=Path,required=True);p.add_argument('--cargo-home',type=Path,required=True);p.add_argument('--target-library-profile',choices=['linux-v1.44-sbpf'],required=True);p.add_argument('--target-libraries',type=Path,required=True);p.add_argument('--wrapper',type=Path,required=True);p.add_argument('--target-directory',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--jobs',type=int,default=2);a=p.parse_args()
for raw in [a.source_directory,a.output,*([a.target_directory]if a.target_directory else [])]:
 for q in [raw.absolute(),*raw.absolute().parents]:
  if q.is_symlink():raise ValueError('Source/output selector contains a symlink: '+str(q))
primary=a.source_directory.resolve();sdk=a.sdk.resolve();registry=a.cargo_home.resolve();wrapper=a.wrapper.resolve();out=a.output.resolve();target=a.target_directory.resolve()if a.target_directory else out/'target'
if any(q.is_symlink()for q in primary.rglob('*')):raise ValueError('Maintained inputs must be regular files/directories, without symlinks')
for protected in [primary,sdk,registry]:
 if out.is_relative_to(protected)or target.is_relative_to(protected):raise ValueError('Output/target overlaps a protected input')
configs=set()
for start in [primary,out]:
 for directory in [start,*start.parents]:
  for name in ['.cargo/config','.cargo/config.toml']:
   if(directory/name).exists():configs.add(str(directory/name))
for name in ['config','config.toml']:
 if(registry/name).exists():configs.add(str(registry/name))
if configs:raise ValueError('Ambient Cargo configuration is unsupported: '+', '.join(sorted(configs)))
overrides=[k for k in os.environ if k.startswith(('CARGO_PROFILE_','CARGO_TARGET_','CARGO_BUILD_'))or k in ['RUSTFLAGS','CARGO_ENCODED_RUSTFLAGS','RUSTC','RUSTDOC','RUSTC_WRAPPER','RUSTC_WORKSPACE_WRAPPER','RUSTUP_TOOLCHAIN','RUSTC_BOOTSTRAP','RUST_TARGET_PATH']]
if overrides:raise ValueError('Ambient compiler/profile overrides are unsupported: '+', '.join(sorted(overrides)))
assert not out.exists()and not target.exists()and primary.is_dir();out.mkdir(parents=True);shutil.copy2(Path(__file__),out/'executed-builder.py')
expected=json.loads((P/'build-inputs.json').read_text());assert sha(wrapper)==expected['source_wrapper_sha256']
primary_before=source_manifest(primary,primary,R,cwd=primary)
assert {str((R/name).relative_to(primary)):digest for name,digest in primary_before.items()}==expected['source_inputs'], 'Actual maintained compiler inputs differ from selected source'
# Self-contained source staging, including the nested local crate and IDLs.
text=(primary/'Cargo.toml').read_text();parsed=tomllib.loads(text);assert parsed.get('workspace')=={} and set(parsed.get('profile',{}))=={'release'}
ps=text.index('[profile.release]');ws=text.index('[workspace]');assert not text[ws+len('[workspace]'):].strip();release=text[ps:ws].strip()+'\n'
workspace=out/'source';crate=workspace/'programs/pump';crate.mkdir(parents=True)
for n in primary_before:
 src=R/n;rel=src.relative_to(primary)
 if str(rel)in['Cargo.toml','Cargo.lock']:continue
 dst=crate/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
(crate/'Cargo.toml').write_text(text[:ps].rstrip()+'\n');(workspace/'Cargo.toml').write_text('[workspace]\nmembers = ["programs/pump"]\nresolver = "2"\n\n'+release);shutil.copy2(primary/'Cargo.lock',workspace/'Cargo.lock')
prepared,profile_record=profile.prepare(a.target_library_profile,sdk,a.target_libraries.resolve(),out/'profile-sdk');tools={'rustc':prepared/'rust/bin/rustc','cargo':prepared/'rust/bin/cargo','objcopy':prepared/'llvm/bin/llvm-objcopy','clang':prepared/'llvm/bin/clang','ar':prepared/'llvm/bin/llvm-ar'}
tools_before={n:sha(f)for n,f in tools.items()};assert tools_before==expected['tool_sha256'],'SDK tools differ from qualified native v1.44 cohort'
libs_before=profile.inventory(prepared/'rust/lib/rustlib/sbpf-solana-solana/lib');assert libs_before==expected['target_libraries_sha256']
sdk_before={str(f.relative_to(prepared)):sha(f)for f in sorted(prepared.rglob('*'))if f.is_file()and(f.is_relative_to(prepared/'rust/lib')or f in tools.values())}
env=os.environ.copy()
for k in list(env):
 if k in ['RUSTFLAGS','CARGO_ENCODED_RUSTFLAGS','RUSTC_WORKSPACE_WRAPPER','CARGO_BUILD_TARGET_DIR']or k.startswith(('CARGO_TARGET_','CARGO_PROFILE_')):env.pop(k,None)
env.update(RUSTC_WRAPPER=str(wrapper),PUMP_LOGICAL_REGISTRY_SRC=str(registry/'registry/src'),PUMP_SOURCE_WRAPPER_LOG=str(out/'physical-source-calls.jsonl'),CARGO_HOME=str(registry),CARGO_TARGET_DIR=str(target),CARGO_BUILD_JOBS=str(a.jobs),RUSTC=str(tools['rustc']),CC=str(tools['clang']),AR=str(tools['ar']),OBJDUMP=str(prepared/'llvm/bin/llvm-objdump'),OBJCOPY=str(tools['objcopy']),CARGO_TARGET_SBPF_SOLANA_SOLANA_RUSTFLAGS='-Zremap-cwd-prefix=')
manifest=str(crate/'Cargo.toml');common=['--manifest-path',manifest,'--locked','--offline'];metadata_command=[str(tools['cargo']),'metadata',*common,'--format-version','1','--filter-platform','sbpf-solana-solana'];metadata=json.loads(subprocess.check_output(metadata_command,cwd=workspace,env=env,text=True))
lock=tomllib.loads((workspace/'Cargo.lock').read_text());checks={(x['name'],x['version']):x['checksum']for x in lock['package']if x.get('source','').startswith('registry+')};archives={}
for(name,version),checksum in checks.items():
 matches=sorted((registry/'registry/cache').glob('*/'+name+'-'+version+'.crate'));assert matches,(name,version);assert all(sha(f)==checksum for f in matches),(name,version);f=matches[0];archives[name+'-'+version]={'path':str(f),'equivalent_archive_paths':[str(x)for x in matches],'sha256':checksum}
registry_sources={};files_checked=0
for pkg in metadata['packages']:
 if not pkg.get('source'):continue
 assert pkg['source']=='registry+https://github.com/rust-lang/crates.io-index';name=pkg['name']+'-'+pkg['version'];root=Path(pkg['manifest_path']).parent.resolve();arch=Path(archives[name]['path']);expected_files={}
 with tarfile.open(arch,'r:gz')as t:
  for member in t:
   if not member.isfile():continue
   rel=Path(member.name).relative_to(name);assert'..'not in rel.parts;data=t.extractfile(member).read();f=root/rel;assert f.is_file()and not f.is_symlink()and f.read_bytes()==data,(name,str(rel));expected_files[str(rel)]=hashlib.sha256(data).hexdigest();files_checked+=1
 actual={str(f.relative_to(root))for f in root.rglob('*')if f.is_file()};assert actual-set(expected_files)<={'.cargo-ok','.cargo-checksum.json'},(name,actual-set(expected_files));registry_sources[str(root)]=expected_files
registry_report={'metadata_command':metadata_command,'locked_registry_archives':archives,'actual_registry_source_files':registry_sources,'files_checked':files_checked};(out/'registry-authentication.json').write_text(json.dumps(registry_report,indent=2)+'\n')
before=source_manifest(crate,workspace,R,cwd=workspace);assert not target.exists(),'metadata unexpectedly created target';command=[str(tools['cargo']),'build',*common,'--release','--target','sbpf-solana-solana','-vv']
record={'scope':__doc__,'cold_empty_target':True,'target_existed_before':False,'builder_sha256':sha(Path(__file__)),'source_wrapper_sha256':sha(wrapper),'registry_authentication_sha256':sha(out/'registry-authentication.json'),'source_directory':str(crate),'primary_source_directory':str(primary),'primary_source_sha256':primary_before,'source_sha256':before,'workspace_directory':str(workspace),'workspace_layout':True,'tool_sha256':tools_before,'sdk_rust_libraries_sha256':sdk_before,'target_libraries_sha256':libs_before,'target_library_profile':profile_record,'command':command,'environment':{k:env[k]for k in ['RUSTC_WRAPPER','PUMP_LOGICAL_REGISTRY_SRC','PUMP_SOURCE_WRAPPER_LOG','CARGO_HOME','CARGO_TARGET_DIR','CARGO_BUILD_JOBS','RUSTC','CC','AR','OBJDUMP','OBJCOPY','CARGO_TARGET_SBPF_SOLANA_SOLANA_RUSTFLAGS']}}
(out/'build-attempt.json').write_text(json.dumps(record,indent=2)+'\n');start=time.time()
with(out/'build.log').open('w')as f:r=subprocess.run(command,cwd=workspace,env=env,stdout=f,stderr=subprocess.STDOUT)
record.update(returncode=r.returncode,seconds=round(time.time()-start,3),source_after_sha256=source_manifest(crate,workspace,R,cwd=workspace),primary_source_after_sha256=source_manifest(primary,primary,R,cwd=primary))
record['source_unchanged']=record['source_sha256']==record['source_after_sha256']and record['primary_source_sha256']==record['primary_source_after_sha256'];record['tools_unchanged']=tools_before=={n:sha(f)for n,f in tools.items()};record['sdk_rust_libraries_unchanged']=all(sha(prepared/n)==h for n,h in sdk_before.items());record['registry_sources_unchanged']=all(sha(Path(root)/n)==h for root,files in registry_sources.items()for n,h in files.items());record['target_libraries_unchanged']=libs_before==profile.inventory(prepared/'rust/lib/rustlib/sbpf-solana-solana/lib');record['target_library_profile']=profile.finish(profile_record)
(out/'build-attempt.json').write_text(json.dumps(record,indent=2)+'\n');r.check_returncode();assert all(record[k]for k in ['source_unchanged','tools_unchanged','sdk_rust_libraries_unchanged','registry_sources_unchanged','target_libraries_unchanged'])
log=(out/'build.log').read_text();assert'exceeded max offset'not in log
built=target/'sbpf-solana-solana/release/pump_recovered.so';shutil.copy2(built,out/'unstripped.so');subprocess.run([str(tools['objcopy']),'--strip-all',str(built),str(out/'candidate.so')],check=True)
record.update(unstripped_sha256=sha(out/'unstripped.so'),build_log_sha256=sha(out/'build.log'),comparison=compare((R/'evidence/original/pump/deployed.so').read_bytes(),(out/'candidate.so').read_bytes()))
record['qualified_image_hashes_equal']=record['comparison']['candidate_sha256']==expected['comparison']['candidate_sha256']and record['unstripped_sha256']==expected['unstripped_sha256']
for n in ['build-attempt.json','build-comparison.json']:(out/n).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'returncode':r.returncode,'cold_empty_target':True,'locked_registry_packages':len(archives),'registry_source_files':files_checked,'candidate_sha256':record['comparison']['candidate_sha256'],'unstripped_sha256':record['unstripped_sha256'],'qualified_image_hashes_equal':record['qualified_image_hashes_equal'],'seconds':record['seconds']},indent=2));assert record['qualified_image_hashes_equal']
