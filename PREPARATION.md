# From resource discovery to a training manifest

This guide covers dataset selection and local preparation for sports video-language work. The repository supplies an index and offline tools; it does not supply a trained model, third-party media, or measured training results.

## 1. Select the supervision you actually need

| Experiment | Inspect first | Preparation decision |
|---|---|---|
| Video question answering / SFT | SoccerChat; VideoNet's `training-data/` | Check paired question/answer fields and media paths; retain official validation material. |
| Expert action evaluation | ExAct; VideoNet's `benchmarks/` | Treat benchmark questions as held out unless authors document another protocol. |
| Repetition counting | RepCount / TransRAC | Counting targets need a counting pipeline; generated language labels are a separate dataset artifact. |
| Motion and text | MotionMillion | Use the documented motion representation and component provenance; RGB-video access is a separate question. |
| Spatial vision targets | OpenTTGames | Ball, segmentation and event annotations are not existing language QA. |
| Image/instruction prototyping | Free Exercise DB | Exercise instructions and images are reference material, not exercise-video annotations. |

The catalog records dated source evidence for these distinctions. Check each [full record](CATALOG.md) and its original sources. A Hugging Face split called `train` can be a storage convention; it does not establish that benchmark answers should be used in SFT.

```bash
python3 catalog.py --task video_qa --language paired_text --format json
python3 catalog.py --modality video --access gated
python3 catalog.py --type benchmark
```

## 2. Record access and provenance before conversion

For each resource version, record the original URL, release/revision, annotation and media licenses separately, application conditions, acquisition date and actual file hashes. The index's MIT license covers the index only. A public annotation repository does not establish rights to its source videos.

Use an experiment-local provenance file. Record `unknown` explicitly until checked. Keep restricted media and access tokens outside this repository. Access applications are user-owned decisions; the catalog tools do not submit them.

For BFMD, preserve the difference between paper-wide numbers and the released package rather than combining them into one sample count. For ShuttleSet, identify the exact version. For MotionMillion, retain component-dataset provenance and licenses.

## 3. Preserve the official protocol and prevent leakage

Keep official train/validation/test membership when provided. If an experiment needs a new split, document the reason and separate by the strongest available source group: match, recording/session, subject, or original video. Multiple questions, crops, camera views and neighboring clips from one source should not cross splits.

Use a **globally scoped `group_id`**. Include dataset/version and the match/session identity when needed. Related media appearing in different datasets should share a cross-dataset group after deduplication. The tool can detect only the relationships you declare; it cannot discover near-duplicate videos.

Check exact file hashes and near-duplicate clips separately. Keep benchmark questions and answers out of training. Record conversion scripts, label provenance, frame sampling, resolution and temporal units. Review a sample manually before large-scale conversion; answer quality and temporal grounding cannot be established by JSON validation.

## 4. Build and audit a local video-QA manifest

The [example manifest](example-manifest.jsonl) is **synthetic**. Its media paths do not exist and its answers are not dataset samples. It demonstrates the format only.

Each line is one JSON object:

| Field | Meaning |
|---|---|
| `sample_id` | Unique across all manifest shards |
| `resource_name` | Original dataset and, preferably, version |
| `source_url` | Original HTTP(S) provenance entry point |
| `media_path` | Your local media path; existence and decoding are not checked |
| `split` | `train`, `validation`, or `test` |
| `group_id` | Globally scoped source-video/match/session/subject group |
| `question`, `answer` | Non-empty text from documented annotations or a documented conversion |
| `start_seconds`, `end_seconds` | Optional pair of finite clip boundaries: `0 <= start < end` |

```bash
# Pass every shard together: leakage may cross files.
python3 manifest.py example-manifest.jsonl
python3 manifest.py local-train.jsonl local-validation.jsonl local-test.jsonl
```

Exit codes: `0` format/group checks pass; `1` record errors or split leakage; `2` unreadable or invalid JSON input. The audit neither writes your manifest nor downloads media. It does not verify licenses, media duration/decoding, annotation truth or model quality.

## 5. Make an experiment reproducible

Keep the dataset revision, conversion commit, manifest hashes, split policy, sampling settings, model/checkpoint, random seed, hardware and evaluation protocol together. Report task-appropriate metrics and the held-out set. Publish results only after running the experiment; this project currently makes no fine-tuning performance claim.

## 中文执行要点

先明确任务，再确认媒体与标注的访问条件和许可。按官方划分准备数据；自行划分时，以比赛、视频、会话或受试者分组，避免同源片段跨集合。每个转换过程应保存版本、来源、采样与标签生成方式。`manifest.py` 只检查格式和已声明分组的泄漏，示例为合成数据；通过检查并不代表媒体、标注或训练质量已验证。
