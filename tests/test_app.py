from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity = activities["Chess Club"]
    original_participants = list(activity["participants"])

    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"
    assert activity["participants"] == original_participants


def test_unregister_participant_removes_email_from_activity():
    activity = activities["Chess Club"]
    activity["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.delete(
        "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activity["participants"]
    assert "daniel@mergington.edu" in activity["participants"]
