# Team workflow rules

- Start every session: `git pull`, read `TASKS.md` (mode header + your tasks), read `plans/00-team-plan.md`.
- ONE-LAPTOP mode: work top-to-bottom through TASKS.md; commit to `main` after each task; push at least hourly.
- MULTI-LAPTOP mode: work only in the folders your role owns; branch `role/<name>`; small PRs; the merge captain merges hourly. Never edit `contract/openapi.yaml`, dependency manifests, or route registration directly unless you are the captain — leave a PR comment or a line in `docs/DECISIONS.md` instead.
- Conflict etiquette: if a task needs a file outside your lane, stop and surface it (chat + DECISIONS.md), don't quietly edit.
- Commits: present-tense one-liners, prefix with area — `backend: add verify endpoint`, `consumer: refusal card`.
- Don't run `/init` to regenerate AGENTS.md; this repo already has one. If you believe it's wrong, propose the change to the captain.
- Keep secrets out: no tokens, no real URLs with credentials. API keys for the day are local dev values in config, fine to commit.
- Before any PR / end-of-task commit: run tests, start the service, open `checker/checker.html`, and record the score in TASKS.md.
