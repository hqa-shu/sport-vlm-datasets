# Contributing

Thank you for improving this sports vision-language resource. English and Chinese contributions are welcome.

## Add a resource

Use the dataset suggestion form or submit a pull request with:

- Dataset or benchmark name and the original authors' paper/project URL.
- Sport, task, modalities, annotation format, and scale with a primary source.
- An official access URL and a dated access note: open, gated, request required, unavailable, or unknown.
- Dataset/media license and any usage restrictions. Do not infer these from this index's MIT license.
- Preparation requirements and evidence for any suggested S/A/B/C tier.
- Official train/validation/test splits, when documented. Identify evaluation-only benchmarks and avoid promoting test annotations as training data.

Do not attach restricted media, credentials, or private access URLs.

## Correct a record

Use the correction form. Identify the row, explain the incorrect claim, provide the primary source, and state what you actually checked. A page loading is different from downloading the dataset or running training.

For a pull request, update both `README.md` and `data/datasets.json`. Preserve the same spelling and resource count, and add a short dated changelog entry. Candidates already in the main catalog must not be counted again.

## JSON schema

`data/datasets.json` is an export of the catalog, not a dataset loader.

- `id`, `name`, `sport`: catalog identifier, display name, and scope.
- `tier_from_original_curation`: inherited S/A/B/C grouping, or null for additional candidates.
- `scale_note`: a source-backed scale or an explicit uncertainty note.
- `paper_or_source_urls`, `access_urls`: original source and access entry points.
- `access_note`: conditions and evidence limits; historical notes may need refreshing.
- `source_review`: `needs_review`, `paper_identity_only`, or `partial_primary_source_check`.
- `source_review_date`: date of that source check, or null.
- `download_tested`: true only after an actual download test; all entries in the 2026-10-03 revision are false.

A partial source check does not verify every field. Record evidence for changed claims in the pull request, and use null/unknown rather than inventing values.

## Local consistency check

Run this from the repository root:

```bash
python3 - <<'PY'
import json
from pathlib import Path

catalog = json.loads(Path("data/datasets.json").read_text())
entries = catalog["datasets"]
assert len(entries) == catalog["total_entries"]
assert catalog["main_entries"] + catalog["additional_candidates"] == len(entries)
assert len({entry["name"] for entry in entries}) == len(entries)
assert [entry["id"] for entry in entries] == list(range(1, len(entries) + 1))
print("Catalog counts, names, and IDs are consistent.")
PY
```

This checks index structure. It does not validate source claims or network accessibility.

