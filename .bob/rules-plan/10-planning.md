# Plan-mode rules

- Read first: `TASKS.md`, `contract/openapi.yaml`, `plans/00-team-plan.md`, `docs/CONVENTIONS.md`.
- Write plans only under `plans/`. Your file is `plans/<role>-plan.md` (backend, documents, consumer, tests) — or `00-team-plan.md` in the kickoff session only.
- Every step must name the exact files it will touch. Flag any step touching shared files (contract, dependency manifests, route registration) as `[CAPTAIN]`.
- No vague steps ("update appropriately", "handle errors properly"). Name the endpoint, the field, the error code.
- Plans are small: aim ≤ 12 steps, each ≤ 30 minutes, with the minimum demo path (contract → verify → detail+purpose → consumer card → refusal → access log) scheduled before any stretch item.
- End every plan with: files touched summary, handoffs needed (what from whom, by when), and risks.
- Do not start implementing in Plan mode. Hand off: new conversation, Agent mode, referencing `@plans/<role>-plan.md`.
