"""Explicit read-only local ELF comparison; no Git/network/build/VM/receipt access."""
import hashlib,importlib.util,json,struct
from pathlib import Path
if not __debug__:
 raise RuntimeError("Static verification requires Python assertions enabled")
P=Path(__file__).resolve().parent
OUTPUTS = {'baseline': {'candidate.so': 'cdd050b71f4df64f6a2f75b40c15eb2189ae75de2df77d71d2bd13198910e474', 'symbols.so': '1d2a0ac774a464a984c7407ea8b1a490f66ddae39e3539e17748020a9b7e8bab'}, 'candidate': {'candidate.so': '2f2613def4f89fb55e998c9581b48055760baf967b2bc7661f6b53eeaf68013d', 'symbols.so': 'c661a3a69b6197b14aa53b4601996cf198d539a8b2cb4f4b80e09372d1b24164'}}
H=lambda b:hashlib.sha256(b).hexdigest()
def location(w,image,target):
 rel=dict(w.m.relocations(image));assert rel.get(target,0)&0xffffffff==8
 raw=w.m.at_address(image,target,24);low,ptr,n,line,column=struct.unpack('<IIQII',raw)
 assert low==0 and 0<n<=300 and 0<line<=100000 and 0<column<=300
 section=next(s for s in w.m.elf_layout(image)['sections']if s['name']=='.rodata');assert section['address']<=ptr and ptr+n<=section['address']+section['size']
 name=w.m.at_address(image,ptr,n);assert name.endswith(b'.rs')and all(32<=b<127 for b in name)
 return name.decode(),line,column
def cohort(w,original,candidate,pairs):
 rows={};orr=dict(w.m.relocations(original));crr=dict(w.m.relocations(candidate))
 for pair in pairs:
  a,b=pair['original'],pair['candidate'];x=w.m.instructions(original,a['address'],a['bytes']);y=w.m.instructions(candidate,b['address'],b['bytes']);assert len(x)==len(y)
  for p,q in zip(x,y):
   if orr.get(a['address']+p['offset'],0)&0xffffffff!=8:continue
   assert crr.get(b['address']+q['offset'],0)&0xffffffff==8
   try:left=location(w,original,p['lddw_value'])
   except(AssertionError,ValueError,StopIteration,struct.error):continue
   right=location(w,candidate,q['lddw_value']);rows[(a['address'],p['offset'])]=(left,right)
 return rows
def direct_edges(w,original,candidate,ow,cw,pairs):
 oi={x['address']:x for x in ow};ci={x['address']:x for x in cw};orr=dict(w.m.relocations(original));crr=dict(w.m.relocations(candidate));edges=[]
 for pair in pairs:
  a,b=pair['original'],pair['candidate'];x=w.m.instructions(original,a['address'],a['bytes']);y=w.m.instructions(candidate,b['address'],b['bytes']);assert len(x)==len(y)
  for p,q in zip(x,y):
   if 'call_target'not in p or orr.get(a['address']+p['offset'],0)&0xffffffff==10:continue
   assert 'call_target'in q and crr.get(b['address']+q['offset'],0)&0xffffffff!=10
   af,bf=oi[p['call_target']],ci[q['call_target']];edges.append([a['address'],p['offset'],af['signature'],bf['signature']])
 return sorted(edges)

def recompute(original_path,baseline,candidate,parser_root):
 for name,h in json.loads((P/'parser-inputs.json').read_bytes()).items():
  path=parser_root/name;assert not path.is_symlink()and H(path.read_bytes())==h
 path=parser_root/'research/fees-crank-relay-rejection/window_map.py';s=importlib.util.spec_from_file_location('fees_union_pinned_window_map',path);w=importlib.util.module_from_spec(s);s.loader.exec_module(w)
 original=original_path.read_bytes();assert H(original)=='4f2955d0f6b40cc9ff7daa18ccad7d19119ba1249759f4e7e3bb691beee6b35e';ow=w.windows(original);ol=w.m.elf_layout(original);reports={};edges={};locations={};pairs_by={}
 for label,folder in [('baseline',baseline),('candidate',candidate)]:
  raw=(folder/'candidate.so').read_bytes();symbols=(folder/'symbols.so').read_bytes();assert H(raw)==OUTPUTS[label]['candidate.so'] and H(symbols)==OUTPUTS[label]['symbols.so'];cl=w.m.elf_layout(raw);sl=w.m.elf_layout(symbols)
  for section in cl['sections']:
   if section['flags']&2 and section['type']!=8:
    other=next(x for x in sl['sections']if x['name']==section['name']);assert section['address']==other['address']and w.m.section_data(raw,section['name'])==w.m.section_data(symbols,section['name'])
  cw=w.windows(symbols);pairs=w.compare(ow,cw)['unique_pairs'];pairs_by[label]={x['original']['address']:x for x in pairs};sig={x['signature']for x in cw};rh={x['raw_sha256']for x in cw};normalized=[x['address']for x in ow if x['signature']in sig];raw_matches=[x['address']for x in ow if x['raw_sha256']in rh];edge=direct_edges(w,original,raw,ow,cw,pairs);edges[label]={(x[0],x[1]):x for x in edge};locations[label]=cohort(w,original,raw,pairs);assert all(a==b for a,b in locations[label].values())
  sections=[]
  for sec in ol['sections']:
   if not sec['name']:continue
   a=w.m.section_data(original,sec['name']);b=w.m.section_data(raw,sec['name']);sections.append({'name':sec['name'],'original_bytes':len(a),'candidate_bytes':len(b),'raw_equal':a==b,'common_position_differences':sum(x!=y for x,y in zip(a,b))})
  reports[label]={'candidate_sha256':H(raw),'symbols_sha256':H(symbols),'candidate_bytes':len(raw),'normalized':len(normalized),'raw':len(raw_matches),'unique_pairs':len(pairs),'candidate_windows':len(cw),'normalized_inventory':normalized,'raw_inventory':raw_matches,'actual_direct_edges':len(edge),'unequal_complete_callee_edges':sum(x[2]!=x[3]for x in edge),'edge_ledger_sha256':H((json.dumps(edge,sort_keys=True)+'\n').encode()),'equal_location_uses':len(locations[label]),'sections':sections,'common_position_differences':sum(a!=b for a,b in zip(original,raw)),'whole_capture_equal':original==raw,'whole_meaningful_elf_equal':original[:ol['elf_extent']]==raw,'runtime_verified':False}
 gains=sorted(set(reports['candidate']['normalized_inventory'])-set(reports['baseline']['normalized_inventory']));losses=sorted(set(reports['baseline']['normalized_inventory'])-set(reports['candidate']['normalized_inventory']));assert gains==[199072]and not losses
 raw_gains=sorted(set(reports['candidate']['raw_inventory'])-set(reports['baseline']['raw_inventory']));raw_losses=sorted(set(reports['baseline']['raw_inventory'])-set(reports['candidate']['raw_inventory']));assert not raw_losses
 previous={k:r for k,r in edges['baseline'].items()if r[2]==r[3]};assert all(k in edges['candidate']and edges['candidate'][k][2]==edges['candidate'][k][3]for k in previous)
 assert locations['candidate'].keys()>=locations['baseline'].keys()and all(locations['candidate'][k]==v for k,v in locations['baseline'].items())
 new=[]
 for address in gains:
  pair=pairs_by['candidate'][address];calls=[r for (a,_),r in edges['candidate'].items()if a==address];assert all(r[2]==r[3]for r in calls);new.append({'original_address':address,'candidate_address':pair['candidate']['address'],'bytes':pair['original']['bytes'],'actual_direct_callees':len(calls),'all_complete_callee_shapes_equal':True,'actual_callee_shape_ledger_sha256':H((json.dumps(calls,sort_keys=True)+'\n').encode())})
 assert [reports[x]['normalized']for x in ['baseline','candidate']]==[573,574]and [reports[x]['raw']for x in ['baseline','candidate']]==[143,143];assert len(previous)==3765 and sum(x['actual_direct_callees']for x in new)==15
 return {'original_sha256':H(original),'original_capture_bytes':len(original),'original_elf_extent':ol['elf_extent'],'reports':reports,'normalized_gains':gains,'normalized_losses':losses,'raw_gains':raw_gains,'raw_losses':raw_losses,'preserved_prior_equal_direct_callee_obligations':len(previous),'new_windows':new,'rejected_static_mutations':negative_controls(w,original,(baseline/'symbols.so').read_bytes(),(candidate/'symbols.so').read_bytes()),'preparation_operand_audit':object_audit(w,original,(candidate/'symbols.so').read_bytes()),'scope':'Complete normalized windows, actual one-hop callee shapes, decoded Location values and raw sections only. No arbitrary duplicate pairing, general object extents, recursive/indirect semantics or target execution.'}

def object_audit(w,original,candidate):
 """All direct operands with explicitly bounded extents, not allocation closure."""
 ow,cw=w.windows(original),w.windows(candidate);oi={x['address']:x for x in ow};ci={x['address']:x for x in cw}
 a=oi[199072];matches=[x for x in cw if x['signature']==a['signature']];assert len(matches)==1;b=matches[0];assert a['bytes']==b['bytes']==5008
 def rows(image,f):return w.m.instructions(image,f['address'],f['bytes'])
 def pair(x,y):
  u,v=oi[x],ci[y];assert u['signature']==v['signature'] and u['bytes']==v['bytes'];return {'original':x,'candidate':y,'bytes':u['bytes'],'signature':u['signature']}
 def refs(image,f):
  rel=dict(w.m.relocations(image));return {r['offset']:r['lddw_value']for r in rows(image,f)if rel.get(f['address']+r['offset'],0)&0xffffffff==8}
 def calls(image,f):
  rel=dict(w.m.relocations(image));return {r['offset']:r['call_target']for r in rows(image,f)if 'call_target'in r and rel.get(f['address']+r['offset'],0)&0xffffffff!=10}
 def imports(image,f):
  rel=dict(w.m.relocations(image));dyn=w.dynamic_symbols(image);return [(r['offset'],dyn[rel[f['address']+r['offset']]>>32]['name'])for r in rows(image,f)if rel.get(f['address']+r['offset'],0)&0xffffffff==10]
 def ptr(image,address):
  assert dict(w.m.relocations(image)).get(address,0)&0xffffffff==8
  low,target=struct.unpack('<II',w.m.at_address(image,address,8));assert low==0;return target
 left,right=calls(original,a),calls(candidate,b);assert left.keys()==right.keys() and len(left)==15
 direct=[{'offset':off,**pair(left[off],right[off])}for off in sorted(left)]
 ii,jj=imports(original,a),imports(candidate,b);assert ii==jj and len(ii)==1 and ii[0][1]=='abort'
 assert not any(r['opcode']==0x8d for image,f in [(original,a),(candidate,b)]for r in rows(image,f))
 lr,rr=refs(original,a),refs(candidate,b);expected=[792,2952,3000,3096,3152,3200,3296,3344,3368,3384,3504,3728,4648];assert sorted(lr)==sorted(rr)==expected;proof=[]
 for off in expected:
  x,y=lr[off],rr[off];row={'offset':off,'original_target':x,'candidate_target':y,'allocation_boundary_proven':False}
  if off in [792,3384,4648]:
   u,v=location(w,original,x),location(w,candidate,y);assert u==v;row.update(kind='inferred_Rust_Location',record_extent=24,path=u[0],line=u[1],column=u[2])
  elif off in [3000,3200,3368]:
   n=32 if off==3368 else 48;u,v=w.m.at_address(original,x,n),w.m.at_address(candidate,y,n);assert u[8:24]==v[8:24]
   slots=[0,24]if n==32 else[0,24,32,40];targets=[{'slot':slot,**pair(ptr(original,x+slot),ptr(candidate,y+slot))}for slot in slots]
   row.update(kind='inferred_formatter_vtable',record_extent=n,size=int.from_bytes(u[8:16],'little'),alignment=int.from_bytes(u[16:24],'little'),actual_function_targets=targets)
  else:
   n=4 if off in [2952,3096,3152,3296]else 55 if off==3344 else 68
   u,v=w.m.at_address(original,x,n),w.m.at_address(candidate,y,n);assert u==v;row.update(kind='bounded_error_discriminant'if n==4 else'explicit_string_extent',extent=n,content_sha256=H(u))
   if n==4:assert int.from_bytes(u,'little')in[13,20];row['discriminant']=int.from_bytes(u,'little')
   if n==68:
    assert u==b'programs/pump-fees/src/instructions/fee_sharing/update_fee_shares.rs'
    for image,f in [(original,a),(candidate,b)]:
     assert struct.unpack('<BBhi',w.m.at_address(image,f['address']+off+48,8))==(0x7a,10,-264,68)
     assert struct.unpack('<BBhi',w.m.at_address(image,f['address']+off+40,8))==(0x62,10,-256,186 if off==3504 else 188)
  proof.append(row)
 # Distinguish a shape-ambiguous panic callee through its actual descriptor/message.
 pa,pb=left[min(left)],right[min(right)];aa,bb=oi[pa],ci[pb];ar,br=refs(original,aa),refs(candidate,bb);assert len(ar)==len(br)==1
 da,db=next(iter(ar.values())),next(iter(br.values()));u,v=w.m.at_address(original,da,16),w.m.at_address(candidate,db,16)
 assert int.from_bytes(u[8:],'little')==int.from_bytes(v[8:],'little')==28
 assert w.m.at_address(original,ptr(original,da),28)==w.m.at_address(candidate,ptr(candidate,db),28)==b'attempt to add with overflow'
 ac,bc=calls(original,aa),calls(candidate,bb);assert ac.keys()==bc.keys() and len(ac)==1;panic=pair(next(iter(ac.values())),next(iter(bc.values())))
 # This existing matched payout calls the recovered preparation, not a dead helper.
 payout=oi[204080];targets=[x for x in cw if x['signature']==payout['signature']];assert len(targets)==1;p=targets[0]
 assert calls(original,payout)[80]==a['address'] and calls(candidate,p)[80]==b['address']
 return {'original_address':a['address'],'candidate_address':b['address'],'body_bytes':5008,'complete_direct_callee_shapes':direct,'abort_import_offset':ii[0][0],'indirect_calls':0,'direct_bounded_operands':proof,'overflow_message_extent':28,'overflow_actual_panicking_target':panic,'incoming_payout_original':204080,'incoming_payout_candidate':p['address'],'incoming_call_offset':80,'scope':'Complete normalized body and actual one-hop call shapes, 13 bounded direct operands, inferred Location/vtable layouts and actual incoming payout edge. No general allocation-boundary, recursive-data, arbitrary-state or whole-file equivalence claim.'}

def negative_controls(w,original,baseline,candidate):
 """Read-only in-memory static mutations; these never execute target programs."""
 ow,cw=w.windows(original),w.windows(candidate);oi={x['address']:x for x in ow};a=oi[199072];b=next(x for x in cw if x['signature']==a['signature'])
 rows=w.m.instructions(candidate,b['address'],b['bytes']);rel=dict(w.m.relocations(candidate));refs={r['offset']:r['lddw_value']for r in rows if rel.get(b['address']+r['offset'],0)&0xffffffff==8}
 payout=next(x for x in cw if x['signature']==oi[204080]['signature'])
 def change(address):
  out=bytearray(candidate)
  section=next(s for s in w.m.elf_layout(out)['sections']if s['type']!=8 and s['address']<=address<s['address']+s['size'])
  out[section['offset']+address-section['address']]^=1
  return bytes(out)
 variants=[('old unmatched parent',baseline),('actual source path',change(refs[3504])),('Location line',change(refs[792]+16)),('vtable size',change(refs[3000]+8)),('error discriminant',change(refs[2952])),('actual incoming payout target',change(payout['address']+80+4))]
 rejected=[]
 for name,data in variants:
  try:object_audit(w,original,data)
  except (AssertionError,ValueError,KeyError,StopIteration,IndexError,struct.error):rejected.append(name)
  else:raise AssertionError('Static negative control accepted: '+name)
 return rejected
