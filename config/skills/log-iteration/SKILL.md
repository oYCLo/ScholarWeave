---
name: log-iteration
description: >
  Read Aim experiment results, decide if the hypothesis is supported or rejected,
  and write the conclusion back into the experiment + synthesis. Triggers on
  "/log-iteration", "记录迭代结果", "log the experiment results", "what did the runs show".
allowed-tools: Read Write Edit Glob Bash
---

# log-iteration

Input: Aim runs for one `EXP-*`. Output: updated `results.md` + maybe `70-synthesis/`.

Steps:
1. Read run metrics from Aim (`aim runs ls`, or the Aim UI / SDK). Pull only the
   summary numbers, not full logs.
2. Fill the results table in `vault/60-experiments/<EXP>/results.md`.
3. Apply the falsification rule from `config.yaml`:
   - supported -> link evidence into `vault/70-synthesis/` (toward a proposal).
   - rejected  -> derive the next hypothesis in `vault/50-ideas/`, start a new round.
4. Record the single most informative "next variable to change".

Return verdict (support/reject) + key number to the orchestrator.
