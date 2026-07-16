import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import UserProfile


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def beginner_profile() -> UserProfile:
    return UserProfile(goal="general_fitness", fitness_level="beginner", workout_location="home", available_equipment=["none", "chair", "wall"], preferred_duration_minutes=10, preferred_intensity="low", preferred_categories=["cardio", "strength", "mobility"], target_body_areas=["full_body"], movement_restrictions=[], low_impact_required=False, maximum_recommendations=5)

