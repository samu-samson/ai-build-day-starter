## What this changes

-

## Readiness checklist

- [ ] Stays inside my role's folders (or I'm the captain / flagged it)
- [ ] Contract at `contract/openapi.yaml` still matches the running `/openapi.json`
- [ ] New/changed endpoints: auth + scope enforced, errors use `{code, detail, action}`
- [ ] Personal-data reads require `X-Purpose`; calls land in the access log
- [ ] Writes honor `Idempotency-Key` (+ `X-Human-Confirmed` where it acts for a person)
- [ ] Responses carry `"synthetic": true`; no realistic personal identifiers
- [ ] Tests pass; checker score noted in `TASKS.md`
