import csv
from pathlib import Path

COLUMNS = [
    "exercise_id", "name", "description", "category", "movement_pattern", "primary_body_area", "secondary_body_areas", "difficulty", "intensity", "equipment", "workout_locations", "space_requirement", "estimated_duration_minutes", "recommended_repetitions", "recommended_sets", "beginner_friendly", "low_impact", "involves_jumping", "involves_kneeling", "involves_overhead_movement", "involves_floor_position", "involves_deep_squat", "involves_single_leg_balance", "high_impact", "cardio", "strength", "mobility", "flexibility", "balance", "core", "relaxation", "supports_general_fitness", "supports_weight_management", "supports_strength", "supports_endurance", "supports_mobility", "supports_flexibility", "supports_stress_reduction", "supports_cardio", "instructions", "safety_notes", "tags"
]

SPECS = [
    ("Walking in Place", "cardio", "march", "full_body", "beginner", "low", "none", "home|gym", 8, "low", "general_fitness|weight_management|endurance|cardio"),
    ("Brisk Walking in Place", "cardio", "march", "full_body", "intermediate", "moderate", "none", "home|gym", 10, "low", "general_fitness|weight_management|endurance|cardio"),
    ("Seated March", "cardio", "march", "legs", "beginner", "low", "chair", "home|gym", 6, "low", "general_fitness|endurance|cardio"),
    ("Seated Boxing", "cardio", "punch", "upper_body", "beginner", "moderate", "chair", "home|gym", 8, "low", "general_fitness|weight_management|endurance|cardio"),
    ("Shadow Boxing", "cardio", "punch", "upper_body", "intermediate", "moderate", "none", "home|gym|outdoors", 10, "low", "general_fitness|weight_management|endurance|cardio"),
    ("Low-Impact Step Jacks", "cardio", "lateral_step", "full_body", "beginner", "moderate", "none", "home|gym|outdoors", 8, "low", "general_fitness|weight_management|endurance|cardio"),
    ("Jumping Jacks", "cardio", "jump", "full_body", "intermediate", "high", "none", "home|gym|outdoors", 8, "jump|high", "general_fitness|weight_management|endurance|cardio"),
    ("Jump Rope", "cardio", "jump", "full_body", "intermediate", "high", "jump_rope", "home|gym|outdoors", 10, "jump|high", "weight_management|endurance|cardio"),
    ("High Knees", "cardio", "run", "full_body", "advanced", "high", "none", "home|gym|outdoors", 6, "jump|high", "weight_management|endurance|cardio"),
    ("Outdoor Easy Walk", "cardio", "walk", "full_body", "beginner", "low", "none", "outdoors", 20, "low", "general_fitness|weight_management|endurance|stress_reduction|cardio"),
    ("Outdoor Brisk Walk", "cardio", "walk", "full_body", "intermediate", "moderate", "none", "outdoors", 25, "low", "general_fitness|weight_management|endurance|cardio"),
    ("Treadmill Walk", "cardio", "walk", "full_body", "beginner", "low", "treadmill", "gym", 15, "low", "general_fitness|weight_management|endurance|cardio"),
    ("Treadmill Incline Walk", "cardio", "walk", "legs", "intermediate", "moderate", "treadmill", "gym", 15, "low", "weight_management|endurance|cardio"),
    ("Stationary Cycling", "cardio", "cycle", "legs", "beginner", "moderate", "stationary_bike", "gym", 15, "low", "general_fitness|weight_management|endurance|cardio"),
    ("Fast Stationary Cycling", "cardio", "cycle", "legs", "advanced", "high", "stationary_bike", "gym", 12, "low", "weight_management|endurance|cardio"),
    ("Step-Ups", "cardio", "step", "legs", "intermediate", "moderate", "step", "home|gym", 10, "single", "general_fitness|weight_management|strength|endurance|cardio"),
    ("Wall Push-Ups", "strength", "push", "chest", "beginner", "low", "wall", "home|gym", 8, "low", "general_fitness|strength|endurance"),
    ("Incline Bench Push-Ups", "strength", "push", "chest", "intermediate", "moderate", "bench", "gym", 8, "low", "general_fitness|strength|endurance"),
    ("Kneeling Push-Ups", "strength", "push", "chest", "intermediate", "moderate", "mat", "home|gym", 8, "kneel|floor", "strength|endurance"),
    ("Standard Push-Ups", "strength", "push", "chest", "advanced", "high", "none", "home|gym|outdoors", 8, "floor", "strength|endurance"),
    ("Chair Squats", "strength", "squat", "legs", "beginner", "low", "chair", "home|gym", 8, "low", "general_fitness|strength|endurance"),
    ("Bodyweight Squats", "strength", "squat", "legs", "intermediate", "moderate", "none", "home|gym|outdoors", 8, "deep", "general_fitness|weight_management|strength|endurance"),
    ("Goblet Squats", "strength", "squat", "legs", "intermediate", "moderate", "kettlebell", "home|gym", 10, "deep", "strength|endurance"),
    ("Dumbbell Front Squats", "strength", "squat", "legs", "advanced", "high", "dumbbells", "gym", 10, "deep", "strength|endurance"),
    ("Reverse Lunges", "strength", "lunge", "legs", "intermediate", "moderate", "none", "home|gym|outdoors", 8, "single", "general_fitness|strength|endurance"),
    ("Supported Reverse Lunges", "strength", "lunge", "legs", "beginner", "low", "chair", "home|gym", 8, "single|low", "general_fitness|strength"),
    ("Forward Lunges", "strength", "lunge", "legs", "intermediate", "moderate", "none", "home|gym|outdoors", 8, "single", "strength|endurance"),
    ("Dumbbell Romanian Deadlift", "strength", "hinge", "legs", "intermediate", "moderate", "dumbbells", "gym", 10, "low", "strength|endurance"),
    ("Kettlebell Deadlift", "strength", "hinge", "legs", "beginner", "moderate", "kettlebell", "home|gym", 10, "low", "general_fitness|strength"),
    ("Good Morning", "strength", "hinge", "back", "intermediate", "low", "none", "home|gym", 8, "low", "strength|mobility"),
    ("Standing Calf Raises", "strength", "calf_raise", "legs", "beginner", "low", "none", "home|gym|outdoors", 6, "low", "general_fitness|strength|endurance"),
    ("Single-Leg Calf Raises", "strength", "calf_raise", "legs", "intermediate", "moderate", "none", "home|gym", 7, "single", "strength|balance"),
    ("Resistance-Band Rows", "strength", "pull", "back", "beginner", "moderate", "resistance_band", "home|gym", 8, "low", "general_fitness|strength|endurance"),
    ("Seated Resistance-Band Rows", "strength", "pull", "back", "beginner", "low", "resistance_band|chair", "home|gym", 8, "low", "general_fitness|strength"),
    ("One-Arm Dumbbell Rows", "strength", "pull", "back", "intermediate", "moderate", "dumbbells|bench", "gym", 10, "low", "strength|endurance"),
    ("Dumbbell Biceps Curls", "strength", "curl", "arms", "beginner", "low", "dumbbells", "home|gym", 7, "low", "strength|endurance"),
    ("Resistance-Band Biceps Curls", "strength", "curl", "arms", "beginner", "low", "resistance_band", "home|gym", 7, "low", "strength|endurance"),
    ("Dumbbell Shoulder Press", "strength", "overhead_press", "shoulders", "intermediate", "moderate", "dumbbells", "home|gym", 8, "overhead", "strength|endurance"),
    ("Seated Dumbbell Shoulder Press", "strength", "overhead_press", "shoulders", "intermediate", "moderate", "dumbbells|chair", "home|gym", 8, "overhead", "strength"),
    ("Resistance-Band Chest Press", "strength", "push", "chest", "beginner", "low", "resistance_band", "home|gym", 8, "low", "general_fitness|strength"),
    ("Glute Bridges", "strength", "bridge", "hips", "beginner", "low", "mat", "home|gym", 8, "floor", "general_fitness|strength|mobility"),
    ("Single-Leg Glute Bridges", "strength", "bridge", "hips", "advanced", "moderate", "mat", "home|gym", 9, "floor|single", "strength|balance"),
    ("Standing Side Leg Raises", "strength", "abduction", "hips", "beginner", "low", "none", "home|gym", 7, "single|low", "general_fitness|strength|balance"),
    ("Resistance-Band Side Steps", "strength", "lateral_step", "hips", "intermediate", "moderate", "resistance_band", "home|gym", 8, "low", "general_fitness|strength|endurance"),
    ("Arm Circles", "mobility", "arm_circle", "shoulders", "beginner", "low", "none", "home|gym|outdoors", 4, "overhead|low", "general_fitness|mobility|stress_reduction"),
    ("Shoulder Rolls", "mobility", "shoulder_roll", "shoulders", "beginner", "low", "none", "home|gym|outdoors", 4, "low", "general_fitness|mobility|stress_reduction"),
    ("Standing Torso Rotations", "mobility", "rotation", "core", "beginner", "low", "none", "home|gym|outdoors", 5, "low", "general_fitness|mobility"),
    ("Standing Hip Circles", "mobility", "hip_circle", "hips", "beginner", "low", "none", "home|gym|outdoors", 5, "low", "general_fitness|mobility"),
    ("Ankle Circles", "mobility", "ankle_circle", "legs", "beginner", "low", "chair", "home|gym", 4, "single|low", "mobility|balance"),
    ("Cat-Cow Stretch", "mobility", "spinal_mobility", "back", "beginner", "low", "mat", "home|gym", 6, "kneel|floor", "mobility|flexibility|stress_reduction"),
    ("Bird Dog", "core", "cross_body", "core", "beginner", "low", "mat", "home|gym", 8, "kneel|floor", "general_fitness|strength|mobility|balance"),
    ("Dead Bug", "core", "cross_body", "core", "beginner", "low", "mat", "home|gym", 8, "floor", "general_fitness|strength|mobility"),
    ("Forearm Plank", "core", "plank", "core", "intermediate", "moderate", "mat", "home|gym", 6, "floor", "general_fitness|strength|endurance"),
    ("Kneeling Modified Plank", "core", "plank", "core", "beginner", "low", "mat", "home|gym", 6, "kneel|floor", "general_fitness|strength"),
    ("Side Plank", "core", "side_plank", "core", "advanced", "high", "mat", "home|gym", 6, "floor", "strength|balance|endurance"),
    ("Seated Knee Lifts", "core", "knee_lift", "core", "beginner", "low", "chair", "home|gym", 7, "low", "general_fitness|strength|endurance"),
    ("Standing Knee-to-Elbow", "core", "cross_body", "core", "intermediate", "moderate", "none", "home|gym|outdoors", 8, "single", "general_fitness|strength|balance|endurance"),
    ("Seated Hamstring Stretch", "flexibility", "hamstring_stretch", "legs", "beginner", "low", "chair", "home|gym", 6, "low", "flexibility|mobility|stress_reduction"),
    ("Standing Hamstring Stretch", "flexibility", "hamstring_stretch", "legs", "beginner", "low", "none", "home|gym|outdoors", 6, "low", "flexibility|mobility"),
    ("Standing Quadriceps Stretch", "flexibility", "quadriceps_stretch", "legs", "beginner", "low", "none", "home|gym|outdoors", 5, "single|low", "flexibility|mobility"),
    ("Wall Calf Stretch", "flexibility", "calf_stretch", "legs", "beginner", "low", "wall", "home|gym", 5, "low", "flexibility|mobility"),
    ("Doorway Chest Stretch", "flexibility", "chest_stretch", "chest", "beginner", "low", "wall", "home|gym", 5, "low", "flexibility|mobility|stress_reduction"),
    ("Cross-Body Shoulder Stretch", "flexibility", "shoulder_stretch", "shoulders", "beginner", "low", "none", "home|gym|outdoors", 5, "low", "flexibility|mobility|stress_reduction"),
    ("Overhead Triceps Stretch", "flexibility", "triceps_stretch", "arms", "beginner", "low", "none", "home|gym|outdoors", 5, "overhead|low", "flexibility|mobility"),
    ("Child's Pose", "flexibility", "spinal_stretch", "back", "beginner", "low", "mat", "home|gym", 6, "kneel|floor", "flexibility|mobility|stress_reduction"),
    ("Supine Figure-Four Stretch", "flexibility", "hip_stretch", "hips", "beginner", "low", "mat", "home|gym", 6, "floor", "flexibility|mobility|stress_reduction"),
    ("Standing Side Bend", "flexibility", "side_bend", "core", "beginner", "low", "none", "home|gym|outdoors", 5, "overhead|low", "flexibility|mobility"),
    ("Single-Leg Stand", "balance", "static_balance", "legs", "beginner", "low", "chair", "home|gym", 5, "single|low", "general_fitness|balance"),
    ("Tandem Stance", "balance", "static_balance", "legs", "beginner", "low", "none", "home|gym", 5, "low", "balance|mobility"),
    ("Heel-to-Toe Walk", "balance", "balance_walk", "legs", "intermediate", "low", "none", "home|gym|outdoors", 6, "single|low", "general_fitness|balance"),
    ("Lateral Weight Shifts", "balance", "weight_shift", "legs", "beginner", "low", "chair", "home|gym", 5, "single|low", "balance|mobility"),
    ("Clock Reach", "balance", "reach", "legs", "intermediate", "moderate", "none", "home|gym", 7, "single", "balance|strength"),
    ("Single-Leg Romanian Reach", "balance", "hinge", "legs", "advanced", "moderate", "none", "home|gym", 8, "single", "balance|strength"),
    ("Diaphragmatic Breathing", "relaxation", "breathing", "core", "beginner", "low", "none", "home|gym|outdoors", 5, "low", "stress_reduction|mobility"),
    ("Box Breathing", "relaxation", "breathing", "core", "beginner", "low", "none", "home|gym|outdoors", 5, "low", "stress_reduction"),
    ("Seated Body Scan", "relaxation", "body_scan", "full_body", "beginner", "low", "chair", "home|gym", 8, "low", "stress_reduction"),
    ("Standing Shake-Out", "relaxation", "shake", "full_body", "beginner", "low", "none", "home|gym|outdoors", 4, "low", "general_fitness|stress_reduction"),
    ("Supine Relaxation", "relaxation", "rest", "full_body", "beginner", "low", "mat", "home|gym", 8, "floor", "stress_reduction|flexibility"),
    ("Seated Neck Release", "relaxation", "neck_mobility", "upper_body", "beginner", "low", "chair", "home|gym", 5, "low", "mobility|flexibility|stress_reduction"),
    ("Wall Angels", "mobility", "wall_slide", "upper_body", "beginner", "low", "wall", "home|gym", 7, "overhead|low", "general_fitness|mobility|strength"),
]


def make_row(index: int, spec: tuple) -> dict:
    name, category, pattern, primary, level, intensity, equipment, locations, duration, flags_text, goals_text = spec
    flags = set(flags_text.split("|"))
    goals = set(goals_text.split("|"))
    secondary = {"full_body": "upper_body|lower_body", "upper_body": "arms|shoulders", "lower_body": "hips|legs", "chest": "upper_body|arms", "back": "upper_body|core", "shoulders": "upper_body|arms", "arms": "upper_body|shoulders", "hips": "lower_body|core", "legs": "lower_body|hips", "core": "back|full_body"}[primary]
    attributes = {value: category == value for value in ["cardio", "strength", "mobility", "flexibility", "balance", "core", "relaxation"]}
    row = {
        "exercise_id": f"EX{index:03d}",
        "name": name,
        "description": f"A {intensity}-intensity {category} exercise focused on {primary.replace('_', ' ')} movement.",
        "category": category,
        "movement_pattern": pattern,
        "primary_body_area": primary,
        "secondary_body_areas": secondary,
        "difficulty": level,
        "intensity": intensity,
        "equipment": equipment,
        "workout_locations": locations,
        "space_requirement": "large" if "jump" in flags or pattern in {"walk", "jump_rope"} else "small",
        "estimated_duration_minutes": duration,
        "recommended_repetitions": "30-60 seconds" if category in {"cardio", "mobility", "flexibility", "balance", "relaxation"} else "8-12 repetitions",
        "recommended_sets": "1-2 rounds" if level == "beginner" else "2-3 rounds",
        "beginner_friendly": level == "beginner",
        "low_impact": "low" in flags,
        "involves_jumping": "jump" in flags,
        "involves_kneeling": "kneel" in flags,
        "involves_overhead_movement": "overhead" in flags,
        "involves_floor_position": "floor" in flags,
        "involves_deep_squat": "deep" in flags,
        "involves_single_leg_balance": "single" in flags,
        "high_impact": "high" in flags,
        **attributes,
        "supports_general_fitness": "general_fitness" in goals,
        "supports_weight_management": "weight_management" in goals,
        "supports_strength": "strength" in goals,
        "supports_endurance": "endurance" in goals,
        "supports_mobility": "mobility" in goals,
        "supports_flexibility": "flexibility" in goals,
        "supports_stress_reduction": "stress_reduction" in goals,
        "supports_cardio": "cardio" in goals,
        "instructions": f"Perform {name.lower()} with controlled movement and stop if the motion feels unsafe or painful.",
        "safety_notes": "Use a stable surface, keep a comfortable range of motion, and seek professional advice when unsure.",
        "tags": f"{category}|{pattern}|{primary}|{intensity}",
    }
    return row


def main() -> None:
    rows = [make_row(index, spec) for index, spec in enumerate(SPECS, start=1)]
    path = Path(__file__).with_name("exercises.csv")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} synthetic exercises to {path}")


if __name__ == "__main__":
    main()
