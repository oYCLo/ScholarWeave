# ScholarWeave

A personal **research knowledge-base hub** for an AI researcher working on single-cell
trajectory inference. It vendors three mature, community-built Claude Code skill repos and
wires them into one coherent workflow: **read papers → grow an Obsidian knowledge base →
ideate → write & review**.

ScholarWeave doesn't reinvent anything — it pins, installs, and *documents* existing tools
so the whole stack is reproducible from this one directory.

> **已安装全套**（含 claude-scholar）。日常怎么用看 **[docs/USAGE.md](docs/USAGE.md)**。
> 安装带来的全局变化（全局 `CLAUDE.md`、新增 hooks）见 USAGE §8。

---

## The stack (4 layers)

```
                 ┌─────────────────────────────────────────────────────────┐
  WRITE / REVIEW │  ARS plugin (already loaded)  +  claude-scholar (opt-in)  │
                 │  /ars-* pipeline, nature-* writing, kb-* commands, rebuttal│
                 └─────────────────────────────────────────────────────────┘
                 ┌─────────────────────────────────────────────────────────┐
  IDEATE         │  first-principles-ideation committee (already in ~/.claude)│
                 └─────────────────────────────────────────────────────────┘
                 ┌─────────────────────────────────────────────────────────┐
  INGEST         │  dailypaper-skills   (HF/arXiv daily → scored → notes)    │
                 └─────────────────────────────────────────────────────────┘
                 ┌─────────────────────────────────────────────────────────┐
  SUBSTRATE      │  obsidian-skills (kepano)   markdown · bases · canvas · cli│
                 └─────────────────────────────────────────────────────────┘
                        ▼ all of the above read/write your Obsidian vault ▼
                              /Users/ycl/Workspace/dailypaper/omo
```

### 1. `obsidian-skills` (kepano) — the substrate *(NEW, installed by this repo)*
Teaches the agent to manipulate an Obsidian vault using its open formats — so every note,
index, and diagram the higher layers produce is *correct* Obsidian, not generic markdown.

| skill | what it gives you |
|---|---|
| `obsidian-markdown` | Wikilinks `[[ ]]`, embeds, callouts, YAML properties — proper OFM |
| `obsidian-bases`    | Database-style **Bases** views/filters/formulas over your notes |
| `json-canvas`       | Build **Canvas** mind-maps / concept graphs programmatically |
| `obsidian-cli`      | Drive the vault from the CLI; plugin & theme dev |
| `defuddle`          | Strip a web page to clean markdown (low-token capture) |

### 2. `dailypaper-skills` (huangkiki) — the ingestion pipeline *(already installed, tuned to your field)*
Your daily reading funnel. Already configured with your keywords (trajectory inference,
flow matching, neural ODE, Schrödinger bridge, score/action matching…) and arXiv
categories (`q-bio.QM`, `q-bio.CB`, `cs.LG`, `stat.ML`, `cond-mat.stat-mech`).

| skill | what it does |
|---|---|
| `daily-papers` / `daily-papers-fetch` / `daily-papers-review` | Pull HF Daily + arXiv, score against your keywords, bucket into must-read / worth-reading / skip |
| `paper-reader` | Turn an arXiv link / local PDF into a structured Obsidian note (method, experiments, formulas, figures, limitations) |
| `daily-papers-notes` | Generate the per-paper note files |
| `generate-mocs` | Auto-build **Maps of Content** (directory + concept index pages) |

### 3. first-principles-ideation committee *(already in your ~/.claude)*
Your existing multi-agent committee (proposer / skeptic / methodologist / math-ledger /
experiment-designer / referee). Feeds on the knowledge base the layers above build.

### 4. `claude-scholar` (Galaxy-Dawn) — full research lifecycle *(opt-in, see below)*
A 47-skill superset covering ideation → coding → experiments → Nature-style writing →
self-review → rebuttal → post-acceptance, plus a `kb-*` command suite for KB hygiene.
**It overlaps your already-loaded ARS plugin** (both do write/review/rebuttal), so it's an
explicit opt-in rather than a default install.

---

## What you can now *do*

- **Every morning:** `今日论文推荐` → a scored, deduped digest of new single-cell /
  generative-dynamics papers, written straight into your vault as a dated note.
- **Deep-read a paper:** `读一下这篇论文 https://arxiv.org/abs/XXXX` → a full structured note
  with wikilinks to existing concepts; `更新索引` rebuilds the MoCs so it's discoverable.
- **Grow a real knowledge graph:** the kepano layer means concepts link with `[[ ]]`, a
  Canvas can map "OT ↔ Schrödinger bridge ↔ flow matching", and Bases can table every
  paper note by method/year/dataset.
- **Ideate against your own corpus:** point the first-principles committee at the vault to
  pressure-test a new idea before you build it.
- **(with `--with-scholar`) Draft & defend:** Nature-style writing skills, citation
  verification, anti-AI-writing polish, and a structured rebuttal workflow.

---

## Install

```bash
cd /Users/ycl/Workspace/ScholarWeave

# Layers 1 + 2 — safe, additive, reversible (symlinks only, no settings changes):
./install.sh

# Add the full claude-scholar suite (mutates ~/.claude/settings.json + adds global
# hooks; backup-aware, reversible via ./uninstall.sh --scholar):
./install.sh --with-scholar
```

The installer is **non-destructive**: any skill already present as a real directory (e.g.
your existing dailypaper install) is left untouched, and your
`~/.claude/skills/_shared/user-config.json` is never overwritten.

After installing, restart Claude Code (or `/reload`) so new skills register.

### Requirements
- Claude Code, Git, Bash.
- claude-scholar's installer additionally needs **Node.js** (its hooks are Node-based).
- Obsidian (you already have a vault). No Zotero needed — this is an Obsidian-only setup.

---

## Configure

Your live dailypaper config lives at `~/.claude/skills/_shared/user-config.json`.
A versioned copy is kept here at [`config/dailypaper-user-config.json`](config/dailypaper-user-config.json)
(used only to seed a fresh machine). To change what gets surfaced, edit `keywords` /
`negative_keywords` / `domain_boost_keywords` / `arxiv_categories` there.

`obsidian_vault` currently points at `/Users/ycl/Workspace/dailypaper/omo`.

---

## Update / Uninstall

```bash
./update.sh                 # pull latest upstream, re-pin versions.lock, re-link
./update.sh --with-scholar  # also re-run claude-scholar's installer

./uninstall.sh              # remove only the symlinks this repo created
./uninstall.sh --scholar    # also run claude-scholar's own uninstaller
```

---

## Layout

```
ScholarWeave/
├── README.md                         # this file
├── install.sh                        # idempotent, non-destructive installer
├── update.sh                         # pull upstream + re-pin + re-link
├── uninstall.sh                      # remove symlinks (+ optional scholar uninstall)
├── versions.lock                     # pinned upstream SHAs (reproducible)
├── config/
│   └── dailypaper-user-config.json   # versioned copy of your tuned dailypaper config
└── vendor/                           # managed cache of upstreams (gitignored)
    ├── obsidian-skills/              # kepano       (MIT)
    ├── dailypaper-skills/            # huangkiki
    └── claude-scholar/               # Galaxy-Dawn  (MIT)
```

`vendor/` is gitignored and rebuilt from `versions.lock` by `./install.sh`, so the repo
stays light while remaining fully reproducible.

## Overlap & precedence notes
- claude-scholar bundles its *own* `defuddle` and Obsidian KB skills. The installer installs
  kepano's `obsidian-bases`/`json-canvas`/`obsidian-cli`/`obsidian-markdown` (which scholar
  lacks) and skips any name already present, so nothing collides.
- claude-scholar's write/review/rebuttal skills duplicate the ARS plugin's `/ars-*` pipeline.
  Pick one per task; they don't conflict, but you'll see two ways to do the same thing.

## Credits / licenses
- [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) — MIT
- [huangkiki/dailypaper-skills](https://github.com/huangkiki/dailypaper-skills)
- [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) — MIT
