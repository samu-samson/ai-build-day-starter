# Document processing rules (Docling)

- All document processing runs locally. Never send document content to an external API. Docling (MIT) is the default engine; `docs/SETUP.md` has install + offline-model steps.
- Python backends: use `docling` as a library (`DocumentConverter`). Non-Python backends: call `docling-serve` on `http://127.0.0.1:5001` (`POST /v1/convert/file`) and treat it as an internal dependency, not part of your public contract.
- Default pipeline: convert to DoclingDocument/Markdown, then extract fields with deterministic rules (regex/anchors over text + tables). Do NOT use VLM/experimental extraction today — slow on CPU, nondeterministic.
- Keep provenance: every extracted field stores `{value, page, bbox or anchor text, confidence}`. The consumer shows the field next to where it came from.
- Extracted data is a DRAFT. Status flow: `UPLOADED → EXTRACTED → REVIEWED(by a human) → ACCEPTED`. Only ACCEPTED records count for verify endpoints.
- Uploads are writes: require `Idempotency-Key` (hash the file to detect re-uploads) and log the upload with purpose.
- Test against `documents/` and score with `documents/answer_key.json`; put accuracy in `tests/extraction-results.md`. Turn OCR on only for the `*_scanned` files; keep it off for digital PDFs (speed).
- Reject files over 10 MB and non-PDF/image types with `UNSUPPORTED_DOCUMENT` + action.
