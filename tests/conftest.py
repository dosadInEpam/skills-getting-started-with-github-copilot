"""
Pytest fixtures and configuration for FastAPI tests.

This module provides reusable test fixtures following the AAA (Arrange-Act-Assert) pattern.
Fixtures handle test data setup and provide a TestClient for making HTTP requests.
"""

import pytest
from fastapi.testclient import TestClient
import src.app as app_module


# Store the original activities state for reset between tests
INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball training and intramural games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis lessons and friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["james@mergington.edu", "lisa@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and sculpture techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Orchestra and band performance group",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop critical thinking and public speaking skills",
        "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["ethan@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and STEM exploration",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """
    ARRANGE: Provide a TestClient for making HTTP requests to the FastAPI app.
    
    This fixture is function-scoped, ensuring test isolation for each test.
    Before each test, reset the in-memory activities database to its initial state
    by clearing and repopulating it with fresh data copied from INITIAL_ACTIVITIES.
    The TestClient allows synchronous testing of async endpoints.
    
    Yields:
        TestClient: A client for making HTTP requests to the test app.
    """
    # Reset activities to initial state before each test
    # Clear the current activities dict and repopulate it
    app_module.activities.clear()
    app_module.activities.update({
        name: {
            "description": data["description"],
            "schedule": data["schedule"],
            "max_participants": data["max_participants"],
            "participants": data["participants"].copy()  # Deep copy the list
        }
        for name, data in INITIAL_ACTIVITIES.items()
    })
    
    return TestClient(app_module.app)


@pytest.fixture
def sample_activities_state():
    """
    ARRANGE: Provide the initial state of activities for test verification.
    
    Returns a copy of the expected activity structure with baseline participants.
    This fixture helps verify that the app's in-memory database is initialized correctly.
    
    Returns:
        dict: Activities structure with Chess Club and Programming Class as examples.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        }
    }


@pytest.fixture
def test_email():
    """
    ARRANGE: Provide a unique test email for signup scenarios.
    
    Returns:
        str: A test email address that is not in the default participant lists.
    """
    return "test.student@mergington.edu"
