#!/usr/bin/env python3
"""Search, export, and validate the local catalog; never downloads dataset media."""
import argparse
import csv
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit

DEFAULT_CATALOG = Path(__file__).resolve().parent / 'data' / 'datasets.json'
REVIEW_STATES = {'needs_review', 'paper_identity_only', 'partial_primary_source_check'}
RESOURCE_TYPES = {'dataset', 'benchmark', 'dataset_and_benchmark', 'reference', 'research_work', 'candidate', 'unknown'}
ACCESS_STATES = {'public', 'gated', 'request', 'mixed', 'unknown'}
LANGUAGE_STATES = {'paired_text', 'labels_only', 'instructions', 'motion_text', 'unknown'}
TASKS = {'video_qa', 'video_captioning', 'instructional_feedback', 'highlight_detection', 'action_localization', 'instructional_retrieval', 'action_recognition', 'action_understanding', 'action_quality_assessment', 'repetition_counting', 'pose_estimation', 'motion_generation', 'stroke_forecasting', 'tactical_analysis', 'ball_detection', 'event_spotting', 'segmentation', 'exercise_reference'}
MODALITIES = {'video', 'image', 'text', 'pose_3d', 'motion_3d', 'structured_events', 'spatial_annotations'}


def valid_url(value):
    try:
        parsed = urlsplit(value) if isinstance(value, str) else None
        return bool(parsed and parsed.scheme in ('http', 'https') and parsed.hostname and not parsed.username and not parsed.password and not any(c.isspace() for c in value))
    except ValueError:
        return False


def valid_date(value):
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def validate_catalog(catalog):
    """Return structural errors; does not validate research claims or live access."""
    if not isinstance(catalog, dict):
        return ['catalog must be an object']
    errors = []
    if type(catalog.get('schema_version')) is not int or catalog.get('schema_version') != 2:
        errors.append('unsupported schema_version (expected 2)')
    entries = catalog.get('datasets')
    if not isinstance(entries, list):
        return errors + ['datasets must be a list']
    for key in ('main_entries', 'additional_candidates', 'total_entries'):
        if type(catalog.get(key)) is not int or catalog[key] < 0:
            errors.append(key + ' must be a non-negative integer')
    if catalog.get('total_entries') != len(entries):
        errors.append('total_entries does not match datasets')
    ids, names, candidates = [], [], 0
    for index, entry in enumerate(entries, 1):
        prefix = 'entry ' + str(index) + ': '
        if not isinstance(entry, dict):
            errors.append(prefix + 'must be an object')
            continue
        if type(entry.get('id')) is not int:
            errors.append(prefix + 'id must be an integer')
        ids.append(entry.get('id'))
        for field in ('tier_from_original_curation', 'source_review_date', 'sport_en'):
            if field not in entry:
                errors.append(prefix + 'missing required field ' + field)
        if 'sport_en' in entry and (not isinstance(entry['sport_en'], str) or not entry['sport_en'].strip()):
            errors.append(prefix + 'sport_en must be non-empty text when supplied')
        for key in ('name', 'sport', 'scale_note', 'access_note'):
            if not isinstance(entry.get(key), str) or not entry[key].strip():
                errors.append(prefix + key + ' must be non-empty text')
        if isinstance(entry.get('name'), str):
            names.append(entry['name'].strip().casefold())
        tier = entry.get('tier_from_original_curation')
        if tier is None:
            candidates += 1
        elif not isinstance(tier, str) or tier not in ('S', 'A', 'B', 'C'):
            errors.append(prefix + 'invalid preparation tier')
        review = entry.get('source_review')
        if not isinstance(review, str) or review not in REVIEW_STATES:
            errors.append(prefix + 'invalid source_review')
        checked = entry.get('source_review_date')
        if checked is not None:
            try:
                if not isinstance(checked, str) or date.fromisoformat(checked).isoformat() != checked:
                    raise ValueError
            except (ValueError, TypeError):
                errors.append(prefix + 'source_review_date must be YYYY-MM-DD or null')
        if review != 'needs_review' and checked is None:
            errors.append(prefix + 'reviewed entry needs a source_review_date')
        if type(entry.get('download_tested')) is not bool:
            errors.append(prefix + 'download_tested must be boolean')
        for field in ('paper_or_source_urls', 'access_urls'):
            urls = entry.get(field)
            if not isinstance(urls, list):
                errors.append(prefix + field + ' must be a list')
                continue
            for url in urls:
                if not valid_url(url):
                    errors.append(prefix + field + ' contains an invalid HTTP(S) URL')
        if review != 'needs_review' and not entry.get('paper_or_source_urls'):
            errors.append(prefix + 'reviewed entry needs a primary source URL')
        for field, choices in (('resource_type', RESOURCE_TYPES), ('access_status', ACCESS_STATES), ('language_status', LANGUAGE_STATES)):
            if not isinstance(entry.get(field), str) or entry[field] not in choices:
                errors.append(prefix + 'invalid ' + field)
        if (tier is None) != (entry.get('resource_type') == 'candidate'):
            errors.append(prefix + 'candidate type must match null preparation tier')
        for field, choices in (('tasks', TASKS), ('modalities', MODALITIES)):
            values = entry.get(field)
            if not isinstance(values, list) or any(not isinstance(v, str) or v not in choices for v in values):
                errors.append(prefix + 'invalid ' + field)
            elif len(values) != len(set(values)):
                errors.append(prefix + 'duplicate ' + field)
        for field in ('official_splits', 'preparation_note', 'legacy_scale_note', 'legacy_access_note'):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                errors.append(prefix + field + ' must be non-empty text')
        license_info = entry.get('license')
        if not isinstance(license_info, dict):
            errors.append(prefix + 'license must be an object')
        else:
            status = license_info.get('status')
            if not isinstance(status, str) or status not in ('unknown', 'documented', 'restricted'):
                errors.append(prefix + 'invalid license status')
            if 'name' not in license_info or (license_info.get('name') is not None and (not isinstance(license_info['name'], str) or not license_info['name'].strip())):
                errors.append(prefix + 'license name must be text or null')
            if not isinstance(license_info.get('note'), str) or not license_info['note'].strip():
                errors.append(prefix + 'license note must be text')
            if status == 'documented' and not license_info.get('name'):
                errors.append(prefix + 'documented license needs a name')
        evidence = entry.get('evidence')
        covered = set()
        evidence_fields = {'resource_type', 'tasks', 'modalities', 'language_status', 'access_status', 'license', 'official_splits', 'scale_note', 'access_note', 'preparation_note'}
        if not isinstance(evidence, list):
            errors.append(prefix + 'evidence must be a list')
        else:
            for item in evidence:
                if not isinstance(item, dict):
                    errors.append(prefix + 'evidence item must be an object'); continue
                source_urls = entry.get('paper_or_source_urls')
                if not valid_url(item.get('url')) or not isinstance(source_urls, list) or item.get('url') not in source_urls:
                    errors.append(prefix + 'evidence needs a listed primary source URL')
                if not valid_date(item.get('checked_on')) or (valid_date(catalog.get('catalog_revision_date')) and item.get('checked_on', '') > catalog['catalog_revision_date']):
                    errors.append(prefix + 'invalid evidence date')
                if item.get('method') != 'page_read':
                    errors.append(prefix + 'unsupported evidence method')
                fields = item.get('fields')
                if not isinstance(fields, list) or not fields or any(not isinstance(f, str) or f not in evidence_fields for f in fields):
                    errors.append(prefix + 'invalid evidence fields')
                else:
                    covered.update(fields)
                if not isinstance(item.get('summary'), str) or not item['summary'].strip():
                    errors.append(prefix + 'evidence summary must be text')
        asserted = {field for field in ('resource_type', 'access_status', 'language_status') if entry.get(field) not in ('unknown', 'candidate')}
        asserted.update(field for field in ('tasks', 'modalities') if entry.get(field))
        if isinstance(license_info, dict) and license_info.get('status') != 'unknown':
            asserted.add('license')
        if isinstance(entry.get('official_splits'), str) and not entry['official_splits'].startswith('Unknown;'):
            asserted.add('official_splits')
        for field in sorted(asserted - covered):
            errors.append(prefix + 'asserted ' + field + ' needs field-level evidence')
    if ids != list(range(1, len(entries) + 1)):
        errors.append('IDs must be consecutive, ordered, and unique')
    if len(names) != len(set(names)):
        errors.append('duplicate resource names (case-insensitive)')
    if catalog.get('additional_candidates') != candidates:
        errors.append('additional_candidates does not match null-tier entries')
    if catalog.get('main_entries') != len(entries) - candidates:
        errors.append('main_entries does not match tiered entries')
    try:
        revision = catalog.get('catalog_revision_date')
        if not isinstance(revision, str) or date.fromisoformat(revision).isoformat() != revision:
            raise ValueError
    except (ValueError, TypeError):
        errors.append('catalog_revision_date must be YYYY-MM-DD')
    return errors


def select_entries(entries, query='', sport='', tier=None, review=None, task=None, modality=None, resource_type=None, access=None, language=None):
    selected = []
    for entry in entries:
        searchable = ' '.join(str(entry.get(key, '')) for key in ('name', 'sport', 'sport_en', 'scale_note', 'access_note', 'tasks', 'modalities', 'preparation_note'))
        if query.casefold() not in searchable.casefold():
            continue
        scopes = (entry['sport'].lstrip('⚽🎾💪🌐🏸🥋🏀🏓 ').casefold(), entry.get('sport_en', '').casefold())
        if sport and sport.casefold() not in scopes:
            continue
        if tier is not None and (entry['tier_from_original_curation'] or 'candidate') != tier:
            continue
        if review is not None and entry['source_review'] != review:
            continue
        if task and task not in entry['tasks']:
            continue
        if modality and modality not in entry['modalities']:
            continue
        if any(value is not None and entry[field] != value for field, value in (('resource_type', resource_type), ('access_status', access), ('language_status', language))):
            continue
        selected.append(entry)
    return selected


def write_entries(entries, output_format, stream):
    if output_format == 'json':
        json.dump(entries, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    elif output_format == 'csv':
        fields = ['id', 'name', 'sport', 'sport_en', 'resource_type', 'tasks', 'modalities', 'access_status', 'language_status', 'license', 'official_splits', 'tier_from_original_curation', 'source_review', 'source_review_date', 'download_tested', 'paper_or_source_urls', 'access_urls', 'access_note', 'evidence']
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        for entry in entries:
            row = {key: entry.get(key) for key in fields}
            for key in ('paper_or_source_urls', 'access_urls', 'tasks', 'modalities', 'license', 'evidence'):
                row[key] = json.dumps(entry[key], ensure_ascii=False)
            writer.writerow(row)
    else:
        stream.write('ID\tName\tSport / scope\tType\tAccess\tTasks\n')
        for entry in entries:
            stream.write('\t'.join(str(value) for value in (entry['id'], entry['name'], entry.get('sport_en', entry['sport']), entry['resource_type'], entry['access_status'], ','.join(entry['tasks']) or 'unknown')) + '\n')
        stream.write(str(len(entries)) + ' resource(s). Tiers are inherited preparation groups, not quality scores.\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG, help='catalog JSON path (default: relative to this script)')
    parser.add_argument('--query', default='', help='case-insensitive substring across names and notes')
    parser.add_argument('--sport', default='', help='exact Chinese or English sport/scope label (case-insensitive)')
    parser.add_argument('--tier', choices=['S', 'A', 'B', 'C', 'candidate'])
    parser.add_argument('--review', choices=sorted(REVIEW_STATES))
    parser.add_argument('--task', choices=sorted(TASKS))
    parser.add_argument('--modality', choices=sorted(MODALITIES))
    parser.add_argument('--type', dest='resource_type', choices=sorted(RESOURCE_TYPES))
    parser.add_argument('--access', choices=sorted(ACCESS_STATES))
    parser.add_argument('--language', choices=sorted(LANGUAGE_STATES))
    parser.add_argument('--format', choices=['text', 'json', 'csv'], default='text')
    parser.add_argument('--validate', action='store_true', help='check structure and exit; not source verification')
    parser.add_argument('--audit', action='store_true', help='summarize curation gaps as JSON and exit')
    args = parser.parse_args(argv)
    if args.validate and args.audit:
        parser.error('choose either --validate or --audit')
    if (args.validate or args.audit) and any((args.query, args.sport, args.tier, args.review, args.task, args.modality, args.resource_type, args.access, args.language)):
        parser.error('validation/audit operate on the full catalog; remove filters')
    try:
        catalog = json.loads(args.catalog.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        parser.exit(2, 'Cannot read catalog: ' + str(exc) + '\n')
    errors = validate_catalog(catalog)
    if errors:
        parser.exit(2, 'Invalid catalog:\n- ' + '\n- '.join(errors) + '\n')
    entries = catalog['datasets']
    if args.validate:
        print('Valid catalog structure: ' + str(len(entries)) + ' unique resources. Source claims and downloads were not tested.')
    elif args.audit:
        json.dump({'total_entries': len(entries), 'source_review_counts': dict(sorted(Counter(e['source_review'] for e in entries).items())), 'field_evidence_count': sum(bool(e['evidence']) for e in entries), 'without_primary_source': [e['name'] for e in entries if not e['paper_or_source_urls']], 'without_field_evidence': [e['name'] for e in entries if not e['evidence']], 'unknown_license': [e['name'] for e in entries if e['license']['status'] == 'unknown'], 'unknown_access': [e['name'] for e in entries if e['access_status'] == 'unknown'], 'download_tested_count': sum(e['download_tested'] for e in entries), 'scope': 'Local metadata audit; not live source/access verification.'}, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        write_entries(select_entries(entries, args.query, args.sport, args.tier, args.review, args.task, args.modality, args.resource_type, args.access, args.language), args.format, sys.stdout)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
