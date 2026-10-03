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
        self.assertIn('Fitness-AQA', audit['without_primary_source'])

    def test_required_nullable_fields_cannot_be_omitted(self):
        for field in ('tier_from_original_curation', 'source_review_date'):
            bad = copy.deepcopy(self.data)
            del bad['datasets'][-1][field]
            self.assertIn('missing required field ' + field, '\n'.join(catalog.validate_catalog(bad)))

    def test_bilingual_catalogs_cover_every_json_record(self):
        english = (ROOT / 'CATALOG.md').read_text(encoding='utf-8')
        chinese = (ROOT / 'README.zh-CN.md').read_text(encoding='utf-8')
        english_rows = [line for line in english.splitlines() if line.startswith('| ')][1:]
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


if __name__ == '__main__':
    unittest.main()
