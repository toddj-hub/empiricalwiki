# EmpiricalWiki — Runtime Schema

> 面向经管、会计、金融、管理、经济学实证研究的垂类 LLM Wiki。由 Claude Code 驱动。
> 本文件是 wiki 的运行时入口，定义页面结构、链接规范、workflow 约束。

---

## 仓库布局

需要完整仓库树时，再打开 `docs/runtime-directory-structure.zh.md`。

平时请优先记住这个心智地图：

### `wiki/` 是主要工作面（Obsidian 友好分组）

- `wiki/index.md` 是所有 wiki 页面的目录
- `wiki/log.md` 是 append-only 活动日志
- `wiki/01_论文库/papers/` 存放实证论文结构化卡片
- `wiki/02_研究设计/` 存放实证研究设计层 + 理论建模层：`variables/`、`datasets/`、`models/`、`mechanisms/`、`hypotheses/`、`identification/`、`robustness/`、`heterogeneity/`、`tables/`、`assumptions/`（模型原语）、`propositions/`（形式化结论）
- `wiki/03_知识体系/` 存放可复用知识结构：`concepts/`、`topics/`、`foundations/`、`Summary/`
- `wiki/04_研究者与想法/` 存放研究者、假设、实验和断言：`people/`、`ideas/`、`experiments/`、`claims/`
- `wiki/05_产出/outputs/` 存放生成产物
- `wiki/_系统/graph/` 是派生状态，禁止手动编辑
- 想把 wiki 看成带图谱/搜索/反链的本地网站：跑 `tools/view.sh`，详见 `docs/view-quartz.zh.md`（基于 Quartz，只读渲染，不改内容）

### 格式护栏

- 在新建或修复 wiki 页面结构、YAML、正文章节前，先打开 `docs/runtime-page-templates.zh.md`
- 需要 graph 派生文件细节或 `index.md` / `log.md` 格式时，打开 `docs/runtime-support-files.zh.md`
- `SKILL.md` 是 skill 的即时入口；较大的 skill 也可以在各自目录下提供按需读取的本地参考文件
- `/init` 是这一模式的第一个具体例子：先读 `skills/init/SKILL.md`，只有在需要时再打开 `skills/init/references/*`

### `raw/` 与 `config/`

- `raw/papers/`、`raw/notes/`、`raw/web/` 是用户自有输入
- `raw/discovered/` 存放 `/init` 与 `/daily-arxiv` 抓取的外部论文
- `raw/tmp/` 存放 `/init` 与直接本地 `/ingest` 使用的生成型 prepared sidecar
- `config/` 存放环境与远程服务器模板

---

## 页面类型

实证研究核心类型：`papers`、`variables`、`datasets`、`models`、`mechanisms`、`hypotheses`、`identification`、`robustness`、`heterogeneity`、`tables`。

理论建模核心类型：`assumptions`（模型原语：参与人/偏好/信息/时序/约束）、`propositions`（形式化结论：命题/定理/引理）。`papers` 用 `paper_kind: empirical|theory|both` 区分范式，决定 ingest 走 `/empirical-ingest` 还是 `/theory-ingest`。

保留的通用研究 wiki 类型：`concepts`、`topics`、`people`、`ideas`、`experiments`、`claims`、`Summary`、`foundations`。

页面模板看 `docs/runtime-page-templates.zh.md`；理论建模 6 槽位骨架看 `docs/runtime-theory-skeleton.zh.md`；graph/index/log 参考看 `docs/runtime-support-files.zh.md`。

---

## 链接语法

所有内部链接使用 Obsidian wikilink：

```markdown
[[slug]]                    ← 链接到本 wiki 内任意页面
[[patient-capital]] ← 链接到 variables/patient-capital.md 或 concepts/patient-capital.md
[[耐心资本]]        ← 中文实证论文允许使用 CJK slug
```

**命名规范**：
- **中文论文 slug**：`作者姓氏-年份-关键词1-关键词2`（如 `吕冰洋-2024-省以下财政收入体制-非税收入`）——禁止使用英文音译长串
- **英文论文 slug**：`author-year-keyword`（如 `ang-2025-adaptive-political-economy`）——保持现有格式
- **概念/方法 slug**：英文或 CJK 均可，优先可读性，长度 ≤60 字符
- 禁止模式：`zuozhe-ming-2018-zhongwen-lunwen-biaoti-yinyi-changchuan`（中文论文的英文音译 slug）

---

## Cross Reference 规则

写正向链接时**必须同步写反向链接**：

| 正向操作 | 必须同步的反向操作 |
|----------|-------------------|
| papers/A 写 `Related: [[concept-B]]` | concepts/B 的 `key_papers` 追加 `A` |
| papers/A 写 `[[researcher-C]]` | people/C 的 `Key papers` 追加 `A` |
| papers/A 写 `supports: [[claim-D]]` | claims/D 的 `evidence` 追加 `{source: A, type: supports}` |
| papers/A 写 `operationalizes: [[variable-V]]` | variables/V 的 `source_papers` 追加 A |
| papers/A 写 `uses_dataset: [[dataset-D]]` | datasets/D 的 `source_papers` 追加 A |
| papers/A 写 `estimates_model: [[model-M]]` | models/M 的 `source_papers` 追加 A |
| papers/A 写 `tests_mechanism: [[mechanism-M]]` | mechanisms/M 的 `source_papers` 或 `evidence` 追加 A |
| papers/A 写 `tests_hypothesis: [[hypothesis-H]]` | hypotheses/H 的 `source_papers` 追加 A |
| papers/A 写 `addresses_endogeneity_with: [[identification-I]]` | identification/I 的 `source_papers` 追加 A |
| papers/A 写 `uses_robustness_check: [[robustness-R]]` | robustness/R 的 `source_papers` 追加 A |
| papers/A 写 `uses_heterogeneity_split: [[heterogeneity-H]]` | heterogeneity/H 的 `source_papers` 追加 A |
| papers/A 写 `assumes: [[assumption-X]]` | assumptions/X 的 `source_papers` 追加 A |
| papers/A 写 `proves: [[proposition-P]]` | propositions/P 的 `source_papers` 追加 A |
| papers/A 写 `formalizes_mechanism: [[mechanism-M]]` | mechanisms/M 的 `source_papers` 或 `evidence` 追加 A（理论侧），并在 `## Theoretical Logic` 补理论来源 |
| propositions/P 写 `predicts: [[hypothesis-H]]` | hypotheses/H 的 `source_papers` 追加 P，并在 `## Literature Basis` 标注理论来源 |
| topics/T 写 `key_people: [[person-D]]` | people/D 的 `Research areas` 追加 T |
| concepts/K 写 `key_papers: [[paper-E]]` | papers/E 的 `Related` 追加 `K` |
| concepts/K 写 part_of `[[topic-F]]` | topics/F 的概述段落追加 `K` |
| ideas/I 写 `origin_gaps: [[claim-C]]` | claims/C 的 `## Linked ideas` 追加 I |
| experiments/E 写 `target_claim: [[claim-C]]` | claims/C 的 `evidence` 追加 `{source: E, type: tested_by}` |
| claims/C 写 `source_papers: [[paper-P]]` | papers/P 的 `## Related` 追加 C |
| 任意页面链接到 `[[foundation-X]]` | **不写反向链接** — foundations 是终端节点：接收来自 papers/concepts 等页面的入链，但不写 `key_papers` 或任何反向引用字段 |

---

## Graph 规则

- `graph/` 是自动生成目录，不要手动编辑
- 核心派生文件是 `edges.jsonl`、`citations.jsonl`、`context_brief.md`、`open_questions.md`
- semantic edge type 包括 paper-paper（`same_problem_as`、`similar_method_to`、`complementary_to`、`builds_on`、`compares_against`、`improves_on`、`challenges`、`surveys`）、paper-concept（`introduces_concept`、`uses_concept`、`extends_concept`、`critiques_concept`）、实证抽取（`operationalizes`、`uses_dataset`、`estimates_model`、`tests_mechanism`、`tests_hypothesis`、`addresses_endogeneity_with`、`uses_robustness_check`、`uses_heterogeneity_split`、`reports_table`）、理论抽取（`assumes`、`proves`、`formalizes_mechanism`、`predicts`），以及既有 claim/experiment/provenance 类型（`supports`、`contradicts`、`tested_by`、`invalidates`、`addresses_gap`、`derived_from`、`inspired_by`）
- `/ingest` 产生的 paper-paper 与 paper-concept semantic edge 必须带 `confidence: high|medium|low`
- `/theory-ingest` 的 `assumes`、`proves` 是结构事实，不带 confidence；`formalizes_mechanism`、`predicts` 是判断，必须带 `confidence: high|medium|low`
- 对称 paper-paper edge 只存一行，endpoint 按顺序排序，并写 `symmetric: true`
- bibliographic citation 存在 `citations.jsonl`，`type: cites`
- 用 `tools/research_wiki.py add-edge`、`add-citation`、`rebuild-context-brief`、`rebuild-open-questions` 维护

## log.md 格式

标准日志行：

```markdown
## [YYYY-MM-DD] skill | details
```

## Python 环境

- 有 `.venv/` 时优先用 `.venv/bin/python`（Unix/macOS）或 `.venv/Scripts/python.exe`（Windows）
- 否则使用当前激活的 conda 环境
- 再否则回退到 `python3`（Unix/macOS）或 `python`（Windows）
- Python 工具会通过 `tools/_env.py` 自动加载 `~/.env` 与项目根目录 `.env`

---

## 约束

- **`raw/papers/`、`raw/notes/`、`raw/web/` 归用户所有**：把它们当作权威输入。`/init` 与 `/daily-arxiv` 只能把外部抓取论文追加到 `raw/discovered/`。`/init` 与直接本地 `/ingest` 可以把生成的本地预处理 sidecar 写到 `raw/tmp/`（只增不改，绝不覆盖用户自有文件）。`/edit` 仅在用户明确要求时才允许新增 raw 来源。`/init` 在 INIT MODE 下 fan-out 的 `/ingest` 子代理仍必须把 `raw/` 视为严格只读，并直接消费交接的 canonical path。
- **skill 的用户可见参数归用户所有**：skill 的 `argument-hint` 中列出的 flag 与取值属于用户命令，而不是 agent 可自行决定的策略开关。不得仅根据仓库状态擅自补出、切换或删除这些参数。若用户未提供某个参数，只有在该 skill 明确写出省略时的默认或推导规则时，才可使用该默认或推导值；否则应保持未设置，必要时询问用户。不是用户可见参数的内部派生设置，skill 仍可自行推断。
- **INIT MODE 交接由 manifest 驱动**：当 `/init` 写出 `.checkpoints/init-sources.json` 后，该 manifest 就是 ingest 顺序与规范来源路径的唯一真相来源。预处理后的本地输入应指向 `raw/tmp/`；外部引入论文应指向 `raw/discovered/`。
- **graph/ 自动生成**：不得手动编辑 `graph/` 下的文件，仅通过 `tools/research_wiki.py` 维护。
- **实证抽取优先**：阅读实证论文时，先抽取变量、数据来源、模型设定、理论机制、异质性、稳健性和识别策略，再写通用概念或 idea。
- **理论抽取优先**：阅读理论建模论文（`paper_kind: theory`）时，对着 `docs/runtime-theory-skeleton.zh.md` 的 6 槽位先抽取假设/原语、命题/定理、解概念、可检验推论，再写通用概念或 idea。形式化陈述逐字引用，禁止释义改写成立条件。
- **双向链接**：写正向链接时同步写反向链接。
- **tex 优先**：.tex > .pdf，fallback 链：tex 失败 → PDF 解析，PDF 失败 → vision API。
- **index.md 每次 ingest 立即更新**，log.md append-only。
- **lint 默认只报告**：`--fix` 自动修复确定性问题（xref 反向链接、缺失字段默认值）；`--suggest` 输出非确定性问题的建议供用户批准；`--fix --dry-run` 预览修复。
- **slug 生成规则**：论文标题关键词，连字符连接；英文全小写，中文标题允许保留 CJK 字符。
- **importance 评分**：1 = niche, 2 = useful, 3 = field-standard, 4 = influential, 5 = seminal。
- **idea 失败必须记录原因**：`failure_reason` 字段是反重复记忆，防止重复探索已知死路。
- **claim confidence 区间**：0.0-1.0，evidence 每次变动时重新评估。
- **实验模块对经管实证是可选项**：Stata 式实证流程优先使用 `models/`、`tables/`、`identification/` 和 `robustness/`。`experiments/` 仅保留给计算实验、仿真或机器学习任务。
- **DeepXiv token**：`DEEPXIV_TOKEN` 环境变量。未设置时 SDK 自动注册（写入 `~/.env`）。免费额度 10,000 请求/天。DeepXiv 不可用时所有 skill 自动回退到 S2+RSS 模式。

---

## Skills

| Skill | 文件 | 触发 |
|-------|------|------|
| `/setup` | `skills/setup/SKILL.md` | 手动（首次配置） |
| `/reset` | `skills/reset/SKILL.md` | 手动（`--scope wiki\|raw\|log\|checkpoints\|all`） |
| `/init` | `skills/init/SKILL.md` | 手动 |
| `/prefill` | `skills/prefill/SKILL.md` | 手动（`[domain] [--add concept]`） |
| `/ingest` | `skills/ingest/SKILL.md` | 手动 |
| `/empirical-ingest` | `skills/empirical-ingest/SKILL.md` | 手动 |
| `/theory-ingest` | `skills/theory-ingest/SKILL.md` | 手动 |
| `/variable-map` | `skills/variable-map/SKILL.md` | 手动 |
| `/empirical-design` | `skills/empirical-design/SKILL.md` | 手动 |
| `/stata-plan` | `skills/stata-plan/SKILL.md` | 手动 |
| `/discover` | `skills/discover/SKILL.md` | 手动 / 内部（`/ingest --discover` 时调用） |
| `/ask` | `skills/ask/SKILL.md` | 手动 |
| `/edit` | `skills/edit/SKILL.md` | 手动 |
| `/check` | `skills/check/SKILL.md` | 每两周/手动 |
| `/daily-arxiv` | `skills/daily-arxiv/SKILL.md` | cron 08:00 / 手动 |
| `/novelty` | `skills/novelty/SKILL.md` | 手动 |
| `/review` | `skills/review/SKILL.md` | 手动 |
| `/ideate` | `skills/ideate/SKILL.md` | 手动 |
| `/exp-design` | `skills/exp-design/SKILL.md` | 手动 |
| `/exp-run` | `skills/exp-run/SKILL.md` | 手动（`<slug> [--collect] [--full] [--env local\|remote]`） |
| `/exp-status` | `skills/exp-status/SKILL.md` | 手动（`[--pipeline <slug>] [--collect-ready] [--auto-advance]`） |
| `/exp-eval` | `skills/exp-eval/SKILL.md` | 手动 |
| `/refine` | `skills/refine/SKILL.md` | 手动 |
| `/paper-plan` | `skills/paper-plan/SKILL.md` | 手动 |
| `/paper-draft` | `skills/paper-draft/SKILL.md` | 手动 |
| `/paper-compile` | `skills/paper-compile/SKILL.md` | 手动 |
| `/survey` | `skills/survey/SKILL.md` | 手动 |
| `/research` | `skills/research/SKILL.md` | 手动 |
| `/rebuttal` | `skills/rebuttal/SKILL.md` | 手动 |

---

## 原文通路规程

Agent 从 Obsidian 笔记查找原文的标准路径（优先级递减）：

1. **paper 卡片 `zotero_key`** → Zotero MCP `get_item_details` → PDF 附件 / 完整书目
2. **paper 卡片 `pdf_path`** → 文献包直接打开 PDF
3. **`zotero_key` + `pdf_path` 均缺失** → Zotero MCP `search_library`（title/author 模糊匹配）
4. **仍未找到** → 标记 `NEEDS_SOURCE`，记录到 paper 卡片的 `## 溯源状态`

原文摘抄存入 `raw/notes/`，在 paper 卡片的引用溯源表中标注 PDF 页码。

### 配置

- **文献包根目录**：`C:\Users\HONOR\Desktop\文献包`
- **Zotero MCP 端点**：`http://127.0.0.1:23120/mcp`（20 个工具可用）
- **paper 卡片字段**：
  - `zotero_key`：Zotero 条目 ID（8 位字母数字，如 `THJGZC9A`）
  - `pdf_path`：文献包内 PDF 相对路径（如 `T/Tang-2020-Institutional-Foundation.pdf`）
  - `source_status`：`zotero_linked` | `pdf_only` | `needs_source`

---

## 论文阅读双模规则（2026-07-22）

每篇文献的阅读服务于两个目标：「内容积累」和「写法学习」。

### 快速模式触发条件（满足任一）

- 用户说"查一下XX""补引用""找素材""搜文献"
- 论文 importance ≤ 3 且用户未指定深度阅读

**快速模式操作**：搜索→定位相关段落→摘抄原文≥30字（不设上限，有用的全摘）→写入章节素材库「关键引用溯源」表→汇报"为ChX主题积累了Y条引用素材"。

### 深度模式触发条件（满足任一）

- 用户说"拆解这篇""学习一下""精读""读论文"
- 论文 importance ≥ 4
- 论文发表在顶刊（经济研究/管理世界/AER/Econometrica/JPE/QJE等）
- 论文直接对应论文章节核心论点

**深度模式操作（四步，必须全部执行）**：

- **第一步-内容提取**：摘抄写入 `raw/notes/{paper-slug}.md`（不限条数、不限字数、完整存档），同时精选最相关条目写入章节素材库「关键引用溯源」表（四列格式，追加第五列"与论文关联"）
- **第二步-写法拆解**：将论文的摘要/引言/文献综述/方法/结果/讨论/结论逐一拆解，标注具体可迁移的技法
- **第三步-方法论反哺**：将拆解出的新技法写入 `03_知识体系/方法论/经济学论文写作模式/` 对应子目录的「优秀范例」或「常见错误」section，标注来源论文
- **第四步-汇报**："深度阅读XX论文：内容积累Y条→raw/notes/ + 写法拆解Z个技法→方法论/ + Skill更新建议W条"

### 摘抄双层存储（与原文通路规程对齐）

- `raw/notes/{paper-slug}.md`：全文所有摘抄的原始存档，不限条数、不限字数
- 素材库「关键引用溯源」表：从 raw/notes 中精选最相关的条目，四列格式（段落位置→引文→原文摘抄≥30字→来源页码），追加第五列"与论文关联"

### Skill更新阈值（两层）

- **笔记层**（每次深度阅读都做）：追加到对应方法笔记的「优秀范例」或「常见错误」
- **Skill层**（积累到阈值才触发）：当某方法笔记的「优秀范例」≥5条 或「常见错误」≥8条时，触发一次skill更新，将笔记中的模式提炼为写作规范规则。触发时主动告知用户："XX部分已积累N条范例/M条错误，建议更新写作skill，是否执行？"

### 禁止行为

- 深度模式下只摘抄不拆解写法
- 摘抄设上限或断尾
- 素材库四列表格出现"待填充"

### 政策背景查询规则（写作前）

- 写作引言/研究背景/政策建议段落前，先查 `07_政策与法规/导航`，检索相关条目
- 摘抄写入对应章节素材库的「制度背景素材」section 后再动笔写正文
- 政策引用格式：`[[07_政策与法规/分类/文件名]]`（日期）+ 核心内容摘抄
