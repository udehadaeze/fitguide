from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import BODY_AREAS, CATEGORIES, EQUIPMENT, GOALS, INTENSITIES, LEVELS, LOCATIONS, RESTRICTIONS
from app.models import FeedbackRequest, FeedbackResponse, UserProfile
from app.recommender import recommend
from app.repository import exercise_exists, load_exercises

app = FastAPI(title="FitGuide Recommender API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
feedback_store: list[dict] = []


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "exercise_count": len(load_exercises())}


@app.get("/metadata")
def metadata() -> dict:
    return {"goals": GOALS, "levels": LEVELS, "categories": CATEGORIES, "body_areas": BODY_AREAS, "equipment": EQUIPMENT, "locations": LOCATIONS, "intensities": INTENSITIES, "movement_restrictions": RESTRICTIONS}


@app.get("/exercises")
def exercises(category: str | None = Query(default=None), difficulty: str | None = Query(default=None), location: str | None = Query(default=None)) -> list[dict]:
    frame = load_exercises()
    if category:
        if category not in CATEGORIES:
            raise HTTPException(status_code=422, detail="Unsupported category")
        frame = frame[frame["category"] == category]
    if difficulty:
        if difficulty not in LEVELS:
            raise HTTPException(status_code=422, detail="Unsupported difficulty")
        frame = frame[frame["difficulty"] == difficulty]
    if location:
        if location not in LOCATIONS:
            raise HTTPException(status_code=422, detail="Unsupported location")
        if location != "any":
            frame = frame[frame["workout_locations"].map(lambda values: location in values or "any" in values)]
    return frame.to_dict(orient="records")


@app.post("/recommendations")
def recommendations(profile: UserProfile):
    return recommend(profile)


@app.get("/recommendations/example")
def example():
    profile = UserProfile(goal="general_fitness", fitness_level="beginner", workout_location="home", available_equipment=["none", "chair"], preferred_duration_minutes=10, preferred_intensity="low", preferred_categories=["cardio", "strength", "mobility"], target_body_areas=["full_body"], movement_restrictions=["avoid_jumping"], low_impact_required=True, maximum_recommendations=5)
    return {"profile": profile, "result": recommend(profile)}


@app.post("/feedback", response_model=FeedbackResponse)
def feedback(request: FeedbackRequest) -> FeedbackResponse:
    if not exercise_exists(request.exercise_id):
        raise HTTPException(status_code=404, detail="Exercise ID not found")
    feedback_store.append(request.model_dump())
    return FeedbackResponse(accepted=True, message="Anonymous feedback recorded for this server session.")

