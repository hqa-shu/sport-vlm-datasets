# Contributing

English and Chinese corrections and resource suggestions are welcome. For a small change, use the [suggestion form](https://github.com/hqa-shu/sport-vlm-datasets/issues/new?template=dataset.yml) or [correction form](https://github.com/hqa-shu/sport-vlm-datasets/issues/new?template=correction.yml).

## Evidence checklist

- Use an original paper, author project or official dataset card. Distinguish a downstream adaptation from the original dataset.
- Record the exact checked fields, source URL, check date and scope. A page loading differs from a successful download or a training experiment.
- Separate dataset, benchmark, reference resource and candidate. Check supervision rather than inferring VLM-training readiness from the name.
- Describe annotation/media access and terms separately from the code license. Use unknown when unconfirmed.
- Preserve official splits and distinguish benchmark material from training data. For grouped resources, identify the version and avoid counting aliases twice.
- Do not attach restricted media, credentials, private URLs or unapproved contact information.

## Submit a change

1. Edit `data/datasets.json`, the single metadata source. Preserve existing IDs and historical notes. See [SCHEMA.md](SCHEMA.md).
2. Add an `evidence` item naming every changed classification/task/modality/language/access/license/split field. List its original URL in `paper_or_source_urls`; date it no later than the catalog revision. Leave unchecked fields unknown.
3. Regenerate the views and run the offline checks:

```bash
python3 catalog.py --validate
python3 generate_catalogs.py
python3 generate_catalogs.py --check
python3 -m unittest discover -s tests -v
python3 manifest.py example-manifest.jsonl
```

4. Include evidence and check results in the PR. Keep `CATALOG.md`, `README.zh-CN.md` and `index.html` generated, rather than editing them independently. Update the concise README when the project behavior changes.

CI checks Python 3.9 and 3.12 with read-only repository permissions. It does not visit third-party sources or download datasets. Reviewers must assess whether cited sources support the claims.

## Review queue

`python3 catalog.py --audit` lists missing field evidence, references and unknown access/license states. Work on these gaps before increasing the resource count. [ROADMAP.md](ROADMAP.md) records priorities and the completed improvements.

## 中文说明

请优先提交有原始来源的修正。JSON 是唯一元数据来源，中英文目录与网页均由脚本生成。每条新判断注明核查字段、日期与范围；不确定信息保留 unknown。实际下载、标注检查与训练结果必须分别验证，不能用网页可访问替代。
