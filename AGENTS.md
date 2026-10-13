# AGENTS.md — read me first

You are building at a one-day government AI build event. The team owns one agency service; several people may run their own Bob against this same repo at once. Your job: implement the team's plan **inside your owner's folder**, to the conventions below, without stepping on anyone else's lane.

## The project

One internal agency capability, exposed as if another agency will call it tomorrow:

- `backend/` — the service, on `http://localhost:8000`
- `consumer/` — the screen an officer uses (and a simulated partner identity that gets refused beyond `verify`)
- `contract/openapi.yaml` — the single source of truth for the API
- `data/`, `documents/` — synthetic inputs. **Never invent real-looking personal data; reuse these.**

## Non-negotiable service rules (details in docs/CONVENTIONS.md)

1. Serve the contract at `GET /openapi.json`; keep `contract/openapi.yaml` in sync with it.
2. Reject calls without `X-Client-Id` + valid `X-Api-Key` (401, code `UNAUTHENTICATED`).
3. Enforce scopes: partner identities reach only `…/verify`; refuse the rest with 403 `ACCESS_DENIED` + an `action`.
4. Personal-data endpoints require `X-Purpose`; store it in the access log.
5. Provide `…/{id}/verify` returning found/valid + at most 3–4 fields.
6. Every error body: `{"code": "...", "detail": "...", "action": "..."}` — stable code, human next step.
7. Append every call to an access log; expose `GET /access-log?subject=<id>`.
8. Writes: honor `Idempotency-Key` (same key → same result, no duplicate); state-changing actions on a person's behalf need `X-Human-Confirmed: true`, else 428 `CONFIRMATION_REQUIRED`.
9. Every response body includes `"synthetic": true`. IDs start with `SBX-`.
10. Enable permissive CORS in dev (the checker and consumer pages run from `file://`).

## How to work in this repo

- **Read `TASKS.md` first, every session.** The header says whether this team is ONE-LAPTOP or MULTI-LAPTOP and who owns what.
- **Stay in your lane.** Only modify files under the folder your task owns. Shared files (`contract/openapi.yaml`, dependency manifests, route registration, this file) belong to the merge captain — propose changes, don't make them.
- **Pull before you start; commit small; after each completed task:** multi-laptop → branch + PR; one-laptop → commit to `main` and push hourly.
- **Plan before building.** In Plan mode, write/update `plans/<your-role>-plan.md`; every step names the files it touches. Implement from a fresh Agent conversation referencing `@plans/` and `@contract/openapi.yaml`.
- **Log decisions** in `docs/DECISIONS.md` (one line each). Never resolve a cross-folder conflict silently.
- **Test before PR.** Run the project's tests and, when the service is up, the checker (`checker/checker.html`). Fix reds before adding features.
- **Documents:** process files with Docling **locally**; keep source page/position for each extracted field; extracted data is a draft until a human confirms it. See `.bob/rules/30-documents.md`.
- Default stack if the team has no preference: Python 3.10+, FastAPI, SQLite. Any stack is fine if the rules pass.

## Demo bias

Build so the demo leads with what's on screen: a card, a receipt, a timeline, a refusal, the access log. A terminal full of JSON is not a demo.
