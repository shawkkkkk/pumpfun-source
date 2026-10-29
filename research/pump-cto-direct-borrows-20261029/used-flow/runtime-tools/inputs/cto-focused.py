from pathlib import Path
import sys,json,base64,hashlib,gzip,argparse
sys.path.insert(0,'/workspace/pump-admin-cto/runtime-control/repo/scripts')
import pump_admin_cto_differential as f
from solders.transaction import Transaction
ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();baseline=Path('/workspace/pump-admin-cto/used-flow-runtime/inputs/cto-control.so')
sites={6090: (298, 306), 6030: (307, 312), 6078: (338, 332), 6083: (289, 284), 6077: (334, 331)};cases={6090: {'name': 'holder-new', 'holder': True}, 6030: {'name': 'new-zero', 'new_creator': '11111111111111111111111111111111'}, 6078: {'name': 'stable-1', 'quote': '6ws1bVyu3F8wGy1fPHhrc2v8UyWiGbRAAuek8SwikKPD', 'fee': 0}, 6083: {'name': 'curve-state-124-1', 'curve_patches': [[124, '01']]}, 6077: {'name': 'quote-global-0', 'quote': '6ws1bVyu3F8wGy1fPHhrc2v8UyWiGbRAAuek8SwikKPD', 'fee': 100, 'global_patches': [[1045, '00']]}}
main_logs=lambda r:[s for s in r['logs']if s.startswith('Program log: ')or s.startswith('Program data: ')]
rows=[]
for code,case in cases.items():
 results={name:f.run(case,binary)for name,binary in [('original',None),('baseline',baseline),('candidate',args.candidate)]}
 for r in results.values():Transaction.from_bytes(base64.b64decode(r['transaction_base64'])).verify();assert r['signatures_verified']and not r['pool_authority_top_level_signer']
 diff=[k for k in['error','before','after','events','inner','return']if results['original'][k]!=results['candidate'][k]]
 if main_logs(results['original'])!=main_logs(results['candidate']):diff.append('ordered_program_messages')
 line,oldline=sites[code];assert any(f'admin_cto.rs:{line}.'in s for s in results['original']['logs']);assert any(f'admin_cto.rs:{oldline}.'in s for s in results['baseline']['logs'])
 rows.append({'case':case,'code':code,'original_line':line,'baseline_line':oldline,'signature_verifications':3,'differences':diff,**results})
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();report={'case_count':len(rows),'signature_verifications':3*len(rows),'original_sha256':sha(f.ROOT/'evidence/original/pump/deployed.so'),'baseline_sha256':sha(baseline),'candidate_sha256':sha(args.candidate),'producer_sha256':sha(Path(__file__)),'fixture_harness_sha256':sha(Path(f.__file__)),'mismatches':[r['code']for r in rows if r['differences']],'cases':rows};args.output.write_bytes(gzip.compress(json.dumps(report,indent=2).encode(),mtime=0));print({k:report[k]for k in['case_count','signature_verifications','mismatches']});assert not report['mismatches']
