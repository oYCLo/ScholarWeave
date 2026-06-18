# ScholarWeave 用法手册

整套已融合安装完成。这份文档讲**怎么用**——按研究生命周期组织，给出该说什么/敲什么命令，并标注重叠工具该选哪个。

> 触发方式有两种：
> - **自然语言**（中文即可）→ 命中某个 skill 的触发词，Claude 自动调用。
> - **斜杠命令** `/xxx` → 显式调用某个 command。
>
> 改完任何配置或重装后，`/reload` 或重启 Claude Code 生效。

---

## 0. 一分钟全景

```
每天晨读        →  知识库沉淀        →  选题打磨          →  代码&实验        →  写作&投稿
今日论文推荐        kb-* / obsidian      first-principles    daily-coding       ml-paper-writing
paper-reader       -skills 整理         -ideation 委员会     experiment-setup   nature-* / ars-*
更新索引(MoC)                                                results-analysis   review-response
        └──────────────── 全部读写同一个 Obsidian vault：/Users/ycl/Workspace/dailypaper/omo ─────────┘
```

四套来源混在一起，按场景取用即可：
- **dailypaper-skills**（中文）：每日论文流水线。
- **obsidian-skills（kepano）**：底层 vault 操作原语。
- **claude-scholar**：47 skills + 101 commands 的全生命周期套件（含 `kb-*`、`sc:*`、`nature-*`）。
- **ARS 插件**：`/ars-*` 论文写作/评审流水线（与 scholar 的写作部分重叠，见 §6）。

---

## 1. 每日晨读（dailypaper）

| 你说 | 发生什么 |
|---|---|
| `今日论文推荐` | 抓 arXiv + HuggingFace 最新论文 → 按你的关键词打分 → 必读/值得读/可跳过，写进 vault 的 `DailyPapers/` |
| `过去3天论文推荐` / `最近一周论文` | 同上，多天模式 |
| `读一下这篇论文 https://arxiv.org/abs/XXXX` | 单篇精读 → 结构化笔记（方法/实验/公式/图/局限）落到 `论文笔记/`，并回链已有概念 |
| `批量笔记` | 给本轮推荐的重点论文批量生成笔记 |
| `更新索引` | 重建 Obsidian 的目录页 / 概念 MoC（`generate-mocs`） |

调口味：编辑 `~/.claude/skills/_shared/user-config.json` 的 `keywords` / `negative_keywords` / `domain_boost_keywords` / `arxiv_categories`（版本化副本在 `config/dailypaper-user-config.json`）。

---

## 2. 知识库沉淀（obsidian-skills + claude-scholar 的 kb-*）

两层能力：

**底层原语（kepano，自然语言触发）**
- 写规范的 Obsidian 笔记（wikilink / callout / frontmatter）→ `obsidian-markdown`
- 建数据库式视图（按方法/年份/数据集列出所有论文笔记）→ `obsidian-bases`，说“给论文笔记建一个 Base 表”
- 画概念图谱（OT ↔ Schrödinger bridge ↔ flow matching）→ `json-canvas`，说“画一张 canvas”
- 命令行批量操作 vault → `obsidian-cli`
- 把网页抽成干净 markdown → `defuddle`（给个 URL 说“读一下这个网页”）

**项目级 KB 工作流（scholar 的 `/kb-*` 命令）** —— 适合「为某个课题维护一个结构化子库」
| 命令 | 用途 |
|---|---|
| `/kb-init` | 在 `Research/{项目}/` 下初始化项目知识库骨架 |
| `/kb-ingest` | 把外部材料（论文/网页/数据）收进 `Sources/` |
| `/kb-literature-review` | 项目内文献综述（落到 `Knowledge/`） |
| `/kb-map` | 生成/更新文献 canvas（`Maps/literature.canvas`） |
| `/kb-log` / `/kb-status` | 每日记录 / 看项目 KB 状态 |
| `/kb-links` / `/kb-lint` | 修复链接 / 体检 |
| `/kb-index` / `/kb-promote` / `/kb-archive` | 索引 / 升级笔记 / 归档 |

> 注意：你原有的 `obsidian-vault` skill 指向另一个 vault 路径（`/mnt/d/...`，疑似旧机器）。dailypaper 用的是 `/Users/ycl/Workspace/dailypaper/omo`。如果想统一，改 `obsidian-vault/SKILL.md` 里的路径。

---

## 3. 选题打磨（你已有的委员会）

想法成型前，先过 **first-principles-ideation** 委员会（proposer / skeptic / methodologist / math-ledger / experiment-designer / referee）：
- 说 `帮我从第一性原理拆一下这个想法` / `poke holes in this` / `最小可行实验是什么` / `/first-principles-ideation`
- 特别适合你的领域：单细胞扰动建模、轨迹推断、生成式建模、最优传输/Schrödinger bridge。
- 它**只停留在研究思考层**，不写代码、不出稿子。

配套 scholar skill：`research-ideation`（5W1H、gap analysis）、`/research-init`（起项目）。

---

## 4. 写代码 & 跑实验（claude-scholar 的 ML 工具）

| 场景 | 工具 / 触发 |
|---|---|
| 日常写/改代码 | `daily-coding` |
| 设计网络、估参数量/FLOPs | `model-architect`：“帮我搭个模型 / 这个模型怎么改” |
| 写训练循环、混合精度、DDP/FSDP | `training-helper`：“写个训练循环 / 多卡训练” |
| 配 wandb、实验目录、可复现 | `experiment-setup`：“配置 wandb / 实验怎么组织” |
| 报错调试（CUDA/shape/NaN/OOM） | `pytorch-debugger`：“报错了 / loss 不降 / NaN” |
| 严格统计分析 + 科研图 | `results-analysis`：“分析实验结果 / 做消融 / 显著性检验” |
| 出版级图表/表格 | `publication-chart-skill` |
| 实验复盘报告 | `results-report`：“写实验总结报告” |
| 代码审查 | `code-reviewer`（PyTorch 反模式）/ `/code-review`（diff 级） |

---

## 5. 写论文 —— 这里有两条重叠路线，二选一

你现在**同时**有：
- **ARS 插件**：`/ars-full`、`/ars-outline`、`/ars-plan`、`/ars-abstract`、`/ars-lit-review`、`/ars-citation-check` …（多 agent 流水线，模型已在 frontmatter 钉好）
- **claude-scholar**：`ml-paper-writing`、`nature-writing`、`nature-polishing`、`nature-data`、`citation-verification`、`paper-self-review`、`writing-anti-ai`

**建议选法：**
- **投 ML 顶会（NeurIPS/ICML/ICLR…）** → 用 scholar 的 `ml-paper-writing`（自带这些会议的 LaTeX 模板 + 引用核验）。
- **投 Nature 系 / 强调英文润色** → 用 scholar 的 `nature-writing` / `nature-polishing`。
- **想要"研究→写→评审→修改→定稿"一条龙、且要可复现质量门** → 用 ARS 的 `/ars-full` 或 `academic-pipeline`。
- **润掉 AI 味**（中英都行）→ `writing-anti-ai`。
- **投稿前自检**（过度声称/结论是否被结果支撑）→ `paper-self-review`。

> 不要在同一篇稿子上混用两条流水线——它们对结构/状态的假设不同。挑一条走到底。

---

## 6. 投稿、Rebuttal、接收后

| 阶段 | 工具 |
|---|---|
| 回复审稿意见（逐点） | scholar `review-response` / `nature-response`（“写 rebuttal / 逐点回复 / 如何回复 reviewer”）；或 ARS `/ars-revision`、`/ars-revision-coach` |
| 引用核验 / 报错 | scholar `citation-verification`；ARS `/ars-citation-check` |
| 模拟审稿 | ARS `/ars-reviewer`（5 人评审团） |
| AI 使用声明 | ARS `/ars-disclosure` |
| 接收后：海报/Slides/推广 | scholar `post-acceptance` + `/poster` `/presentation` `/promote` |

---

## 7. 命令速查（按场景）

```
晨读      今日论文推荐 · 读一下这篇论文 <url> · 批量笔记 · 更新索引
知识库    /kb-init /kb-ingest /kb-literature-review /kb-map /kb-status /kb-lint
选题      /first-principles-ideation · /research-init · research-ideation
实验      model-architect · training-helper · experiment-setup · pytorch-debugger · results-analysis
写作(顶会) ml-paper-writing      写作(Nature) nature-writing/nature-polishing
写作(一条龙) /ars-full · academic-pipeline
投稿      review-response/nature-response · /ars-reviewer · /ars-citation-check
接收后    post-acceptance · /poster · /presentation
SuperClaude  /sc:* （/sc:research /sc:implement /sc:analyze /sc:document … 通用工程命令集）
```

---

## 8. ⚠️ 安装带来的全局变化（请过目）

claude-scholar 是**全局安装**，改了 `~/.claude`：

1. **全局 `CLAUDE.md` 现在是 scholar 的**（"Claude Scholar Core Instructions"）。你之前没有全局 CLAUDE.md，所以它直接成了你**所有项目**的默认指令。建议读一遍 `~/.claude/CLAUDE.md`，不合适的段落可删。
2. **新增 5 个全局 hooks**：`PreToolUse`(security-guard) `SessionStart`(session-start) `UserPromptSubmit`(skill-forced-eval) `Stop`/`SessionEnd`(summary)。其中 `skill-forced-eval` 会在每次输入时强制评估要不要调 skill；`SessionStart` 与你 ARS 插件的 SessionStart 会**叠加**（都跑，不冲突，但开场信息更长）。
3. **覆盖了 3 个原有文件**（已备份）：`agents/code-reviewer.md`、`commands/commit.md`、`skills/defuddle/SKILL.md`。
4. 备份位置：`~/.claude/.claude-scholar-backups/20260618-132255/` 和 `~/.claude/settings.json.bak`。

**全部可回退**：`cd /Users/ycl/Workspace/ScholarWeave && ./uninstall.sh --scholar`

---

## 9. 维护

```bash
cd /Users/ycl/Workspace/ScholarWeave
./update.sh                 # 拉上游最新 + 重新钉 versions.lock + 重链
./update.sh --with-scholar  # 顺带重跑 scholar 安装器
./uninstall.sh              # 只删本仓建的软链
./uninstall.sh --scholar    # 连 scholar 一起卸
```

配置 / 路径速记：
- dailypaper 配置：`~/.claude/skills/_shared/user-config.json`
- Obsidian vault：`/Users/ycl/Workspace/dailypaper/omo`
- 全局指令：`~/.claude/CLAUDE.md`（scholar 的）
- skills 安装目录：`~/.claude/skills/`（kepano 是软链到 `vendor/`，scholar/dailypaper 是真实目录）
