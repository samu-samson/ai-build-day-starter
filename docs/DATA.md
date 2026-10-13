# Synthetic data — what's in the box

Everything is invented. IDs start `SBX-`; emails use `.example`; no real agencies, officials or ID-number formats. Adapt freely to your domain — or regenerate: `python data/generate_data.py`.

## data/

| File | Rows | What it models | Key field |
|---|---|---|---|
| `employees.csv` | 60 | staff with position, unit, status, hire date, VL/SL earned-used | `employeeNo` (SBX-####) |
| `registry.csv` | 20 | accredited/licensed entities with status + validity (the verify pattern) | `registryNo` (SBX-REG-####) |
| `document_log.csv` | 40 | routed documents with class (simple/complex/highly_technical), offices, dates | `controlNumber` (SBX-DOC-2026-####) |
| `assets.csv` | 50 | ICT equipment with accountable employee, cost, PAR/ICS custody | `propertyNo` (SBX-PROP-####) |

Useful built-in stories: 3 separated employees (verify → employed:false); registry rows in PROVISIONAL/SUSPENDED/EXPIRED; overdue documents vs their 3/7/20 working-day targets; assets split PAR (≥ ₱50k) vs ICS.

## documents/

~10 synthetic PDFs for document intake: leave applications, travel orders, purchase request, disbursement voucher, memo, COE request, ICT request, registry renewal. Files with `_scanned` are image-only (need OCR). `answer_key.json` maps each file to the fields a correct extraction should produce — score yourself into `tests/extraction-results.md`.

## Rules of use

- Don't add real personal data, even your own.
- Keep the `synthetic: true` marker on everything derived from these.
- Need different fields? Change the generator, not just the CSV, so teammates can regenerate.
