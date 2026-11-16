"""Pure business rules (unit-tested, no DB)."""
from datetime import date, timedelta

ACTIVE_STATUSES = {"to_contact", "waiting", "interview"}
CLOSED_STATUSES = {"closed", "rejected", "accepted"}
ALL_STATUSES = ACTIVE_STATUSES | CLOSED_STATUSES
KINDS = {"application", "contact"}


def next_followup(last_contact: date | None, followup_days: int) -> date | None:
    """Date at which a follow-up is due, or None if never contacted."""
    if last_contact is None:
        return None
    return last_contact + timedelta(days=followup_days)


def is_due(status: str, last_contact: date | None, followup_days: int, today: date) -> bool:
    """An active entry is due if never contacted, or its follow-up date is today or past."""
    if status in CLOSED_STATUSES:
        return False
    due_on = next_followup(last_contact, followup_days)
    return due_on is None or due_on <= today
