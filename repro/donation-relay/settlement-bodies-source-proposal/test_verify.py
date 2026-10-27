#!/usr/bin/env python3
import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('tight_source_verify',HERE/'verify.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.source=v.sources()
 def test_integrity(self):v.manifest();self.assertFalse(v.reports()['runtime_verified'])
 def test_source_maps(self):self.assertEqual([len(s)for s in self.source.values()],[60]*2)
 def test_materialize(self):
  with tempfile.TemporaryDirectory()as t:
   d=Path(t)/'source';v.materialize(d,self.source[v.ORDER[-1]]);self.assertEqual(len(list(p for p in d.rglob('*')if p.is_file())),60)
   with self.assertRaises(AssertionError):v.materialize(d,self.source[v.ORDER[-1]])
 def test_paths(self):
  for name in ['../bad','/bad','a/../b','a\\b','a//b']:
   with self.assertRaises(AssertionError):v.safe(name)
 def test_symlink(self):
  with tempfile.TemporaryDirectory()as t:
   d=Path(t);(d/'alias').symlink_to(d,target_is_directory=True)
   with self.assertRaises(AssertionError):v.materialize(d/'alias'/'out',self.source[v.ORDER[-1]])
 def test_mutation(self):
  with tempfile.TemporaryDirectory()as t:
   d=Path(t)/'packet';shutil.copytree(HERE,d);f=d/'source/src/tools/checks.rs';f.write_bytes(f.read_bytes()+b'\n')
   with self.assertRaises(AssertionError):v.manifest(d)
   with self.assertRaises(AssertionError):v.sources(d)
 def test_patch_mutation(self):
  with tempfile.TemporaryDirectory()as t:
   d=Path(t)/'packet';shutil.copytree(HERE,d);(d/'source.patch').write_text('')
   with self.assertRaises(AssertionError):v.sources(d)
 def test_default_no_artifacts(self):
  original=Path.read_bytes
  def guarded(p):
   self.assertFalse(p.name.endswith(('.so','.gz','.bz2')));self.assertNotIn('receipt',p.name);return original(p)
  with patch.object(Path,'read_bytes',guarded):v.manifest();v.sources();v.reports()
 def test_gain_counts(self):
  r=v.read(HERE/'expected.json');self.assertEqual(r['gains'],[97,98,100]);self.assertEqual(r['losses'],[]);self.assertEqual(r['recovered']['summary']['original_normalized_match_windows'],488)
if __name__=='__main__':unittest.main()
