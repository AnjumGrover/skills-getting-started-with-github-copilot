"""
Comprehensive test suite for the High School Management System API

This module contains unit and integration tests for all FastAPI endpoints
using the AAA (Arrange-Act-Assert) pattern with clear comments for each section.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# ============================================================================
# Setup and Fixtures
# ============================================================================

@pytest.fixture
def client():
    """Fixture to provide a TestClient for the FastAPI application"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture to reset the activities database to initial state before each test
    This ensures test isolation and prevents side effects between tests
    """
    # Store initial state
    initial_activities = {
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
        "Basketball Club": {
            "description": "Competitive basketball team and practice",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Join the soccer team for matches and training",
            "schedule": "Tuesdays and Fridays, 3:45 PM - 5:15 PM",
            "max_participants": 22,
            "participants": ["alex@mergington.edu", "maya@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and other visual arts",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater, acting, and performance arts",
            "schedule": "Tuesdays and Thursdays, 4:45 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "grace@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate and public speaking",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["marcus@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore biology, chemistry, physics, and experimental science",
            "schedule": "Fridays, 3:30 PM - 4:45 PM",
            "max_participants": 20,
            "participants": ["zoe@mergington.edu", "noah@mergington.edu"]
        }
    }
    
    yield
    
    # Restore activities to initial state after test
    activities.clear()
    activities.update(initial_activities)


# ============================================================================
# Tests for GET / (Root Redirect Endpoint)
# ============================================================================

class TestRootEndpoint:
    """Test suite for the root endpoint that redirects to index.html"""

    def test_root_redirect_status_code(self, client):
        """Test that root endpoint returns redirect status code (307)"""
        # Arrange: TestClient is configured to follow redirects by default
        
        # Act: Send GET request to root endpoint
        response = client.get("/", follow_redirects=False)
        
        # Assert: Verify the response status code is a redirect
        assert response.status_code == 307

    def test_root_redirect_location(self, client):
        """Test that root endpoint redirects to the correct static HTML file"""
        # Arrange: Expected redirect target path
        expected_location = "/static/index.html"
        
        # Act: Send GET request to root endpoint without following redirects
        response = client.get("/", follow_redirects=False)
        
        # Assert: Verify the redirect location header points to index.html
        assert response.headers["location"] == expected_location


# ============================================================================
# Tests for GET /activities (Retrieve All Activities Endpoint)
# ============================================================================

class TestGetActivitiesEndpoint:
    """Test suite for the endpoint that retrieves all available activities"""

    def test_get_activities_returns_success_status(self, client, reset_activities):
        """Test that get_activities endpoint returns successful status code"""
        # Arrange: TestClient is ready for requests
        
        # Act: Send GET request to retrieve all activities
        response = client.get("/activities")
        
        # Assert: Verify the response status code is 200 OK
        assert response.status_code == 200

    def test_get_activities_returns_json_content_type(self, client, reset_activities):
        """Test that get_activities endpoint returns JSON content type"""
        # Arrange: Valid endpoint path
        
        # Act: Send GET request to activities endpoint
        response = client.get("/activities")
        
        # Assert: Verify response content type is application/json
        assert response.headers["content-type"] == "application/json"

    def test_get_activities_returns_all_nine_activities(self, client, reset_activities):
        """Test that get_activities returns all nine activities"""
        # Arrange: Expected number of activities in the system
        expected_activity_count = 9
        
        # Act: Send GET request and parse JSON response
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert: Verify all activities are returned
        assert len(activities_data) == expected_activity_count

    def test_get_activities_includes_chess_club(self, client, reset_activities):
        """Test that Chess Club is included in activities response"""
        # Arrange: Expected activity name and key fields
        
        # Act: Send GET request and retrieve activities data
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert: Verify Chess Club exists with correct structure
        assert "Chess Club" in activities_data
        assert "description" in activities_data["Chess Club"]
        assert "schedule" in activities_data["Chess Club"]
        assert "max_participants" in activities_data["Chess Club"]
        assert "participants" in activities_data["Chess Club"]

    def test_get_activities_includes_participant_lists(self, client, reset_activities):
        """Test that activities include existing participant lists"""
        # Arrange: Expected initial participants for Chess Club
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # Act: Send GET request and retrieve activities data
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert: Verify participants list matches expected initial state
        assert activities_data["Chess Club"]["participants"] == expected_chess_participants

    def test_get_activities_returns_valid_json_structure(self, client, reset_activities):
        """Test that all activities have required fields in response"""
        # Arrange: Required fields for each activity object
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act: Send GET request and retrieve activities data
        response = client.get("/activities")
        activities_data = response.json()
        
        # Assert: Verify each activity has all required fields
        for activity_name, activity_data in activities_data.items():
            for field in required_fields:
                assert field in activity_data, f"Activity '{activity_name}' missing field '{field}'"


# ============================================================================
# Tests for POST /activities/{activity_name}/signup (Signup Endpoint)
# ============================================================================

class TestSignupEndpoint:
    """Test suite for the endpoint that signs up students for activities"""

    def test_signup_successful_for_new_participant(self, client, reset_activities):
        """Test successful signup for a new participant"""
        # Arrange: New participant email and target activity
        new_email = "newstudent@mergington.edu"
        activity_name = "Chess Club"
        
        # Act: Send POST request to signup endpoint
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert: Verify successful response and message content
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert new_email in response_data["message"]
        assert activity_name in response_data["message"]

    def test_signup_adds_participant_to_activity_list(self, client, reset_activities):
        """Test that signup adds participant to the activity's participant list"""
        # Arrange: New participant and activity details
        new_email = "newstudent@mergington.edu"
        activity_name = "Chess Club"
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"]
        initial_count = len(initial_participants)
        
        # Act: Sign up the new participant
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert: Verify participant was added to the list
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[activity_name]["participants"]
        assert len(updated_participants) == initial_count + 1
        assert new_email in updated_participants

    def test_signup_fails_for_nonexistent_activity(self, client, reset_activities):
        """Test that signup fails when activity doesn't exist"""
        # Arrange: Valid email but nonexistent activity
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act: Attempt to sign up for nonexistent activity
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )
        
        # Assert: Verify 404 error with appropriate message
        assert response.status_code == 404
        response_data = response.json()
        assert "Activity not found" in response_data["detail"]

    def test_signup_fails_for_duplicate_registration(self, client, reset_activities):
        """Test that signup fails when student is already registered"""
        # Arrange: Email of existing participant
        existing_email = "michael@mergington.edu"
        activity_name = "Chess Club"
        
        # Act: Attempt to sign up existing participant again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert: Verify 400 error with duplicate message
        assert response.status_code == 400
        response_data = response.json()
        assert "already signed up" in response_data["detail"]

    def test_signup_allows_multiple_activities_for_same_student(self, client, reset_activities):
        """Test that a student can sign up for multiple different activities"""
        # Arrange: Same email for different activities
        email = "multiactivity@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"
        
        # Act: Sign up for first activity
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        
        # Sign up for second activity
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )
        
        # Assert: Both signups should succeed
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify student appears in both activity lists
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity1]["participants"]
        assert email in activities_data[activity2]["participants"]


# ============================================================================
# Tests for DELETE /activities/{activity_name}/signup (Unregister Endpoint)
# ============================================================================

class TestUnregisterEndpoint:
    """Test suite for the endpoint that unregisters students from activities"""

    def test_unregister_successful_for_existing_participant(self, client, reset_activities):
        """Test successful unregister for an existing participant"""
        # Arrange: Email of existing participant
        existing_email = "michael@mergington.edu"
        activity_name = "Chess Club"
        
        # Act: Send DELETE request to unregister endpoint
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert: Verify successful response and message content
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert existing_email in response_data["message"]
        assert "Unregistered" in response_data["message"]

    def test_unregister_removes_participant_from_activity_list(self, client, reset_activities):
        """Test that unregister removes participant from the activity's participant list"""
        # Arrange: Email of existing participant
        existing_email = "michael@mergington.edu"
        activity_name = "Chess Club"
        
        # Get initial participant count
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[activity_name]["participants"]
        initial_count = len(initial_participants)
        
        # Act: Unregister the participant
        client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert: Verify participant was removed from the list
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[activity_name]["participants"]
        assert len(updated_participants) == initial_count - 1
        assert existing_email not in updated_participants

    def test_unregister_fails_for_nonexistent_activity(self, client, reset_activities):
        """Test that unregister fails when activity doesn't exist"""
        # Arrange: Valid email but nonexistent activity
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act: Attempt to unregister from nonexistent activity
        response = client.delete(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )
        
        # Assert: Verify 404 error with appropriate message
        assert response.status_code == 404
        response_data = response.json()
        assert "Activity not found" in response_data["detail"]

    def test_unregister_fails_for_non_participant(self, client, reset_activities):
        """Test that unregister fails when student is not registered"""
        # Arrange: Email not in the activity
        non_participant_email = "notregistered@mergington.edu"
        activity_name = "Chess Club"
        
        # Act: Attempt to unregister non-participant
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": non_participant_email}
        )
        
        # Assert: Verify 404 error with appropriate message
        assert response.status_code == 404
        response_data = response.json()
        assert "not signed up" in response_data["detail"]

    def test_signup_after_unregister_works(self, client, reset_activities):
        """Test that a student can sign up again after unregistering"""
        # Arrange: Email and activity
        email = "rejoin@mergington.edu"
        activity_name = "Chess Club"
        
        # First sign up
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act: Unregister, then sign up again
        client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert: Second signup should succeed
        assert response.status_code == 200
        
        # Verify student is back in the list
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]


# ============================================================================
# Integration Tests (Combining Multiple Endpoints)
# ============================================================================

class TestIntegrationScenarios:
    """Test suite for integration scenarios combining multiple endpoints"""

    def test_complete_signup_unregister_workflow(self, client, reset_activities):
        """Test the complete workflow of signup and unregister"""
        # Arrange: New participant details
        email = "workflowtest@mergington.edu"
        activity_name = "Programming Class"
        
        # Act & Assert: Initial state - not signed up
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        assert email not in initial_data[activity_name]["participants"]
        
        # Act: Sign up
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert: Signup successful
        assert signup_response.status_code == 200
        
        # Act & Assert: Verify signed up
        after_signup_response = client.get("/activities")
        after_signup_data = after_signup_response.json()
        assert email in after_signup_data[activity_name]["participants"]
        
        # Act: Unregister
        unregister_response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert: Unregister successful
        assert unregister_response.status_code == 200
        
        # Act & Assert: Verify unregistered
        final_response = client.get("/activities")
        final_data = final_response.json()
        assert email not in final_data[activity_name]["participants"]

    def test_multiple_students_can_join_same_activity(self, client, reset_activities):
        """Test that multiple students can join the same activity"""
        # Arrange: Multiple student emails and activity
        emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        activity_name = "Science Club"
        
        # Act: Sign up all students
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Assert: All students are in the participant list
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        participants = activities_data[activity_name]["participants"]
        
        for email in emails:
            assert email in participants
