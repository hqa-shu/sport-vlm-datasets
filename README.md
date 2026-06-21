# 🏀 Sport-VLM-Datasets

体育多模态微调数据集汇总 — 面向 VLM 微调的体育领域开源数据集全景索引

> 按格式就绪度分 S/A/B/C 四级，所有获取路径已逐一验证

<p align="center">
  <a href="https://github.com/hqa-shu/sport-vlm-datasets"><img src="https://img.shields.io/github/stars/hqa-shu/sport-vlm-datasets.svg?style=social"></a>
  <a href="https://github.com/hqa-shu/sport-vlm-datasets"><img src="https://img.shields.io/github/forks/hqa-shu/sport-vlm-datasets.svg?style=social"></a>
  <a href="https://github.com/hqa-shu/sport-vlm-datasets/issues"><img src="https://img.shields.io/github/issues/hqa-shu/sport-vlm-datasets.svg"></a>
  <img src="https://img.shields.io/badge/license-MIT-blue.svg">
  <img src="https://img.shields.io/badge/datasets-32-green.svg">
</p>

## 📊 统计概览

| 指标 | 数量 |
|------|:----:|
| 数据集总数 | 32 |
| ✅ 可直接下载 | 18 |
| ⚠️ 需申请/受限 | 7 |
| ❌ 暂不可获取 | 7 |

## 🎯 数据集分类

### 🏆 S级 - 格式完美就绪（已有微调模型）

| # | **名称** | **运动类型** | **规模** | **论文** | **获取方式** |
|:---:|----------|--------------|----------|:--------:|--------------|
| 1 | **SoccerChat** | ⚽ 足球 | 90K QA · 85K训练 | [[arXiv](https://arxiv.org/abs/2505.16630)] | [[HF](https://huggingface.co/datasets/SimulaMet/SoccerChat)] [[GitHub](https://github.com/simula/SoccerChat)] |
| 2 | **VideoNet** | 🌐 37域 | 160K clips · 500K QA | [[arXiv](https://arxiv.org/abs/2605.02834)] | [[HF](https://huggingface.co/datasets/raivn/VideoNet)] |
| 3 | **TennisVL** | 🎾 网球 | 202场 · 471小时 | [[arXiv](https://arxiv.org/abs/2506.06277)] | [[GitHub](https://github.com/LZYAndy/TennisExpert)] [[GD](https://drive.google.com/drive/folders/1GkLHT6tyFb874HcEEmIu0S47wYzzbhkN)] |
| 4 | **Fitness-AQA** | 💪 健身 | 小规模 | [[arXiv](https://arxiv.org/abs/2603.26938)] | ⚠️ [[申请表](https://forms.gle/PbPTX1eVxGpa3QG88)] [[GitHub](https://github.com/GaetanoDibenedetto/UMAP25)] |
| 5 | **SportR** | 🌐 多运动 | 20K+ QA · 6.8K CoT | [[arXiv](https://arxiv.org/abs/2511.06499)] | ❌ [[GitHub](https://github.com/chili-lab/SportR)] · ICLR 2026前发布 |

<div align="right">
  <b><a href="#sport-vlm-datasets">↥ back to top</a></b>
</div>

### 🥈 A级 - 高质量且易用（可直接用于SFT）

| # | **名称** | **运动类型** | **规模** | **论文** | **获取方式** |
|:---:|----------|--------------|----------|:--------:|--------------|
| 6 | **SoccerNet-XFoul** | ⚽ 足球 | 22K+ video-QA | [[arXiv](https://arxiv.org/abs/2404.06332)] | [[官网](https://www.soccer-net.org/)] |
| 7 | **QEVD** | 💪 健身 | 1M+ QA · 474小时 | [[arXiv](https://arxiv.org/abs/2404.06332)] | [[Qualcomm官网](https://www.qualcomm.com/developer/software/qevd-dataset/downloads)] [[HF Benchmark](https://huggingface.co/datasets/Voxel51/qualcomm-exercise-video-dataset-benchmark)] |
| 8 | **ExAct** | 🏀 6类 | 3.5K video QA | [[arXiv](https://arxiv.org/abs/2506.06277)] | [[HF](https://huggingface.co/datasets/Alexhimself/ExAct)] [[GitHub](https://github.com/Texaser/Exact)] |
| 9 | **SPORTU** | 🌐 7种 | 1.7K视频 · 12K QA | [[arXiv](https://arxiv.org/abs/2410.08474)] | [[GitHub](https://github.com/chili-lab/SPORTU)] [[GD](https://drive.google.com/drive/folders/1nvA8gqF32lrhqzhbJ2r39-TwwW5tEvsu)] |
| 10 | **Sports-QA** | 🌐 8种 | 94K QA | [[arXiv](https://arxiv.org/abs/2401.01505)] | [[GitHub](https://github.com/HopLee6/Sports-QA)] [[HF](https://huggingface.co/datasets/HopLeeTop/Sports-QA)] |
| 11 | **BioCoach** | 💪 健身 | 149训练+74测试 | [[arXiv](https://arxiv.org/abs/2603.26938)] | ❌ [[arXiv](https://arxiv.org/abs/2603.26938)] · 需联系作者 |
| 12 | **Domain Adaptation** | ⚽ 足球 | 20K instruction | [[arXiv](https://arxiv.org/abs/2505.13860)] | ⚠️ [[arXiv](https://arxiv.org/abs/2505.13860)] · CVPR 2025 · 数据未公开发布 |

<div align="right">
  <b><a href="#sport-vlm-datasets">↥ back to top</a></b>
</div>

### 🥉 B级 - 可用但需转换格式

| # | **名称** | **运动类型** | **规模** | **论文** | **获取方式** |
|:---:|----------|--------------|----------|:--------:|--------------|
| 13 | **FineBadminton** | 🏸 羽毛球 | 3.2K回合 · 120场 | [[arXiv](https://arxiv.org/abs/2508.07554)] | [[项目页](https://finebadminton.github.io/FineBadminton/)] · 需联系作者 |
| 14 | **BFMD** | 🏸 羽毛球 | 1.7K回合 · 16K击球 | [[CVPR 2026W]](https://arxiv.org/abs/2508.07554)] | [[GitHub](https://github.com/Ning-D/BFMD)] |
| 15 | **Shot2Tactic-Caption** | 🏸 羽毛球 | 5.5K标注 | [[arXiv](https://arxiv.org/abs/2510.14617)] | ⚠️ [[arXiv](https://arxiv.org/abs/2510.14617)] · ACM MMSports 2025 · 需联系作者 |
| 16 | **MotionMillion** | 💪🥋 健身 | 1M+样本 · 2000小时 | [[arXiv](https://arxiv.org/abs/2508.07554)] | [[HF](https://huggingface.co/datasets/InternRobotics/MotionMillion)] · 需同意条款 |
| 17 | **TaiChi-AQA** | 🥋 太极 | 1.3K视频 | [[arXiv](https://arxiv.org/abs/2508.07554)] | [[GitHub](https://github.com/mlxger/TaiChi-AQA)] · 需填申请表 |
| 18 | **FLAG3D** | 💪 健身 | 180K视频 · 60类 | [[CVPR 2023]](https://arxiv.org/abs/2508.07554)] | [[项目页](https://andytang15.github.io/FLAG3D/#data)] [[GitHub](https://github.com/AndyTang15/FLAG3D)] |
| 19 | **EgoExo-Fitness** | 💪 健身 | 1.3K视频 · 32小时 | [[ECCV 2024]](https://arxiv.org/abs/2406.08877)] | [[GitHub](https://github.com/iSEE-Laboratory/EgoExo-Fitness)] [[HF](https://huggingface.co/datasets/Lymann/EgoExo-Fitness)] |
| 20 | **RepCount** | 💪 健身 | 1.4K视频 · 20K标注 | [[arXiv](https://arxiv.org/abs/2508.07554)] | [[官网](https://svip-lab.github.io/dataset/RepCount_dataset.html)] [[OneDrive](https://shanghaitecheducn-my.sharepoint.com/:f:/g/personal/dongsx_shanghaitech_edu_cn/EqveZdlGsPxPrfBLQcO_IrgBs6bz7KX1zGGSz_GtLDIfAg)] [[GitHub](https://github.com/SvipRepetitionCounting/TransRAC)] |
| 21 | **Fit3D / AIFit** | 💪 健身 | 611序列 · 2.96M帧3D | [[CVPR 2021]](https://arxiv.org/abs/2508.07554)] | [[官网](https://fit3d.imar.ro/)] [[训练集](https://fit3d.imar.ro/data/fit3d_train.tar.gz)] [[测试集](https://fit3d.imar.ro/data/fit3d_test.tar.gz)] |
| 22 | **SpaceJam** | 🏀 篮球 | 32.5K标注 | [[arXiv](https://arxiv.org/abs/2508.07554)] | ⚠️ [[GitCode](https://gitcode.com/gh_mirrors/sp/SpaceJam)] · 可用性存疑 |

<div align="right">
  <b><a href="#sport-vlm-datasets">↥ back to top</a></b>
</div>

### ⚠️ C级 - 非多模态/需大量工作

| # | **名称** | **运动类型** | **规模** | **论文** | **获取方式** |
|:---:|----------|--------------|----------|:--------:|--------------|
| 23 | **ShuttleSet系列** | 🏸 羽毛球 | 33K-43K击球 | [[AAAI'22/KDD'23/IJCAI'23]](https://arxiv.org/abs/2508.07554)] | [[GitHub](https://github.com/wywyWang/CoachAI-Projects)] |
| 24 | **OpenTTGames** | 🏓 乒乓球 | 12视频 · 4.3K事件 | [[arXiv](https://arxiv.org/abs/2508.07554)] | [[官网](https://lab.osai.ai/)] · CC BY-NC-SA 4.0 |
| 25 | **Free Exercise DB** | 💪 健身 | 800+动作 | - | [[GitHub](https://github.com/wrkout/exercises.json)] · Unlicense |
| 26 | **P²ANet** | 🏓 乒乓球 | 200视频 · 139K事件 | [[TOMM 2024]](https://arxiv.org/abs/2508.07554)] | ⚠️ 需确认论文中的具体获取方式 |
| 27 | **Extended OpenTTGames** | 🏓 乒乓球 | 1.5K击球 | - | ❌ [[GitLab](https://gitlab.compute.dtu.dk/emilh/table_tennis_data)] · 空仓库 |
| 28 | **MultiSenseBadminton** | 🏸 羽毛球 | 7.8K挥拍 | [[Scientific Data 2024]](https://www.nature.com/articles/s41597-024-03271-5)] | ❌ 传感器数据为主，无视频下载入口 |
| 29 | **ALEX-GYM-1** | 💪 健身 | 二分类 | [[SCITEPRESS 2025]](https://arxiv.org/abs/2508.07554)] | ❌ 无可下载数据集 |

<div align="right">
  <b><a href="#sport-vlm-datasets">↥ back to top</a></b>
</div>

### ❌ 待发布

| **名称** | **运动类型** | **预计发布** | **信息来源** |
|----------|--------------|--------------|--------------|
| **SportR** | 🌐 多运动 | ICLR 2026前 | [[GitHub](https://github.com/chili-lab/SportR)] [[arXiv](https://arxiv.org/abs/2511.06499)] |
| **FLEX-VideoQA** | 💪 健身 | 论文接受后 | [[OpenReview](https://openreview.net/forum?id=Fje6v8JnB0)] · ICLR 2026被拒 |
| **SportSkills** | 🌐 55种运动 | 待定 | [[arXiv](https://arxiv.org/abs/2603.25163)] · "will be publicly available" |
| **BioCoach** | 💪 健身 | 待定 | [[arXiv](https://arxiv.org/abs/2603.26938)] |

<div align="right">
  <b><a href="#sport-vlm-datasets">↥ back to top</a></b>
</div>

## 🔍 按运动方向速查

| **方向** | ✅ **首选** | ⚠️ **备选** | ❌ **待发布** |
|----------|------------|------------|--------------|
| ⚽ 足球 | SoccerChat, SoccerNet-XFoul | Domain Adaptation | SportR |
| 🎾 网球 | - | TennisVL | - |
| 🏸 羽毛球 | BFMD | FineBadminton, Shot2Tactic | - |
| 🏓 乒乓球 | OpenTTGames | P²ANet | SportR |
| 🏀 篮球 | ExAct | SpaceJam | SportR |
| 💪 健身(教练) | QEVD, RepCount, Fit3D | BioCoach, EgoExo-Fitness | FLEX |
| 💪 健身(评估) | ExAct, Fit3D | TaiChi-AQA, FLAG3D | FLEX |
| 🌐 多运动 | VideoNet, ExAct, MotionMillion | SPORTU | SportR, SportSkills |
| 🥋 太极 | - | TaiChi-AQA | - |

<div align="right">
  <b><a href="#sport-vlm-datasets">↥ back to top</a></b>
</div>

## 🏋️ 健身方向专项推荐

### AI健身教练（实时反馈+纠正）
- **QEVD** — 1M+ QA，规模最大，[[Qualcomm官网](https://www.qualcomm.com/developer/software/qevd-dataset/downloads)]
- **Fit3D/AIFit** — 3M+帧3D标注，[[官网](https://fit3d.imar.ro/)]
- **RepCount** — 1,451视频+细粒度重复标注，[[OneDrive](https://shanghaitecheducn-my.sharepoint.com/:f:/g/personal/dongsx_shanghaitech_edu_cn/EqveZdlGsPxPrfBLQcO_IrgBs6bz7KX1zGGSz_GtLDIfAg)]
- **MotionMillion** — 1M+样本，[[HF](https://huggingface.co/datasets/InternRobotics/MotionMillion)]

### 动作质量评估（打分）
- **ExAct** — 3,521视频QA，NeurIPS 2025，[[HF](https://huggingface.co/datasets/Alexhimself/ExAct)]
- **Fit3D/AIFit** — 3M+帧3D标注，[[官网](https://fit3d.imar.ro/)]

### 3D姿态+语言
- **Fit3D** — 官网18GB直接下载
- **FLAG3D** — 部分下载，[[项目页](https://andytang15.github.io/FLAG3D/#data)]，Raw Data需邮件

<div align="right">
  <b><a href="#sport-vlm-datasets">↥ back to top</a></b>
</div>

## 🌑 空白方向

| **方向** | **现状** |
|----------|----------|
| 🏃 跑步/骑行/游泳 | 基本空白，动作单一 |
| 🧘 瑜伽/舞蹈 | 有原始视频但缺instruction QA |
| 🏓 乒乓球instruction | 无直接可用，建议OpenTTGames+GPT造 |

## 📝 更新记录

- **2026-06-16**：完成所有链接验证，更新状态标识
- **2026-06-05**：完成32个数据集的整理与验证

---

## 📖 Citation

If you find this resource helpful, please consider giving a ⭐ and citing:

```bibtex
@misc{huang2026sportvlm,
  title={Sport-VLM-Datasets: A Curated List of Sports Vision-Language Fine-Tuning Datasets},
  author={Huang, Qian'an},
  year={2026},
  url={https://github.com/hqa-shu/sport-vlm-datasets}
}
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Add a dataset**: Open an [Issue](https://github.com/hqa-shu/sport-vlm-datasets/issues/new) with the dataset name, paper link, and access method
2. **Fix a link**: Submit a PR with the corrected link
3. **Update status**: If a previously unavailable dataset becomes accessible, let us know

Please follow the existing tier format (S/A/B/C) when suggesting additions.

---

**License**: MIT — See [LICENSE](LICENSE) for details

**状态说明**：
- ✅ = 可直接下载使用
- ⚠️ = 需申请/受限/部分可用/需联系作者
- ❌ = 暂不可获取/未发布/空仓库