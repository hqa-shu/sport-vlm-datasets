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

## Submit a pull request

1. Update `data/datasets.json` and both `CATALOG.md` (English) and `README.zh-CN.md` (Chinese). Keep resource names and counts consistent; use `README.md` for concise landing-page updates.
2. Preserve the main/candidate distinction and preparation tiers. Record a source URL, verification date, and scope for changed claims. Do not count aliases or main entries again as candidates.
3. Run the offline checks from the repository root:

```bash
python3 catalog.py --validate
python3 -m unittest discover -s tests -v
```

4. Include those results and the evidence in your PR. For access changes, state whether you only read the page, obtained approval, downloaded annotations/media, or tested a format.

For a smaller contribution, open a [dataset suggestion](https://github.com/hqa-shu/sport-vlm-datasets/issues/new?template=dataset.yml) or [correction](https://github.com/hqa-shu/sport-vlm-datasets/issues/new?template=correction.yml). You do not need to clone the repository.

## JSON schema

`data/datasets.json` is an export of the catalog, not a dataset loader.

- `id`, `name`, `sport`, optional `sport_en`: catalog identifier, display name, and scope.
- `tier_from_original_curation`: inherited S/A/B/C grouping, or null for additional candidates.
- `scale_note`: a source-backed scale or an explicit uncertainty note.
- `paper_or_source_urls`, `access_urls`: original source and access entry points.
- `access_note`: conditions and evidence limits; historical notes may need refreshing.
- `source_review`: `needs_review`, `paper_identity_only`, or `partial_primary_source_check`.
- `source_review_date`: date of that source check, or null.
- `download_tested`: true only after an actual download test; all entries in the 2026-10-03 revision are false.

A partial source check does not verify every field. Record evidence for changed claims in the pull request, and use null/unknown rather than inventing values.

## Review queue

```bash
python3 catalog.py --audit
python3 catalog.py --review needs_review --format csv > review_queue.csv
```

A `needs_review` record can be useful without pretending it is verified. Confirm fields against original authors’ resources and retain unknown values when evidence is missing. The checks validate catalog structure; they do not validate licenses, live network access, or training suitability.

## 中文贡献说明

小修正可直接提交 Issue，写明条目、原文问题、原始来源以及核查日期。提交 PR 时请同步 JSON、英文目录与中文详表，并运行上面的结构检查和测试。仅浏览网页、实际下载和训练验证是不同证据，请分别说明。
