# TASKS

> **Fill this header at kickoff.** Every Bob session reads it first.

- Team: ___
- Agency: ___
- Service (one sentence): ___
- Mode: **ONE-LAPTOP** / **MULTI-LAPTOP**  ← delete one
- Merge captain (owns shared files): ___
- Roles: backend=___ · documents/data=___ · consumer=___ · tests/docs=___
  - 3 people: backend also takes tests; consumer also takes docs/demo
  - 2 people: A=backend+documents, B=consumer+data+tests+docs (consider ONE-LAPTOP)
- Latest checker score: ___ / ___  (update hourly)

## Minimum demo path — do these in order, nothing else until green

- [ ] M1 · Team plan merged (`plans/00-team-plan.md`); domain + record type chosen; `data/` CSVs adapted or regenerated — *all, 10:15*
- [ ] M2 · Contract drafted in `contract/openapi.yaml` (verify + detail + list + access-log + one write) — *backend (captain), 10:45*
- [ ] M3 · Service skeleton runs; `/healthz` + `/openapi.json` live — *backend, 11:15*
- [ ] M4 · Caller identity + scopes: internal full, partner verify-only; 401/403 with code+action — *backend, 12:00*
- [ ] M5 · Verify endpoint (minimal fields) + detail endpoint (requires `X-Purpose`) over synthetic data — *backend, 12:00*
- [ ] M6 · Access log appending + `GET /access-log?subject=` — *backend, 13:00*
- [ ] M7 · Consumer screen: lookup card + detail view w/ purpose prompt — *consumer, 13:30*
- [ ] M8 · Partner simulation in consumer: identity switch, clean refusal card, log entry visible — *consumer, 14:00*
- [ ] M9 · One safe write (Idempotency-Key + X-Human-Confirmed flow) wired to a confirm dialog — *backend+consumer, 14:30*
- [ ] M10 · Checker ≥ green on rules 1–9; fix reds — *tests, 15:00*
- [ ] M11 · README (how to run), `docs/DEMO.md` script, `docs/POC-ASK.md` drafted — *tests/docs, 15:30*
- [ ] M12 · Dry-run the 4-minute demo once — *all, 15:45*

## Stretch (only after M10)

- [ ] S1 · Document intake with Docling: upload → extracted fields with provenance → human review → ACCEPTED (see `.bob/rules/30-documents.md`) — *documents*
- [ ] S2 · Extraction accuracy vs `documents/answer_key.json` in `tests/extraction-results.md` — *documents/tests*
- [ ] S3 · Timeline / ageing view in consumer (who held it longest, overdue flags) — *consumer*
- [ ] S4 · Scripted failure demo (unknown ID, replayed Idempotency-Key) in the demo script — *tests*
- [ ] S5 · Second record type or a search endpoint — *backend*

## Handoffs (write the time when done)

| What | From → To | Agreed shape | Done at |
|---|---|---|---|
| Contract frozen for the morning | backend → all | `contract/openapi.yaml` on main | |
| Extraction function | documents → backend | `extract(file) -> {fields:[{name,value,page,anchor,confidence}]}` | |
| Test data final | data → tests | `data/*.csv` on main | |

## Parking lot / blocked

- …
