# ScholarWeave 工作计划

> 本地、私有、AI 驱动、可长期迭代的科研知识库系统
> 版本 v3 · 2026-06-17 · 维护人：black
> v3 新增：论文搜索环（§5）+ Multi-agent 编排降低上下文（§6）

---

## 1. 目标

把零散的论文、网页、笔记、实验记录，沉淀成一个**本地纯 Markdown、双向链接**的知识库；
再让 AI agent 作为"图书管理员 + 科研合作者"，驱动一个**带搜索、验证和迭代的研究闭环**：

论文搜索 → 凝练科学问题 → 构建 idea/方法 → 设计验证(toy 实验/可证伪) → 迭代结果 → 回写知识库。

并且把 AI 协作过程中产生的大量问答，**凝练、去重、归档**成可检索的笔记，而不是聊完即弃。
整套编排采用 **multi-agent**：一个主负责人(orchestrator)只规划和派活，不亲自干活，从而把每个 agent 的上下文压到最短。

### 五条设计原则
1. **本地优先**：数据是你自己磁盘上的纯 Markdown，不锁定任何厂商。
2. **AI 是管理员不是数据库**：AI 负责读、关联、整理、生成；数据始终可读可迁移。
3. **闭环而非单向**：搜索、验证、迭代结果都要回流，知识库越用越厚。
4. **问答即资产**：协作对话凝练后归档，达到"可归档级"而非"问题级"。
5. **主从分工**：主 agent 不持有大上下文，重活分派给短上下文的子 agent。

---

## 2. 整体架构（v3）

```
                          ┌──────────── Orchestrator 主负责人(不干活,只派活) ────────────┐
                          │   持有：任务清单 + index.md 摘要(短上下文)                    │
                          ▼            ▼            ▼            ▼            ▼            ▼
                      SearchAgent  IngestAgent  DistillAgent  MethodAgent ValidationAgent ArchiveAgent
                          │            │            │            │            │            │
关键词/描述 ─▶ ⓪论文搜索 ─▶ 00-inbox ─▶ MarkItDown ─▶ Obsidian Vault ◀───────────────────┘
(arxiv/SS)                                → Markdown  (双向链接,纯MD)
                                                      10-literature(每篇一文件夹)/20-entities/
                                                      30-concepts/40-questions/50-ideas/
                                                      60-experiments/70-synthesis
                                                          │
            研究闭环：① 凝练问题 ─▶ ② 构建方法 ─▶ ③ 验证设计(toy实验/可证伪) ─▶ ④ 迭代结果 ──┐
                          ▲                                                                   │
                          └──────────────── 下一轮迭代 · 回写 vault ───────────────────────────┘

            对话归档旁路：AI 问答流 ─▶ 凝练/去重 ─▶ basic-memory(MCP→MD) ─▶ 回写 vault
```

层次：
- **⓪ 论文搜索环**（v3 新增）：从关键词/描述出发，检索论文进 `00-inbox/`。
- **采集→转换→存储**：raw → MarkItDown → Obsidian vault。
- **编排闭环**：①凝练 → ②构建 → ③验证 → ④迭代，结果回流。
- **归档旁路**：basic-memory 把对话凝练成可归档笔记。
- **Multi-agent**：Orchestrator 派活给 6 个专职子 agent（§6）。

---

## 3. 技术选型（核心仓库已拉到 `repos/`）

| 角色 | 仓库 / 工具 | Star | 许可证 | 说明 |
|---|---|---|---|---|
| ⓪论文检索 | blazickjp/arxiv-mcp-server | — | Apache-2.0 | arXiv 搜索+下载的 MCP，agent 直接调 |
| ⓪论文检索 | openags/paper-search-mcp | — | — | 跨源(arXiv/PubMed/bioRxiv 等)论文搜索 MCP |
| ⓪自治检索 | claude-obsidian `autoresearch` skill | — | MIT | Karpathy autoresearch：搜→综合→入库 |
| ⓪自治检索 | obsidian-wiki `wiki-research` skill | — | MIT | 多轮 web 搜索→结构化入库 |
| 转换 | microsoft/markitdown | ~139k | MIT | PDF/Word/PPT/网页/音频 → Markdown，含 MCP |
| 编排核心 | AgriciDaniel/claude-obsidian | ~5.8k | MIT | 15 skills + 多 agent + hot cache，**首选** |
| 编排(目录范式) | NicholasSpisak/second-brain | ~393 | 无 LICENSE | sources/entities/concepts/synthesis 最清晰 |
| 编排(skills 最多) | Ar9av/obsidian-wiki | ~1.5k | MIT | 30+ skills，含 vault-skill-factory 造 skill |
| 文献问答 | Future-House/paper-qa | ~8.6k | Apache-2.0 | 高精度 RAG，带引用 + 撤稿检查 |
| ①凝练/综述 | stanford-oval/storm | ~25k | MIT | Co-STORM 多视角提问 → 带引用综述 |
| ①深研报告 | assafelovic/gpt-researcher | ~27k | Apache-2.0 | 自治深研 agent |
| ③验证/自动实验 | SakanaAI/AI-Scientist | ~14k | Apache-2.0 | 假设→实验→分析→写稿范式 |
| ③④实验追踪 | aimhubio/aim | 开源 | Apache-2.0 | 记录/对比 toy 实验，承载迭代结果 |
| ④对话归档 | basicmachines-co/basic-memory | ~3.1k | **AGPL-3.0** | MCP→Markdown，对话写成可归档笔记 |

> **许可证提醒**：second-brain 无 LICENSE；basic-memory 为 AGPL-3.0（传染性强，商用前复核）。

---

## 4. 项目目录结构（有章法的总布局）

### 4.1 根目录：五大区，各归各位
原则：**配置、第三方工具、知识库、实验代码、对外产出**互不混放；知识库(vault)是纯 Markdown 主体，代码和大文件不进 vault。

```
ScholarWeave/
├── README.md                  # 项目说明
├── WORK_PLAN.md               # 本计划
├── ORCHESTRATOR.md            # 主负责人派活规则
├── .gitignore                 # 忽略 pdf 大文件 / .aim / __pycache__
├── config/                    # ① 配置区
│   ├── agents/                #   子 agent 定义(search/ingest/...)
│   ├── skills/                #   自建 skills
│   └── templates/             #   note 模板(paper/question/idea/experiment)
├── repos/                     # ② 第三方工具(已克隆,只读参考)
│   ├── markitdown/  claude-obsidian/  paper-qa/  ...
├── vault/                     # ③ 知识库(Obsidian 打开这里,纯 Markdown)
│   └── …见 4.2
├── code/                      # ④ 实验代码(与 vault/experiments 一一对应)
│   └── <exp-id>/  run.py  config.yaml  .aim/
└── outputs/                   # ⑤ 对外产出：proposal / 报告 / 导出 PDF
```

### 4.2 vault 内部：固定语义目录（编号前缀保证排序）
```
vault/
├── index.md               # MOC 总索引(Orchestrator 只读这个,保持短上下文)
├── 00-inbox/              # 收件箱：搜索/剪藏来的原始素材(待处理)
├── 10-literature/         # ★ 论文库：每篇论文一个独立子文件夹(见 4.3)
├── 20-entities/           # 人物、机构、工具、数据集
├── 30-concepts/           # 概念、框架、理论
├── 40-questions/          # 凝练出的科学问题(重要性/意义/related work)
├── 50-ideas/              # idea 与方法草案
├── 60-experiments/        # 每个实验一个子文件夹(design/results)
├── 70-synthesis/          # 综合 → proposal 雏形
├── 80-archive/            # 凝练归档的 AI 问答结论
└── 90-search/             # 检索：关键词、查询串、命中清单、检索日志
```
> 编号前缀(00/10/…)让 Obsidian 文件树和资源管理器里顺序稳定，新增类别留出空档(如 15-、25-)，是 Johnny-Decimal 式的"有章法"。
>
> **名称映射**（后文沿用语义简称）：`00-inbox`=raw 收件箱 · `10-literature`=sources 论文库 · `40-questions`=questions · `50-ideas`=ideas · `60-experiments`=experiments · `70-synthesis`=synthesis · `80-archive`=archive · `90-search`=search。

### 4.3 ★ 每篇论文 = 一个独立子文件夹
`10-literature/` 下，每篇论文一个文件夹，命名用 **citekey = 作者+年份+关键词**（如 `vaswani2017attention`）：
```
10-literature/
└── vaswani2017attention/
    ├── note.md            # 主笔记：结构化摘要(下方模板)
    ├── meta.yaml          # 题录元数据(标题/作者/年/DOI/引用数/撤稿状态)
    ├── highlights.md      # 原文摘录与标注
    ├── paper.pdf          # 原文(.gitignore 排除,或软链到 code 外)
    └── assets/            # 图表截图、公式图
```
好处：论文相关的一切(笔记/原文/图/标注)聚在一处，`[[vaswani2017attention]]` 一个链接即可在 ideas/questions 里引用；删除/迁移一篇论文是原子操作。

### 4.4 命名规范（统一才不乱）
| 对象 | 规则 | 示例 |
|---|---|---|
| 论文文件夹(citekey) | `作者姓+年份+首个关键词`，全小写 | `chen2024diffusion` |
| 科学问题 | `Q<编号>-<短名>` | `Q01-few-shot-anomaly` |
| idea/方法 | `I<编号>-<短名>` | `I03-diffusion-recon` |
| 实验 | `EXP-<编号>-<短名>` | `EXP-007-recon-vs-baseline` |
| 假设 | `H<编号>` 写在实验内 | `H1` |
| 归档对话 | `YYYY-MM-DD-<主题>` | `2026-06-17-loss-design` |
| 文件名 | 小写中划线，不含空格 | `note.md` |

### 4.5 论文 note.md 模板（放 config/templates/paper.md）
```markdown
---
citekey: vaswani2017attention
title: "Attention Is All You Need"
authors: [Vaswani, ...]
year: 2017
venue: NeurIPS
doi:
citations:
retracted: false
tags: [transformer, attention]
status: read        # to-read / reading / read
priority: high
---

# {{title}}

## 一句话
## 解决的问题 / 动机
## 方法核心
## 实验设置与数据集
## 可证伪条件 / 局限   ← 给 ③验证环复用
## 与我的关系（链接到 [[Q..]] / [[I..]]）
## 关键摘录 → highlights.md
```

> 其它类型(question/idea/experiment)的模板同样放 `config/templates/`，由对应子 agent 套用，保证每页结构一致。

---

## 5. ⓪ 论文搜索环（项目起点）

每个项目从这里开始：把一段方向描述，变成可执行的检索，再把命中论文喂进 `raw/`。

### 5.1 起点：项目描述模板
在 `search/<项目名>.md` 里填：
```
## 项目描述
一句话方向：____
我想解决的问题（口语版）：____
已知的种子论文（必读，若有）：____
约束 / 不感兴趣的方向：____
```

### 5.2 SearchAgent 据描述自动产出关键词
让 SearchAgent 把描述展开成结构化检索词（输出回写 `search/<项目名>.md`）：
```
## 检索关键词
- 核心概念词（3–5）：____
- 同义 / 近义扩展：____
- 方法关键词：____
- 任务 / 数据集关键词：____
- 组合查询串（arXiv 语法）：例如  (all:"keyword A" AND all:"method B") ANDNOT cat:xx
- 组合查询串（Semantic Scholar）：____
- 种子论文 → 滚雪球：引用 / 被引 各追 1 跳
```

**示例**（方向＝"用扩散模型做小样本时间序列异常检测"）：
- 核心概念：time series anomaly detection, diffusion model, few-shot
- 扩展：outlier detection, generative model, score-based, limited labels
- 方法：denoising diffusion, reconstruction error, self-supervised
- arXiv 串：`(all:"time series" AND all:"anomaly detection" AND all:"diffusion") AND cat:cs.LG`

### 5.3 检索执行（工具任选/组合）
- **MCP 直连**：arxiv-mcp-server / paper-search-mcp，agent 直接搜 arXiv/PubMed/bioRxiv。
- **自治 skill**：claude-obsidian `autoresearch` 或 obsidian-wiki `wiki-research`，搜完直接结构化入库。
- **元数据增强**：paper-qa 自动抓引用数 + 撤稿检查，给论文打优先级。
- **滚雪球**：对种子论文追引用/被引各 1 跳，补全 related work。

### 5.4 产出
- `search/<项目名>.md`：关键词 + 查询串 + 命中清单（标题/作者/年份/链接/优先级）。
- 选中的论文 PDF/链接落 `raw/`，交给 IngestAgent 转 Markdown 入 `sources/`。
- 验收：给一段方向描述 → 自动产出 ≥15 篇候选 + 一份带优先级的命中清单。

---

## 6. Multi-agent 编排（降低上下文）

**核心思想**：主负责人不亲自读论文、不跑实验，只看 `index.md` 和任务清单（上下文极短），
把每个重活拆成独立子任务，派给一个**全新、短上下文**的子 agent；子 agent 干完只回传**压缩结论**，不把原文塞回主线程。

### 6.1 角色分工
| Agent | 职责 | 只加载 | 回传 |
|---|---|---|---|
| **Orchestrator(主负责人)** | 规划、派活、汇总、决定下一步 | index.md + 任务清单 | — |
| SearchAgent | 关键词→检索→命中清单 | 项目描述 | search/*.md |
| IngestAgent | raw→Markdown 摘要+链接 | 单篇论文 | sources/*.md |
| DistillAgent | 凝练科学问题+重要性 | 若干 sources | questions/*.md |
| MethodAgent | 生成 idea/方法 | question + 相关 sources | ideas/*.md |
| ValidationAgent | 假设+toy实验+可证伪 | 单个 idea | experiments/*.md + 代码 |
| ArchiveAgent | 对话凝练去重归档 | 当前对话片段 | archive/*.md |
| LintAgent | 去重、修链接、合并概念 | 受影响的几页 | 变更摘要 |

### 6.2 为什么能降上下文
- **主 agent 不持有原文**：它只读"索引 + 各子 agent 回传的几行摘要"，永远不把整篇论文/整段实验日志load 进自己的窗口。
- **子 agent 即用即弃**：每个子任务开一个新 agent，只喂它需要的那 1–3 个文件，干完即销毁，上下文不累积。
- **磁盘做共享内存**：agent 之间通过 vault 里的 Markdown 文件交接，而不是把内容互相复述。
- **并行**：互不依赖的子任务（如同时 ingest 10 篇论文）并行跑，主线程只等汇总。

### 6.3 落地方式
- **Claude Code / Agent SDK**：用 subagent（Task 工具）派发；主会话写一份 `ORCHESTRATOR.md` 作为派活规则。
- **claude-obsidian 已内置多 agent**：`agents/` 下有 verifier / wiki-ingest / wiki-lint 等子 agent，并支持批量并行 ingestion——直接复用。
- **每个 §9 的自建 skill = 一个子 agent 的工作说明书**：skill 文件即子 agent 的 system prompt。

### 6.4 Orchestrator 工作循环（伪流程）
```
读 index.md + 任务清单
while 有待办:
    选一个任务 → 派给对应子 agent（只给它必要文件）
    收子 agent 的压缩回传 → 更新 index.md / 任务清单
    不把原文留在自己上下文里
汇报阶段结论 + 决定下一轮
```

---

## 7. 分阶段实施计划

### 阶段 0 · 环境准备（0.5 天）
- 安装 Obsidian，新建 vault 指向 `ScholarWeave/vault/`。
- 安装 Claude Code / Cursor；接入 arxiv-mcp-server / paper-search-mcp / basic-memory。
- `pip install markitdown[all] paper-qa aim`。
- 主编排选 **claude-obsidian**，写 `ORCHESTRATOR.md` 派活规则。

### 阶段 1 · ⓪ 论文搜索环（1 天）
- 填项目描述模板 → SearchAgent 产出关键词 + 命中清单（§5）。
- 验收：一段方向 → ≥15 篇候选 + 优先级清单，选中的落 `raw/`。

### 阶段 2 · 采集→转换→入库（1 天）
- IngestAgent：raw → MarkItDown → `sources/` 摘要 + 双向链接 + 更新 index。
- 验收：1 篇论文 PDF 自动产出结构化摘要并双链。

### 阶段 3 · ① 凝练科学问题（1 天）
- DistillAgent + Co-STORM/gpt-researcher：输出 `questions/`，含 问题陈述/为什么重要/现有不足/可证伪预期。
- 验收：从一批 sources 凝练出 1 个带"重要性+意义"的科学问题页。

### 阶段 4 · ②③ 构建方法 + 验证设计（2 天）
- MethodAgent → `ideas/`；ValidationAgent → `experiments/`（假设/toy实验/可证伪条件/指标）。
- 用 AI-Scientist 范式把 toy 实验跑起来（见 §8）。

### 阶段 5 · ④ 迭代结果回流（1 天）
- Aim 记录每次 run；`log-iteration` 把结论回写 `experiments/` 与 `synthesis/`。
- 验收：跑 3 变体 → Aim 对比 → 结论回写，触发下一轮。

### 阶段 6 · ④ 对话归档旁路（0.5 天）
- ArchiveAgent + basic-memory：对话结论凝练去重 → `archive/`。

### 阶段 7 · 固化与迭代（持续）
- 高频流程沉淀成子 agent / skill；定期 LintAgent 去重修链接。

---

## 8. 验证设计专题：AI-Scientist + Aim 怎么做"可证伪"

### 8.1 用 AI-Scientist 的范式做可证伪验证
借用它"生成假设 → 写实验 → 跑 → 分析 → 结论"的循环，重点是强制每个 idea 配一个**可执行最小验证**：
1. 把方法表述成**可证伪假设**：H1 = "条件 X 下，方法 A 的指标 M 显著优于 baseline B"。
2. 写 **toy 实验**（小数据/小模型/短训练），目标是**最快能证伪**而非刷 SOTA。
3. 预先写死**证伪条件**：如"M 提升 < 2% 或 seed 间方差 > 均值差，则 H1 被推翻"。
4. 让 ValidationAgent 生成脚本并执行，产出结构化结论。

### 8.2 用 Aim 承载 toy 实验与迭代
```python
from aim import Run
run = Run(experiment="H1_methodA_vs_baseline")
run["hparams"] = {"lr": 3e-4, "seed": 0, "variant": "A"}
for step, m in enumerate(metrics):
    run.track(m, name="metric_M", step=step)
run.track(int(passed_falsification), name="falsified")   # 证伪条件作为标量
```
- 每个变体/seed 一个 run，打 tag（假设编号、是否证伪）。
- Aim UI 多 run 叠加，一眼看"提升是否稳健、方差是否过大"。

### 8.3 闭环回写
跑完 → `log-iteration` 读 Aim 结论 → 更新 `experiments/H1.md`：支持/推翻、关键数字、下一步改的变量。
推翻→在 `ideas/` 派生新假设进入下一轮；支持→把证据链接进 `synthesis/` 推进 proposal。

> 一句话：**AI-Scientist 给"怎么设计可证伪验证"的范式，Aim 给"怎么记录对比迭代结果"的工具，子 agent 负责把结论回流知识库。**

---

## 9. 需要自建的 Skills（= 子 agent 工作说明书）

| Skill / 子 agent | 作用 | 对应需求 |
|---|---|---|
| `search-papers` | 描述→关键词→检索→命中清单 | ⓪搜索环 |
| `ingest` | raw → Markdown 摘要 + 链接 | 入库 |
| `distill-question` | 凝练科学问题 + 重要性/意义 | 需求② |
| `design-validation` | 假设 + toy 实验 + 可证伪条件 | 需求① |
| `log-iteration` | Aim 结论回写 experiments/synthesis | 需求③ |
| `consolidate-chat` | 协作问答凝练去重归档 | 需求④ |
| `lint` | 去重、修链接、合并概念 | 维护 |
| `orchestrate` | 主负责人派活规则（不干活，只调度） | multi-agent |

---

## 10. 里程碑清单

- [ ] 阶段0：环境就绪，主编排 claude-obsidian + 搜索/归档 MCP 接通
- [ ] 阶段1：一段方向描述 → ≥15 篇候选 + 优先级命中清单
- [ ] 阶段2：1 篇论文自动入库并双向链接
- [ ] 阶段3：凝练出首个带"重要性+意义"的科学问题
- [ ] 阶段4：首个方法配齐"假设 + toy 实验 + 可证伪条件"
- [ ] 阶段5：3 变体经 Aim 对比，结论回写 synthesis
- [ ] 阶段6：basic-memory 接通，对话结论自动归档
- [ ] 阶段7：Orchestrator + ≥5 子 agent 跑通一次完整闭环

---

## 11. 风险与注意

- **许可证**：second-brain 无 LICENSE；basic-memory 为 AGPL-3.0；商用前复核。
- **过度自动化**：AI-Scientist 全自动质量参差，"假设与证伪条件"必须人审。
- **多 agent 协调成本**：子 agent 太碎会增加交接开销，先粗后细。
- **知识库膨胀**：定期 lint 去重，否则链接网噪声化。
- **隐私**：全流程本地优先，云端模型只传必要文本。

---

## 12. 下一步建议

1. 先把 basic-memory / storm / aim 也 clone 进 `repos/`，并接通搜索 + 归档 MCP。
2. 跑通阶段 1+2："一段描述 → 检索 → 1 篇论文自动入库"作为最小闭环。
3. 写好 `ORCHESTRATOR.md` 与 `search-papers` / `ingest` 两个子 agent，再逐步接 ①②③④。
