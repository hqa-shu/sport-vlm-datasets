# Catalog schema v2

`data/datasets.json` is the single source for generated catalogs and the HTML explorer. It describes resources, not downloadable training samples. `catalog.py --validate` checks structure and evidence coverage without network access.

## Record fields

| Field | Meaning / allowed values |
|---|---|
| `id`, `name`, `sport`, `sport_en` | Stable ordered ID, canonical resource name, Chinese and English scope labels |
| `resource_type` | `dataset`, `benchmark`, `dataset_and_benchmark`, `reference`, `research_work`, `candidate`, `unknown` |
| `tasks` | Controlled task list from `catalog.TASKS`; empty means unchecked |
| `modalities` | Controlled modality list from `catalog.MODALITIES`; empty means unchecked |
| `language_status` | `paired_text`, `labels_only`, `instructions`, `motion_text`, `unknown` |
| `access_status` | `public`, `gated`, `request`, `mixed`, `unknown` |
| `license` | `{status: unknown/documented/restricted, name: string/null, note: string}`; describes dataset/media, not automatically the code license |
| `official_splits` | Source-backed protocol note, or an explicit `Unknown; ...` note |
| `scale_note`, `access_note`, `preparation_note` | Current notes; unknowns and limitations stay visible |
| `evidence` | Dated URL, checked fields, concise source summary and check method |
| `paper_or_source_urls`, `access_urls` | Primary-source references and access entry points; no file-availability guarantee |
| `source_review`, `source_review_date` | Legacy record-level review scope/date; a partial check does not verify every field |
| `download_tested` | Actual download test flag; currently false for every resource |
| `tier_from_original_curation` | Historical preparation grouping S/A/B/C; null denotes a candidate |
| `legacy_scale_note`, `legacy_access_note` | Preserved earlier curation; displayed only as unverified historical notes |

`public` means a primary-source page documents an open entry point. `gated` means account/terms acceptance; `request` means an author/application process; `mixed` means different components have different conditions. None implies that this maintainer downloaded the files.

`paired_text` identifies a documented language pairing, not automatic SFT approval. `labels_only` means the reviewed use provides task labels rather than conversational supervision. `instructions` describes exercise-reference text; `motion_text` describes motion/text pairing. Unknown fields are not negative findings.

## Field evidence

```json
{
  "url": "https://lab.osai.ai/",
  "checked_on": "2026-10-04",
  "method": "page_read",
  "fields": ["access_status", "license", "official_splits"],
  "summary": "Original page lists train/test downloads and dataset terms."
}
```

Every asserted type, task, modality, language/access state, documented license and known split requires coverage by a listed primary source. The validator checks that coverage and syntax; reviewers assess whether the source actually supports the claim. Dates cannot exceed the catalog revision. A page read is not a download test.

## v1 migration

Existing IDs, names, source links and historical preparation groups remain. Earlier free-form notes are retained in `legacy_*`; unreviewed new fields start as `unknown` or empty lists. Query/export flags from v1 still work. CSV adds nested JSON columns for tasks, modalities, licenses and evidence. Consumers should check `schema_version` and tolerate additional fields.

## 中文字段说明

`dataset` 数据集；`benchmark` 评估基准；`reference` 参考资料；`research_work` 研究工作（尚未确认独立数据发布）；`candidate` 候选。`unknown` 或空列表表示缺少本次字段级核查，不能据此断言“不存在”或“不可用”。旧 S/A/B/C 只保留整理历史。引用证据注明字段和日期；实际下载、许可确认与训练实验需要另行验证。
