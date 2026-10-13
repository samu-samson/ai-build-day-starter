# Setup — one laptop per builder (or per team)

Everything below is free and open source and runs offline once installed. Do installs **before 10:00**; venue Wi-Fi is the bottleneck.

## 1 · Core (everyone)

- Git + a GitHub account (test: clone this repo)
- IBM Bob, signed in
- Your runtime:
  - **Default:** Python 3.10+ → `python -m venv .venv` → activate → `pip install fastapi "uvicorn[standard]" python-multipart`
  - Laravel/PHP, Node, .NET, Java are all fine — the rules are stack-neutral

Run check: `uvicorn --version` (or your stack's equivalent).

## 2 · Docling (only if your team does document intake)

Python 3.10+ required even for PHP/Node teams (Docling itself is Python).

```bash
pip install docling            # library (Python backends)
pip install "docling-serve[ui]"   # local HTTP API for non-Python backends
docling-serve run --enable-ui     # → http://127.0.0.1:5001  (API docs at /docs, demo UI at /ui)
```

**Models:** Docling downloads models on first use. On venue Wi-Fi, don't let 15 laptops do that at 10:00:

```bash
docling-tools models download     # prefetch to ~/.cache/docling/models
```

Organizers carry a USB copy of that models folder. To use it:

```bash
export DOCLING_ARTIFACTS_PATH=/path/to/models   # or copy into ~/.cache/docling/models
```

Speed tips: keep OCR off for digital PDFs (most of `documents/`); turn it on only for `*_scanned` files. CPU-only is fine; limit threads with `OMP_NUM_THREADS=4` if the laptop struggles.

## 3 · Sanity test (5 minutes)

```bash
cd reference && pip install -r requirements.txt && uvicorn app:app --port 8000
```

Open `checker/checker.html` in a browser → defaults point at the reference service → **Run checks** → everything green means your laptop is ready. Stop the reference service and build your own.

## 4 · Known traps

- Corporate proxy/SSL errors on pip: try `pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org …` or use the organizer's offline wheel USB.
- Port 8000 busy → `--port 8010` and update the checker's Base URL.
- Windows PowerShell venv activation: `.venv\Scripts\Activate.ps1` (if blocked: `Set-ExecutionPolicy -Scope Process Bypass`).
- `file://` page can't reach your API → you forgot dev CORS (see conventions §8).
