from pathlib import Path
from collections import Counter
from functools import lru_cache
import gzip,hashlib,importlib.util,json
P=Path(__file__).resolve().parent;R=P.parents[1];D=P/'run-40622104447'
sha=lambda b:hashlib.sha256(b).hexdigest()
for base in [P,D]:
 m=json.loads((base/'MANIFEST.json').read_text())
 assert all(sha((base/k).read_bytes())==v for k,v in m.items())
assert (D/'revision.txt').read_text().strip()=='ec657c8253d86a6c45e504ce7164642a1dd59074'
assert json.loads((D/'host.json').read_text())['system']=='Darwin'
spec=json.loads((D/'inputs.json').read_text())
a=importlib.util.spec_from_file_location('windows',R/spec['window_reader']);w=importlib.util.module_from_spec(a);a.loader.exec_module(w)
w.m.elf_layout=lru_cache(maxsize=8)(w.m.elf_layout);w.m.relocations=lru_cache(maxsize=8)(w.m.relocations)
original=(R/'evidence/original/pump/deployed.so').read_bytes();ow=w.windows(original);oc=Counter(x['signature']for x in ow);raw=Counter(x['raw_sha256']for x in ow)
assert len(ow)==1035 and sha(original)=='7a19affaa2c6187e04a5fe0ea298cee81fa5eb8c24cfcc30d85f615e89f7b02d'
measurement=json.loads((D/'measurement.json').read_text());images={};counters={}
for label,count,raw_count in [('baseline',744,121),('candidate',795,121),('repeat',795,121),('round37-identity',744,121),('round37-canonical',744,175)]:
 b=D/label;images[label]={n:gzip.decompress((b/(n+'.gz')).read_bytes())for n in ['candidate.so','unstripped.so']}
 record=json.loads(gzip.decompress((b/'build-comparison.json.gz').read_bytes()));assert record['returncode']==0 and record['source_unchanged']
 rows=w.windows(images[label]['unstripped.so']);cc=Counter(x['signature']for x in rows);counters[label]=cc
 assert sum((oc&cc).values())==count and sum((raw&Counter(x['raw_sha256']for x in rows)).values())==raw_count
 assert sha(images[label]['candidate.so'])==measurement['builds'][label]['candidate_sha256']
 assert sha(images[label]['unstripped.so'])==measurement['builds'][label]['unstripped_sha256']
profile_spec=json.loads((R/'scripts/pump_linux_v144_sbf_libraries.json').read_text())
checkpoint=json.loads((R/'repro/pump/main-contract-round37-20261027/CHECKPOINT.json').read_text())
digest=lambda x:sha(json.dumps(x,sort_keys=True,separators=(',',':')).encode())
for label in images:
 record=json.loads(gzip.decompress((D/label/'build-comparison.json.gz').read_bytes()))
 profile=record['target_library_profile'];assert profile['native_host_files_unchanged'] is True
 assert profile['cache_context']==checkpoint['target_library_profile_context']
 data=gzip.decompress((D/label/'target-library-profile-files.json.gz').read_bytes())
 assert sha(data)==profile['file_manifest_sha256'];files=json.loads(data)
 assert digest(files['native'])==profile['cache_context']['native_sdk_manifest_sha256']
 assert digest(files['prepared'])==profile['cache_context']['prepared_sdk_manifest_sha256']
 assert all(files['native'][name]['sha256']==h for name,h in profile_spec['native_tools'].items())
 assert profile['cache_context']['target_libraries']==profile_spec['target_libraries']
 if label!='baseline':assert record['dependency_cache']['main_freshly_compiled'] is True
assert images['candidate']==images['repeat']
assert sum(((oc&counters['baseline'])&counters['candidate']).values())==744
assert sha(images['round37-canonical']['candidate.so'])==spec['round37_candidate_sha256']
assert sha(images['round37-canonical']['unstripped.so'])==spec['round37_unstripped_sha256']
assert not measurement['whole_elf_equal']
print('Verified 57 artifact hashes, exact canonical Round37 hashes, repeated native 795 builds, all 744 retained; whole original ELF equality remains false.')

import tarfile
assert spec==json.loads((P/'inputs.json').read_text())
assert sha((R/spec['primary_archive']).read_bytes())==spec['primary_archive_sha256']
for label in images:
 record=json.loads(gzip.decompress((D/label/'build-comparison.json.gz').read_bytes()))
 with tarfile.open(D/label/'compiled-source.tar.gz')as archive:files={m.name:sha(archive.extractfile(m).read())for m in archive.getmembers()if m.isfile()}
 assert all('/source/'in key and files[key.split('/source/',1)[1]]==digest for key,digest in record['source_sha256'].items())
print('Verified actual compiled-source archives for all five native builds; full runtime qualification remains separate.')



T=P/'runtime'
m=json.loads((T/'MANIFEST.json').read_text());assert all(sha((T/k).read_bytes())==v for k,v in m.items())
full=json.loads(gzip.decompress((T/'full.json.gz').read_bytes()));rec=json.loads((T/'recipients.json').read_text());binding=json.loads((T/'native-input-binding.json').read_text())
h=sha(images['candidate']['candidate.so'])
assert full['candidate_sha256']==rec['candidate_sha256']==binding['candidate_sha256']==h
assert binding['native_artifact_manifest_sha256']==sha((D/'MANIFEST.json').read_bytes())
assert binding['native_build_record_sha256']==sha(gzip.decompress((D/'candidate/build-comparison.json.gz').read_bytes()))
assert binding['compiled_source_sha256']==full['compiled_source_sha256']
assert len(full['suites'])==44 and full['case_count']==10468 and not full['mismatches']
assert full['diagnostics']['log_bearing_cases']==10464 and not full['diagnostics']['mismatches']
assert rec['case_count']==42 and not rec['mismatches']
assert len(full['loader_receipts'])==44
for name,receipt in full['loader_receipts'].items():
 p=T/'full.json.gz.suites'/(name+'.loader.json');assert sha(p.read_bytes())==receipt['sha256']
 doc=json.loads(p.read_text())
 loads=doc['loads'];assert len(loads)==receipt['load_count']
 for load in loads:
  assert load['elf_sha256'] in [h,sha(original)] and load['elf_prefix_unchanged'] and load['zero_allocation_tail']
  assert load['program_bytes']==36 and load['programdata_bytes']==10485760
print('Verified native-bound 44-suite runtime corpus (10,468 cases, zero diagnostic mismatches) and separate 42 recipient cases.')

from importlib import util
s=util.spec_from_file_location('audit',R/'scripts/pump_diagnostic_audit.py');audit=util.module_from_spec(s);s.loader.exec_module(audit)
for label,count in [('legacy_migration_quote',20),('v2_migration_quote',40)]:
 report=json.loads(gzip.decompress((T/(label+'.json.gz')).read_bytes()))
 assert report['candidate_sha256']==h and report['original_sha256']==sha(original)
 assert report['case_count']==len(report['cases'])==count and not report['mismatches']
 check=audit.audit({label:report});assert check['log_bearing_cases']==count and not check['mismatches']
 receipt=json.loads((T/(label+'.loader.json')).read_text());assert {x['elf_sha256']for x in receipt['loads']}=={h,sha(original)}
 assert all(x['program_bytes']==36 and x['programdata_bytes']==10485760 and x['elf_prefix_unchanged']and x['zero_allocation_tail']for x in receipt['loads'])
print('Independently verified additional 20 legacy and 40 migration-v2 post-completion quote cases; controls can overlap.')
