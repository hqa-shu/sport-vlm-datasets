# Sports Vision-Language Datasets

![Sports dataset discovery, bilingual catalogs and Python data tools](hero.svg)

**A curated index of sports datasets and benchmarks for VLM fine-tuning, video question answering, and action understanding.**

体育多模态数据集索引：按运动领域、标注形式与准备成本比较研究资源。

[English catalog](CATALOG.md) · [中文](README.zh-CN.md) · [JSON index](data/datasets.json) · [Use the CLI](#search-and-reuse-locally) · [Contribute](CONTRIBUTING.md) · [Cite](#citation)

**33 resources · 31 main entries + 2 candidates · Partial source review**

## Choose a task

- **Soccer video QA / fine-tuning:** Start with [SoccerChat](https://github.com/simula/SoccerChat). Inspect video + query/response fields and preserve the official validation split.
- **Expert action understanding:** Start with [ExAct](https://github.com/Texaser/Exact). It is a multiple-choice benchmark; a Hugging Face split called `train` does not establish training suitability.
- **Repetition counting:** Start with [RepCount / TransRAC](https://github.com/SvipRepetitionCounting/TransRAC). Counting annotations need task-specific preparation.

These are source-backed entry points, not a best-dataset ranking. Check original media access, usage terms, and official splits before preparing any training data.

Browse in [English](CATALOG.md) or [中文](README.zh-CN.md), or reuse the [JSON index](data/datasets.json).


## Search and reuse locally

Python **3.9+**, standard library only. No package installation, credentials, or media download required.

```bash
git clone https://github.com/hqa-shu/sport-vlm-datasets.git
cd sport-vlm-datasets
python3 catalog.py --sport tennis
python3 catalog.py --query ExAct --format json
python3 catalog.py --review needs_review --format csv > review_queue.csv
python3 catalog.py --validate
```

[CLI usage and output →](USAGE.md) · [Catalog structure](data/datasets.json) · [Contribution checklist](CONTRIBUTING.md)

<a id="scope-and-evidence"></a>

<details>
<summary><b>Scope, review status & preparation tiers</b></summary>

| Coverage | Count |
|----------|------:|
| Main catalog entries | 31 |
| Additional candidates | 2 |
| Unique resources in this index | 33 |

Counts describe catalog entries, including benchmarks and candidate resources; they do not imply 33 downloadable training datasets. Aliases grouped in one row count as one resource.

**Review: 2026-10-04, partial.** This revision checked selected original papers and project pages, corrected mismatched references, and updated selected access notes. Other sizes and access notes are inherited from the earlier curation and may be outdated. No full dataset download or end-to-end fine-tuning validation was performed. Old availability totals were removed because they could not be reconciled with the rows.

The S/A/B/C tiers preserve the original maintainer's preparation-cost grouping; they are not a measured quality ranking. Availability and license restrictions are independent of tier. Paper identity checks do not establish that media are accessible or suitable for training.

**Highlighted corrections:** [TennisVL / TennisExpert](https://arxiv.org/abs/2603.13397), [QEVD official source](https://www.qualcomm.com/developer/software/qevd-dataset), [FLAG3D](https://arxiv.org/abs/2212.04638), and [RepCount / TransRAC](https://arxiv.org/abs/2204.01018). [SportR](https://huggingface.co/datasets/haotianxia/SportR) now provides annotation and media entry points, with gated non-commercial media access. References still needing repair are explicitly marked in the catalog.


</details>

<a id="catalog"></a>

## Browse the catalog

- **[English catalog →](CATALOG.md)** — 33 resources with sports, preparation tiers, and source-review status.
- **[中文详表 →](README.zh-CN.md)** — 规模、论文、访问说明和原整理的运动方向速查。
- **[Structured JSON →](data/datasets.json)** — reusable names, source URLs, access notes, and provenance fields.

## Latest update

**2026-10-04:** Added an English catalog; repaired BFMD, TaiChi-AQA, and Fit3D / AIFit source references. BFMD paper and released-package sizes differ; Fit3D requires account login. Details and dated limits are in the [Chinese catalog](README.zh-CN.md) and [JSON](data/datasets.json).

## Citation

If this index helps your research, please cite the collection and the original datasets you use. GitHub's citation menu is configured through [CITATION.cff](CITATION.cff).

```bibtex
@misc{huang2026sportvlm,
  title={Sport-VLM-Datasets: A Curated Index of Sports Vision-Language Datasets and Benchmarks},
  author={Huang, Qian'an},
  year={2026},
  url={https://github.com/hqa-shu/sport-vlm-datasets}
}
```

## Contributing

Corrections, new datasets, and clearer access notes are welcome. Use the [dataset suggestion](https://github.com/hqa-shu/sport-vlm-datasets/issues/new?template=dataset.yml) or [correction](https://github.com/hqa-shu/sport-vlm-datasets/issues/new?template=correction.yml) form. See [CONTRIBUTING.md](CONTRIBUTING.md) for the evidence checklist and JSON schema.

Maintained by [Qian'an Huang (@hqa-shu)](https://github.com/hqa-shu). 中英文反馈均可。

## License and access notes

This repository's original documentation and index are under [MIT](LICENSE). Linked datasets, media, annotations, and papers retain their own licenses and access conditions; the index's MIT license does not grant rights to them.

Catalog symbols are inherited access notes: ✅ a download path was previously recorded; ⚠️ application, partial access, or restrictions; ❌ previously unavailable or unpublished. Unless a row says otherwise, these are historical notes rather than a current download guarantee.
