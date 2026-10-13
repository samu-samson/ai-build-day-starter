# Readiness rules (enforced in code you write)

- Contract-first: `contract/openapi.yaml` is the source of truth; the running service must serve the same contract at `/openapi.json`. When asked to add an endpoint, update the contract in the same change — or flag the contract owner if that file is not yours.
- Identity: every endpoint (except `/healthz` and `/openapi.json`) authenticates `X-Client-Id` + `X-Api-Key`. Client identities and scopes live in one config structure (`clients` map), never scattered through handlers.
- Scopes: `full` (internal app) vs `verify` (partner). Deny by default; a denied call returns 403 `{"code":"ACCESS_DENIED","detail":...,"action":"Request access from the data owner, or call the verify endpoint instead."}` and is still logged.
- Purpose: endpoints returning personal data require `X-Purpose` (min 5 chars). Missing → 400 `PURPOSE_REQUIRED`. Store the purpose with the log entry.
- Verify endpoints disclose at most: found/valid flag, name/title, status, validity date. Never contact details, never free-text records.
- Errors: always `{"code","detail","action"}` with a stable UPPER_SNAKE code. Map: fix_input, request_access, retry_later, ask_human.
- Access log: append {ts, clientId, method, path, subjectId, purpose, status} per call; expose `GET /access-log?subject=`; internal scope only.
- Writes: require `Idempotency-Key`; replaying a key returns the original result with the same ID. Actions on a person's behalf (filing, submitting, sending) require `X-Human-Confirmed: true`, else 428 `CONFIRMATION_REQUIRED` with a summary the UI can show for confirmation.
- Synthetic only: `"synthetic": true` in every body; IDs prefixed `SBX-`; never generate realistic PhilSys/TIN/GSIS-format numbers, real names of officials, or real agency letterheads.
- Dev CORS: allow all origins/headers so `file://` tooling works. Note it as dev-only in README.
