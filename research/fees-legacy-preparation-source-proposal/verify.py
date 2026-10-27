#!/usr/bin/env python3
"""Verify source only, optionally remeasure explicitly supplied local compiler outputs."""
from pathlib import Path
import argparse,json
from source_tools import verify,materialize
P=Path(__file__).resolve().parent

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--parent-source',type=Path);p.add_argument('--materialize',type=Path)
 for name in ['original','baseline-build','candidate-build','parser-root']:p.add_argument('--'+name,type=Path)
 a=p.parse_args();m,overrides=verify(P);r={'before_source_inputs':44,'after_source_inputs':44,'overrides':len(overrides),'native_build_verified':False,'runtime_verified':False,'whole_binary_identity_verified':False,'local_static_comparison':False}
 if bool(a.parent_source)!=bool(a.materialize):p.error('provide --parent-source and --materialize together')
 if a.materialize:r['materialized']=materialize(P,a.parent_source,a.materialize)
 values=[a.original,a.baseline_build,a.candidate_build,a.parser_root]
 if any(values)and not all(values):p.error('supply all four explicit comparison inputs')
 if all(values):
  from compare import recompute
  actual=recompute(*values);r['local_static_comparison']=True;r['static_summary']={k:actual[k]for k in ['normalized_gains','normalized_losses','preserved_prior_equal_direct_callee_obligations','new_windows','preparation_operand_audit','rejected_static_mutations']}
 print(json.dumps(r,sort_keys=True))
if __name__=='__main__':main()
