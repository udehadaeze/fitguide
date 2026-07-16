from typing import Literal

from pydantic import BaseModel, Field, field_validator

from app.config import BODY_AREAS, CATEGORIES, EQUIPMENT, GOALS, INTENSITIES, LEVELS, LOCATIONS, RESTRICTIONS


class UserProfile(BaseModel):
    goal: Literal[*GOALS]
    fitness_level: Literal[*LEVELS]
    workout_location: Literal[*LOCATIONS]
    available_equipment: list[Literal[*EQUIPMENT]] = Field(default_factory=lambda: ["none"])
    preferred_duration_minutes: int = Field(ge=3, le=60)
    preferred_intensity: Literal[*INTENSITIES]
    preferred_categories: list[Literal[*CATEGORIES]] = Field(min_length=1)
    target_body_areas: list[Literal[*BODY_AREAS]] = Field(min_length=1)
    movement_restrictions: list[Literal[*RESTRICTIONS]] = Field(default_factory=list)
    exercises_to_avoid: list[str] = Field(default_factory=list, max_length=20)
    low_impact_required: bool = False
    maximum_recommendations: int = Field(default=5, ge=1, le=8)

    @field_validator("available_equipment", "preferred_categories", "target_body_areas", "movement_restrictions")
    @classmethod
    def unique_values(cls, values: list[str]) -> list[str]:
        return list(dict.fromkeys(values))

    @field_validator("exercises_to_avoid")
    @classmethod
    def clean_exclusions(cls, values: list[str]) -> list[str]:
        cleaned = [value.strip() for value in values if value.strip()]
        return list(dict.fromkeys(cleaned))


class Exercise(BaseModel):
    exercise_id: str
    name: str
    description: str
    category: str
    movement_pattern: str
    primary_body_area: str
    secondary_body_areas: list[str]
    difficulty: str
    intensity: str
    equipment: list[str]
    workout_locations: list[str]
    space_requirement: str
    estimated_duration_minutes: int
    recommended_repetitions: str
    recommended_sets: str
    beginner_friendly: bool
    low_impact: bool
    instructions: str
    safety_notes: str
    tags: list[str]


class Recommendation(Exercise):
    score: float
    matched_features: list[str]
    explanation: str
    routine_position: int
    routine_role: str


class ProcessedProfile(BaseModel):
    goal: str
    fitness_level: str
    workout_location: str
    preferred_duration_minutes: int
    preferred_intensity: str
    hard_restrictions_applied: list[str]


class RecommendationResponse(BaseModel):
    processed_profile: ProcessedProfile
    recommendations: list[Recommendation]
    eligible_count: int
    warning: str | None = None


class FeedbackRequest(BaseModel):
    exercise_id: str
    feedback_type: Literal["like", "dislike", "unsuitable"]
    session_id: str | None = Field(default=None, max_length=80)
    reason: str | None = Field(default=None, max_length=300)


class FeedbackResponse(BaseModel):
    accepted: bool
    message: str

