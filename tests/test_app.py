from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email():
    from src import app as app_module

    app_module.activities["Gym Class"]["participants"] = [
        "alice@mergington.edu",
        "bob@mergington.edu",
    ]

    response = client.delete("/activities/Gym%20Class/unregister?email=alice@mergington.edu")

    assert response.status_code == 200
    assert "alice@mergington.edu" not in app_module.activities["Gym Class"]["participants"]
    assert "bob@mergington.edu" in app_module.activities["Gym Class"]["participants"]


def test_duplicate_signup_is_rejected():
    from src import app as app_module

    app_module.activities["Chess Club"]["participants"] = ["already@mergington.edu"]

    response = client.post(
        "/activities/Chess%20Club/signup?email=already@mergington.edu"
    )

    assert response.status_code == 400
