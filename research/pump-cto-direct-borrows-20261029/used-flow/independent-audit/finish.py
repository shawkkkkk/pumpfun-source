#!/usr/bin/env python3
"""Seal actual 5203 payout callee/depth2 and token-helper Location constraints."""
from pathlib import Path
import hashlib,importlib.util,json,re,struct,tarfile
P=Path(__file__).resolve().parent;D=P.parent;T=D/'layout-frontier-reconcile/tools/elf_reader.py';s=importlib.util.spec_from_file_location('seal_elf',T);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);sha=lambda b:hashlib.sha256(b).hexdigest()
paths={'original':Path('/workspace/pumpfun-source-latest/evidence/original/pump/deployed.so'),'f4':Path('/workspace/pump-current673-native-results/cto-40792775552/unstripped.so'),'5203':Path('/workspace/pump-current673-native-results/cto-used-flow-40794982049/unstripped.so')};es={n:m.Elf(p)for n,p in paths.items()};fs={}
for n,e in es.items():
 fs[n]={}
 for f in e.funcs:
  if f['start']not in fs[n]or fs[n][f['start']]['size']<f['size']:fs[n][f['start']]=f
ends=dict(zip(es['original'].entries,es['original'].entries[1:]+[es['original'].hi]));parent=next(f for f in fs['5203'].values()if'9admin_cto7execute'in f['name']);root_calls=[c for c in es['5203'].callsites(parent['start'],parent['size'])if'17create_idempotent'in fs['5203'][c['target']]['name']or'21transfer_vault_tokens'in fs['5203'][c['target']]['name']]
pending=[(0x17e428,c['target'],0)for c in root_calls if'17create_idempotent'in fs['5203'][c['target']]['name']]+[(0x93898,c['target'],0)for c in root_calls if'21transfer_vault_tokens'in fs['5203'][c['target']]['name']];rows=[];seen=set()
while pending:
 a,b,d=pending.pop(0)
 if(a,b)in seen:continue
 seen.add((a,b));size=ends[a]-a;f=fs['5203'].get(b);o,n=es['original'],es['5203'];eq=bool(f and f['size']==size and o.normalized[a:a+size]==n.normalized[b:b+size]and o.pattern(a,size)==n.pattern(b,size));r={'original':hex(a),'actual_new_target':hex(b),'depth':d,'bytes':size,'new_bytes':f['size']if f else None,'same_complete_normalized_body_and_relocation_pattern':eq,'actual_symbol':f['name']if f else None,'actual_child_edges':[]}
 if eq and d<2:
  oc,nc=o.callsites(a,size),n.callsites(b,size);assert [x['offset']for x in oc]==[x['offset']for x in nc]
  for x,y in zip(oc,nc):r['actual_child_edges'].append({'offset':hex(x['offset']),'original_target':hex(x['target']),'new_target':hex(y['target'])});pending.append((x['target'],y['target'],d+1))
 rows.append(r)
result={'scope':'Original actual holder/wallet ATA and holder transfer vs actual5203 callee bodies and actual outgoing edges depth2. No alternate-target substitution; static pointee/whole semantics excluded.','new_parent':{'start':hex(parent['start']),'bytes':parent['size']},'actual_source_identified_root_calls':root_calls,'pairs':rows,'pairs_checked':len(rows),'pairs_equal':sum(r['same_complete_normalized_body_and_relocation_pattern']for r in rows),'mismatches':[r for r in rows if not r['same_complete_normalized_body_and_relocation_pattern']]};assert result['pairs_checked']==result['pairs_equal']==21;(P/'original-actual-depth2.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
# Exact four token helper edges, not old addresses or arbitrary named alternatives.
token={n:next(f for f in fs[n].values()if'admin_cto16token_raw_amount'in f['name'])for n in ['f4','5203']};a,b=token.values();left=es['f4'].callsites(a['start'],a['size']);right=es['5203'].callsites(b['start'],b['size']);assert [r['offset']for r in left]==[r['offset']for r in right]==[0x18,0x40,0xc0,0x158];direct=[];locations=[];todo=[(x['target'],y['target'],0)for x,y in zip(left,right)];done=set();closure=[]
while todo:
 x,y,d=todo.pop(0)
 if(x,y)in done:continue
 done.add((x,y));xf,yf=fs['f4'][x],fs['5203'][y];e1,e2=es['f4'],es['5203'];size=xf['size'];assert size==yf['size']and e1.normalized[x:x+size]==e2.normalized[y:y+size]and e1.pattern(x,size)==e2.pattern(y,size)
 row={'f4_actual':hex(x),'new_actual':hex(y),'bytes':size,'depth':d,'symbol':yf['name'],'full_normalized_body_and_relocation_pattern_equal':True};closure.append(row)
 if d==0:
  direct.append(row)
  for rel in e1.pattern(x,size):
   if rel['type']!=8:continue
   off=rel['offset'];pair=[]
   for elf,at in [(e1,x+off),(e2,y+off)]:
    assert elf.b[at]==0x18;p=struct.unpack_from('<I',elf.b,at+4)[0]|struct.unpack_from('<I',elf.b,at+12)[0]<<32
    assert elf.relocations.get(p,{}).get('type')==8
    file=struct.unpack_from('<Q',elf.b,p)[0]>>32;n=struct.unpack_from('<Q',elf.b,p+8)[0];line,col=struct.unpack_from('<II',elf.b,p+16)
    pair.append({'record':hex(p),'file_pointer':hex(file),'file':elf.b[file:file+n].decode(),'length':n,'line':line,'column':col})
   assert {k:v for k,v in pair[0].items()if k not in ['record','file_pointer']}=={k:v for k,v in pair[1].items()if k not in ['record','file_pointer']}
   locations.append({'callee_offset':hex(off),'f4':pair[0],'new':pair[1],'typed_scope':'Location supplied by actual AccountInfo::data_is_empty borrow-failure path; no arbitrary table extent inferred.'})
 if d<2:
  xc,yc=e1.callsites(x,size),e2.callsites(y,size);assert [q['offset']for q in xc]==[q['offset']for q in yc]
  todo.extend((q['target'],r['target'],d+1)for q,r in zip(xc,yc))
assert len(direct)==4 and len(locations)==1 and locations[0]['new']['file']=='src/lib.rs'and locations[0]['new']['line']==102 and locations[0]['new']['column']==19
sources={}
for n in ['f4','5203']:
 with tarfile.open(paths[n].parent/'compiled-source.tar.gz')as tar:sources[n]=next(tar.extractfile(t).read()for t in tar if t.name=='programs/pump/src/creator/admin_cto.rs')
assert sha(sources['f4'])=='f4a2bb7d33431e0fb4911e39d5e03c8bb9f45c6f7a184da21d1a6762f9127955'and sha(sources['5203'])=='5203d20c2e63be7337204491588e0ec69808f8ddd39d96b8b5fa1964d6ec201d'
source_tokens={n:[{'token':r.group(),'line':v[:r.start()].count(b'\n')+1}for r in re.finditer(rb'(?:error!\(|err!\(|require(?:_eq|_neq|_keys_eq|_keys_neq|_gt|_gte)?!\(|\.unwrap\()',v)]for n,v in sources.items()}
# Source token set is a lexical observation, not the compiler's complete Source inventory.
lexical_equal=source_tokens['f4']==source_tokens['5203'];assert lexical_equal
for n in source_tokens:
 for r in source_tokens[n]:r['token']=r['token'].decode()
helper_lines={n:next(i+1 for i,line in enumerate(v.splitlines())if line.startswith(b'fn token_raw_amount('))for n,v in sources.items()};assert helper_lines=={'f4':775,'5203':772}
r={'scope':'Four actual token_raw_amount callee bodies/edges plus its actual SDK borrow-failure Location; no universal parent/semantic proof.','actual_sources_sha256':{n:sha(v)for n,v in sources.items()},'helper_source_lines':helper_lines,'four_actual_direct_callees':direct,'actual_recursive_edges_depth2':closure,'all_bounded_actual_pairs_equal':True,'bounded_pair_count':len(closure),'actual_location_records':locations,'lexical_error_require_unwrap_tokens':source_tokens,'lexical_tokens_equal':lexical_equal,'helper_direct_relocation_count':0,'observed_775_to_772_location_change':False,'meaning':'Only the lexical function-definition line moves. The448B helper differs only in its4actualCALL operands; its actual callees and depth2 actual edge identities match. The sole directcallee Location is unchanged src/lib.rs102:19, with naturally shifted addresses. This is not a claim that every parent Location/semantic effect is closed.'};(P/'token-helper-closure.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
files={q.name:{'sha256':sha(q.read_bytes()),'bytes':q.stat().st_size}for q in sorted(P.iterdir())if q.is_file()and q.name!='SUMMARY.json'};summary={'schema':'CTO_5203_INDEPENDENT_READ_ONLY_AUDIT_V1','images':{n:sha(v.b)for n,v in es.items()},'source_sha256':sha(sources['5203']),'published_source_selection_changed':False,'new_compile_or_source_edit':False,'body_bytes':{'original':27400,'f4':18104,'5203':18464},'defined_parent_calls':{'original':154,'f4':170,'5203':178},'reachable_accountinfo_copy_sites':{'original':54,'f4':55,'5203':54},'holder_extra_copy_removed':True,'three_program_first_context_groups_reproduce_original_source_pointer_order':True,'actual_original_payout_depth2_pairs_equal':21,'token_helper_actual_depth2_pairs_equal':len(closure),'helper_location':{'file':'src/lib.rs','line':102,'column':19,'unchanged':True},'source_line_775_to_772_is_lexical_only_in_observed_helper_evidence':True,'memcmp_parent_counts':{'original':14,'f4':15,'5203':15},'memcpy_parent_counts':{'original':6,'f4':7,'5203':8},'limits':'Bounded static body/actualedge/copy-source and typed Location observations. Official1035counts remain1019normalized/188raw; no window gain/wholeparent/runtime/private-source/semantic proof. Partial pointer slicer does not model callee sret writes; numeric amount uses separate explicit witnesses.','files':files};(P/'SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');print(json.dumps({'summary':str(P/'SUMMARY.json'),'sha256':sha((P/'SUMMARY.json').read_bytes()),'four_actual_callees_closed':4,'token_actual_pairs':len(closure),'payout_original_actual_pairs':21,'lexical_source_token_count':len(source_tokens['5203']),'Location':locations,'files':len(files)},indent=2))
