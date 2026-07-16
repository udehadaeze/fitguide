from collections import Counter

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from app.config import BODY_AREAS, CATEGORIES, EQUIPMENT, GOALS, INTENSITIES, LEVEL_ORDER, LOCATIONS, SCORE_WEIGHTS
from app.models import Exercise, ProcessedProfile, Recommendation, RecommendationResponse, UserProfile
from app.repository import load_exercises

RESTRICTION_COLUMNS = {
    "avoid_jumping": "involves_jumping",
    "avoid_kneeling": "involves_kneeling",
    "avoid_overhead_movements": "involves_overhead_movement",
    "avoid_floor_exercises": "involves_floor_position",
    "avoid_high_impact": "high_impact",
    "avoid_deep_squats": "involves_deep_squat",
    "avoid_single_leg_balance": "involves_single_leg_balance",
}


def filter_exercises(frame: pd.DataFrame, profile: UserProfile) -> pd.DataFrame:
    eligible = frame.copy()
    avoided = {name.casefold() for name in profile.exercises_to_avoid}
    if avoided:
        eligible = eligible[~eligible["name"].str.casefold().isin(avoided)]
    for restriction in profile.movement_restrictions:
        eligible = eligible[~eligible[RESTRICTION_COLUMNS[restriction]]]
    if profile.low_impact_required:
        eligible = eligible[eligible["low_impact"]]
    available = set(profile.available_equipment) | {"none"}
    eligible = eligible[eligible["equipment"].map(lambda items: set(items).issubset(available))]
    if profile.workout_location != "any":
        eligible = eligible[eligible["workout_locations"].map(lambda items: profile.workout_location in items or "any" in items)]
    level = LEVEL_ORDER[profile.fitness_level]
    eligible = eligible[eligible["difficulty"].map(lambda value: LEVEL_ORDER[value] <= level)]
    eligible = eligible[eligible["estimated_duration_minutes"] <= profile.preferred_duration_minutes]
    return eligible.reset_index(drop=True)


def feature_names() -> list[str]:
    names = [f"goal:{value}" for value in GOALS]
    names += [f"category:{value}" for value in CATEGORIES]
    names += [f"body:{value}" for value in BODY_AREAS]
    names += [f"intensity:{value}" for value in INTENSITIES]
    names += [f"level:{value}" for value in LEVEL_ORDER]
    names += [f"equipment:{value}" for value in EQUIPMENT]
    names += [f"location:{value}" for value in LOCATIONS if value != "any"]
    names += ["attribute:low_impact", "attribute:duration_fit"]
    return names


def profile_vector(profile: UserProfile) -> np.ndarray:
    values: dict[str, float] = {name: 0.0 for name in feature_names()}
    values[f"goal:{profile.goal}"] = 1.0
    for category in profile.preferred_categories:
        values[f"category:{category}"] = 1.0
    for area in profile.target_body_areas:
        values[f"body:{area}"] = 1.0
    values[f"intensity:{profile.preferred_intensity}"] = 1.0
    values[f"level:{profile.fitness_level}"] = 1.0
    for item in set(profile.available_equipment) | {"none"}:
        values[f"equipment:{item}"] = 1.0
    if profile.workout_location != "any":
        values[f"location:{profile.workout_location}"] = 1.0
    if profile.low_impact_required:
        values["attribute:low_impact"] = 1.0
    values["attribute:duration_fit"] = 1.0
    return np.array([values[name] for name in feature_names()], dtype=float)


def exercise_vector(row: pd.Series, profile: UserProfile) -> np.ndarray:
    values: dict[str, float] = {name: 0.0 for name in feature_names()}
    for goal in GOALS:
        values[f"goal:{goal}"] = float(row[f"supports_{goal.replace('cardiovascular_fitness', 'cardio')}"])
    values[f"category:{row['category']}"] = 1.0
    values[f"body:{row['primary_body_area']}"] = 1.0
    for area in row["secondary_body_areas"]:
        key = f"body:{area}"
        if key in values:
            values[key] = 1.0
    values[f"intensity:{row['intensity']}"] = 1.0
    values[f"level:{row['difficulty']}"] = 1.0
    for item in row["equipment"]:
        values[f"equipment:{item}"] = 1.0
    for location in row["workout_locations"]:
        key = f"location:{location}"
        if key in values:
            values[key] = 1.0
    values["attribute:low_impact"] = float(row["low_impact"])
    values["attribute:duration_fit"] = max(0.0, 1.0 - abs(row["estimated_duration_minutes"] - profile.preferred_duration_minutes) / profile.preferred_duration_minutes)
    return np.array([values[name] for name in feature_names()], dtype=float)


def match_details(row: pd.Series, profile: UserProfile) -> tuple[dict[str, float], list[str]]:
    goal_column = f"supports_{profile.goal.replace('cardiovascular_fitness', 'cardio')}"
    category_match = float(row["category"] in profile.preferred_categories)
    areas = {row["primary_body_area"], *row["secondary_body_areas"]}
    body_match = len(areas & set(profile.target_body_areas)) / len(set(profile.target_body_areas))
    intensity_match = float(row["intensity"] == profile.preferred_intensity)
    level_gap = abs(LEVEL_ORDER[row["difficulty"]] - LEVEL_ORDER[profile.fitness_level])
    level_fit = max(0.0, 1.0 - 0.5 * level_gap)
    duration_fit = max(0.0, 1.0 - abs(row["estimated_duration_minutes"] - profile.preferred_duration_minutes) / profile.preferred_duration_minutes)
    location_match = float(profile.workout_location == "any" or profile.workout_location in row["workout_locations"])
    equipment_match = float(set(row["equipment"]) == {"none"} or bool(set(row["equipment"]) & set(profile.available_equipment)))
    parts = {
        "goal": float(row[goal_column]),
        "category": category_match,
        "body_area": body_match,
        "intensity": intensity_match,
        "level": level_fit,
        "duration": duration_fit,
        "location": location_match,
        "equipment": equipment_match,
    }
    matches: list[str] = []
    if parts["goal"]:
        matches.append(f"supports {profile.goal.replace('_', ' ')}")
    if category_match:
        matches.append(f"matches the {row['category']} preference")
    if body_match:
        matched_areas = sorted(areas & set(profile.target_body_areas))
        matches.append(f"targets {', '.join(area.replace('_', ' ') for area in matched_areas)}")
    if intensity_match:
        matches.append(f"matches {profile.preferred_intensity} intensity")
    if row["difficulty"] == profile.fitness_level:
        matches.append(f"matches {profile.fitness_level} level")
    if profile.low_impact_required and row["low_impact"]:
        matches.append("meets the low-impact requirement")
    if duration_fit >= 0.75:
        matches.append("fits the preferred time")
    if location_match:
        matches.append(f"works at {profile.workout_location}" if profile.workout_location != "any" else "works in the selected setting")
    if equipment_match:
        matches.append("uses available equipment")
    return parts, matches


def score_exercises(eligible: pd.DataFrame, profile: UserProfile) -> list[dict]:
    if eligible.empty:
        return []
    user = profile_vector(profile).reshape(1, -1)
    items = np.vstack([exercise_vector(row, profile) for _, row in eligible.iterrows()])
    similarities = cosine_similarity(user, items)[0]
    scored: list[dict] = []
    for index, (_, row) in enumerate(eligible.iterrows()):
        parts, matches = match_details(row, profile)
        score = SCORE_WEIGHTS["cosine"] * similarities[index]
        score += sum(SCORE_WEIGHTS[key] * value for key, value in parts.items())
        scored.append({"row": row, "score": round(float(score), 4), "matched_features": matches})
    return sorted(scored, key=lambda item: (-item["score"], item["row"]["exercise_id"]))


def preferred_roles(goal: str) -> list[tuple[str, set[str]]]:
    if goal in {"mobility", "flexibility"}:
        return [("prepare", {"mobility"}), ("develop", {"mobility", "flexibility"}), ("develop", {"mobility", "flexibility"}), ("balance", {"balance", "core"}), ("recover", {"flexibility", "relaxation"})]
    if goal == "strength":
        return [("prepare", {"mobility"}), ("primary", {"strength"}), ("primary", {"strength"}), ("support", {"core", "balance"}), ("recover", {"flexibility", "relaxation"})]
    if goal in {"endurance", "cardiovascular_fitness", "weight_management"}:
        return [("prepare", {"mobility"}), ("primary", {"cardio"}), ("primary", {"cardio", "strength"}), ("support", {"core", "strength"}), ("recover", {"flexibility", "relaxation"})]
    if goal == "stress_reduction":
        return [("prepare", {"mobility"}), ("move", {"cardio", "mobility"}), ("release", {"flexibility"}), ("steady", {"balance", "core"}), ("recover", {"relaxation"})]
    return [("prepare", {"mobility"}), ("energise", {"cardio"}), ("strengthen", {"strength"}), ("stabilise", {"core", "balance"}), ("recover", {"flexibility", "relaxation"})]


def diversify(scored: list[dict], profile: UserProfile) -> list[tuple[dict, str]]:
    selected: list[tuple[dict, str]] = []
    used_ids: set[str] = set()
    category_counts: Counter[str] = Counter()
    pattern_counts: Counter[str] = Counter()
    roles = preferred_roles(profile.goal)[: profile.maximum_recommendations]
    for role, categories in roles:
        choice = next((item for item in scored if item["row"]["exercise_id"] not in used_ids and item["row"]["category"] in categories and category_counts[item["row"]["category"]] < 2 and pattern_counts[item["row"]["movement_pattern"]] < 2), None)
        if choice is None:
            choice = next((item for item in scored if item["row"]["exercise_id"] not in used_ids and category_counts[item["row"]["category"]] < 2 and pattern_counts[item["row"]["movement_pattern"]] < 2), None)
        if choice is None:
            choice = next((item for item in scored if item["row"]["exercise_id"] not in used_ids), None)
        if choice is None:
            break
        selected.append((choice, role))
        used_ids.add(choice["row"]["exercise_id"])
        category_counts[choice["row"]["category"]] += 1
        pattern_counts[choice["row"]["movement_pattern"]] += 1
    return selected


def row_to_exercise(row: pd.Series) -> dict:
    fields = Exercise.model_fields.keys()
    return {field: row[field] for field in fields}


def recommend(profile: UserProfile) -> RecommendationResponse:
    eligible = filter_exercises(load_exercises(), profile)
    selected = diversify(score_exercises(eligible, profile), profile)
    recommendations: list[Recommendation] = []
    for position, (item, role) in enumerate(selected, start=1):
        matches = item["matched_features"]
        explanation = "Recommended because it " + ", ".join(matches[:4]) + "." if matches else "Recommended as the closest compatible catalogue item."
        recommendations.append(Recommendation(**row_to_exercise(item["row"]), score=item["score"], matched_features=matches, explanation=explanation, routine_position=position, routine_role=role))
    warning = None
    if not recommendations:
        warning = "No exercises satisfy every hard restriction. Change one or more preferences and try again."
    elif len(recommendations) < profile.maximum_recommendations:
        warning = "The compatible catalogue could not provide the requested number without relaxing hard restrictions."
    processed = ProcessedProfile(goal=profile.goal, fitness_level=profile.fitness_level, workout_location=profile.workout_location, preferred_duration_minutes=profile.preferred_duration_minutes, preferred_intensity=profile.preferred_intensity, hard_restrictions_applied=profile.movement_restrictions)
    return RecommendationResponse(processed_profile=processed, recommendations=recommendations, eligible_count=len(eligible), warning=warning)

