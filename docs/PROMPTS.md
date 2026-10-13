# Prompt starters for Bob

Copy, fill the blanks, paste. Always start in **Plan mode** for anything bigger than one endpoint.

## Kickoff (Plan mode, whole team watching)

> Read AGENTS.md, TASKS.md, docs/CONVENTIONS.md and plans/00-team-plan.md. We are team ___ from ___. Our service wraps ___ with record type ___ (IDs `SBX-___-####`). Help us complete plans/00-team-plan.md: propose the record fields, which 3–4 fields the verify endpoint may disclose, which fields are personal (purpose-required), and the one safe write. Ask us the questions you need answered. Do not write code.

## Contract (backend/captain, Plan then Agent)

> From plans/00-team-plan.md, write contract/openapi.yaml for our service following docs/CONVENTIONS.md §1–7: /healthz, /records, /records/{id}, /records/{id}/verify, /access-log, and POST /___ as the safe write. camelCase operationIds, summaries, error schema {code, detail, action}, and the X-Client-Id / X-Api-Key / X-Purpose / Idempotency-Key / X-Human-Confirmed headers documented per operation. Only modify files under contract/.

## Backend (Agent mode)

> Implement contract/openapi.yaml as a FastAPI app under backend/, following .bob/rules/10-readiness.md exactly: clients map (INTERNAL-APP/full/int-dev-key, PARTNER-AGENCY/verify/partner-dev-key), 401/403/400/428 error shapes with stable codes, X-Purpose enforcement on personal endpoints, in-memory-or-SQLite access log with GET /access-log?subject=, Idempotency-Key store, permissive CORS, and "synthetic": true in every body. Load records from data/___.csv. Only modify files under backend/. Then show me how to run it on port 8000.

*(Laravel variant: "…as a Laravel 11 app under backend/ using routes/api.php + a middleware for identity/scope/purpose/logging; serve the contract file at /openapi.json…")*

## Document intake (documents owner, after M5)

> Following .bob/rules/30-documents.md, add document intake to our service: POST /documents (multipart, Idempotency-Key = file hash), Docling conversion (OCR only when filename contains "scanned"), rule-based extraction of the fields for the document type ___ from documents/ (see documents/answer_key.json for expected fields), per-field provenance {value, page, anchor, confidence}, status flow UPLOADED→EXTRACTED→REVIEWED→ACCEPTED with POST /documents/{id}/review requiring X-Human-Confirmed. Only modify files under backend/documents/ plus one route include [CAPTAIN].

## Consumer (consumer owner, Agent mode)

> Build consumer/app.html as a single self-contained page (no CDN, works from file://) against contract/openapi.yaml: a config bar (base URL + client identity switch INTERNAL-APP/PARTNER-AGENCY), a lookup box that renders a verify card, a detail view that prompts for X-Purpose, a refusal card for 403s showing code+action, an access-log table for a subject, and a confirm dialog for the write (sends X-Human-Confirmed). Lead with what's on screen: cards and timelines, not raw JSON. Only modify files under consumer/.

## Tests (tests owner)

> Write tests under tests/ that call the running service like the checker does: discovery, 401 without identity, 403 partner-on-detail, 400 missing purpose, verify field minimalism, 404 shape, idempotent write, 428 without confirmation, access-log contains purpose. Use pytest+httpx (or our stack's equivalent). Only modify files under tests/.

## Unsticking Bob

- "Re-read .bob/rules/10-readiness.md and check your last change against each rule; list violations, then fix them."
- "The checker fails test ___ with ___. Diagnose against docs/CONVENTIONS.md and fix only what that test needs."
- "Before coding: list the files you will touch. If any is outside my folders, stop and tell me."
