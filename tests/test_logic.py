"""Unit tests: pure business rules, no DB, no HTTP."""
from datetime import date

from app.logic import is_due, next_followup

TODAY = date(2026, 11, 15)


def test_next_followup_none_when_never_contacted():
    assert next_followup(None, 7) is None


def test_next_followup_adds_days():
    assert next_followup(date(2026, 11, 8), 7) == date(2026, 11, 15)


def test_never_contacted_active_entry_is_due():
    assert is_due("to_contact", None, 7, TODAY)


def test_due_exactly_on_followup_date():
    assert is_due("waiting", date(2026, 11, 8), 7, TODAY)


def test_not_due_before_followup_date():
    assert not is_due("waiting", date(2026, 11, 10), 7, TODAY)


def test_overdue_is_due():
    assert is_due("interview", date(2026, 10, 1), 7, TODAY)


def test_closed_statuses_never_due():
    for status in ("closed", "rejected", "accepted"):
        assert not is_due(status, None, 7, TODAY)
