import json
import logging
import time
import uuid
from contextlib import asynccontextmanager
from datetime import date
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from . import logic
from .db import Base, engine, get_db
from .models import Entry
from .schemas import EntryIn, EntryOut

# --- structured JSON logs, one request_id per request ---------------------------------
logger = logging.getLogger("followup")
logging.basicConfig(level=logging.INFO, format="%(message)s")


def log(event: str, **fields):
    logger.info(json.dumps({"event": event, **fields}, default=str))


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Follow-up Tracker", version="1.0.0", lifespan=lifespan)
STATIC = Path(__file__).parent / "static"


@app.middleware("http")
async def request_logging(request: Request, call_next):
    request_id = request.headers.get("x-request-id", uuid.uuid4().hex[:12])
    start = time.perf_counter()
    response = await call_next(request)
    response.headers["x-request-id"] = request_id
    log(
        "http_request",
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        ms=round((time.perf_counter() - start) * 1000, 1),
    )
    return response


def today() -> date:
    return date.today()


def to_out(e: Entry, now: date) -> EntryOut:
    out = EntryOut.model_validate(e)
    out.next_followup = logic.next_followup(e.last_contact, e.followup_days)
    out.due = logic.is_due(e.status, e.last_contact, e.followup_days, now)
    return out


def _get_or_404(db: Session, entry_id: int) -> Entry:
    entry = db.get(Entry, entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/api/entries", response_model=list[EntryOut])
def list_entries(due_only: bool = False, db: Session = Depends(get_db), now: date = Depends(today)):
    rows = db.scalars(select(Entry).order_by(Entry.id)).all()
    items = [to_out(r, now) for r in rows]
    return [i for i in items if i.due] if due_only else items


@app.post("/api/entries", response_model=EntryOut, status_code=201)
def create_entry(payload: EntryIn, db: Session = Depends(get_db), now: date = Depends(today)):
    entry = Entry(**payload.model_dump())
    db.add(entry)
    db.commit()
    log("entry_created", entry_id=entry.id, kind=entry.kind)  # ids only, no personal data
    return to_out(entry, now)


@app.put("/api/entries/{entry_id}", response_model=EntryOut)
def update_entry(entry_id: int, payload: EntryIn, db: Session = Depends(get_db), now: date = Depends(today)):
    entry = _get_or_404(db, entry_id)
    for k, v in payload.model_dump().items():
        setattr(entry, k, v)
    db.commit()
    return to_out(entry, now)


@app.post("/api/entries/{entry_id}/contacted", response_model=EntryOut)
def mark_contacted(entry_id: int, db: Session = Depends(get_db), now: date = Depends(today)):
    """One click: I just followed up. Sets last_contact=today, 'to_contact' -> 'waiting'."""
    entry = _get_or_404(db, entry_id)
    entry.last_contact = now
    if entry.status == "to_contact":
        entry.status = "waiting"
    db.commit()
    log("entry_contacted", entry_id=entry.id)
    return to_out(entry, now)


@app.delete("/api/entries/{entry_id}", status_code=204)
def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    entry = _get_or_404(db, entry_id)
    db.delete(entry)
    db.commit()


app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")
