"""
Test suite for FastAPI activities endpoints.

Tests follow the Arrange-Act-Assert (AAA) pattern:
- ARRANGE: Set up test data and fixtures
- ACT: Execute the endpoint under test
- ASSERT: Verify the response and side effects
"""

import pytest
from fastapi.testclient import TestClient


class TestGetActivities:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client: TestClient):
        """
        ARRANGE: Use the TestClient fixture (provided by conftest.py)
        ACT: Make a GET request to /activities
        ASSERT: Verify status is 200 and response contains all activities
        """
        # ACT
        response = client.get("/activities")

        # ASSERT
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0
        assert "Chess Club" in activities
        assert "Programming Class" in activities
        assert "Tennis Club" in activities

    def test_get_activities_returns_correct_structure(self, client: TestClient):
        """
        ARRANGE: Use the TestClient fixture
        ACT: Make a GET request to /activities
        ASSERT: Verify each activity has required fields
        """
        # ACT
        response = client.get("/activities")
        activities = response.json()

        # ASSERT
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_participants_are_emails(self, client: TestClient):
        """
        ARRANGE: Use the TestClient fixture
        ACT: Make a GET request to /activities
        ASSERT: Verify participants are email strings (basic validation)
        """
        # ACT
        response = client.get("/activities")
        activities = response.json()

        # ASSERT
        for activity_data in activities.values():
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success_adds_participant(self, client: TestClient, test_email: str):
        """
        ARRANGE: Use the TestClient and test email fixtures
        ACT: Sign up a new student for an activity
        ASSERT: Verify response status is 200 and participant was added
        """
        activity_name = "Chess Club"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # ASSERT
        assert response.status_code == 200
        assert "message" in response.json()
        assert test_email in response.json()["message"]

    def test_signup_success_updates_participant_list(self, client: TestClient, test_email: str):
        """
        ARRANGE: Use the TestClient and test email fixtures
        ACT: Sign up a student, then fetch activities
        ASSERT: Verify the participant list was updated
        """
        activity_name = "Chess Club"

        # ACT - Sign up student
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        assert signup_response.status_code == 200

        # ACT - Get activities to verify participant was added
        activities_response = client.get("/activities")

        # ASSERT
        activities = activities_response.json()
        assert test_email in activities[activity_name]["participants"]

    def test_signup_activity_not_found_returns_404(self, client: TestClient, test_email: str):
        """
        ARRANGE: Use the TestClient and test email fixtures with a non-existent activity
        ACT: Try to sign up for an activity that doesn't exist
        ASSERT: Verify response status is 404
        """
        nonexistent_activity = "Nonexistent Activity"

        # ACT
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": test_email}
        )

        # ASSERT
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_signup_duplicate_email_returns_400(self, client: TestClient):
        """
        ARRANGE: Use an email that is already a participant in Chess Club
        ACT: Try to sign up the same email again
        ASSERT: Verify response status is 400
        """
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"  # Already in Chess Club

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )

        # ASSERT
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"].lower()

    def test_signup_multiple_activities_same_email(self, client: TestClient, test_email: str):
        """
        ARRANGE: Use a test email and two different activities
        ACT: Sign up the same email for multiple activities
        ASSERT: Verify both signups succeed
        """
        activity1 = "Chess Club"
        activity2 = "Programming Class"

        # ACT - Sign up for first activity
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": test_email}
        )
        assert response1.status_code == 200

        # ACT - Sign up for second activity
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": test_email}
        )

        # ASSERT
        assert response2.status_code == 200
        activities = client.get("/activities").json()
        assert test_email in activities[activity1]["participants"]
        assert test_email in activities[activity2]["participants"]

    def test_signup_response_message_format(self, client: TestClient, test_email: str):
        """
        ARRANGE: Use the TestClient and test email fixtures
        ACT: Sign up a student
        ASSERT: Verify the response message has the correct format
        """
        activity_name = "Tennis Club"

        # ACT
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )

        # ASSERT
        assert response.status_code == 200
        message = response.json()["message"]
        assert "Signed up" in message
        assert test_email in message
        assert activity_name in message
