from urllib.parse import quote


def _signup_path(activity_name: str) -> str:
    return f"/activities/{quote(activity_name, safe='')}/signup"


def test_get_activities_returns_all(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success(client):
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    response = client.post(_signup_path(activity_name), params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_duplicate_returns_400(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    response = client.post(
        _signup_path(activity_name),
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_unknown_activity_returns_404(client):
    response = client.post("/activities/Unknown/signup", params={"email": "a@b.com"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_success(client):
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"

    response = client.delete(_signup_path(activity_name), params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_unknown_participant_returns_404(client):
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(_signup_path(activity_name), params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
