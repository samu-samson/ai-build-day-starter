# How this team works today

Pick one mode at kickoff and write it in the `TASKS.md` header.

## ONE-LAPTOP mode

- Roles rotate every 45–60 min: **driver** (keyboard+Bob) · **navigator** (contract + conventions open, steers) · **reviewer** (reads every diff before commit) · **tester** (runs service + checker).
- Git: commit to `main` after each completed task; push at least hourly (backup). No branches, no PRs.
- Plan together in one Plan-mode session → `plans/00-team-plan.md`; skip role plans.

## MULTI-LAPTOP mode

- Folder ownership (from `TASKS.md`): backend / documents+data / consumer / tests+docs. Your Bob only edits your folders.
- Shared files — `contract/openapi.yaml`, dependency manifests (requirements.txt, composer.json, package.json), route registration, `AGENTS.md` — belong to the **merge captain**. Everyone else proposes via PR comment or `docs/DECISIONS.md`.
- Git: branch `role/<name>` → small PR → captain merges. Everyone pulls at the hourly stand-up.
- Hourly stand-up (5 min, at :00): captain merges open PRs → all pull → tester runs checker on main → update TASKS.md checkboxes + score → unblock handoffs.
- Plans: kickoff team plan together on one screen; then each role writes `plans/<role>-plan.md` on their own laptop; captain scans all plans for file overlaps **before** anyone implements.

## Both modes

- Contract changes after the morning freeze: captain edits, notes it in `docs/DECISIONS.md`, announces; affected roles re-plan before re-coding.
- Don't fight Bob mid-merge: pull first, keep PRs under ~200 lines, merge hourly.
- The demo is the deliverable: anything not on the minimum demo path waits.
