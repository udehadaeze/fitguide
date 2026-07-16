from app.repository import BOOLEAN_COLUMNS, load_exercises


def test_dataset_has_80_unique_exercises():
    frame = load_exercises()
    assert len(frame) == 80
    assert frame["exercise_id"].is_unique
    assert frame["name"].is_unique


def test_dataset_contains_every_category():
    assert set(load_exercises()["category"]) == {"cardio", "strength", "mobility", "flexibility", "balance", "core", "relaxation"}


def test_dataset_boolean_columns_are_boolean():
    frame = load_exercises()
    assert all(frame[column].map(type).eq(bool).all() for column in BOOLEAN_COLUMNS)


def test_dataset_has_restriction_conflicts_to_test():
    frame = load_exercises()
    columns = ["involves_jumping", "involves_kneeling", "involves_overhead_movement", "involves_floor_position", "involves_deep_squat", "involves_single_leg_balance", "high_impact"]
    assert all(frame[column].any() for column in columns)

