#!/usr/bin/env python3
"""Stage exactly three qualified files on current-main65; no Cargo/compiler execution."""
from pathlib import Path
import base64,copy,difflib,gzip,hashlib,io,json,re,shutil,subprocess,tarfile,tomllib
P=Path(__file__).resolve().parent;REV='5634890b9b7aa03dccb82b22ec0e1dc9f2e1eaa1';PKG='research/pump-multihop-accrual-qualification-20261028';CONTROL=Path('/workspace/pump-current673-native-results/perhop-40792780769');BOUND=Path('/workspace/pumpfun-source-workers/pump-creation/work/pump-creation/resume-1285b5e9/perhop-clock-snapshot/MAIN-65-BOUND.json')
sha=lambda b:hashlib.sha256(b).hexdigest();blob=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();load=lambda p:json.loads(Path(p).read_text())
def dump(name,x):(P/name).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def read_archive(path):
 out={}
 with tarfile.open(path)as t:
  for q in t:
   assert q.isfile()and not Path(q.name).is_absolute()and'..'not in Path(q.name).parts and q.name not in out
   out[q.name]=t.extractfile(q).read()
 return out

def save_tree(folder,files):
 assert not folder.exists()
 for name,raw in files.items():
  q=folder/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(raw)
 assert {str(q.relative_to(folder)):sha(q.read_bytes())for q in folder.rglob('*')if q.is_file()}=={n:sha(b)for n,b in files.items()}

def archive(name,files):
 stream=io.BytesIO()
 with tarfile.open(fileobj=stream,mode='w')as t:
  for n,b in sorted(files.items()):
   q=tarfile.TarInfo(n);q.size=len(b);q.mode=0o644;q.mtime=0;t.addfile(q,io.BytesIO(b))
 (P/name).write_bytes(gzip.compress(stream.getvalue(),mtime=0))

def wrap(standalone):
 # Exact staging transformation from current c7d215 builder, checked against actual control66 below.
 text=standalone['Cargo.toml'].decode();parsed=tomllib.loads(text);assert parsed.get('workspace')=={} and set(parsed.get('profile',{}))=={'release'}
 ps=text.index('[profile.release]');ws=text.index('[workspace]');assert not text[ws+len('[workspace]'):].strip();release=text[ps:ws].strip()+'\n';files={'programs/pump/'+n:b for n,b in standalone.items()if n not in ['Cargo.toml','Cargo.lock']};files['programs/pump/Cargo.toml']=(text[:ps].rstrip()+'\n').encode();files['Cargo.toml']=('[workspace]\nmembers = ["programs/pump"]\nresolver = "2"\n\n'+release).encode();files['Cargo.lock']=standalone['Cargo.lock'];return files

ref=P/'references';ref.mkdir(exist_ok=True)
response=json.loads(subprocess.check_output(['gh','api',f'repos/lalalune/pumpfun-source/contents/{PKG}/build-inputs.json?ref={REV}']));inputs_raw=base64.b64decode(response['content']);assert blob(inputs_raw)==response['sha'];assert sha(inputs_raw)=='67b568a5ca6141f0607be9cce90fe12fd4fe86d2ca240f3d6953eecd117e5a4b';(ref/'current-build-inputs.json').write_bytes(inputs_raw);expected=json.loads(inputs_raw)
assert sha((P/'current-maintained-build.py').read_bytes())=='c7d215a92dbb733cae044b40d06ce5da45df7d5c84fe2985acea023ecd316241'
proof=load(BOUND);tree={r['path']:r['sha']for r in load(P/'main-pump-tree.json')['tree']if r['type']=='blob'};actual66=read_archive(CONTROL/'compiled-source.tar.gz');assert len(actual66)==66
base={};bindings=[]
for row in proof['files']:
 name=row['path'].removeprefix('programs/pump/');assert tree[name]==row['main_git_oid']
 raw=(P/'main-standalone-Cargo.toml').read_bytes()if name=='Cargo.toml'else actual66['Cargo.lock'if name=='Cargo.lock'else'programs/pump/'+name]
 assert sha(raw)==row['main_sha256']and blob(raw)==tree[name],name;base[name]=raw;bindings.append({'path':'programs/pump/'+name,'sha256':sha(raw),'git_blob':blob(raw)})
assert len(base)==65 and{n:sha(b)for n,b in base.items()}==expected['source_inputs'];assert wrap(base)==actual66
control=load(CONTROL/'build-attempt.json');assert control['returncode']==0 and control['source_unchanged']and control['tools_unchanged']and control['target_libraries_unchanged']
assert sha((CONTROL/'candidate.so').read_bytes())=='c0e29e2d41c30e854f3548b37e87798d516e4e0e7769f40b7d8d16e31429795f';assert sha((CONTROL/'unstripped.so').read_bytes())=='dd73afe77d90d289e9383ee1aa12cdb26608752eb1a1f8b3a4135c0af786cb17'
assert control['tool_sha256']==expected['tool_sha256']and control['target_libraries_sha256']==expected['target_libraries_sha256'];assert len(expected['tool_sha256'])==5 and expected['target_libraries_sha256']
for n in ['host.json','build-attempt.json','target-library-profile-files.json','registry-authentication.json','executed-builder.py','measurement-adapter.patch']:
 if(CONTROL/n).is_file():shutil.copy2(CONTROL/n,ref/('current-control-'+n))
components=[{'name':'cto-used-cpi-flow','file':'src/creator/admin_cto.rs','source':Path('/workspace/pump-admin-cto/candidates/used-cpi-flow/admin_cto.rs'),'sha':'5203d20c2e63be7337204491588e0ec69808f8ddd39d96b8b5fa1964d6ec201d','build':Path('/workspace/pump-current673-native-results/cto-used-flow-40794982049'),'pr':'https://github.com/lalalune/pumpfun-source/pull/730','head':'1d9326956d272b25498cd8aad3fae73d4b6ae9a5'}, {'name':'sweep-native-read-order','file':'src/sweep_fees.rs','source':Path('/workspace/pumpfun-source-workers/pump-lifecycle/work/pump-lifecycle/sweep-native-read-order-673/source/programs/pump/src/sweep_fees.rs'),'sha':'3d3363ddd7713999363bf950fb404fa4e35e42731d43806cb6ceeccda94985e9','build':Path('/workspace/pump-current673-native-results/sweep-read-timing-40796286687'),'pr':None,'head':None}, {'name':'perhop-clock-snapshot','file':'src/multi_hop_curve_swap.rs','source':Path('/workspace/pumpfun-source-workers/pump-creation/work/pump-creation/resume-1285b5e9/perhop-clock-snapshot/multi_hop_curve_swap.rs'),'sha':'5871a2cf35ebe0db502eb242db0f1652ef93e51e4971e56483016d900349ac2b','build':Path('/workspace/pump-current673-native-results/perhop-clock-40795474496'),'pr':'https://github.com/lalalune/pumpfun-source/pull/731','head':'77e1701644494179606fa83d082934eff9dcdaa1'}]
composed=dict(base);component_records=[]
for c in components:
 raw=c['source'].read_bytes();assert sha(raw)==c['sha'];archive_files=read_archive(c['build']/'compiled-source.tar.gz');assert archive_files['programs/pump/'+c['file']]==raw
 actual=load(c['build']/'build-attempt.json');assert actual['returncode']==0 and actual['source_unchanged']and actual['tools_unchanged']and actual['target_libraries_unchanged'];assert actual['tool_sha256']==expected['tool_sha256']and actual['target_libraries_sha256']==expected['target_libraries_sha256'];assert actual['sdk_rust_libraries_sha256']==control['sdk_rust_libraries_sha256'];assert len(archive_files)==66
 compared=[n for n in sorted(actual66)if archive_files[n]!=actual66[n]];assert set(compared)<={'programs/pump/'+c['file'],'programs/pump/src/multi_hop_curve_swap.rs'},compared
 composed[c['file']]=raw
 record={k:(str(v)if isinstance(v,Path)else v)for k,v in c.items()};record.update({'before_main_sha256':sha(base[c['file']]),'actual_source_archive_sha256':sha((c['build']/'compiled-source.tar.gz').read_bytes()),'actual_source_archive_deltas_from_current_control66':compared,'actual_candidate_sha256':sha((c['build']/'candidate.so').read_bytes()),'actual_symbols_sha256':sha((c['build']/'unstripped.so').read_bytes()),'actual_build_record_sha256':sha((c['build']/'build-attempt.json').read_bytes()),'same_all_recorded_tool_and_target_library_pins_as_current711':True,'target_library_file_count':len(expected['target_libraries_sha256']),'component_build_host':load(c['build']/'host.json')})
 component_records.append(record)
changes=[n for n in sorted(base)if base[n]!=composed[n]];assert set(changes)=={c['file']for c in components};compiled=wrap(composed);assert len(compiled)==66;workspace_changes=[n for n in sorted(actual66)if actual66[n]!=compiled[n]];assert set(workspace_changes)=={'programs/pump/'+n for n in changes}
# Public signatures are unchanged; record private helper changes rather than concealing them.
def signatures(raw):
 text=re.sub(r'(?m)//[^\n]*','',raw.decode());return [{'public':bool(m.group(1)),'name':m.group(2),'signature':' '.join(m.group(0).rsplit('{',1)[0].split())}for m in re.finditer(r'(?m)(pub(?:\([^)]*\))?\s+)?fn\s+(\w+)[^{;]+\{',text)]
api=[]
for n in changes:
 before,after=signatures(base[n]),signatures(composed[n]);assert [v for v in before if v['public']]==[v for v in after if v['public']],n
 api.append({'file':n,'public_signature_equality':True,'before_signatures':before,'after_signatures':after})
for folder,files in [('current-standalone/programs/pump',base),('current-workspace',actual66),('composed-standalone/programs/pump',composed),('composed-workspace',compiled)]:save_tree(P/folder,files)
archive('composed-standalone-source65.tar.gz',{'programs/pump/'+n:b for n,b in composed.items()});archive('composed-workspace66.tar.gz',compiled)
patch=''.join(''.join(difflib.unified_diff(base[n].decode().splitlines(True),composed[n].decode().splitlines(True),fromfile='a/programs/pump/'+n,tofile='b/programs/pump/'+n))for n in changes);(P/'source.patch').write_text(patch)
dump('CURRENT-MAIN-65.json',{'current_main':REV,'current_program_tree':next(v['sha']for v in load(P/'main-programs-tree.json')['tree']if v['path']=='pump'),'all65_actual_bytes_match_current_Git_blob_ids':True,'published_current_build_inputs_sha256':sha(inputs_raw),'published65_source_map_exact':True,'actual_current_control66_source_map_exact':True,'files':bindings})
dump('COMPONENTS.json',component_records);dump('API-COMPATIBILITY.json',api);dump('MANIFESTS.json',{'standalone_inputs':65,'workspace_inputs':66,'current_main':REV,'current_standalone_sha256':{'programs/pump/'+n:sha(b)for n,b in sorted(base.items())},'current_workspace_sha256':{n:sha(b)for n,b in sorted(actual66.items())},'composed_standalone_sha256':{'programs/pump/'+n:sha(b)for n,b in sorted(composed.items())},'composed_workspace_sha256':{n:sha(b)for n,b in sorted(compiled.items())},'only_changed_standalone_paths':['programs/pump/'+n for n in changes],'only_changed_workspace_paths':workspace_changes,'source_or_library_or_Cargo_or_SDK_variants':False,'compilation_executed':False})
dump('RECIPE-INSPECTION.json',{'current_main':REV,'selected_package':PKG,'published_builder_sha256':sha((P/'current-maintained-build.py').read_bytes()),'published_build_inputs_sha256':sha(inputs_raw),'actual_current_control':str(CONTROL),'actual_current_host':load(CONTROL/'host.json'),'actual_tool_pins_all5':control['tool_sha256'],'actual_target_library_pins_entire_recorded_map':control['target_libraries_sha256'],'actual_target_library_file_count':len(control['target_libraries_sha256']),'actual_target_empty_directories':control['target_library_profile']['cache_context']['empty_directories'],'actual_sdk_rust_libraries_entire_map':control['sdk_rust_libraries_sha256'],'actual_source_wrapper_sha256':control['source_wrapper_sha256'],'actual_target_library_profile':control['target_library_profile'],'actual_build_command':control['command'],'actual_environment':control['environment'],'actual_registry_authentication_sha256':control['registry_authentication_sha256'],'current_expected_stripped':'c0e29e2d41c30e854f3548b37e87798d516e4e0e7769f40b7d8d16e31429795f','current_expected_symbols':'dd73afe77d90d289e9383ee1aa12cdb26608752eb1a1f8b3a4135c0af786cb17','candidate_output_hashes_predicted':False,'candidate_window_counts_predicted':False,'native_Linux_host_portability_claimed':False,'compiler_invocations_by_this_plan':0})
print(json.dumps({'current_main':REV,'base_source65':True,'workspace66_exact_to_current_native_control':True,'only_changed':changes,'component_hosts':[r['component_build_host']for r in component_records],'all_recorded_tools_and_target_library_files_exact':True,'tool_files':len(expected['tool_sha256']),'target_library_files':len(expected['target_libraries_sha256']),'empty_target_directories':control['target_library_profile']['cache_context']['empty_directories'],'compiler_invocations':0,'staging':str(P)}))
