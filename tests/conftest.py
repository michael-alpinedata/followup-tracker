import os

os.environ["DATABASE_URL"] = "sqlite://"  # in-memory; must be set before importing the app

from datetime import date  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from app.db import Base, engine  # noqa: E402
from app.main import app, today  # noqa: E402

FIXED_TODAY = date(2026, 11, 15)


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[today] = lambda: FIXED_TODAY
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
