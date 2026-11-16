from datetime import date

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Entry(Base):
    """A job application or a networking contact to follow up on."""

    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(20), default="application")  # application | contact
    name: Mapped[str] = mapped_column(String(200))
    organization: Mapped[str] = mapped_column(String(200), default="")
    status: Mapped[str] = mapped_column(String(30), default="to_contact")
    last_contact: Mapped[date | None] = mapped_column(Date, nullable=True)
    followup_days: Mapped[int] = mapped_column(Integer, default=7)
    notes: Mapped[str] = mapped_column(Text, default="")
