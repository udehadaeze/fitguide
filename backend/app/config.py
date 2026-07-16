from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "exercises.csv"

GOALS = (
    "general_fitness",
    "weight_management",
    "strength",
    "endurance",
    "mobility",
    "flexibility",
    "stress_reduction",
    "cardiovascular_fitness",
)

LEVELS = ("beginner", "intermediate", "advanced")
LOCATIONS = ("home", "gym", "outdoors", "any")
INTENSITIES = ("low", "moderate", "high")
CATEGORIES = ("cardio", "strength", "mobility", "flexibility", "balance", "core", "relaxation")
BODY_AREAS = ("full_body", "upper_body", "lower_body", "core", "back", "chest", "shoulders", "arms", "hips", "legs")
EQUIPMENT = ("none", "chair", "wall", "mat", "resistance_band", "dumbbells", "kettlebell", "bench", "step", "treadmill", "stationary_bike", "jump_rope")
RESTRICTIONS = (
    "avoid_jumping",
    "avoid_kneeling",
    "avoid_overhead_movements",
    "avoid_floor_exercises",
    "avoid_high_impact",
    "avoid_deep_squats",
    "avoid_single_leg_balance",
)

SCORE_WEIGHTS = {
    "cosine": 0.50,
    "goal": 0.15,
    "category": 0.10,
    "body_area": 0.08,
    "intensity": 0.06,
    "level": 0.05,
    "duration": 0.03,
    "location": 0.02,
    "equipment": 0.01,
}

LEVEL_ORDER = {"beginner": 0, "intermediate": 1, "advanced": 2}

