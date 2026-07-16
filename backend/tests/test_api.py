def valid_payload() -> dict:
    return {"goal": "general_fitness", "fitness_level": "beginner", "workout_location": "home", "available_equipment": ["none", "chair"], "preferred_duration_minutes": 10, "preferred_intensity": "low", "preferred_categories": ["cardio", "mobility"], "target_body_areas": ["full_body"], "movement_restrictions": ["avoid_jumping"], "exercises_to_avoid": [], "low_impact_required": True, "maximum_recommendations": 5}


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "exercise_count": 80}


def test_metadata_endpoint(client):
    response = client.get("/metadata")
    assert response.status_code == 200
    assert "avoid_jumping" in response.json()["movement_restrictions"]


def test_recommendation_endpoint(client):
    response = client.post("/recommendations", json=valid_payload())
    assert response.status_code == 200
    assert len(response.json()["recommendations"]) == 5


def test_invalid_request_is_rejected(client):
    payload = valid_payload()
    payload["fitness_level"] = "expert"
    response = client.post("/recommendations", json=payload)
    assert response.status_code == 422
    assert "traceback" not in response.text.lower()


def test_exercise_filters_reject_unsupported_value(client):
    response = client.get("/exercises?category=medical")
    assert response.status_code == 422


def test_feedback_accepts_available_exercise(client):
    response = client.post("/feedback", json={"exercise_id": "EX001", "feedback_type": "like"})
    assert response.status_code == 200
    assert response.json()["accepted"] is True


def test_feedback_rejects_unavailable_exercise(client):
    response = client.post("/feedback", json={"exercise_id": "EX999", "feedback_type": "unsuitable"})
    assert response.status_code == 404

