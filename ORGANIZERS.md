# Organizer runbook (delete before sharing if you prefer)

## Before doors open

- [ ] Mark this repo as a **Template** (Settings → check "Template repository") so teams get "Use this template".
- [ ] Projector laptop: clone repo; run `reference/` once; open `checker/checker.html` → all green = demo-able.
- [ ] USB sticks (2–3): this repo zipped · Docling models (`docling-tools models download`, then copy `~/.cache/docling/models`) · offline wheels: `pip download fastapi "uvicorn[standard]" python-multipart docling docling-serve -d wheels/` on both Windows and mac if possible.
- [ ] Wi-Fi test: clone from GitHub + `pip install fastapi` from the venue network. If blocked → wheels USB is plan A.
- [ ] Print per-team card: repo URL, dev client IDs/keys (CONVENTIONS §2), "first green check by 11:00".

## Message to participants (send now)

> Before the build day: (1) bring a laptop you can install software on; (2) install Git + Python 3.10+ (or your stack) — https://python.org; (3) create a GitHub account and send us your username; (4) make sure IBM Bob is installed and signed in. We build everything locally — no cloud accounts needed. All data is synthetic.

## Run of show

09:30 kickoff: why interoperability (RA 12254 → agencies expose data "through a secure API"; once-only target ≈2028), the 9 rules, this kit, demo of reference+checker (5 min).
10:15 team plans merged → build. Mentors roam with `reference/` open.
11:00 every team: first green checks (1–4). Unstick anyone below 2 greens.
13:00 milestone M6 check-in on TASKS.md.
15:30 code freeze for demo dry-runs.
16:00 demos (4 min each): screen → refusal → access log → checker score.
Judging = checker JSON export + the demo. Collect each team's repo URL + `docs/POC-ASK.md`.

## Mentor cheat sheet

- Team stuck on CORS from `file://` → CONVENTIONS §8; FastAPI: `CORSMiddleware(allow_origins=["*"])`.
- Bob editing outside its lane → re-read `.bob/rules/20-workflow.md` prompt in docs/PROMPTS.md ("Unsticking Bob").
- Docling slow → OCR only `*_scanned`; `OMP_NUM_THREADS=4`; or drop S1, it's a stretch goal.
- Checker test 12/13 failing → they log after returning; log before refusing, store purpose with the entry.
- Team with no domain by 10:30 → hand them `data/registry.csv` and the "standing check" framing; rename fields later.
