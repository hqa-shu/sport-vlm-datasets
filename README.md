# Sports Vision-Language Datasets

**A curated index of sports datasets and benchmarks for VLM fine-tuning, video question answering, and action understanding.**

体育多模态数据集索引：按运动领域、标注形式与准备成本比较研究资源。

[Browse the catalog](#catalog) · [JSON index](data/datasets.json) · [Suggest a dataset](https://github.com/hqa-shu/sport-vlm-datasets/issues/new?template=dataset.yml) · [Report a correction](https://github.com/hqa-shu/sport-vlm-datasets/issues/new?template=correction.yml) · [Contribute](CONTRIBUTING.md) · [Cite](#citation)

## Choose a task

| Goal | Starting point | What to check next |
|------|----------------|--------------------|
| Soccer video QA / fine-tuning | [SoccerChat](https://github.com/simula/SoccerChat) | Video + query/response fields; keep the official validation split separate. |
| Expert action understanding | [ExAct](https://github.com/Texaser/Exact) | Multiple-choice evaluation; a HF split named `train` does not make the benchmark training data. |
| Repetition counting | [RepCount / TransRAC](https://github.com/SvipRepetitionCounting/TransRAC) | Counting annotations need task-specific preparation rather than assumed language supervision. |

These are source-backed entry points, not a best-dataset ranking. Check original media access, usage terms, and official splits before preparing any training data.

**33 resources · 31 main entries + 2 candidates · Partial source review**

The detailed catalog is in Chinese. Reuse the [JSON index](data/datasets.json) or inspect a resource’s original source before training.


<details>
<summary><b>Scope, review status & preparation tiers</b></summary>

| Coverage | Count |
|----------|------:|
| Main catalog entries | 31 |
| Additional candidates | 2 |
| Unique resources in this index | 33 |

Counts describe catalog entries, including benchmarks and candidate resources; they do not imply 33 downloadable training datasets. Aliases grouped in one row count as one resource.

**Review: 2026-10-03, partial.** This revision checked selected original papers and project pages, corrected mismatched references, and updated two access notes. Other sizes and access notes are inherited from the earlier curation and may be outdated. No full dataset download or end-to-end fine-tuning validation was performed. Old availability totals were removed because they could not be reconciled with the rows.

The S/A/B/C tiers preserve the original maintainer's preparation-cost grouping; they are not a measured quality ranking. Availability and license restrictions are independent of tier. Paper identity checks do not establish that media are accessible or suitable for training.

**Highlighted corrections:** [TennisVL / TennisExpert](https://arxiv.org/abs/2603.13397), [QEVD official source](https://www.qualcomm.com/developer/software/qevd-dataset), [FLAG3D](https://arxiv.org/abs/2212.04638), and [RepCount / TransRAC](https://arxiv.org/abs/2204.01018). [SportR](https://huggingface.co/datasets/haotianxia/SportR) now provides annotation and media entry points, with gated non-commercial media access. References still needing repair are explicitly marked in the catalog.


</details>

<a id="catalog"></a>

## 🎯 数据集分类

### 🏆 S级 - 原整理中的优先候选

| # | **名称** | **运动类型** | **规模** | **论文** | **获取方式** |
|:---:|----------|--------------|----------|:--------:|--------------|
| 1 | **SoccerChat** | ⚽ 足球 | 90K QA · 85K训练 | [arXiv](https://arxiv.org/abs/2505.16630) | [HF](https://huggingface.co/datasets/SimulaMet/SoccerChat) [GitHub](https://github.com/simula/SoccerChat) |
| 2 | **VideoNet** | 🌐 37域 | 160K clips · 500K QA | [arXiv](https://arxiv.org/abs/2605.02834) | [HF](https://huggingface.co/datasets/raivn/VideoNet) |
| 3 | **TennisVL** | 🎾 网球 | 202场 · 471小时 | [arXiv](https://arxiv.org/abs/2603.13397) | [GitHub](https://github.com/LZYAndy/TennisExpert) [GD](https://drive.google.com/drive/folders/1GkLHT6tyFb874HcEEmIu0S47wYzzbhkN) |
| 4 | **Fitness-AQA** | 💪 健身 | 小规模 | 待核实（移除错配论文） | ⚠️ [申请表](https://forms.gle/PbPTX1eVxGpa3QG88) [GitHub](https://github.com/GaetanoDibenedetto/UMAP25) |
| 5 | **SportR** | 🌐 多运动 | 20K+ QA · 6.8K CoT | [arXiv](https://arxiv.org/abs/2511.06499) | [GitHub annotations](https://github.com/chili-lab/SportR/tree/main/annotations) · [HF media](https://huggingface.co/datasets/haotianxia/SportR) · ⚠️ 媒体需申请，仅限非商业研究（2026-10-03 核查） |

<div align="right">
  <b><a href="#sports-vision-language-datasets">↥ back to top</a></b>
</div>

### 🥈 A级 - 原整理中的 QA / 指令候选

| # | **名称** | **运动类型** | **规模** | **论文** | **获取方式** |
|:---:|----------|--------------|----------|:--------:|--------------|
| 6 | **SoccerNet-XFoul** | ⚽ 足球 | 22K+ video-QA | [arXiv](https://arxiv.org/abs/2404.06332) | [官网](https://www.soccer-net.org/) |
| 7 | **QEVD** | 💪 健身 | 1M+ QA · 474小时 | [Qualcomm dataset page](https://www.qualcomm.com/developer/software/qevd-dataset) | [Qualcomm官网](https://www.qualcomm.com/developer/software/qevd-dataset/downloads) [HF Benchmark](https://huggingface.co/datasets/Voxel51/qualcomm-exercise-video-dataset-benchmark) |
| 8 | **ExAct** | 🌐 多领域（含体育） | 3,521 视频 / QA（主要为 MCQ 评估） | [arXiv](https://arxiv.org/abs/2506.06277) | [HF](https://huggingface.co/datasets/Alexhimself/ExAct) [GitHub](https://github.com/Texaser/Exact) |
| 9 | **SPORTU** | 🌐 7种 | 1.7K视频 · 12K QA | [arXiv](https://arxiv.org/abs/2410.08474) | [GitHub](https://github.com/chili-lab/SPORTU) [GD](https://drive.google.com/drive/folders/1nvA8gqF32lrhqzhbJ2r39-TwwW5tEvsu) |
| 10 | **Sports-QA** | 🌐 8种 | 94K QA | [arXiv](https://arxiv.org/abs/2401.01505) | [GitHub](https://github.com/HopLee6/Sports-QA) [HF](https://huggingface.co/datasets/HopLeeTop/Sports-QA) |
| 11 | **BioCoach** | 💪 健身 | 规模待核实（原记录可能混用 QEVD 划分） | [arXiv](https://arxiv.org/abs/2603.26938) | ❌ [arXiv](https://arxiv.org/abs/2603.26938) · 需联系作者 |
| 12 | **Domain Adaptation** | ⚽ 足球 | 20K instruction | [arXiv](https://arxiv.org/abs/2505.13860) | ⚠️ [arXiv](https://arxiv.org/abs/2505.13860) · CVPR 2025 · 数据未公开发布 |

<div align="right">
  <b><a href="#sports-vision-language-datasets">↥ back to top</a></b>
</div>

### 🥉 B级 - 原整理中需转换格式的候选

| # | **名称** | **运动类型** | **规模** | **论文** | **获取方式** |
|:---:|----------|--------------|----------|:--------:|--------------|
| 13 | **FineBadminton** | 🏸 羽毛球 | 3.2K回合 · 120场 | [arXiv](https://arxiv.org/abs/2508.07554) | [项目页](https://finebadminton.github.io/FineBadminton/) · 需联系作者 |
| 14 | **BFMD** | 🏸 羽毛球 | 1.7K回合 · 16K击球 | 待核实（移除错配论文） | [GitHub](https://github.com/Ning-D/BFMD) |
| 15 | **Shot2Tactic-Caption** | 🏸 羽毛球 | 5.5K标注 | [arXiv](https://arxiv.org/abs/2510.14617) | ⚠️ [arXiv](https://arxiv.org/abs/2510.14617) · ACM MMSports 2025 · 需联系作者 |
| 16 | **MotionMillion** | 💪🥋 健身 | 1M+样本 · 2000小时 | 待核实（移除错配论文） | [HF](https://huggingface.co/datasets/InternRobotics/MotionMillion) · 需同意条款 |
| 17 | **TaiChi-AQA** | 🥋 太极 | 1.3K视频 | 待核实（移除错配论文） | [GitHub](https://github.com/mlxger/TaiChi-AQA) · 需填申请表 |
| 18 | **FLAG3D** | 💪 健身 | 180K视频 · 60类 | [arXiv](https://arxiv.org/abs/2212.04638) | [项目页](https://andytang15.github.io/FLAG3D/) [GitHub](https://github.com/AndyTang15/FLAG3D) · ⚠️ 按官网提交签署的许可协议申请（2026-10-03 核查） |
| 19 | **EgoExo-Fitness** | 💪 健身 | 1.3K视频 · 32小时 | [ECCV 2024](https://arxiv.org/abs/2406.08877) | [GitHub](https://github.com/iSEE-Laboratory/EgoExo-Fitness) [HF](https://huggingface.co/datasets/Lymann/EgoExo-Fitness) |
| 20 | **RepCount** | 💪 健身 | 1.4K视频 · 20K标注 | [arXiv](https://arxiv.org/abs/2204.01018) | [官网](https://svip-lab.github.io/dataset/RepCount_dataset.html) [OneDrive](https://shanghaitecheducn-my.sharepoint.com/:f:/g/personal/dongsx_shanghaitech_edu_cn/EqveZdlGsPxPrfBLQcO_IrgBs6bz7KX1zGGSz_GtLDIfAg) [GitHub](https://github.com/SvipRepetitionCounting/TransRAC) |
| 21 | **Fit3D / AIFit** | 💪 健身 | 611序列 · 2.96M帧3D | 待核实（移除错配论文） | [官网](https://fit3d.imar.ro/) [训练集](https://fit3d.imar.ro/data/fit3d_train.tar.gz) [测试集](https://fit3d.imar.ro/data/fit3d_test.tar.gz) |
| 22 | **SpaceJam** | 🏀 篮球 | 32.5K标注 | 待核实（移除错配论文） | ⚠️ [GitCode](https://gitcode.com/gh_mirrors/sp/SpaceJam) · 可用性存疑 |
| 23 | **SVHighlights** | 🌐 多运动(8种) | 320视频 · 640h · 2.0h avg | [arXiv](https://arxiv.org/abs/2606.06926) | [HF](https://huggingface.co/datasets/ming9710/SVHighlights) · KDD 2026 · 需转 VLM 格式 |

<div align="right">
  <b><a href="#sports-vision-language-datasets">↥ back to top</a></b>
</div>

### ⚠️ C级 - 原整理中需较多准备的候选

| # | **名称** | **运动类型** | **规模** | **论文** | **获取方式** |
|:---:|----------|--------------|----------|:--------:|--------------|
| 24 | **ShuttleSet系列** | 🏸 羽毛球 | 33K-43K击球 | 待核实（移除错配论文） | [GitHub](https://github.com/wywyWang/CoachAI-Projects) |
| 25 | **OpenTTGames** | 🏓 乒乓球 | 12视频 · 4.3K事件 | 待核实（移除错配论文） | [官网](https://lab.osai.ai/) · CC BY-NC-SA 4.0 |
| 26 | **Free Exercise DB** | 💪 健身 | 800+动作 | - | [GitHub](https://github.com/wrkout/exercises.json) · Unlicense |
| 27 | **P²ANet** | 🏓 乒乓球 | 200视频 · 139K事件 | 待核实（移除错配论文） | ⚠️ 需确认论文中的具体获取方式 |
| 28 | **Extended OpenTTGames** | 🏓 乒乓球 | 1.5K击球 | - | ❌ [GitLab](https://gitlab.compute.dtu.dk/emilh/table_tennis_data) · 空仓库 |
| 29 | **MultiSenseBadminton** | 🏸 羽毛球 | 7.8K挥拍 | [Scientific Data 2024](https://www.nature.com/articles/s41597-024-03271-5) | ❌ 传感器数据为主，无视频下载入口 |
| 30 | **ALEX-GYM-1** | 💪 健身 | 二分类 | 待核实（移除错配论文） | ❌ 无可下载数据集 |
| 31 | **CalTennis** | 🎾 网球 | 11M帧 · 51小时 · 40人 · 2-6视角 | [arXiv](https://arxiv.org/abs/2606.20542) | [项目页](https://ilonadem.github.io/caltennis-website/) [HF](https://huggingface.co/datasets/demalenk/caltennis) · 需转 VLM 格式 |

<div align="right">
  <b><a href="#sports-vision-language-datasets">↥ back to top</a></b>
</div>

### 📌 额外候选 / 发布状态待核实

| 名称 | 方向 | 来源 | 说明 |
|------|------|------|------|
| **FLEX-VideoQA** | 健身 | [OpenReview](https://openreview.net/forum?id=Fje6v8JnB0) | 保留原候选；发布状态本轮未核实 |
| **SportSkills** | 多运动 | [arXiv](https://arxiv.org/abs/2603.25163) | 论文标题已核对；数据发布状态待核实 |

SportR 与 BioCoach 已在主表计数，不在此重复计算。SportR 已提供公开标注和需申请的媒体入口，详见主表。

## 🔍 按运动方向速查

| **方向** | **原整理候选** | **需额外准备候选** | **访问状态需核查** |
|----------|------------|------------|--------------|
| ⚽ 足球 | SoccerChat, SoccerNet-XFoul | Domain Adaptation | SportR |
| 🎾 网球 | - | TennisVL, CalTennis | - |
| 🏸 羽毛球 | BFMD | FineBadminton, Shot2Tactic | - |
| 🏓 乒乓球 | OpenTTGames | P²ANet | SportR |
| 🏀 篮球 | ExAct | SpaceJam | SportR |
| 💪 健身(教练) | QEVD, RepCount, Fit3D | BioCoach, EgoExo-Fitness | FLEX |
| 💪 健身(评估) | ExAct, Fit3D | TaiChi-AQA, FLAG3D | FLEX |
| 🌐 多运动 | VideoNet, ExAct, MotionMillion | SPORTU, SVHighlights | SportR, SportSkills |
| 🥋 太极 | - | TaiChi-AQA | - |

<div align="right">
  <b><a href="#sports-vision-language-datasets">↥ back to top</a></b>
</div>

## 🏋️ 健身方向候选（原整理，非训练验证）

### AI健身教练（实时反馈+纠正）
- **QEVD** — 1M+ QA，规模较大（非全领域比较结论），[Qualcomm官网](https://www.qualcomm.com/developer/software/qevd-dataset/downloads)
- **Fit3D/AIFit** — 3M+帧3D标注，[官网](https://fit3d.imar.ro/)
- **RepCount** — 1,451视频+细粒度重复标注，[OneDrive](https://shanghaitecheducn-my.sharepoint.com/:f:/g/personal/dongsx_shanghaitech_edu_cn/EqveZdlGsPxPrfBLQcO_IrgBs6bz7KX1zGGSz_GtLDIfAg)
- **MotionMillion** — 1M+样本，[HF](https://huggingface.co/datasets/InternRobotics/MotionMillion)

### 动作理解与质量分析
- **ExAct** — 3,521 视频 / 多选 QA，面向专家动作理解；并非直接的数值打分数据，[HF](https://huggingface.co/datasets/Alexhimself/ExAct)
- **Fit3D/AIFit** — 3M+帧3D标注，[官网](https://fit3d.imar.ro/)

### 3D姿态+语言
- **Fit3D** — 官网18GB直接下载
- **FLAG3D** — 部分下载，[项目页](https://andytang15.github.io/FLAG3D/#data)，Raw Data需邮件

<div align="right">
  <b><a href="#sports-vision-language-datasets">↥ back to top</a></b>
</div>

## 🌑 本索引的覆盖缺口

| **方向** | **现状** |
|----------|----------|
| 🏃 跑步/骑行/游泳 | 本索引覆盖不足，需补充检索；不代表该领域没有数据 |
| 🧘 瑜伽/舞蹈 | 需补充核查视频与 instruction QA 资源 |
| 🏓 乒乓球instruction | 本索引尚未确认直接可用的指令数据；合成 QA 需人工验证与来源记录 |

## 📝 更新记录

- **2026-10-03**：补充英文入口与 JSON 索引；按实际条目重算为 31 条主表 + 2 条额外候选；修正编号、TennisVL / QEVD / FLAG3D / RepCount 的来源；移除 10 条已错配的论文链接并标注待核实；更新 SportR 与 FLAG3D 访问说明。此轮为部分来源核查，未下载全部数据，也未验证所有训练格式。
- **历史说明**：以下日志保留原维护记录；当时的数量和“全部验证”表述不作为当前核查结果。

- **2026-06-23**：新增 SVHighlights (#23, B级多运动) — KDD 2026 首个长体育视频(>1h)高亮检测benchmark，arXiv:2606.06926
- **2026-06-22**：新增 CalTennis（当前 #31，原记录为 #30） — Caltech 11M帧多视角网球数据集，arXiv:2606.20542
- **2026-06-16**：完成所有链接验证，更新状态标识
- **2026-06-05**：完成32个数据集的整理与验证

---


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
