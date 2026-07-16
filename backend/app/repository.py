from functools import lru_cache

import pandas as pd

from app.config import DATA_PATH

LIST_COLUMNS = ["secondary_body_areas", "equipment", "workout_locations", "tags"]
BOOLEAN_COLUMNS = [
    "beginner_friendly",
    "low_impact",
    "involves_jumping",
    "involves_kneeling",
    "involves_overhead_movement",
    "involves_floor_position",
    "involves_deep_squat",
    "involves_single_leg_balance",
    "high_impact",
    "cardio",
    "strength",
    "mobility",
    "flexibility",
    "balance",
    "core",
    "relaxation",
    "supports_general_fitness",
    "supports_weight_management",
    "supports_strength",
    "supports_endurance",
    "supports_mobility",
    "supports_flexibility",
    "supports_stress_reduction",
    "supports_cardio",
]


@lru_cache(maxsize=1)
def load_exercises() -> pd.DataFrame:
    frame = pd.read_csv(DATA_PATH)
    for column in LIST_COLUMNS:
        frame[column] = frame[column].fillna("").map(lambda value: [item for item in str(value).split("|") if item])
    for column in BOOLEAN_COLUMNS:
        frame[column] = frame[column].map(lambda value: str(value).lower() == "true" if isinstance(value, str) else bool(value))
    return frame


def exercise_exists(exercise_id: str) -> bool:
    return bool((load_exercises()["exercise_id"] == exercise_id).any())

