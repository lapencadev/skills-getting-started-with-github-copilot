def test_signup_increases_participant_count(client):
    # Arrange
    activity_name = "Programming Class"
    email = "newcount@mergington.edu"

    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity_name]["participants"])
    assert final_count == initial_count + 1


def test_remove_decreases_participant_count(client):
    # Arrange
    activity_name = "Gym Class"
    email = "john@mergington.edu"  # Already signed up

    # Get initial count
    initial_response = client.get("/activities")
    initial_count = len(initial_response.json()[activity_name]["participants"])

    # Act
    client.delete(f"/activities/{activity_name}/remove?email={email}")

    # Assert
    final_response = client.get("/activities")
    final_count = len(final_response.json()[activity_name]["participants"])
    assert final_count == initial_count - 1


def test_remove_success(client):
    # Arrange
    activity_name = "Basketball Team"
    email = "james@mergington.edu"  # Already signed up

    # Act
    response = client.delete(f"/activities/{activity_name}/remove?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}


def test_multiple_signups(client):
    # Arrange
    activity_name = "Tennis Club"
    emails = ["multi1@mergington.edu", "multi2@mergington.edu"]

    # Act
    for email in emails:
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200

    # Assert
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    for email in emails:
        assert email in participants


def test_other_activities_unaffected(client):
    # Arrange
    activity_name = "Art Studio"
    email = "newunaffected@mergington.edu"
    other_activity = "Music Ensemble"

    # Get initial state of other activity
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[other_activity]["participants"].copy()

    # Act - signup for different activity
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert - other activity unchanged
    final_response = client.get("/activities")
    final_participants = final_response.json()[other_activity]["participants"]
    assert final_participants == initial_participants