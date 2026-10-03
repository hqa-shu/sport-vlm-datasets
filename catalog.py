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


def validate_catalog(catalog):
    """Return structural errors; does not validate research claims or live access."""
    if not isinstance(catalog, dict):
        return ['catalog must be an object']
    errors = []
    if type(catalog.get('schema_version')) is not int or catalog.get('schema_version') != 1:
        errors.append('unsupported schema_version (expected 1)')
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
        for field in ('tier_from_original_curation', 'source_review_date'):
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
        elif tier not in ('S', 'A', 'B', 'C'):
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
                try:
                    valid = isinstance(url, str) and urlsplit(url).scheme in ('http', 'https') and bool(urlsplit(url).hostname)
                except ValueError:
                    valid = False
                if not valid:
                    errors.append(prefix + field + ' contains an invalid HTTP(S) URL')
        if review != 'needs_review' and not entry.get('paper_or_source_urls'):
            errors.append(prefix + 'reviewed entry needs a primary source URL')
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


def select_entries(entries, query='', sport='', tier=None, review=None):
    selected = []
    for entry in entries:
        searchable = ' '.join(str(entry.get(key, '')) for key in ('name', 'sport', 'sport_en', 'scale_note', 'access_note'))
        if query.casefold() not in searchable.casefold():
            continue
        scopes = (entry['sport'].lstrip('⚽🎾💪🌐🏸🥋🏀🏓 ').casefold(), entry.get('sport_en', '').casefold())
        if sport and sport.casefold() not in scopes:
            continue
        if tier is not None and (entry['tier_from_original_curation'] or 'candidate') != tier:
            continue
        if review is not None and entry['source_review'] != review:
            continue
        selected.append(entry)
    return selected


def write_entries(entries, output_format, stream):
    if output_format == 'json':
        json.dump(entries, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    elif output_format == 'csv':
        fields = ['id', 'name', 'sport', 'sport_en', 'tier_from_original_curation', 'source_review', 'source_review_date', 'download_tested', 'paper_or_source_urls', 'access_urls', 'access_note']
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
        writer.writeheader()
        for entry in entries:
            row = {key: entry.get(key) for key in fields}
            for key in ('paper_or_source_urls', 'access_urls'):
                row[key] = json.dumps(entry[key], ensure_ascii=False)
            writer.writerow(row)
    else:
        stream.write('ID\tName\tSport / scope\tTier\tSource review\n')
        for entry in entries:
            stream.write('\t'.join(str(value) for value in (entry['id'], entry['name'], entry.get('sport_en', entry['sport']), entry['tier_from_original_curation'] or 'candidate', entry['source_review'])) + '\n')
        stream.write(str(len(entries)) + ' resource(s). Tiers are inherited preparation groups, not quality scores.\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, default=DEFAULT_CATALOG, help='catalog JSON path (default: relative to this script)')
    parser.add_argument('--query', default='', help='case-insensitive substring across names and notes')
    parser.add_argument('--sport', default='', help='exact Chinese or English sport/scope label (case-insensitive)')
    parser.add_argument('--tier', choices=['S', 'A', 'B', 'C', 'candidate'])
    parser.add_argument('--review', choices=sorted(REVIEW_STATES))
    parser.add_argument('--format', choices=['text', 'json', 'csv'], default='text')
    parser.add_argument('--validate', action='store_true', help='check structure and exit; not source verification')
    parser.add_argument('--audit', action='store_true', help='summarize curation gaps as JSON and exit')
    args = parser.parse_args(argv)
    if args.validate and args.audit:
        parser.error('choose either --validate or --audit')
    if (args.validate or args.audit) and (args.query or args.sport or args.tier or args.review):
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
        json.dump({'total_entries': len(entries), 'source_review_counts': dict(sorted(Counter(e['source_review'] for e in entries).items())), 'without_primary_source': [e['name'] for e in entries if not e['paper_or_source_urls']], 'download_tested_count': sum(e['download_tested'] for e in entries), 'scope': 'Local metadata audit; not live source/access verification.'}, sys.stdout, ensure_ascii=False, indent=2)
        print()
    else:
        write_entries(select_entries(entries, args.query, args.sport, args.tier, args.review), args.format, sys.stdout)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
