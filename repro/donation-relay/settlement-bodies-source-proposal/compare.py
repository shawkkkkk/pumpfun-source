"""Read-only opt-in ELF remeasurement; never reads build or runtime receipts."""
import collections,hashlib,importlib.util,json,struct,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=next(p for p in HERE.parents if(p/'.git').exists())

def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
def data_graph(a,derived,original,symbols):
 o,c=a.Elf(original),a.Elf(symbols);O=derived['original-function-ledger.json'];C=derived['candidate-function-ledger.json'];os={r['start']:r['ordinal']for r in O};cs={r['start']:r['index']for r in C};w={(r['original_ordinal'],r['candidate_index']):r for r in derived['match-witnesses.json']};so=o.by_name['.data.rel.ro'];sc=c.by_name['.data.rel.ro'];assert so['size']==sc['size'];rows=[];counts=collections.Counter();nonpointer=0
 for off in range(0,so['size'],8):
  u=o.relocations.get(so['address']+off);v=c.relocations.get(sc['address']+off)
  if not u and not v:
   assert o.at(so['address']+off,8)==c.at(sc['address']+off,8);nonpointer+=1;continue
  assert u and v and u['type']==v['type']==8 and u['symbol']==v['symbol'];ol,oa=struct.unpack('<II',o.at(so['address']+off,8));cl,ca=struct.unpack('<II',c.at(sc['address']+off,8));assert ol==cl==0
  ot,ct=o.containing(oa),c.containing(ca);r={'offset':off,'original_target':oa,'candidate_target':ca,'raw_pointer_equal':oa==ca,'original_section':None if not ot else ot['name'],'candidate_section':None if not ct else ct['name']}
  if ot and ct and ot['name']==ct['name']=='.text':
   oi,ci=os.get(oa),cs.get(ca);pair=w.get((oi,ci));r.update(original_function=oi,candidate_function=ci,normalized_matched_body=pair is not None,recursive_call_shape_closed=bool(pair and pair['recursive_call_shape_closed']),has_indirect_calls=bool(pair and pair['indirect_calls']));category='text_closed'if r['recursive_call_shape_closed']else'text_not_closed'
  elif ot and ct and ot['name']==ct['name']=='.rodata':
   x,y=oa-ot['address'],ca-ct['address'];n=min(64,ot['size']-x,ct['size']-y);r.update(section_relative_offsets_equal=x==y,bounded_comparison_bytes=n,bounded_bytes_equal=o.at(oa,n)==c.at(ca,n));category='rodata_equal64'if r['bounded_bytes_equal']else'rodata_bounded_mismatch'
  elif ot and ct and ot['name']==ct['name']=='.data.rel.ro':
   r['section_relative_offsets_equal']=oa-ot['address']==ca-ct['address'];category='data_rel_ro_same_offset'if r['section_relative_offsets_equal']else'data_rel_ro_different_offset'
  else:category='unclassified'
  r['category']=category;counts[category]+=1;rows.append(r)
 full=o.section_bytes(o.by_name['.rodata'])==c.section_bytes(c.by_name['.rodata']);shape=full and all((r['category']=='rodata_equal64'and r['section_relative_offsets_equal'])or r['category']in ['text_closed','data_rel_ro_same_offset']for r in rows)
 return {'full_rodata_equal':full,'relocated_data_shape_equal':shape,'relocated_pointer_count':len(rows),'exact_nonpointer_qwords':nonpointer,'categories':dict(counts),'text_targets_with_indirect_calls':sum(r.get('has_indirect_calls',False)for r in rows),'rows':rows,'scope':'All positional data.rel.ro relocations and nonpointer qwords, complete rodata section. Text targets only direct-call shape; no indirect behavior, full semantic or whole-file proof.'}
def analysis(a,build):
 paths={'original.so':ROOT/'evidence/dependencies/donation_relay/deployed.so','original-windows.json':ROOT/'repro/donation-relay/swap-receipt-coordinate-recovery/original-windows.json','candidate.so':build/'candidate.so','unstripped.so':build/'symbols.so'}
 with tempfile.TemporaryDirectory()as temp:
  d=Path(temp)
  for name,path in paths.items():(d/name).write_bytes(path.read_bytes())
  result=a.analyze(d)
 return result,paths

def compact(result):
 return {'summary':result['comparison-summary.json'],'sections':result['section-comparison.json'],'inventories':{k:[r['ordinal']for r in result['match-ledger.json']if r[k+'_candidate_indices']]for k in ['normalized','raw']}}

def recompute(baseline_build,candidate_build):
 for name,digest in read(HERE/'comparison-inputs.json').items():assert sha((ROOT/name).read_bytes())==digest
 spec=importlib.util.spec_from_file_location('settlement_pinned_parser',ROOT/'repro/donation-relay/swap-receipt-coordinate-recovery/analyze.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
 before,_=analysis(a,baseline_build);after,paths=analysis(a,candidate_build);b,c=compact(before),compact(after)
 result={'baseline':b,'recovered':c}
 for key,prefix in [('normalized',''),('raw','raw_')]:
  result[prefix+'gains']=sorted(set(c['inventories'][key])-set(b['inventories'][key]));result[prefix+'losses']=sorted(set(b['inventories'][key])-set(c['inventories'][key]))
 result['unmatched']=[r['ordinal']for r in after['match-ledger.json']if not r['normalized_candidate_indices']]
 proof=[]
 for ordinal,count in [(97,36),(98,38),(100,25)]:
  ledger=after['match-ledger.json'][ordinal];assert ledger['normalized_candidate_indices']==[ordinal]
  witness=next(r for r in after['match-witnesses.json']if r['original_ordinal']==ordinal and r['candidate_index']==ordinal)
  assert not witness['raw_body'] and witness['recursive_call_shape_closed'] and not witness['indirect_calls'];assert len(witness['direct_calls'])==count
  assert all(r['normalized_body_pair']and r['recursive_call_shape_closed']for r in witness['direct_calls'])
  proof.append({'original_ordinal':ordinal,'candidate_index':ordinal,'bytes':ledger['bytes'],'raw_body_equal':False,'direct_calls':witness['direct_calls'],'indirect_calls':0,'direct_data_reference_count':len(witness['data_references'])})
 result['recovered_direct_calls']=proof
 graph=data_graph(a,after,paths['original.so'].read_bytes(),paths['unstripped.so'].read_bytes());rows=graph.pop('rows');graph['complete_rows_sha256']=sha((json.dumps(rows,sort_keys=True,indent=2)+'\n').encode());result['data_graph']=graph
 assert graph['full_rodata_equal']and graph['relocated_data_shape_equal'] and graph['relocated_pointer_count']==359 and graph['exact_nonpointer_qwords']==507
 return result

def compare(baseline_build,candidate_build):
 actual=recompute(baseline_build,candidate_build);assert actual==read(HERE/'expected.json')
 return {'normalized':488,'raw':142,'gains':actual['gains'],'losses':actual['losses'],'direct_callee_sites':99,'full_rodata_equal':True,'data_pointer_sites_checked':359,'runtime_verified':False}
