"""Scaffold a validation experiment (stages 4-5).

Creates paired folders:
  code/<exp-id>/            run.py (Aim boilerplate) + config.yaml
  vault/60-experiments/<exp-id>/  design.md + results.md
so the falsifiable hypothesis lives next to the runnable toy experiment.
"""
from __future__ import annotations

import re
from pathlib import Path

from .util import repo_root, slugify, write_if_absent

RUN_PY = '''"""Toy experiment for {exp_id}. Tracks runs with Aim (optional)."""
import argparse


def get_run(experiment):
    try:
        from aim import Run
        return Run(experiment=experiment)
    except Exception:
        class _Noop:
            def __setitem__(self, k, v): pass
            def track(self, *a, **k): pass
        print("[aim not installed -> no tracking]  pip install 'scholarweave[track]'")
        return _Noop()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="A")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--lr", type=float, default=3e-4)
    args = ap.parse_args()

    run = get_run("{exp_id}")
    run["hparams"] = {{"variant": args.variant, "seed": args.seed, "lr": args.lr}}

    # TODO: implement the toy experiment. Keep it minimal — aim to FALSIFY fast.
    metric_M = 0.0
    for step in range(10):
        metric_M = step * 0.01  # placeholder
        run.track(metric_M, name="metric_M", step=step)

    # Falsification check (edit the condition for your hypothesis H1)
    baseline = 0.05
    passed = (metric_M - baseline) >= 0.02
    run.track(int(passed), name="falsified_pass")
    print(f"metric_M={{metric_M:.4f}}  passes_H1={{passed}}")


if __name__ == "__main__":
    main()
'''

CONFIG_YAML = """exp_id: {exp_id}
hypothesis: H1
description: ""
baseline: 0.05
falsification_rule: "metric_M improvement < 0.02 OR seed-variance > mean-diff -> H1 rejected"
variants: [A, B]
seeds: [0, 1, 2]
"""

DESIGN_MD = """---
exp_id: {exp_id}
status: designed   # designed / running / done
linked_idea: [[ ]]
linked_question: [[ ]]
---

# {exp_id} — Validation design

## Hypothesis (H1, falsifiable)
> In condition X, method A's metric M is significantly better than baseline B.

## Toy experiment (minimal, fast-to-falsify)
- data:
- model:
- compute budget:

## Falsification condition
- H1 is REJECTED if: metric_M improvement < 2% OR seed-variance > mean-diff.

## Metrics
- primary: metric_M
- guardrails:

## Code
- `code/{exp_id}/run.py`  ·  track with Aim
"""

RESULTS_MD = """# {exp_id} — Results & iteration

| run | variant | seed | metric_M | passes_H1 | note |
|-----|---------|------|----------|-----------|------|
|     |         |      |          |           |      |

## Verdict
- [ ] supports H1  → link evidence into [[70-synthesis]]
- [ ] rejects H1   → derive next hypothesis in [[50-ideas]]

## Next variable to change
-
"""


def run(name: str, root: Path | None = None) -> tuple[Path, Path]:
    root = root or repo_root()
    slug = slugify(name, max_words=4)
    # next numeric id
    exp_root = root / "vault" / "60-experiments"
    existing = [p.name for p in exp_root.glob("EXP-*")] if exp_root.exists() else []
    nums = [int(m.group(1)) for n in existing if (m := re.match(r"EXP-(\d+)", n))]
    nid = (max(nums) + 1) if nums else 1
    exp_id = f"EXP-{nid:03d}-{slug}"

    code_dir = root / "code" / exp_id
    vault_dir = exp_root / exp_id
    write_if_absent(code_dir / "run.py", RUN_PY.format(exp_id=exp_id))
    write_if_absent(code_dir / "config.yaml", CONFIG_YAML.format(exp_id=exp_id))
    write_if_absent(vault_dir / "design.md", DESIGN_MD.format(exp_id=exp_id))
    write_if_absent(vault_dir / "results.md", RESULTS_MD.format(exp_id=exp_id))
    return code_dir, vault_dir
