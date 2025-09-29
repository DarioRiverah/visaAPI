# tests/conftest.py
import itertools
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.routers import clients

@pytest.fixture(autouse=True)
def reset_state():
    """
    Limpia el estado global entre tests.
    - Vacía la "base" en memoria.
    - Reinicia el contador de IDs.
    """
    clients.CLIENTS.clear()
    clients._client_id_seq = itertools.count(1)  # noqa: SLF001 (acceso interno intencional)
    yield
    clients.CLIENTS.clear()
