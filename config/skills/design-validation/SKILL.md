---
name: design-validation
description: >
  Turn an idea into a falsifiable hypothesis plus a minimal toy experiment that
  can be falsified fast, scaffolding code + Aim tracking. Borrows the AI-Scientist
  pattern. Triggers on "/design-validation", "设计验证", "how do we test this idea",
  "design a toy experiment".
allowed-tools: Read Write Edit Glob Bash
---

# design-validation

Input: one idea in `vault/50-ideas/`. Output: a paired experiment folder.

Steps:
1. Scaffold: `scholarweave new-experiment "<short name>"`
   -> `code/<EXP>/run.py` + `config.yaml`, `vault/60-experiments/<EXP>/design.md` + `results.md`.
2. In `design.md`, write the **falsifiable hypothesis H1** and the explicit
   **falsification condition** (e.g. "improvement < 2% OR seed-variance > mean-diff").
3. Implement the **minimal** toy experiment in `run.py` — goal is to falsify fast,
   not to beat SOTA. Track metrics + a `falsified_pass` scalar with Aim.
4. Hand the run command to the iterate agent.

Principle (AI-Scientist): every idea must ship with a runnable minimal validation.
Return the EXP id + the hypothesis to the orchestrator.
