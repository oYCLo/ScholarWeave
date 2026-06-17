<div align="center">

# ScholarWeave

**A local, private, AI-driven research knowledge base.**
Weave papers, ideas, validation experiments and AI conversations into one connected vault you own.

**English** · [中文](./README.zh-CN.md)

![license](https://img.shields.io/badge/license-MIT-blue)
![python](https://img.shields.io/badge/python-3.9%2B-blue)
![status](https://img.shields.io/badge/status-research%20preview-orange)
![built on](https://img.shields.io/badge/built%20on-MarkItDown%20·%20arXiv%20·%20Aim%20·%20Obsidian-555)

</div>

---

## Why

Most "AI second brain" tools stop at note-taking. Research needs more: you start from a
question, search the literature, co-build ideas with an AI, **design falsifiable validation
experiments**, iterate on results, and you don't want the dozens of AI Q&A turns to evaporate.

ScholarWeave is **thin glue over existing best-in-class tools** — it does *not* reinvent them.
It gives you a principled folder layout, a small CLI, and a set of AI sub-agent "skills" that
turn that workflow into something repeatable and archivable.

- **Local & plain Markdown** — your data is yours; AI is the librarian, not the database.
- **Search → distill → build → validate → iterate** — a closed research loop, not a one-way inbox.
- **Per-paper folders** — each paper is a self-contained folder (note + PDF + metadata + figures).
- **Multi-agent, short context** — a lead agent only dispatches; heavy work goes to fresh sub-agents.
- **Conversations are assets** — AI Q&A is distilled and archived, not lost.

## Architecture

```
                    Orchestrator (lead — only dispatches, holds index.md + task list)
                         │ delegates to short-context sub-agents ▼
  keywords/desc ─▶ ⓪ search ─▶ 00-inbox ─▶ MarkItDown ─▶ Obsidian Vault
                                              → Markdown    10-literature (one folder per paper)
                                                            20..90 entities/concepts/...
   research loop:  ① distill question ─▶ ② build idea ─▶ ③ design validation ─▶ ④ iterate ─┐
                        ▲                                  (toy exp / falsifiable, Aim)      │
                        └────────────── next round · write back to vault ───────────────────┘
   archive lane:   AI Q&A ─▶ consolidate/dedup ─▶ basic-memory (MCP→MD) ─▶ vault
```

## Quick start

```bash
# 1. install (core has almost no deps; integrations are optional extras)
pip install -e .                 # or: pip install -e '.[all]'  for arXiv + MarkItDown + Aim

# 2. scaffold the vault/config/code/outputs layout
scholarweave init .

# 3. search arXiv into a triaged hit-list  (needs: pip install '.[search]')
scholarweave search "diffusion model few-shot anomaly detection" --project anomaly -n 25

# 4. ingest a source into a per-paper folder  (needs: pip install '.[ingest]')
scholarweave ingest paper.pdf --title "Attention Is All You Need" --authors "Vaswani, A" --year 2017

# 5. scaffold a falsifiable validation experiment (code + vault, Aim-ready)
scholarweave new-experiment "recon vs baseline"

# 6. quick counts
scholarweave status
```

Then open the `vault/` folder in **Obsidian** to browse the graph, and point your AI agent
(Claude Code / Cursor) at `ORCHESTRATOR.md` + `config/skills/` to run the loop.

## Project structure

```
ScholarWeave/
├── WORK_PLAN.md          # full plan (architecture, stages, validation method)
├── ORCHESTRATOR.md       # lead-agent dispatch rules (multi-agent, short context)
├── scholarweave/         # the CLI package (glue over existing tools)
├── config/
│   ├── agents/  skills/  # 8 sub-agent skills (search / ingest / distill / validate / ...)
│   └── templates/        # paper / question / idea / experiment note templates
├── vault/                # Obsidian knowledge base (plain Markdown)
│   ├── 00-inbox/         # raw sources
│   ├── 10-literature/    # one folder per paper: note.md · meta.yaml · highlights.md · paper.pdf · assets/
│   ├── 20-entities 30-concepts 40-questions 50-ideas
│   ├── 60-experiments/   # one folder per experiment: design.md · results.md
│   ├── 70-synthesis 80-archive 90-search
│   └── index.md          # MOC the orchestrator reads
├── code/                 # experiment code, paired with vault/60-experiments
├── outputs/              # exported proposals / reports
└── repos/                # third-party tools you clone (gitignored)
```

## Tools it builds on

| Stage | Tool | Role |
|------|------|------|
| Search | [arxiv](https://pypi.org/project/arxiv/) · [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) · [paper-search-mcp](https://github.com/openags/paper-search-mcp) | find papers |
| Convert | [MarkItDown](https://github.com/microsoft/markitdown) | any file → Markdown |
| Store / orchestrate | [Obsidian](https://obsidian.md) · [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | vault + LLM-wiki skills |
| Distill / survey | [STORM / Co-STORM](https://github.com/stanford-oval/storm) · [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | question + related work |
| Lit Q&A | [PaperQA2](https://github.com/Future-House/paper-qa) | cited answers, retraction check |
| Validate / iterate | [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) · [Aim](https://github.com/aimhubio/aim) | falsifiable toy experiments + tracking |
| Archive chats | [basic-memory](https://github.com/basicmachines-co/basic-memory) | conversation → Markdown notes |

## Roadmap

See [`WORK_PLAN.md`](./WORK_PLAN.md) for the staged plan and the AI-Scientist + Aim
validation method. This is a research preview; expect rough edges.

## License

MIT (this repo's own code). Third-party tools keep their own licenses — note `basic-memory`
is AGPL-3.0 and `second-brain` ships without a license file.
