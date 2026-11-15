# Tool: Copilot Fusion
#
# Prompt summary: Create a barebones FastAPI app 
#
# AI Contribution: 95%
#
# Human Modifications: Changed position imports bc of link error
#

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
