---
name: orchestrate
description: >
  Lead/orchestrator agent for ScholarWeave. Plans the research workflow and
  dispatches work to short-context sub-agents instead of doing it directly, to
  keep context small. Triggers on "/orchestrate", "plan the next step",
  "run the research loop", "what should we do next".
allowed-tools: Read Glob Grep Task
---

# orchestrate

Follow `ORCHESTRATOR.md` at the repo root. You hold only `vault/index.md` and a
task list. For each task, spawn the matching sub-agent (see the table in
ORCHESTRATOR.md) with the minimum files it needs, collect its compressed result,
update `index.md`, and move on. Never load full papers or logs yourself.

Decision order each round:
1. Any inbox items not ingested? -> Ingest agents (parallel).
2. Enough sources but no question? -> Distill agent.
3. Question but no idea? -> Method agent.
4. Idea but no validation? -> Validation agent.
5. Experiment finished? -> Iterate agent (write back), then decide next hypothesis.
6. Long chat with reusable conclusions? -> Archive agent.
7. Periodically -> Lint agent.
