import uuid

from fastapi.testclient import TestClient

from app.main import app


def test_analysis_run_endpoint() -> None:
    client = TestClient(app)
    payload = {
        "user_id": str(uuid.uuid4()),
        "language": "python",
        "code": "x = 1\nprint(x + 2)",
        "narration_language": "both",
        "optimization_level": "standard",
    }

    response = client.post("/api/v1/analysis/run", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["language"] == "python"
    assert "complexity" in body
    assert "dry_run" in body
