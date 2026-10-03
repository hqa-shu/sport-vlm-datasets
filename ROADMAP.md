# Project improvement plan

The objective is a source-aware sports data resource that researchers can select by task and contributors can maintain reliably. Success means clear evidence and reusable tools; resource counts alone do not measure usefulness.

## Delivered in this revision

1. **Evidence and identity:** add dated, field-level primary-source evidence; separate original Fitness-AQA from a downstream adaptation, distinguish VideoNet training/benchmark folders, and repair Free Exercise DB's upstream-only link.
2. **Selection metadata:** add resource type, task, modality, language supervision, access conditions, dataset/media terms and official-split notes. Unchecked fields remain visible as unknown.
3. **One source of truth:** generate English/Chinese catalogs and a static explorer from JSON; detect stale generated outputs.
4. **Reusable tooling:** extend CLI filters and audit reports; add a video-QA manifest format and cross-shard source-group leakage checks with a clearly synthetic fixture.
5. **Maintenance:** add offline CI, behavioral tests, a contribution workflow and preparation guidance.

## Next evidence work

Prioritize field-level checks over adding unreviewed names. Run `python3 catalog.py --audit` for the current queue. Start with missing original references for SpaceJam, P²ANet, Extended OpenTTGames and ALEX-GYM-1, then review annotation schemas, dataset/media terms and official splits across remaining records. Do not infer releases or licenses from paper titles or code repositories.

A future verified annotation sample could document one permitted download, format inspection and manifest conversion. Record the exact release, hashes, check date and rights scope before calling it reproducible. A real training example and measured baseline follow only after that dataset preparation succeeds.

## Review criteria

- Every new claim has a primary source, scope and date.
- Benchmarks and training resources remain distinguishable.
- Unknown license/access information remains explicit.
- Generated outputs and offline checks pass for a clean checkout.
- A newcomer can find a resource, understand preparation limits and export metadata without credentials.

Track community usefulness through actionable corrections, reproducible contributions and references to the index. Stars are a discovery signal, not evidence of data quality.
