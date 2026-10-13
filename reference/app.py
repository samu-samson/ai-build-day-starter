"""Reference service — a worked example of every readiness rule, over data/registry.csv.

For mentors and for sanity-testing the checker. Your team's entry must be its own domain.
Run:  pip install -r requirements.txt && uvicorn app:app --port 8000
"""
import csv
import hashlib
import time
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Header, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

DATA = Path(__file__).resolve().parent.parent / "data" / "registry.csv"

CLIENTS = {
    "INTERNAL-APP": {"key": "int-dev-key", "scope": "full"},
    "PARTNER-AGENCY": {"key": "partner-dev-key", "scope": "verify"},
}
VERIFY_FIELDS = ["name", "entityType", "status", "validUntil"]  # minimal disclosure
PERSONAL_PATHS = ("/records/",)  # detail reads need a stated purpose

records = {}
with DATA.open(encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        records[row["registryNo"].upper()] = row

access_log = []  # {ts, clientId, method, path, subjectId, purpose, status}
idem = {}        # Idempotency-Key -> (status, body)
requests_filed = {}

app = FastAPI(title="Sandbox registry standing service", version="1.0.0",
              description="Reference implementation of the build-day readiness rules. Synthetic data only.")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])  # dev only


def err(status: int, code: str, detail: str, action: str, extra: dict = None):
    body = {"code": code, "detail": detail, "action": action, "synthetic": True}
    if extra:
        body.update(extra)
    return JSONResponse(body, status_code=status)


def subject_of(path: str) -> Optional[str]:
    parts = [p for p in path.split("/") if p]
    for p in parts:
        if p.upper().startswith("SBX-"):
            return p.upper()
    return None


@app.middleware("http")
async def guard(request: Request, call_next):
    path = request.url.path
    if path in ("/healthz", "/openapi.json", "/docs", "/redoc"):
        return await call_next(request)
    cid = request.headers.get("x-client-id", "")
    key = request.headers.get("x-api-key", "")
    client = CLIENTS.get(cid)

    def log(status: int):
        access_log.append({"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "clientId": cid or "(none)",
                           "method": request.method, "path": path, "subjectId": subject_of(path),
                           "purpose": request.headers.get("x-purpose"), "status": status})

    if not client or client["key"] != key:
        log(401)
        return err(401, "UNAUTHENTICATED", "Missing or invalid X-Client-Id / X-Api-Key.",
                   "fix_input — send both headers; dev keys are in docs/CONVENTIONS.md §2.")
    is_verify = path.endswith("/verify")
    if client["scope"] == "verify" and not is_verify:
        log(403)
        return err(403, "ACCESS_DENIED", f"{cid} has verify-only access.",
                   "request_access — call GET /records/{id}/verify instead, or ask the data owner for a grant.")
    if request.method == "GET" and path.startswith(PERSONAL_PATHS) and not is_verify:
        purpose = request.headers.get("x-purpose", "")
        if len(purpose.strip()) < 5:
            log(400)
            return err(400, "PURPOSE_REQUIRED",
                       "This endpoint returns personal data; state why you need it.",
                       "fix_input — resend with X-Purpose, e.g. 'Renewal case SBX-CASE-0012'.")
    response = await call_next(request)
    log(response.status_code)
    return response


@app.get("/healthz", summary="Liveness check (no auth).")
def healthz():
    return {"ok": True, "synthetic": True}


@app.get("/records", summary="List/search records. Full scope.")
def list_records(q: str = "", limit: int = Query(20, le=200)):
    ql = q.lower()
    items = [r for r in records.values() if not ql or ql in " ".join(r.values()).lower()]
    return {"items": items[:limit], "count": len(items), "synthetic": True}


@app.get("/records/{rid}/verify", summary="Minimal-disclosure standing check. Any scope.")
def verify_record(rid: str):
    r = records.get(rid.upper())
    if not r:
        return {"found": False, "registryNo": rid.upper(), "synthetic": True}
    out = {"found": True, "registryNo": r["registryNo"]}
    out.update({k: r[k] for k in VERIFY_FIELDS if r.get(k)})
    out["synthetic"] = True
    return out


@app.get("/records/{rid}", summary="Full record. Full scope + X-Purpose.")
def get_record(rid: str):
    r = records.get(rid.upper())
    if not r:
        return err(404, "RECORD_NOT_FOUND", f"No record {rid}. Sample IDs run SBX-REG-0001…0020.",
                   "fix_input — check the ID or use GET /records?q= to search.")
    return {**r, "synthetic": True}


class RequestIn(BaseModel):
    recordId: str
    requestType: str = "RENEWAL"
    remarks: str = ""


@app.post("/requests", status_code=201, summary="File a renewal request. Idempotency-Key + X-Human-Confirmed required.")
def file_request(body: RequestIn,
                 idempotency_key: Optional[str] = Header(None),
                 x_human_confirmed: Optional[str] = Header(None)):
    if not idempotency_key:
        return err(400, "IDEMPOTENCY_KEY_REQUIRED", "Writes must carry an Idempotency-Key header.",
                   "fix_input — generate one per user action and reuse it on retries.")
    if idempotency_key in idem:
        status, saved = idem[idempotency_key]
        return JSONResponse(saved, status_code=status)
    rec = records.get(body.recordId.upper())
    if not rec:
        return err(404, "RECORD_NOT_FOUND", f"No record {body.recordId}.", "fix_input — check the ID.")
    if (x_human_confirmed or "").lower() != "true":
        return err(428, "CONFIRMATION_REQUIRED",
                   "This files a request on someone's behalf; a person must confirm first.",
                   "ask_human — show this summary, then resend with X-Human-Confirmed: true.",
                   {"summary": {"recordId": rec["registryNo"], "name": rec["name"], "requestType": body.requestType}})
    ref = "SBX-REQ-" + hashlib.sha1(idempotency_key.encode()).hexdigest()[:6].upper()
    saved = {"referenceNo": ref, "recordId": rec["registryNo"], "requestType": body.requestType,
             "status": "RECEIVED", "receivedAt": time.strftime("%Y-%m-%dT%H:%M:%S"), "synthetic": True}
    requests_filed[ref] = saved
    idem[idempotency_key] = (201, saved)
    return JSONResponse(saved, status_code=201)


@app.get("/access-log", summary="Who asked what about a subject, and why. Full scope.")
def get_access_log(subject: Optional[str] = None, limit: int = Query(50, le=500)):
    items = [e for e in reversed(access_log) if not subject or e["subjectId"] == subject.upper()]
    return {"items": items[:limit], "synthetic": True}
