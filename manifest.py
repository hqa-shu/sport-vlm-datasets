#!/usr/bin/env python3
"""Audit local video-QA JSONL manifests for format errors and split leakage."""
import argparse
import json
import math
import sys
from collections import Counter
from pathlib import Path
from catalog import valid_url

SPLITS = {'train', 'validation', 'test'}
TEXT_FIELDS = ('sample_id', 'resource_name', 'source_url', 'media_path', 'group_id', 'question', 'answer')


def audit_records(records):
    """No media decoding, rights verification, or semantic quality assessment."""
    errors, ids, groups, splits = [], set(), {}, Counter()
    for line, record in enumerate(records, 1):
        prefix = 'record %s: ' % line
        if not isinstance(record, dict):
            errors.append(prefix + 'must be an object'); continue
        for key in TEXT_FIELDS:
            if not isinstance(record.get(key), str) or not record[key].strip():
                errors.append(prefix + key + ' must be non-empty text')
        if not valid_url(record.get('source_url')):
            errors.append(prefix + 'source_url must be an HTTP(S) URL')
        split = record.get('split')
        if not isinstance(split, str) or split not in SPLITS:
            errors.append(prefix + 'split must be train, validation or test')
        else: splits[split] += 1
        sample_id = record.get('sample_id')
        if isinstance(sample_id, str):
            if sample_id in ids: errors.append(prefix + 'duplicate sample_id ' + sample_id)
            ids.add(sample_id)
        group = record.get('group_id')
        if isinstance(group, str) and group.strip() and isinstance(split, str) and split in SPLITS:
            # group_id is globally scoped: use source identity, not a per-QA identifier.
            if group in groups and groups[group] != split:
                errors.append(prefix + 'source-group leakage: ' + group + ' appears in ' + groups[group] + ' and ' + split)
            else: groups[group] = split
        if 'start_seconds' in record or 'end_seconds' in record:
            start, end = record.get('start_seconds'), record.get('end_seconds')
            if not all(type(value) in (int, float) and math.isfinite(value) for value in (start, end)) or not 0 <= start < end:
                errors.append(prefix + 'clip timestamps must be finite numbers with 0 <= start < end')
    if not records: errors.append('manifest is empty')
    return {'records': len(records), 'source_groups': len(groups), 'split_counts': dict(sorted(splits.items())), 'errors': errors, 'scope': 'Format and declared source-group checks only; no media, license or training validation.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paths', nargs='+', type=Path, help='audit all shards together to detect cross-file leakage')
    args = parser.parse_args(argv)
    records = []
    for path in args.paths:
        try:
            with path.open(encoding='utf-8') as stream:
                for line_number, line in enumerate(stream, 1):
                    if not line.strip(): continue
                    try: records.append(json.loads(line))
                    except ValueError as exc: parser.exit(2, '%s:%s: invalid JSON: %s\n' % (path, line_number, exc))
        except OSError as exc: parser.exit(2, 'Cannot read manifest: ' + str(exc) + '\n')
    result = audit_records(records)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2); print()
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
