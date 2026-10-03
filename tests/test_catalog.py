"""Behavior and failure-mode tests for the dependency-free catalog CLI."""
import copy
import csv
import importlib.util
import io
import json
import re
from urllib.parse import unquote
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('catalog', ROOT / 'catalog.py')
catalog = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(catalog)


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads((ROOT / 'data/datasets.json').read_text(encoding='utf-8'))

    def run_cli(self, *args, cwd=None):
        return subprocess.run([sys.executable, str(ROOT / 'catalog.py'), *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8')

    def test_checked_in_catalog(self):
        self.assertEqual(catalog.validate_catalog(self.data), [])

    def test_tennis_is_not_table_tennis_and_chinese_matches(self):
        for sport in ('Tennis', 'tennis', '网球'):
            results = catalog.select_entries(self.data['datasets'], sport=sport)
            self.assertEqual([e['name'] for e in results], ['TennisVL', 'CalTennis'])

    def test_filters_combine_and_query_ignores_case(self):
        self.assertEqual([e['name'] for e in catalog.select_entries(self.data['datasets'], query='exact', tier='A')], ['ExAct'])
        self.assertEqual(catalog.select_entries(self.data['datasets'], query='exact', tier='S'), [])

    def test_csv_preserves_nested_urls_and_comma_notes(self):
        entry = copy.deepcopy(self.data['datasets'][0])
        entry['access_note'] = 'one, two\nline three'
        stream = io.StringIO()
        catalog.write_entries([entry], 'csv', stream)
        row = list(csv.DictReader(io.StringIO(stream.getvalue())))[0]
        self.assertEqual(row['access_note'], entry['access_note'])
        self.assertEqual(json.loads(row['access_urls']), entry['access_urls'])

    def test_json_export_can_be_piped(self):
        result = self.run_cli('--query', 'ExAct', '--format', 'json')
        self.assertEqual(result.returncode, 0, result.stderr)
        entries = json.loads(result.stdout)
        self.assertEqual([e['name'] for e in entries], ['ExAct'])
        self.assertIs(entries[0]['download_tested'], False)

    def test_default_path_works_outside_repo(self):
        with tempfile.TemporaryDirectory() as folder:
            result = self.run_cli('--validate', cwd=folder)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_empty_result_is_successful_empty_json(self):
        result = self.run_cli('--query', '__not_a_resource__', '--format', 'json')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), [])

    def test_incorrect_counts_duplicate_ids_and_names_fail(self):
        bad = copy.deepcopy(self.data)
        bad['total_entries'] += 1
        bad['datasets'][1]['id'] = 1
        bad['datasets'][1]['name'] = bad['datasets'][0]['name'].upper()
        errors = '\n'.join(catalog.validate_catalog(bad))
        for fragment in ('total_entries', 'IDs must', 'duplicate resource names'):
            self.assertIn(fragment, errors)

    def test_review_without_source_or_date_fails(self):
        bad = copy.deepcopy(self.data)
        bad['datasets'][0]['paper_or_source_urls'] = []
        bad['datasets'][0]['source_review_date'] = None
        errors = '\n'.join(catalog.validate_catalog(bad))
        self.assertIn('needs a primary source', errors)
        self.assertIn('needs a source_review_date', errors)

    def test_malformed_types_dates_and_urls_fail_without_crash(self):
        changes = [('download_tested', 'false'), ('source_review_date', '2026-02-30'), ('paper_or_source_urls', ['file:///private/data']), ('source_review', []), ('id', True), ('sport_en', [])]
        for field, value in changes:
            with self.subTest(field=field):
                bad = copy.deepcopy(self.data)
                bad['datasets'][0][field] = value
                self.assertTrue(catalog.validate_catalog(bad))
        bad = copy.deepcopy(self.data)
        bad['schema_version'] = True
        self.assertTrue(catalog.validate_catalog(bad))

    def test_invalid_json_and_missing_file_return_readable_error(self):
        with tempfile.TemporaryDirectory() as folder:
            file = Path(folder) / 'broken.json'
            file.write_text('{not JSON')
            result = self.run_cli('--catalog', str(file))
            missing = self.run_cli('--catalog', str(Path(folder) / 'missing.json'))
        for response in (result, missing):
            self.assertEqual(response.returncode, 2)
            self.assertIn('Cannot read catalog:', response.stderr)
            self.assertNotIn('Traceback', response.stderr)

    def test_audit_preserves_unknown_and_is_not_a_download_claim(self):
        result = self.run_cli('--audit')
        self.assertEqual(result.returncode, 0, result.stderr)
        audit = json.loads(result.stdout)
        self.assertEqual(sum(audit['source_review_counts'].values()), audit['total_entries'])
        self.assertEqual(audit['download_tested_count'], 0)
        self.assertIn('SpaceJam', audit['without_primary_source'])
        self.assertEqual(audit['field_evidence_count'], 27)
        self.assertEqual(len(audit['without_field_evidence']), 6)

    def test_required_fields_cannot_be_omitted(self):
        for field in ('tier_from_original_curation', 'source_review_date', 'sport_en'):
            bad = copy.deepcopy(self.data)
            del bad['datasets'][-1][field]
            self.assertIn('missing required field ' + field, '\n'.join(catalog.validate_catalog(bad)))

    def test_bilingual_catalogs_cover_every_json_record(self):
        english = (ROOT / 'CATALOG.md').read_text(encoding='utf-8')
        chinese = (ROOT / 'README.zh-CN.md').read_text(encoding='utf-8')
        english_rows = [line for line in english.splitlines() if re.match(r'\| \d+ \|', line)]
        self.assertEqual(len(english_rows), self.data['total_entries'])
        for entry in self.data['datasets']:
            display_name = 'ShuttleSet family' if entry['name'] == 'ShuttleSet系列' else entry['name']
            self.assertTrue(any(display_name in line for line in english_rows), display_name)
            self.assertIn('**' + entry['name'] + '**', chinese)

    def test_documentation_relative_file_links_resolve(self):
        for name in ('README.md', 'README.zh-CN.md', 'CATALOG.md', 'USAGE.md', 'CONTRIBUTING.md'):
            text = (ROOT / name).read_text(encoding='utf-8')
            for url in re.findall(r'\]\(([^)]+)\)', text):
                if url.startswith(('https://', 'http://', '#')):
                    continue
                target = unquote(url.split('#', 1)[0])
                self.assertTrue((ROOT / target).is_file(), name + ': ' + target)

    def test_conflicting_modes_and_filtered_audit_fail(self):
        for args in (('--validate', '--audit'), ('--audit', '--sport', 'tennis')):
            result = self.run_cli(*args)
            self.assertEqual(result.returncode, 2)

class EvidenceAndGenerationTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'data/datasets.json').read_text(encoding='utf-8'))

    def test_new_filters_combine_and_unknowns_are_not_matches(self):
        results = catalog.select_entries(self.data['datasets'], task='video_qa', resource_type='dataset', language='paired_text', access='public')
        self.assertEqual([e['name'] for e in results], ['SoccerChat'])
        self.assertEqual(catalog.select_entries(self.data['datasets'], task='video_qa', language='labels_only'), [])

    def test_chinese_query_searches_localized_preparation_notes(self):
        self.assertEqual([e['name'] for e in catalog.select_entries(self.data['datasets'], query='后续适配')], ['Fitness-AQA'])

    def test_asserted_fields_require_evidence(self):
        for field, value in [('resource_type','dataset'),('tasks',['video_qa']),('modalities',['video']),('language_status','paired_text'),('access_status','public'),('official_splits','train/test')]:
            with self.subTest(field=field):
                bad = copy.deepcopy(self.data)
                bad['datasets'][21][field] = value
                self.assertIn('asserted '+field+' needs', '\n'.join(catalog.validate_catalog(bad)))

    def test_license_cannot_be_asserted_without_evidence(self):
        bad = copy.deepcopy(self.data)
        bad['datasets'][21]['license']={'status':'documented','name':'MIT','note':'Unsupported inference from code license.'}
        self.assertIn('asserted license needs', '\n'.join(catalog.validate_catalog(bad)))

    def test_evidence_bad_source_date_and_fields_rejected(self):
        for field,value in [('url','https://unlisted.example/source'),('checked_on','2099-01-01'),('fields',['invented_field']),('method','download_assumed')]:
            with self.subTest(field=field):
                bad=copy.deepcopy(self.data);bad['datasets'][0]['evidence'][0][field]=value
                self.assertTrue(catalog.validate_catalog(bad))

    def test_malformed_new_fields_do_not_crash(self):
        for field,value in [('tasks',[{}]),('modalities',None),('resource_type',[]),('license',None),('evidence',[None]),('official_splits',[]),('tier_from_original_curation',[]),('paper_or_source_urls',None),('notes_zh',[])]:
            with self.subTest(field=field):
                bad=copy.deepcopy(self.data);bad['datasets'][0][field]=value
                self.assertTrue(catalog.validate_catalog(bad))

    def test_candidate_classification_stays_consistent(self):
        bad=copy.deepcopy(self.data);bad['datasets'][-1]['resource_type']='unknown'
        self.assertIn('candidate type must match', '\n'.join(catalog.validate_catalog(bad)))

    def test_urls_cannot_contain_credentials_or_spaces(self):
        for url in ('https://user:secret@example.com/data','https://example.com/a b'):
            self.assertFalse(catalog.valid_url(url))

    def test_csv_preserves_evidence_and_license_objects(self):
        stream=io.StringIO(); entry=self.data['datasets'][24]
        catalog.write_entries([entry],'csv',stream)
        row=list(csv.DictReader(io.StringIO(stream.getvalue())))[0]
        self.assertEqual(json.loads(row['license']),entry['license'])
        self.assertEqual(json.loads(row['evidence']),entry['evidence'])

    def test_generated_views_are_current(self):
        result=subprocess.run([sys.executable,str(ROOT/'generate_catalogs.py'),'--check'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_generator_detects_stale_output_in_isolated_checkout(self):
        import shutil
        with tempfile.TemporaryDirectory() as folder:
            checkout=Path(folder)/'repo';shutil.copytree(ROOT,checkout,ignore=shutil.ignore_patterns('__pycache__'))
            (checkout/'CATALOG.md').write_text('stale')
            result=subprocess.run([sys.executable,str(checkout/'generate_catalogs.py'),'--check'],capture_output=True,text=True)
        self.assertEqual(result.returncode,1)
        self.assertIn('CATALOG.md',result.stderr)

    def test_html_payload_escapes_closing_script_sequences(self):
        spec=importlib.util.spec_from_file_location('generator',ROOT/'generate_catalogs.py')
        generator=importlib.util.module_from_spec(spec);sys.path.insert(0,str(ROOT))
        try:spec.loader.exec_module(generator)
        finally:sys.path.pop(0)
        modified=copy.deepcopy(self.data);modified['datasets'][0]['name']='</script><script>alert(1)</script>'
        output=generator.outputs(modified)['index.html']
        payload=re.search(r'<script id="catalog-data" type="application/json">(.*?)</script>',output,re.S).group(1)
        self.assertNotIn('</script>',payload)
        self.assertEqual(json.loads(payload)['datasets'][0]['name'],modified['datasets'][0]['name'])


if __name__ == '__main__':
    unittest.main()
