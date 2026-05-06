from urllib.parse import quote

from src.app import activities


def test_get_activities_returns_seeded_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert expected_activity in payload
    assert "participants" in payload[expected_activity]


def test_signup_for_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "new.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate_student(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_activity_returns_not_found_for_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Activity"
    encoded_activity_name = quote(unknown_activity, safe="")
    email = "someone@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_success(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = activities[activity_name]["participants"][0]

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_from_activity_returns_not_found_for_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Activity"
    encoded_activity_name = quote(unknown_activity, safe="")
    email = "someone@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_from_activity_rejects_non_member_student(client):
    # Arrange
    activity_name = "Chess Club"
    encoded_activity_name = quote(activity_name, safe="")
    email = "not.registered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{encoded_activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
