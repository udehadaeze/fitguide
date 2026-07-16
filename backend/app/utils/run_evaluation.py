import csv
import json
import platform
import statistics
import time
from collections import Counter
from pathlib import Path

from fastapi.testclient import TestClient

from app.config import LEVEL_ORDER
from app.main import app
from app.models import UserProfile
from app.recommender import RESTRICTION_COLUMNS, match_details, recommend
from app.repository import load_exercises

ROOT = Path(__file__).resolve().parents[3]
EVALUATION_DIR = ROOT / "evaluation"
PROFILES_PATH = EVALUATION_DIR / "test_profiles.json"
RESULTS_PATH = EVALUATION_DIR / "evaluation_results.csv"
SUMMARY_PATH = EVALUATION_DIR / "evaluation_summary.json"
REPORT_PATH = EVALUATION_DIR / "evaluation_report.md"


def record_for(exercise_id: str):
    frame = load_exercises()
    return frame[frame["exercise_id"] == exercise_id].iloc[0]


def constraint_compliant(row, profile: UserProfile) -> bool:
    if row["name"].casefold() in {name.casefold() for name in profile.exercises_to_avoid}:
        return False
    if any(row[RESTRICTION_COLUMNS[value]] for value in profile.movement_restrictions):
        return False
    if profile.low_impact_required and not row["low_impact"]:
        return False
    if not set(row["equipment"]).issubset(set(profile.available_equipment) | {"none"}):
        return False
    if profile.workout_location != "any" and profile.workout_location not in row["workout_locations"] and "any" not in row["workout_locations"]:
        return False
    if LEVEL_ORDER[row["difficulty"]] > LEVEL_ORDER[profile.fitness_level]:
        return False
    return row["estimated_duration_minutes"] <= profile.preferred_duration_minutes


def relevant(profile_id: str, row, profile: UserProfile) -> bool:
    areas = {row["primary_body_area"], *row["secondary_body_areas"]}
    available = set(profile.available_equipment) | {"none"}
    setting = profile.workout_location == "any" or profile.workout_location in row["workout_locations"] or "any" in row["workout_locations"]
    if profile_id == "P01":
        return row["difficulty"] == "beginner" and row["low_impact"] and setting and set(row["equipment"]).issubset(available) and not row["involves_jumping"] and row["supports_general_fitness"]
    if profile_id == "P02":
        return LEVEL_ORDER[row["difficulty"]] <= LEVEL_ORDER["intermediate"] and setting and set(row["equipment"]).issubset(available) and bool(areas & {"upper_body", "core"}) and row["category"] in {"strength", "core"} and row["supports_strength"]
    if profile_id == "P03":
        return setting and set(row["equipment"]).issubset(available) and LEVEL_ORDER[row["difficulty"]] <= LEVEL_ORDER["intermediate"] and row["supports_cardio"] and row["category"] == "cardio"
    if profile_id == "P04":
        return row["difficulty"] == "beginner" and row["low_impact"] and not row["involves_floor_position"] and not row["involves_kneeling"] and setting and row["category"] in {"mobility", "flexibility"} and bool(areas & set(profile.target_body_areas))
    if profile_id == "P05":
        return not row["involves_overhead_movement"] and not row["involves_single_leg_balance"] and row["name"] != "Walking in Place" and setting and set(row["equipment"]).issubset(available) and row["category"] in set(profile.preferred_categories)
    if profile_id == "P06":
        return row["low_impact"] and row["category"] in {"relaxation", "flexibility", "mobility"} and row["supports_stress_reduction"]
    if profile_id == "P07":
        return not row["involves_jumping"] and not row["high_impact"] and setting and set(row["equipment"]).issubset(available) and row["supports_endurance"] and row["category"] in {"cardio", "strength"}
    return False


def goal_relevant(row, profile: UserProfile) -> bool:
    column = f"supports_{profile.goal.replace('cardiovascular_fitness', 'cardio')}"
    return bool(row[column])


def explanation_consistent(row, profile: UserProfile, matched_features: list[str], explanation: str) -> bool:
    _, expected = match_details(row, profile)
    return matched_features == expected and all(feature in explanation for feature in expected[:4])


def diversity(items: list) -> tuple[float, float, float, float]:
    count = len(items)
    if not count:
        return 0.0, 0.0, 0.0, 0.0
    category = len({item.category for item in items}) / count
    pattern = len({item.movement_pattern for item in items}) / count
    roles = len({item.routine_role for item in items}) / count
    body_areas = set()
    for item in items:
        body_areas.add(item.primary_body_area)
        body_areas.update(item.secondary_body_areas)
    body = min(1.0, len(body_areas) / count)
    return category, body, pattern, roles


def time_endpoint(client: TestClient, profile: UserProfile, repeats: int = 50) -> list[float]:
    payload = profile.model_dump()
    client.post("/recommendations", json=payload)
    timings = []
    for _ in range(repeats):
        start = time.perf_counter()
        response = client.post("/recommendations", json=payload)
        elapsed = (time.perf_counter() - start) * 1000
        if response.status_code != 200:
            raise RuntimeError(f"Timing request failed with status {response.status_code}")
        timings.append(elapsed)
    return timings


def main() -> None:
    profile_entries = json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
    client = TestClient(app)
    raw_rows = []
    profile_rows = []
    all_ids = set()
    all_timings = []
    total_returned = 0
    total_relevant = 0
    total_compliant = 0
    total_goal_relevant = 0
    total_explanations = 0
    total_consistent = 0
    deterministic_profiles = 0
    precision_profiles = []

    for entry in profile_entries:
        profile_id = entry["profile_id"]
        profile = UserProfile(**entry["profile"])
        result = recommend(profile)
        repeated = [recommend(profile) for _ in range(3)]
        signature = [(item.exercise_id, item.score, item.routine_role) for item in result.recommendations]
        deterministic = all([(item.exercise_id, item.score, item.routine_role) for item in other.recommendations] == signature for other in repeated)
        deterministic_profiles += int(deterministic)
        category_diversity, body_diversity, pattern_diversity, role_diversity = diversity(result.recommendations)
        profile_relevant = 0
        profile_compliant = 0
        profile_goal = 0
        profile_consistent = 0

        for item in result.recommendations:
            row = record_for(item.exercise_id)
            compliant = constraint_compliant(row, profile)
            is_relevant = relevant(profile_id, row, profile)
            is_goal_relevant = goal_relevant(row, profile)
            is_consistent = explanation_consistent(row, profile, item.matched_features, item.explanation)
            profile_relevant += int(is_relevant)
            profile_compliant += int(compliant)
            profile_goal += int(is_goal_relevant)
            profile_consistent += int(is_consistent)
            all_ids.add(item.exercise_id)
            raw_rows.append({"profile_id": profile_id, "profile_label": entry["label"], "routine_position": item.routine_position, "routine_role": item.routine_role, "exercise_id": item.exercise_id, "exercise_name": item.name, "score": item.score, "constraint_compliant": compliant, "predefined_relevant": is_relevant, "goal_relevant": is_goal_relevant, "explanation_consistent": is_consistent, "category": item.category, "primary_body_area": item.primary_body_area, "movement_pattern": item.movement_pattern})

        returned = len(result.recommendations)
        precision = profile_relevant / returned if returned and profile_id != "P08" else None
        if precision is not None:
            precision_profiles.append(precision)
        timings = time_endpoint(client, profile)
        all_timings.extend(timings)
        total_returned += returned
        total_relevant += profile_relevant
        total_compliant += profile_compliant
        total_goal_relevant += profile_goal
        total_explanations += returned
        total_consistent += profile_consistent
        profile_rows.append({"profile_id": profile_id, "label": entry["label"], "returned": returned, "eligible_count": result.eligible_count, "relevant": profile_relevant, "precision_at_5": precision, "constraint_satisfaction": profile_compliant / returned if returned else 1.0, "goal_relevance": profile_goal / returned if returned else None, "category_diversity": category_diversity, "body_area_diversity": body_diversity, "movement_pattern_diversity": pattern_diversity, "routine_role_diversity": role_diversity, "explanation_consistency": profile_consistent / returned if returned else 1.0, "deterministic": deterministic, "mean_response_ms": statistics.mean(timings), "median_response_ms": statistics.median(timings), "min_response_ms": min(timings), "max_response_ms": max(timings), "warning": result.warning})

    fieldnames = list(raw_rows[0].keys())
    with RESULTS_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(raw_rows)

    summary = {
        "evaluation_date": "2026-07-15",
        "catalogue_size": len(load_exercises()),
        "profiles": len(profile_entries),
        "recommendations_returned": total_returned,
        "micro_precision_at_5": total_relevant / total_returned if total_returned else 0.0,
        "macro_precision_at_5": statistics.mean(precision_profiles),
        "constraint_satisfaction": total_compliant / total_returned if total_returned else 1.0,
        "goal_relevance": total_goal_relevant / total_returned if total_returned else 0.0,
        "catalogue_coverage": len(all_ids) / len(load_exercises()),
        "unique_exercises_recommended": len(all_ids),
        "mean_category_diversity": statistics.mean(row["category_diversity"] for row in profile_rows if row["returned"]),
        "mean_body_area_diversity": statistics.mean(row["body_area_diversity"] for row in profile_rows if row["returned"]),
        "mean_movement_pattern_diversity": statistics.mean(row["movement_pattern_diversity"] for row in profile_rows if row["returned"]),
        "mean_routine_role_diversity": statistics.mean(row["routine_role_diversity"] for row in profile_rows if row["returned"]),
        "explanation_consistency": total_consistent / total_explanations if total_explanations else 1.0,
        "deterministic_profiles": deterministic_profiles,
        "timed_requests": len(all_timings),
        "mean_response_ms": statistics.mean(all_timings),
        "median_response_ms": statistics.median(all_timings),
        "min_response_ms": min(all_timings),
        "max_response_ms": max(all_timings),
        "environment": {"platform": platform.platform(), "python": platform.python_version(), "processor": platform.processor() or "not reported"},
        "profile_results": profile_rows,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    REPORT_PATH.write_text(report(summary), encoding="utf-8")
    print(json.dumps(summary, indent=2))


def percentage(value: float | None) -> str:
    return "Not applicable" if value is None else f"{value * 100:.2f}%"


def report(summary: dict) -> str:
    rows = []
    for item in summary["profile_results"]:
        rows.append(f"| {item['profile_id']} | {item['returned']} | {percentage(item['precision_at_5'])} | {percentage(item['constraint_satisfaction'])} | {percentage(item['goal_relevance'])} | {item['mean_response_ms']:.3f} |")
    table = "\n".join(rows)
    return f"""# FitGuide Offline Evaluation Report

## Method

Eight profiles and their relevance conditions were fixed before this evaluation. Seven profiles represent different goals, settings, equipment and restrictions. P08 is deliberately over-constrained and is evaluated for correct empty-result handling rather than Precision@5. All relevance judgements are derived from the synthetic catalogue fields, so the evaluation measures internal prototype behaviour rather than clinical suitability or user benefit.

Constraint satisfaction checks every returned item against movement restrictions, low-impact need, equipment, location, fitness level, item duration and explicit name exclusions. Precision@5 uses each profile's predefined relevance predicate. Coverage is the proportion of the 80-item catalogue appearing at least once. Category, body-area, movement-pattern and routine-role diversity divide distinct values by list length, with body diversity capped at one. Explanation consistency recomputes matched features and verifies the clauses used in the displayed explanation.

Timing used FastAPI TestClient. Each profile received one warm-up request followed by 50 measured requests, giving {summary['timed_requests']} measurements. This includes validation, filtering, vector construction, ranking, diversification, explanation generation and in-process HTTP handling. It excludes a real network, browser rendering, concurrency, server start-up and deployment overhead.

## Results

| Profile | Returned | Precision@5 | Constraint satisfaction | Goal relevance | Mean response (ms) |
|---|---:|---:|---:|---:|---:|
{table}

Across {summary['recommendations_returned']} returned recommendations, hard-constraint satisfaction was {percentage(summary['constraint_satisfaction'])}. Micro Precision@5 was {summary['micro_precision_at_5']:.4f} and macro Precision@5 across the seven non-empty evaluation profiles was {summary['macro_precision_at_5']:.4f}. Goal relevance was {percentage(summary['goal_relevance'])}. The routines surfaced {summary['unique_exercises_recommended']} of 80 catalogue exercises, corresponding to {percentage(summary['catalogue_coverage'])} coverage.

Mean category diversity was {summary['mean_category_diversity']:.4f}, mean body-area diversity was {summary['mean_body_area_diversity']:.4f}, mean movement-pattern diversity was {summary['mean_movement_pattern_diversity']:.4f}, and mean routine-role diversity was {summary['mean_routine_role_diversity']:.4f}. Explanation consistency was {percentage(summary['explanation_consistency'])}. All {summary['deterministic_profiles']} profiles produced identical IDs, scores and roles in repeated direct runs.

Across {summary['timed_requests']} timed in-process requests, mean response time was {summary['mean_response_ms']:.3f} ms, median was {summary['median_response_ms']:.3f} ms, minimum was {summary['min_response_ms']:.3f} ms and maximum was {summary['max_response_ms']:.3f} ms. The measured environment was {summary['environment']['platform']} with Python {summary['environment']['python']}.

## Interpretation and limitations

Constraint satisfaction shows that the implemented rule set behaved consistently for these profiles. It must not be described as clinical safety validation because the rules and catalogue labels are simplified and synthetic. Precision@5 measures agreement with manually defined field predicates that overlap with the ranking features, which makes the result partly circular. Coverage depends strongly on the small profile set, while the diversity ratios represent catalogue variation rather than perceived variety.

No real user judged usefulness, novelty, serendipity, trust or satisfaction. Recall, MRR and NDCG are not reported because there is no independent interaction history, complete relevance set or graded ground truth. Timing is a local in-process prototype measure and cannot predict deployed performance. These results support claims about reproducibility and encoded behaviour only.
"""


if __name__ == "__main__":
    main()
