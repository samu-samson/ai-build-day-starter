# AI Build Day — team starter kit

Build one internal service for your agency, expose it the way another agency would need it tomorrow, and consume it yourself — all on your own laptop, with IBM Bob as your builder. Everything here is open source and runs locally. **Synthetic data only.**

> You are not connecting to any other team today. You are proving your service is *ready* to be connected: documented, access-controlled, purpose-logged, and safe. That is what the E-Governance Act's interoperability push will ask of every agency system.

## Quickstart (team lead, ~10 minutes)

1. Click **Use this template → Create a new repository** (owner: your account or your agency's). Name it after your service, e.g. `coop-standing-service`.
2. Add your teammates as collaborators (Settings → Collaborators).
3. Everyone: `git clone` the repo and open the folder in **Bob**.
4. Read `AGENTS.md` (Bob already does), then open `TASKS.md` and fill in the header: team name, agency, one-laptop or multi-laptop, roles.
5. Follow `docs/SETUP.md` to install your runtime (and Docling if you process documents).
6. Plan first: Bob in **Plan** mode, together, into `plans/00-team-plan.md`. Then build.

## What you are building

Pick **one internal capability** of your agency — a registry, a request tracker, a records lookup, a document intake — and build:

| Piece | What it must do |
|---|---|
| **Service** (`backend/`) | Your API on `http://localhost:8000`, following `docs/CONVENTIONS.md` |
| **Consumer** (`consumer/`) | A screen your own office would use — upload, lookup, timeline, cards |
| **Partner simulation** | The same consumer switched to a partner identity: it may call `…/verify`, and gets a clean refusal (plus a log entry) for anything more |
| **Contract** (`contract/openapi.yaml`) | The single source of truth; served live at `/openapi.json` |

The **readiness checker** (`checker/checker.html` — open it in a browser) scores your running service against the rules all day. Judges use the same checker at 16:00.

## The readiness rules (the whole point)

1. Published contract at `/openapi.json`
2. Every call names the caller (`X-Client-Id` + `X-Api-Key`); no identity, no answer
3. Least access — a partner gets the verify endpoint, not the full record
4. Personal-data reads carry a stated purpose (`X-Purpose`) and it is recorded
5. A minimal-disclosure `…/verify` endpoint: yes/no plus a few fields
6. Errors carry a stable `code` and the next `action`, never a stack trace
7. An access log: who asked, for what, when, why — queryable per subject
8. Safe writes: `Idempotency-Key` on every write, `X-Human-Confirmed: true` before acting on someone's behalf
9. Synthetic data only, marked `"synthetic": true`

Full detail and header names: `docs/CONVENTIONS.md`.

## The day

| Time | Milestone |
|---|---|
| 09:30 | Kickoff — why interoperability, the rules, this kit |
| 10:15 | Team plan merged (`plans/00-team-plan.md`); domain picked; data generated |
| 12:00 | Contract live at `/openapi.json`; verify + detail endpoints up; caller identity enforced |
| 14:00 | Consumer screen working; access log visible; partner simulation refusing cleanly |
| 15:30 | Checker green (or honestly amber); README + `docs/DEMO.md` + `docs/POC-ASK.md` done |
| 16:00 | Demos — lead with the screen, then the refusal, then the access log |

## Repo map

```
AGENTS.md            Bob's onboarding — read it once yourself
.bob/rules/          Shared rules every teammate's Bob follows
plans/               Plan-mode output; team plan + one per role
contract/            openapi.yaml — change only via the contract owner
backend/  consumer/  Your code
data/                Synthetic CSVs + generator
documents/           Synthetic PDF pack + answer key (for document intake)
checker/             Readiness checker (open in browser)
reference/           A worked example service — for mentors; don't ship it as your entry
docs/                CONVENTIONS, SETUP, PROMPTS, DEMO, POC-ASK, DECISIONS, DATA
tests/               Your tests; checker results land here too
```

## Take-home

This repo **is** the take-home: a working service, its contract, its tests, a demo script, and a proof-of-concept ask (`docs/POC-ASK.md`) your agency can bring to its next ISSP update. Keep building after today.

---
*Not affiliated with DICT, eGovDX or eGovPH. This kit emulates good interagency practice with synthetic data for a one-day build event.*
