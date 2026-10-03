# Sports Vision-Language Datasets

![Sports dataset discovery, bilingual catalogs and Python data tools](hero.svg)

**Find sports data for video-language training, action understanding and evaluation — with explicit source evidence and preparation limits.**

体育多模态数据资源索引：帮助训练、数据与开发用户按任务选型、核查来源、准备可复现的实验。

[English catalog](CATALOG.md) · [中文目录](README.zh-CN.md) · [JSON](data/datasets.json) · [Preparation guide](PREPARATION.md) · [CLI](USAGE.md) · [Improvement plan](ROADMAP.md)

[![Catalog checks](https://github.com/hqa-shu/sport-vlm-datasets/actions/workflows/catalog-checks.yml/badge.svg)](https://github.com/hqa-shu/sport-vlm-datasets/actions/workflows/catalog-checks.yml)

**33 resources · 31 main + 2 candidates · Schema v2 · 27 records with field-level evidence**

## Choose by supervision

| Goal | Starting point | What to distinguish |
|---|---|---|
| Video QA / fine-tuning | [SoccerChat](https://github.com/simula/SoccerChat), [VideoNet](https://huggingface.co/datasets/raivn/VideoNet) | Paired annotations and official splits; VideoNet training and benchmark folders serve different purposes. |
| Expert action evaluation | [ExAct](https://github.com/Texaser/Exact) | A multiple-choice benchmark; the host's `train` label does not establish SFT suitability. |
| Repetition counting | [RepCount / TransRAC](https://github.com/SvipRepetitionCounting/TransRAC) | Counting labels need task-specific preparation. |
| Motion and text | [MotionMillion](https://huggingface.co/datasets/InternRobotics/MotionMillion) | Processed motion/text data; original RGB-video delivery is a separate question. |
| Ball / event / segmentation | [OpenTTGames](https://lab.osai.ai/) | Vision targets rather than existing conversational QA. |

These are source-backed entry points, not a quality ranking. Access to media, license scope and held-out evaluation data need separate checks.

## Explore and export

The **[live dataset explorer](https://hqa-shu.github.io/sport-vlm-datasets/)** provides search, sport/task/modality/type/access/language filters, English/Chinese navigation and filtered JSON export. Its [self-contained HTML](index.html) also works locally: download this repository and open `index.html`; no server or dependencies are required. The Markdown catalogs remain available without JavaScript.

Python **3.9+**, standard library only:

```bash
git clone https://github.com/hqa-shu/sport-vlm-datasets.git
cd sport-vlm-datasets
python3 catalog.py --sport tennis
python3 catalog.py --task video_qa --language paired_text --format json
python3 catalog.py --type benchmark --format csv > benchmarks.csv
python3 catalog.py --access unknown
python3 catalog.py --audit
```

[Complete CLI usage](USAGE.md) · [Schema and access definitions](SCHEMA.md) · [Full catalog](CATALOG.md)

## Prepare an experiment

Follow the [preparation guide](PREPARATION.md) to choose supervision, record provenance, preserve official splits and create a local video-QA manifest. The included manifest is **synthetic**, with placeholder media paths.

```bash
# Check every shard together for declared source-group leakage.
python3 manifest.py example-manifest.jsonl
```

This audit checks JSON format, IDs, temporal boundaries and declared source groups. It does not decode media, confirm rights or validate model quality.

## Evidence and scope

**Revision: 2026-10-04.** This index contains datasets, benchmarks, reference databases and candidates. It does not imply 33 ready-to-download training datasets. Twenty-seven records have new field-level evidence; the other six have no field-level evidence in this revision. Earlier partial checks and paper-identity checks remain labeled separately.

Every asserted classification, task, modality, language/access state, known license and known split requires a dated primary-source reference. Unknown fields remain `unknown` or empty lists. A source-page read is not a download test: **zero dataset downloads or training runs have been validated**.

Historical scale/access notes and original S/A/B/C preparation groups are retained in expandable catalog details. They are not current availability guarantees or measured quality scores. Run `python3 catalog.py --audit` to inspect the remaining evidence queue.

## Maintain one source of truth

Edit `data/datasets.json`, then regenerate both catalogs and the explorer:

```bash
python3 catalog.py --validate
python3 generate_catalogs.py
python3 generate_catalogs.py --check
python3 -m unittest discover -s tests -v
```

CI runs offline checks on Python 3.9 and 3.12. The generator detects stale outputs. See [CONTRIBUTING.md](CONTRIBUTING.md) for evidence requirements, and [ROADMAP.md](ROADMAP.md) for priorities.

## Citation

Please cite the original datasets used in your work as well as this index when it helps discovery. GitHub's citation menu uses [CITATION.cff](CITATION.cff).

```bibtex
@misc{huang2026sportvlm,
  title={Sport-VLM-Datasets: A Curated Index of Sports Vision-Language Datasets and Benchmarks},
  author={Huang, Qian'an},
  year={2026},
  url={https://github.com/hqa-shu/sport-vlm-datasets}
}
```

Maintained by [Qian'an Huang (@hqa-shu)](https://github.com/hqa-shu). [Suggest a resource](https://github.com/hqa-shu/sport-vlm-datasets/issues/new?template=dataset.yml) · [Correct a record](https://github.com/hqa-shu/sport-vlm-datasets/issues/new?template=correction.yml). 中英文贡献均可。

## License

Original index, documentation and tools: [MIT](LICENSE). Linked datasets, media, annotations and papers retain their own terms. This project's MIT license grants no rights to those third-party resources.
