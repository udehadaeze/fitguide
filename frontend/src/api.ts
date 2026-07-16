import type { Metadata, RecommendationResponse, UserProfile } from "./types"

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000"

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, options)
  if (!response.ok) {
    let message = "The service could not complete this request."
    try {
      const payload = await response.json()
      if (typeof payload.detail === "string") message = payload.detail
    } catch {
      message = "The service returned an unreadable response."
    }
    throw new Error(message)
  }
  return response.json() as Promise<T>
}

export function getMetadata(): Promise<Metadata> {
  return request<Metadata>("/metadata")
}

export function getRecommendations(profile: UserProfile): Promise<RecommendationResponse> {
  return request<RecommendationResponse>("/recommendations", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile)
  })
}

export function sendFeedback(exerciseId: string, feedbackType: "like" | "dislike" | "unsuitable"): Promise<{ accepted: boolean }> {
  return request("/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ exercise_id: exerciseId, feedback_type: feedbackType })
  })
}

