from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .logic import ALL_STATUSES, KINDS


class EntryIn(BaseModel):
    kind: str = "application"
    name: str = Field(min_length=1, max_length=200)
    organization: str = Field(default="", max_length=200)
    status: str = "to_contact"
    last_contact: date | None = None
    followup_days: int = Field(default=7, ge=1, le=365)
    notes: str = Field(default="", max_length=5000)

    @field_validator("kind")
    @classmethod
    def _kind(cls, v: str) -> str:
        if v not in KINDS:
            raise ValueError(f"kind must be one of {sorted(KINDS)}")
        return v

    @field_validator("status")
    @classmethod
    def _status(cls, v: str) -> str:
        if v not in ALL_STATUSES:
            raise ValueError(f"status must be one of {sorted(ALL_STATUSES)}")
        return v


class EntryOut(EntryIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    next_followup: date | None = None
    due: bool = False
