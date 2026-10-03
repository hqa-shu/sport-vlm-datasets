# Search, export, and audit the catalog

[Overview](README.md) · [English catalog](CATALOG.md) · [中文详表](README.zh-CN.md)

The dependency-free Python CLI operates on this repository’s metadata. It never loads model weights or downloads dataset media. Python 3.9+ is supported.

## Search

Run from a clone of this repository:

```bash
python3 catalog.py --sport tennis
python3 catalog.py --sport 羽毛球 --tier B
python3 catalog.py --query ExAct --format json
```

Filters combine with AND. `--sport` matches an exact Chinese or English scope label, ignoring case and leading sport symbols; tennis and table tennis are separate. `--query` searches names, scope, scale, and access notes. Preparation tiers are inherited, not quality rankings.

Example result for `--sport tennis` (2026-10-04 catalog):

```text
ID  Name       Sport / scope  Tier  Source review
3   TennisVL   Tennis         S     partial_primary_source_check
31  CalTennis  Tennis         C     partial_primary_source_check
2 resource(s). Tiers are inherited preparation groups, not quality scores.
```

Text output uses tabs. An empty search returns a header and zero resources, with exit code 0.

## Reuse

```bash
python3 catalog.py --query ExAct --format json > exact.json
python3 catalog.py --review needs_review --format csv > review_queue.csv
```

JSON output is an array of complete records, not the full catalog envelope. CSV contains common fields, source URLs, and access notes; URL lists are JSON strings inside CSV cells. Output goes to stdout and the shell writes redirected files. A custom index can be supplied with `--catalog /path/to/datasets.json`. The default catalog path is relative to the script, so it works from another directory.

## Check structure and review gaps

```bash
python3 catalog.py --validate
python3 catalog.py --audit
```

`--validate` checks counts, consecutive unique IDs, duplicate names, field types, tiers, review dates, and HTTP(S) URL structure. It returns 0 on success and 2 for invalid data or input. `--audit` prints review counts, records without primary sources, and the number of tested downloads. Both operate on the full catalog; search filters cannot be combined with them.

These checks do not confirm that a link is live, media can be downloaded, a license permits your use, or a dataset is suitable for training. A partial source review does not validate every field. See the original papers and dataset cards before preparing model inputs.

## Verify a contribution

```bash
python3 -m unittest discover -s tests -v
```

The suite exercises invalid metadata, bilingual filtering, CSV/JSON round trips, command-line errors, execution outside the repository, and catalog/documentation consistency. It runs offline using Python’s standard library.

## 中文说明

用 `--sport 网球` / `--sport tennis` 搜索运动领域，用 `--query 名称` 查资源；`--format json` 或 `csv` 导出元数据。`--validate` 检查结构，`--audit` 汇总待核查条目。所有操作均在本地执行，不下载数据集、不验证训练效果。
