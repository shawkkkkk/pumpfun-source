#!/usr/bin/env python3
"""Read-only actual CTO outgoing-edge census; no source edit/compile/mask change."""
from pathlib import Path
import collections,hashlib,importlib.util,json
P=Path(__file__).resolve().parent;D=P.parent;T=D/'layout-frontier-reconcile/tools/elf_reader.py';s=importlib.util.spec_from_file_location('bounded_elf',T);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);sha=lambda b:hashlib.sha256(b).hexdigest();stable=lambda x:sha(json.dumps(x,sort_keys=True,separators=(',',':')).encode())
paths={'original':Path('/workspace/pumpfun-source-latest/evidence/original/pump/deployed.so'),'f4':Path('/workspace/pump-current673-native-results/cto-40792775552/unstripped.so'),'5203':Path('/workspace/pump-current673-native-results/cto-used-flow-40794982049/unstripped.so')};elves={k:m.Elf(v)for k,v in paths.items()};expected={'original':'7a19affaa2c6187e04a5fe0ea298cee81fa5eb8c24cfcc30d85f615e89f7b02d','f4':'daa2772d4745d8488b357c6c1c088fadc77bf31d341c59f5b50c4706d7b54c78','5203':'388fa73431d68cb0a89e9c939f1645510abd844652f4272ef1a841a0ec60bbe0'};assert{n:sha(e.b)for n,e in elves.items()}==expected
functions={};parents={};tags={}
for name,e in elves.items():
 if name=='original':functions[name]={a:{'start':a,'size':z-a,'name':''}for a,z in zip(e.entries,e.entries[1:]+[e.hi])};assert len(functions[name])==1035;parents[name]=functions[name][0x22a10];assert parents[name]['size']==27400
 else:
  functions[name]={}
  for f in e.funcs:
   if f['start']not in functions[name]or functions[name][f['start']]['size']<f['size']:functions[name][f['start']]=f
  found=[f for f in functions[name].values()if'9admin_cto7execute'in f['name']];assert len(found)==1;parents[name]=found[0]
def tag(name,at,depth):
 key=(name,at,depth)
 if key not in tags:
  fs=functions[name];e=elves[name]
  if at not in fs:tags[key]={'unresolved_actual_target':hex(at)}
  else:
   f=fs[at];n=f['size'];tags[key]={'bytes':n,'normalized_sha256':sha(e.normalized[at:at+n]),'relocation_pattern':e.pattern(at,n),'actual_direct_children':[{'offset':c['offset'],'identity':tag(name,c['target'],depth-1)}for c in e.callsites(at,n)]if depth else []}
 return tags[key]
# Names are labels only, never used to select or substitute an actual callee target.
labels=collections.defaultdict(set)
for name in ['f4','5203']:
 for at,f in functions[name].items():labels[stable(tag(name,at,0))].add(f['name'])
results={};countsets={}
for name,e in elves.items():
 f=parents[name];calls=[]
 for row in e.callsites(f['start'],f['size']):
  at=row['target'];fs=functions[name].get(at);identity=stable(tag(name,at,0));calls.append({'offset':hex(row['offset']),'actual_target':hex(at),'bytes':fs['size']if fs else None,'actual_symbol':fs['name']if fs else None,'same_body_symbol_labels':sorted(labels[identity]),'body_pattern_identity':identity,'depth2_actual_edges_identity':stable(tag(name,at,2))})
 externals=[{'offset':hex(at-f['start']),**r}for at,r in e.relocations.items()if f['start']<=at<f['start']+f['size']and r['type']==10]
 clone=next((at for at,fs in functions[name].items()if'AccountInfo'in fs['name']and'clone'in fs['name']),None)if name!='original'else 0x10c78
 categories={}
 for category in ['clone','memcmp','memcpy','ToString','Display','pay_token']:
  selected=[r for r in calls if(any(category in n for n in r['same_body_symbol_labels'])if name=='original'else category in(r['actual_symbol']or''))]
  categories[category]={'count':len(selected),'actual_targets':sorted(set(r['actual_target']for r in selected)),'offsets':[r['offset']for r in selected],'label_note':'Original labels are normalized-body+pattern class aliases, not a unique historical symbol attribution.'if name=='original'else'Actual symbol at actual called target'}
 results[name]={'parent':{'start':hex(f['start']),'bytes':f['size'],'raw_sha256':sha(e.b[f['start']:f['start']+f['size']])},'defined_direct_calls':len(calls),'indirect_callx_offsets':[hex(i-f['start'])for i in range(f['start'],f['start']+f['size'],8)if e.b[i]==0x8d],'external_relocations':externals,'categories':categories,'calls':calls};countsets[name]={depth:collections.Counter(r[key]for r in calls)for depth,key in [(0,'body_pattern_identity'),(2,'depth2_actual_edges_identity')]}
deltas={}
for before in ['original','f4']:
 deltas[before]={}
 for depth in [0,2]:
  a,b=countsets[before][depth],countsets['5203'][depth];changed=[]
  for k in sorted(set(a)|set(b)):
   if a[k]!=b[k]:
    key='body_pattern_identity'if depth==0 else'depth2_actual_edges_identity';witness=next(r for r in results['5203']['calls']+results[before]['calls']if r[key]==k);changed.append({'identity':k,'before_count':a[k],'candidate_count':b[k],'actual_symbol_labels':witness['same_body_symbol_labels'],'witness_actual_target':witness['actual_target'],'witness_bytes':witness['bytes']})
  deltas[before][str(depth)]=changed
r={'scope':__doc__,'inputs':expected,'existing_decoder_sha256':sha(T.read_bytes()),'normalization_limit':'Existing relocation-only Elf normalized body+relocation pattern, actual target edges to depth2. Names label classes only; no arbitrary alternate target replaces an actual edge. This is not whole-parent, typed data pointee, or semantic equivalence.','parents':results,'actual_callee_count_deltas_to_5203':deltas};(P/'callees.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print(json.dumps({'output':str(P/'callees.json'),'sha256':sha((P/'callees.json').read_bytes()),'parents':{k:{'parent':v['parent'],'defined_calls':v['defined_direct_calls'],'callx':v['indirect_callx_offsets'],'category_counts':{c:row['count']for c,row in v['categories'].items()}}for k,v in results.items()},'f4_deltas':deltas['f4']},indent=2))
