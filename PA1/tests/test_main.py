# Tool: Copilot Fusion
#
# Prompt summary: Create a barebones FastAPI app 
#
# AI Contribution: 100%
#
# Human Modifications: No changes were necessary
#

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
