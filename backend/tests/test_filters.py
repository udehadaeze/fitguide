import pytest

from app.models import UserProfile
from app.recommender import RESTRICTION_COLUMNS, filter_exercises
from app.repository import load_exercises


@pytest.mark.parametrize("restriction", list(RESTRICTION_COLUMNS))
def test_movement_restriction_is_a_hard_filter(beginner_profile: UserProfile, restriction: str):
    profile = beginner_profile.model_copy(update={"fitness_level": "advanced", "movement_restrictions": [restriction], "preferred_duration_minutes": 30, "available_equipment": ["none", "chair", "wall", "mat", "resistance_band", "dumbbells", "kettlebell", "bench", "step", "treadmill", "stationary_bike", "jump_rope"], "workout_location": "any"})
    eligible = filter_exercises(load_exercises(), profile)
    assert not eligible[RESTRICTION_COLUMNS[restriction]].any()


def test_low_impact_requirement_is_a_hard_filter(beginner_profile: UserProfile):
    eligible = filter_exercises(load_exercises(), beginner_profile.model_copy(update={"low_impact_required": True}))
    assert eligible["low_impact"].all()


def test_unavailable_equipment_is_filtered(beginner_profile: UserProfile):
    eligible = filter_exercises(load_exercises(), beginner_profile.model_copy(update={"available_equipment": ["none"]}))
    assert all(items == ["none"] for items in eligible["equipment"])


def test_location_is_filtered(beginner_profile: UserProfile):
    eligible = filter_exercises(load_exercises(), beginner_profile.model_copy(update={"workout_location": "outdoors", "fitness_level": "advanced", "preferred_duration_minutes": 30}))
    assert all("outdoors" in values or "any" in values for values in eligible["workout_locations"])


def test_beginner_does_not_receive_higher_levels(beginner_profile: UserProfile):
    eligible = filter_exercises(load_exercises(), beginner_profile)
    assert set(eligible["difficulty"]) == {"beginner"}


def test_duration_is_filtered(beginner_profile: UserProfile):
    eligible = filter_exercises(load_exercises(), beginner_profile.model_copy(update={"preferred_duration_minutes": 6}))
    assert eligible["estimated_duration_minutes"].max() <= 6


def test_exact_exercise_name_is_filtered(beginner_profile: UserProfile):
    eligible = filter_exercises(load_exercises(), beginner_profile.model_copy(update={"exercises_to_avoid": ["Walking in Place"]}))
    assert "Walking in Place" not in set(eligible["name"])

