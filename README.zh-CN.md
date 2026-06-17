<div align="center">

# ScholarWeave

**本地、私有、AI 驱动的科研知识库。**
把论文、idea、验证实验和 AI 对话，编织进一个你自己拥有的、互相链接的知识库。

[English](./README.md) · **中文**

![license](https://img.shields.io/badge/license-MIT-blue)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![status](https://img.shields.io/badge/status-research%20preview-orange)
![built on](https://img.shields.io/badge/built%20on-MarkItDown%20·%20arXiv%20·%20Aim%20·%20Obsidian-555)

</div>

---

## 为什么做它

大多数"AI 第二大脑"工具止步于记笔记。科研需要更多：从一个问题出发、检索文献、和 AI 一起共建
idea、**设计可证伪的验证实验**、对结果迭代，而且不希望几十轮 AI 问答聊完就蒸发。

ScholarWeave 是**对现有顶级工具的一层薄胶水**——不重复造轮子。它给你一套有章法的目录、
一个小 CLI，以及一组 AI 子 agent "skills"，把上面这套流程变成可复用、可归档的工作流。

- **本地纯 Markdown**——数据是你的；AI 是图书管理员，不是数据库。
- **搜索 → 凝练 → 构建 → 验证 → 迭代**——一个闭环，而不是单向收件箱。
- **每篇论文一个文件夹**——笔记 + 原文 + 元数据 + 图表自成一体。
- **多 agent、短上下文**——主负责人只派活，重活交给即用即弃的子 agent。
- **对话即资产**——AI 问答被凝练归档，而不是丢失。

## 架构

```
                    Orchestrator 主负责人（只派活，持有 index.md + 任务清单）
                         │ 分派给短上下文子 agent ▼
  关键词/描述 ─▶ ⓪ 搜索 ─▶ 00-inbox ─▶ MarkItDown ─▶ Obsidian Vault
                                          → Markdown    10-literature（每篇论文一个文件夹）
                                                        20..90 实体/概念/...
   研究闭环：  ① 凝练问题 ─▶ ② 构建 idea ─▶ ③ 设计验证 ─▶ ④ 迭代结果 ─┐
                   ▲                       (toy 实验 / 可证伪, Aim)      │
                   └──────────── 下一轮 · 回写 vault ─────────────────────┘
   归档旁路：  AI 问答 ─▶ 凝练/去重 ─▶ basic-memory(MCP→MD) ─▶ vault
```

## 快速开始

```bash
# 1. 安装（核心几乎零依赖；集成是可选 extras）
pip install -e .                 # 或：pip install -e '.[all]'  装 arXiv + MarkItDown + Aim

# 2. 生成 vault/config/code/outputs 目录骨架
scholarweave init .

# 3. 搜 arXiv，生成带优先级的命中清单（需要：pip install '.[search]'）
scholarweave search "diffusion model few-shot anomaly detection" --project anomaly -n 25

# 4. 把一篇论文转 Markdown 并入库到独立文件夹（需要：pip install '.[ingest]'）
scholarweave ingest paper.pdf --title "Attention Is All You Need" --authors "Vaswani, A" --year 2017

# 5. 生成一个可证伪的验证实验（代码 + vault，已接好 Aim）
scholarweave new-experiment "recon vs baseline"

# 6. 快速统计
scholarweave status
```

然后用 **Obsidian** 打开 `vault/` 浏览关系图，并让你的 AI agent（Claude Code / Cursor）
读 `ORCHESTRATOR.md` + `config/skills/` 来驱动整个闭环。

## 项目结构

```
ScholarWeave/
├── WORK_PLAN.md          # 完整计划（架构、阶段、验证方法）
├── ORCHESTRATOR.md       # 主负责人派活规则（多 agent、短上下文）
├── scholarweave/         # CLI 包（串联现有工具的胶水）
├── config/
│   ├── agents/  skills/  # 8 个子 agent skill（搜索/入库/凝练/验证/...）
│   └── templates/        # 论文/问题/idea/实验 笔记模板
├── vault/                # Obsidian 知识库（纯 Markdown）
│   ├── 00-inbox/         # 原始素材收件箱
│   ├── 10-literature/    # 每篇论文一个文件夹：note.md · meta.yaml · highlights.md · paper.pdf · assets/
│   ├── 20-entities 30-concepts 40-questions 50-ideas
│   ├── 60-experiments/   # 每个实验一个文件夹：design.md · results.md
│   ├── 70-synthesis 80-archive 90-search
│   └── index.md          # 主负责人读的总索引
├── code/                 # 实验代码，与 vault/60-experiments 一一对应
├── outputs/              # 导出的 proposal / 报告
└── repos/                # 你克隆的第三方工具（已 gitignore）
```

## 依托的现有工具

| 环节 | 工具 | 角色 |
|------|------|------|
| 搜索 | [arxiv](https://pypi.org/project/arxiv/) · [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) · [paper-search-mcp](https://github.com/openags/paper-search-mcp) | 找论文 |
| 转换 | [MarkItDown](https://github.com/microsoft/markitdown) | 任意文件 → Markdown |
| 存储/编排 | [Obsidian](https://obsidian.md) · [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | vault + LLM-wiki skills |
| 凝练/综述 | [STORM / Co-STORM](https://github.com/stanford-oval/storm) · [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | 科学问题 + related work |
| 文献问答 | [PaperQA2](https://github.com/Future-House/paper-qa) | 带引用回答、撤稿检查 |
| 验证/迭代 | [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) · [Aim](https://github.com/aimhubio/aim) | 可证伪 toy 实验 + 追踪 |
| 对话归档 | [basic-memory](https://github.com/basicmachines-co/basic-memory) | 对话 → Markdown 笔记 |

## 路线图

阶段计划与 AI-Scientist + Aim 的验证方法见 [`WORK_PLAN.md`](./WORK_PLAN.md)。
当前为 research preview，难免有粗糙之处。

## 许可证

本仓库自有代码为 MIT。第三方工具各自保留其许可证——注意 `basic-memory` 为 AGPL-3.0，
`second-brain` 未附许可证文件。
