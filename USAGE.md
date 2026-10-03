# Using the catalog tools

Python 3.9+, standard library only. Run from the checkout or use an absolute script path; the default catalog resolves relative to the script, not your current directory. None of these commands downloads media or needs credentials.

## Search and combine filters

```bash
python3 catalog.py --sport tennis
python3 catalog.py --query ExAct --format json
python3 catalog.py --task video_qa --modality video --language paired_text
python3 catalog.py --type benchmark --format csv > benchmarks.csv
python3 catalog.py --access unknown --format json > access-review.json
python3 catalog.py --review needs_review --format csv > review-queue.csv
```

Filters combine with AND. Search is case-insensitive across names, scope, tasks, modalities and preparation notes. Sport is an exact Chinese or English scope label; `tennis` does not match `table tennis`. Task/modality/type/access/language filters use the controlled values in [SCHEMA.md](SCHEMA.md); use `--help` for allowed values. Empty task/modality lists mean unchecked and do not match a known-task filter.

`--tier S/A/B/C/candidate` preserves historical preparation groups, not measured quality. It remains for compatibility; use task and evidence fields for selection.

## Exports and exit codes

JSON is an array of complete selected records; zero matches produces `[]` successfully. CSV includes JSON-encoded arrays/objects in nested columns; parse those cells as JSON when reusing them. Text is a human-readable tab-separated summary.

The catalog CLI returns `0` on success and `2` for bad arguments, unreadable JSON or invalid catalog structure. It writes error messages to stderr and exports to stdout, so piping JSON does not include progress messages.

## Audit and validate

```bash
python3 catalog.py --validate
python3 catalog.py --audit
python3 catalog.py --catalog /path/to/another/catalog.json --validate
```

Audit reports primary-reference gaps, field-evidence gaps, unknown licenses/access and download-test counts. It audits the entire catalog; combining audit/validation with selection filters is rejected. Structural validation checks evidence coverage, not the factual correctness of a claim or live link availability.

## Generate the published views

```bash
python3 generate_catalogs.py
python3 generate_catalogs.py --check
```

The generator creates `CATALOG.md`, `README.zh-CN.md` and `index.html` from the JSON and `explorer-template.html`. `--check` returns `1` for stale output; malformed input returns `2`. Do not manually edit generated files. Open `index.html` locally for a self-contained search UI and filtered JSON export.

## Audit a video-QA manifest

```bash
python3 manifest.py example-manifest.jsonl
python3 manifest.py train.jsonl validation.jsonl test.jsonl
```

Pass all shards together to detect cross-file leakage. See [PREPARATION.md](PREPARATION.md) for required fields, globally scoped source groups and limitations. The checked-in example is synthetic, with nonexistent media paths; no training result is claimed.
