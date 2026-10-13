# Service conventions — the contract of the day

Your service passes the event if a stranger (or the checker) can do everything below against `http://localhost:8000` with nothing but this document and your `/openapi.json`.

## 1 · Discovery

| Endpoint | Rule |
|---|---|
| `GET /healthz` | 200 `{"ok": true, "synthetic": true}` — no auth |
| `GET /openapi.json` | Your live OpenAPI 3.x contract — no auth; must match `contract/openapi.yaml` |

Operation IDs are camelCase verbs (`verifyRecord`, `getRecord`, `listRecords`, `fileRequest`). Every operation has a one-line `summary` and a `description` that says when to use it — an AI agent will read these someday.

## 2 · Caller identity

Every other endpoint requires both headers:

```
X-Client-Id: INTERNAL-APP          # or PARTNER-AGENCY, TEAM-TEST…
X-Api-Key:   <that client's key>
```

Dev clients (commit these; they are sandbox values):

| X-Client-Id | Key | Scope |
|---|---|---|
| `INTERNAL-APP` | `int-dev-key` | `full` |
| `PARTNER-AGENCY` | `partner-dev-key` | `verify` |

Missing/unknown identity → **401** `UNAUTHENTICATED`. Valid identity, insufficient scope → **403** `ACCESS_DENIED` (and the attempt is logged). Both carry an `action`.

## 3 · Minimal disclosure (`verify`) vs full record (`detail`)

- `GET /records/{id}/verify` — any authenticated client. Returns at most: `found/valid`, a display name, a status, a validity date. **Never** contact details or free text.
- `GET /records/{id}` — `full` scope only, and requires `X-Purpose: <why>` (≥ 5 chars, e.g. `Renewal case SBX-CASE-0012`). Missing → **400** `PURPOSE_REQUIRED`. The purpose is stored in the access log.

## 4 · Errors

Every error body, every time:

```json
{"code": "ACCESS_DENIED", "detail": "PARTNER-AGENCY may not read full records.", "action": "request_access — call GET /records/{id}/verify instead, or ask the data owner for a grant."}
```

Stable UPPER_SNAKE `code`; `action` is one of `fix_input · request_access · retry_later · ask_human` plus a human sentence. No stack traces.

## 5 · Access log

Append per call: `ts, clientId, method, path, subjectId, purpose, status`. Expose `GET /access-log?subject=SBX-…` (full scope). This powers the "who looked at my record, and why" screen — the one leaders remember.

## 6 · Safe writes

- Every `POST/PUT/PATCH/DELETE` requires `Idempotency-Key`; replaying a key returns the **same** result and creates nothing new.
- A write that acts on a person's behalf (file leave, submit request, send letter) additionally requires `X-Human-Confirmed: true`. Without it → **428** `CONFIRMATION_REQUIRED` with a `summary` object the UI shows to the officer for confirmation.

## 7 · Synthetic data

`"synthetic": true` in every response body. IDs start `SBX-`. Use `data/` and `documents/`; never fabricate realistic PhilSys/TIN/GSIS numbers or real officials' names.

## 8 · Dev ergonomics

Permissive CORS (all origins/headers) so `checker/checker.html` and `consumer/` pages work from `file://`. Port 8000 by default (document it in your README if different).

## Status flow for document intake (if you build S1)

`UPLOADED → EXTRACTED → REVIEWED → ACCEPTED` — extraction output carries per-field provenance `{value, page, anchor, confidence}`; only a human moves a record to ACCEPTED; only ACCEPTED records answer `verify` with `complete: true`.

---
*Why these rules: they rehearse what the E-Governance Act's interoperability framework will expect agency systems to do — documented APIs, data-owner-controlled access, purpose-bound personal-data sharing, and traceability of access. Build them in now and the future exchange is a config change, not a rewrite.*
