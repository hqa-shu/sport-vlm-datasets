"""Check leakage and malformed-input behavior with synthetic local records."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import manifest
sys.path.pop(0)

class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.records=[json.loads(line) for line in (ROOT/'example-manifest.jsonl').read_text().splitlines()]

    def test_synthetic_fixture_is_valid_and_explicitly_synthetic(self):
        result=manifest.audit_records(self.records)
        self.assertEqual(result['errors'],[])
        self.assertEqual(result['split_counts'],{'train':1,'validation':1})
        self.assertTrue(all('SYNTHETIC' in e['resource_name'] for e in self.records))

    def test_same_source_across_splits_fails(self):
        self.records[1]['group_id']=self.records[0]['group_id']
        self.assertIn('source-group leakage',str(manifest.audit_records(self.records)['errors']))

    def test_multiple_questions_for_same_source_in_one_split_are_allowed(self):
        self.records[1]['group_id']=self.records[0]['group_id'];self.records[1]['split']='train'
        self.assertEqual(manifest.audit_records(self.records)['errors'],[])

    def test_duplicate_sample_ids_fail(self):
        self.records[1]['sample_id']=self.records[0]['sample_id']
        self.assertIn('duplicate sample_id',str(manifest.audit_records(self.records)['errors']))

    def test_invalid_timestamp_pairs_fail(self):
        for start,end in ((-1,2),(2,2),(3,2),(True,4),(0,float('nan')),(0,float('inf')),('0',2),(0,None)):
            with self.subTest(start=start,end=end):
                bad=copy.deepcopy(self.records);bad[0]['start_seconds']=start;bad[0]['end_seconds']=end
                self.assertIn('timestamps',str(manifest.audit_records(bad)['errors']))

    def test_whole_video_record_can_omit_timestamps(self):
        for e in self.records:e.pop('start_seconds');e.pop('end_seconds')
        self.assertEqual(manifest.audit_records(self.records)['errors'],[])

    def test_malformed_record_fields_fail_without_crash(self):
        for field,value in (('split',[]),('question',''),('source_url','file:///x'),('group_id',None)):
            bad=copy.deepcopy(self.records);bad[0][field]=value
            self.assertTrue(manifest.audit_records(bad)['errors'])
        self.assertTrue(manifest.audit_records([None])['errors'])

    def test_empty_manifest_fails(self):
        self.assertEqual(manifest.audit_records([])['errors'],['manifest is empty'])

    def test_cross_shard_leakage_is_detected_by_cli(self):
        self.records[1]['group_id']=self.records[0]['group_id']
        with tempfile.TemporaryDirectory() as folder:
            paths=[]
            for i,record in enumerate(self.records):
                path=Path(folder)/('%s.jsonl'%i);path.write_text(json.dumps(record)+'\n');paths.append(str(path))
            result=subprocess.run([sys.executable,str(ROOT/'manifest.py'),*paths],capture_output=True,text=True)
        self.assertEqual(result.returncode,1)
        self.assertIn('source-group leakage',str(json.loads(result.stdout)['errors']))

    def test_invalid_json_is_a_readable_error(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'bad.jsonl';path.write_text('{broken}\n')
            result=subprocess.run([sys.executable,str(ROOT/'manifest.py'),str(path)],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertIn('invalid JSON',result.stderr)
        self.assertNotIn('Traceback',result.stderr)

    def test_missing_file_is_a_readable_error(self):
        with tempfile.TemporaryDirectory() as folder:
            result=subprocess.run([sys.executable,str(ROOT/'manifest.py'),str(Path(folder)/'missing')],capture_output=True,text=True)
        self.assertEqual(result.returncode,2)
        self.assertIn('Cannot read manifest',result.stderr)
