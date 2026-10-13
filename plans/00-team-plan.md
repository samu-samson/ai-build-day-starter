# Team plan — write this together at kickoff (Plan mode, one screen)

## The service
- Agency: ___
- Capability we are wrapping (one sentence): ___
- Record type + ID format: e.g. accreditation record, `SBX-ACC-####`
- The verify question a partner would ask: "Is ___ valid/complete/eligible?"
- Fields the verify endpoint may disclose (max 4): ___
- Fields that are personal/sensitive (detail endpoint, purpose required): ___
- The one safe write: e.g. file a renewal request / register a document
- Document intake in scope today? yes/no — if yes, which document from `documents/`?

## Stack
- Backend: ___ (default FastAPI + SQLite) · Consumer: ___ (default single HTML page)

## Architecture in five lines
1. ___
2. ___

## Contract decisions (captain implements in `contract/openapi.yaml`)
- Paths: `/records`, `/records/{id}`, `/records/{id}/verify`, `/access-log`, `POST /___`
- Client IDs + scopes: `INTERNAL-APP` (full), `PARTNER-AGENCY` (verify)

## Who owns what (copy into TASKS.md header)
- backend=___ documents/data=___ consumer=___ tests/docs=___ · captain=___

## Risks + fallbacks
- e.g. Docling models not downloaded → fallback: digital PDFs only / skip S1
