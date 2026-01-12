from fastapi.testclient import TestClient
from src.app import app
import urllib.parse

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity check
    assert "Chess Club" in data


def test_signup_and_withdraw():
    activity = "Basketball Team"
    email = "test.student@mergington.edu"

    # Sign up
    signup_resp = client.post(
        f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    )
    assert signup_resp.status_code == 200
    assert email in signup_resp.json()["message"]

    # Verify participant appears
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert email in data[activity]["participants"]

    # Withdraw
    withdraw_resp = client.post(
        f"/activities/{urllib.parse.quote(activity)}/withdraw?email={urllib.parse.quote(email)}"
    )
    assert withdraw_resp.status_code == 200
    assert "Withdrew" in withdraw_resp.json()["message"]

    # Verify removal
    resp2 = client.get("/activities")
    data2 = resp2.json()
    assert email not in data2[activity]["participants"]
