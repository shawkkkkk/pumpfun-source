#!/usr/bin/env python3
"""Read-only actual clone/source-location consequences of the 5203 build."""
from pathlib import Path
import collections,hashlib,importlib.util,json,struct,subprocess,tarfile
P=Path(__file__).resolve().parent;D=P.parent;sha=lambda b:hashlib.sha256(b).hexdigest()
T=D/'layout-frontier-reconcile/tools/elf_reader.py';s=importlib.util.spec_from_file_location('clone_elf',T);e=importlib.util.module_from_spec(s);s.loader.exec_module(e)
partial=Path('/workspace/pump-admin-cto/analysis/clone-boundary-proof.py');s=importlib.util.spec_from_file_location('existing_partial_clone',partial);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
paths={'original':Path('/workspace/pumpfun-source-latest/evidence/original/pump/deployed.so'),'f4':Path('/workspace/pump-current673-native-results/cto-40792775552/unstripped.so'),'5203':Path('/workspace/pump-current673-native-results/cto-used-flow-40794982049/unstripped.so')};elves={n:e.Elf(p)for n,p in paths.items()};parents={};clones={};inline={};fns={}
for name,x in elves.items():
 if name=='original':start,size,clone=0x22a10,27400,0x10c78
 else:
  parent=next(f for f in x.funcs if'9admin_cto7execute'in f['name']);start,size=parent['start'],parent['size'];choices={f['start']for f in x.funcs if'AccountInfo'in f['name']and'clone'in f['name']};assert len(choices)==1;clone=next(iter(choices))
 parents[name]={'start':start,'size':size,'clone_target':clone};f=m.Function(m.Elf(str(paths[name])),start,size);fns[name]=f;clones[name]=f.clones(clone);inline[name]=f.rc_stores()
f4_pay=next(v for v in elves['f4'].funcs if'admin_cto9pay_token'in v['name']);f4_pay_rc=m.Function(m.Elf(str(paths['f4'])),f4_pay['start'],f4_pay['size']).rc_stores();assert len(f4_pay_rc)==14
assert(len(clones['original']),len(inline['original']),len(clones['f4']),len(inline['f4']),len(clones['5203']),len(inline['5203']))==(33,42,48,0,54,0)
# Static constant pointer-add folding only; not register renaming or a byte comparator.
def fold(x):
 if not isinstance(x,tuple):return x
 x=tuple(fold(y)for y in x)
 if x[0]=='load'and isinstance(x[1],tuple)and x[1][0]=='add':return fold(('load',x[1][1],x[1][2]+x[2],x[3]))
 if x[0]=='add'and isinstance(x[1],tuple)and x[1][0]=='add':return fold(('add',x[1][1],x[1][2]+x[2]))
 return x

def rcfields(rows):return collections.Counter(repr(fold(('load',r['source'],offset,3)))for r in rows for offset in[8,16])
original_rc=rcfields(clones['original'])+collections.Counter(repr(fold(r['rc_pointer']))for r in inline['original']);new_rc=rcfields(clones['5203']);assert original_rc==new_rc and sum(new_rc.values())==108
A=('load',('input',('r',2)),8,3);field=lambda off:('load',A,off,3);direct=lambda off:('add',A,off);mint_info=('load',field(0x18),0x58,3)
expected={'sharing':[field(0x98),field(0x68),field(0),('load',field(8),0,3),field(0x10),field(0x90),field(0xa0),field(0x98)],'collect_coin':[field(0x58),mint_info,field(0x20),direct(0xa8),field(0x80),field(0x88),field(0x40),field(0x78),field(0x58)],'pool':[field(0x58),field(0),field(0x60),field(0x70),field(0x68),field(0x30),field(0x78),field(0x58)],'holder_ata':[field(0x28),field(0),field(0x50),direct(0x108),mint_info,field(0x30),field(0x20)]};groups={}
for name,lo,hi in [('sharing',0,8),('collect_coin',16,25),('pool',25,33),('holder_ata',47,54)]:
 selected=clones['5203'][lo:hi];assert [fold(r['source'])for r in selected]==[fold(x)for x in expected[name]];groups[name]=selected
# Original direct context groups and the inline sharing pair-source sequence bind the new order.
for name,lo,hi in [('collect_coin',0x6898,0x69a8),('pool',0x4c70,0x4d60),('holder_ata',0x5eb0,0x5f80)]:
 selected=[r for r in clones['original']if lo<=int(r['offset'],16)<=hi];assert [fold(r['source'])for r in selected]==[fold(x)for x in expected[name]];groups[name+'_original']=selected
sharing_inline=[r for r in inline['original']if 0x3dd0<=int(r['offset'],16)<=0x45f8];assert len(sharing_inline)==16
for i,src in enumerate(expected['sharing']):assert [fold(r['rc_pointer'])for r in sharing_inline[i*2:i*2+2]]==[fold(('load',src,k,3))for k in[8,16]]
groups['sharing_original_inline']=sharing_inline
owners=[r for r in clones['5203']if fold(r['source'])==fold(direct(0x108))];assert len(owners)==1 and owners[0]['offset']=='0x4278'
assert not any('admin_cto9pay_token'in f['name']for f in elves['5203'].funcs)
# Keep the existing source-site recognizer's heuristic boundary explicit.
site_source=subprocess.check_output(['git','show','a18e1e89b59bf9d734955550c92f321c97c95e62:research/pump-final-composition-673-20261028/tools/source_sites.py'],cwd='/workspace/pump-amm-native-repro');namespace={};exec(compile(site_source,'<unchanged source_sites.py>','exec'),namespace)
source_sites={};token={}
for name in ['f4','5203']:
 x=elves[name];sections={n:{'addr':s[3],'offset':s[4],'size':s[5]}for n,s in x.secs.items()};f=parents[name];rows=namespace['sites'](x.b,sections,f['start'],x.b[f['start']:f['start']+f['size']]);source_sites[name]=rows
 tf=next(f for f in x.funcs if'admin_cto16token_raw_amount'in f['name']);token[name]={'start':hex(tf['start']),'bytes':tf['size'],'normalized_sha256':sha(x.normalized[tf['start']:tf['start']+tf['size']]),'relocations':x.pattern(tf['start'],tf['size']),'calls':x.callsites(tf['start'],tf['size']),'direct_source_sites':namespace['sites'](x.b,sections,tf['start'],x.b[tf['start']:tf['start']+tf['size']])}
assert token['f4']['bytes']==token['5203']['bytes']==448 and token['f4']['normalized_sha256']==token['5203']['normalized_sha256']and token['f4']['relocations']==token['5203']['relocations']==[]
site_key=lambda r:(r['path'],r['line'])
assert collections.Counter(site_key(r)for r in source_sites['f4'])==collections.Counter(site_key(r)for r in source_sites['5203'])
# Globally scan the exact filename/length-shaped relocated records. No generic typed-extent claim.
filename=b'programs/pump/src/creator/admin_cto.rs';records={}
for name in ['f4','5203']:
 x=elves[name];found=[]
 for at,rel in x.relocations.items():
  if rel['type']!=8 or x.lo<=at<x.hi or at+24>len(x.b):continue
  ptr=struct.unpack_from('<Q',x.b,at)[0]>>32;n=struct.unpack_from('<Q',x.b,at+8)[0]
  if n==len(filename)and x.b[ptr:ptr+n]==filename:
   line,col=struct.unpack_from('<II',x.b,at+16);found.append({'record':hex(at),'file_pointer':hex(ptr),'filename':filename.decode(),'length':n,'line_word':line,'column_or_next_word':col,'raw24':x.b[at:at+24].hex()})
 records[name]=found
assert not any(r['line_word']==775 for r in records['f4'])and not any(r['line_word']==772 for r in records['5203'])
result={'scope':__doc__,'hashes':{n:sha(x.b)for n,x in elves.items()},'derived_parents':parents,'existing_partial_slicer_sha256':sha(partial.read_bytes()),'clone_counts':{n:{'direct':len(clones[n]),'inline_increment_stores':len(inline[n]),'parent_copy_sites':len(clones[n])+len(inline[n])//2,'used_pay_helper_copy_sites':7 if n=='f4'else 0,'parent_plus_used_pay_copy_sites':len(clones[n])+len(inline[n])//2+(7 if n=='f4'else 0)}for n in paths},'all_108_Rc_source_pointer_expressions_equal_original_to_5203':True,'constant_pointer_add_folding_only':True,'groups':groups,'only_holder_owner_copy':owners,'pay_token_symbol_absent':True,'token_raw_amount':token,'source_site_recognizer_sha256':sha(site_source),'heuristic_parent_source_sites':source_sites,'heuristic_source_site_multiset_equal':True,'filename_length_shaped_data_records':records,'source_line_775_to_772':{'actual_direct_helper_location_change_observed':False,'old_775_data_records':0,'new_772_data_records':0,'interpretation':'Lexical source shift only in observed executable/helper evidence. Helper has zero relocations and zero direct recognized Source sites; no Location movement is claimed. Typed/indirect/transitive consumption beyond these bounded observations is not proved.'},'limits':['Partial pointer slices ignore callee output writes; numeric values/whole-parent CFG are outside this result.','Static Source record recognizer is shape based; no arbitrary data extent or unique Rust type is inferred.','Raw/normalized original parent equality and exhaustive runtime equivalence remain false/unproved.']};(P/'clones-locations.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'path':str(P/'clones-locations.json'),'sha256':sha((P/'clones-locations.json').read_bytes()),'clone_counts':result['clone_counts'],'Rc_expression_multiset_equal':True,'only_holder_owner_offset':owners[0]['offset'],'parent_source_sites':{n:len(v)for n,v in source_sites.items()},'filename_length_shaped_records':{n:len(v)for n,v in records.items()},'helper_has_no_relocations_or_direct_source_sites':True}))
