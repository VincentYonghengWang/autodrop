from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ExceptionRecord
from app.robots.common import log_activity


def run(db: Session) -> dict:
    pending = db.scalars(select(ExceptionRecord).where(ExceptionRecord.status == "open")).all()
    handled = 0
    for record in pending:
        if record.type == "refund_review":
            continue
        record.status = "triaged"
        handled += 1
    db.commit()
    log_activity(db, "CS Bot", f"Auto-triaged {handled} exception and support events.")
    return {"handled": handled}

