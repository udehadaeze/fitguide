from app.models import UserProfile
from app.recommender import recommend, score_exercises, filter_exercises
from app.repository import load_exercises


def test_scored_candidates_are_ordered(beginner_profile: UserProfile):
    scores = [item["score"] for item in score_exercises(filter_exercises(load_exercises(), beginner_profile), beginner_profile)]
    assert scores == sorted(scores, reverse=True)


def test_recommendations_are_deterministic(beginner_profile: UserProfile):
    first = recommend(beginner_profile)
    second = recommend(beginner_profile)
    assert [(item.exercise_id, item.score) for item in first.recommendations] == [(item.exercise_id, item.score) for item in second.recommendations]


def test_routine_limits_repeated_categories(beginner_profile: UserProfile):
    result = recommend(beginner_profile)
    counts = {category: sum(item.category == category for item in result.recommendations) for category in {item.category for item in result.recommendations}}
    assert max(counts.values()) <= 2


def test_routine_limits_repeated_movement_patterns(beginner_profile: UserProfile):
    result = recommend(beginner_profile)
    counts = {pattern: sum(item.movement_pattern == pattern for item in result.recommendations) for pattern in {item.movement_pattern for item in result.recommendations}}
    assert max(counts.values()) <= 2


def test_explanations_are_derived_from_matches(beginner_profile: UserProfile):
    result = recommend(beginner_profile)
    for item in result.recommendations:
        assert item.matched_features
        assert item.explanation.startswith("Recommended because it ")
        assert item.matched_features[0] in item.explanation


def test_recommendations_preserve_combined_restrictions(beginner_profile: UserProfile):
    profile = beginner_profile.model_copy(update={"fitness_level": "advanced", "preferred_duration_minutes": 30, "available_equipment": ["none", "chair", "wall", "mat"], "movement_restrictions": ["avoid_jumping", "avoid_kneeling", "avoid_overhead_movements", "avoid_floor_exercises", "avoid_deep_squats", "avoid_single_leg_balance"], "low_impact_required": True})
    ids = [item.exercise_id for item in recommend(profile).recommendations]
    frame = load_exercises().set_index("exercise_id").loc[ids]
    conflict_columns = ["involves_jumping", "involves_kneeling", "involves_overhead_movement", "involves_floor_position", "involves_deep_squat", "involves_single_leg_balance"]
    assert not frame[conflict_columns].any().any()


def test_no_compatible_result_returns_warning(beginner_profile: UserProfile):
    profile = beginner_profile.model_copy(update={"workout_location": "outdoors", "preferred_duration_minutes": 3, "available_equipment": ["jump_rope"], "movement_restrictions": ["avoid_jumping", "avoid_high_impact", "avoid_single_leg_balance"], "low_impact_required": True})
    result = recommend(profile)
    assert result.recommendations == []
    assert result.warning is not None

