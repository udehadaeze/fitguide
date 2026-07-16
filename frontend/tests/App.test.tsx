import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { beforeEach, describe, expect, it, vi } from "vitest"

import App from "../src/App"
import * as api from "../src/api"
import type { Metadata, RecommendationResponse } from "../src/types"

vi.mock("../src/api", () => ({ getMetadata: vi.fn(), getRecommendations: vi.fn(), sendFeedback: vi.fn() }))

const metadata: Metadata = {
  goals: ["general_fitness", "strength"],
  levels: ["beginner", "intermediate", "advanced"],
  categories: ["cardio", "strength", "mobility", "flexibility", "balance", "core", "relaxation"],
  body_areas: ["full_body", "upper_body", "lower_body", "core", "back", "shoulders", "hips", "legs"],
  equipment: ["none", "chair", "wall", "mat"],
  locations: ["home", "gym", "outdoors", "any"],
  intensities: ["low", "moderate", "high"],
  movement_restrictions: ["avoid_jumping", "avoid_kneeling", "avoid_floor_exercises"]
}

const result: RecommendationResponse = {
  processed_profile: { goal: "general_fitness", fitness_level: "beginner", workout_location: "home", preferred_duration_minutes: 10, preferred_intensity: "low", hard_restrictions_applied: [] },
  eligible_count: 24,
  warning: null,
  recommendations: [{ exercise_id: "EX001", name: "Walking in Place", description: "A low-intensity cardio movement.", category: "cardio", movement_pattern: "march", primary_body_area: "full_body", secondary_body_areas: ["legs"], difficulty: "beginner", intensity: "low", equipment: ["none"], workout_locations: ["home"], estimated_duration_minutes: 8, recommended_repetitions: "30-60 seconds", recommended_sets: "1-2 rounds", beginner_friendly: true, low_impact: true, instructions: "Move with control.", safety_notes: "Use a stable surface.", tags: ["cardio"], score: .82, matched_features: ["supports general fitness"], explanation: "Recommended because it supports general fitness.", routine_position: 1, routine_role: "energise" }]
}

beforeEach(() => {
  vi.mocked(api.getMetadata).mockResolvedValue(metadata)
  vi.mocked(api.getRecommendations).mockResolvedValue(result)
  vi.mocked(api.sendFeedback).mockResolvedValue({ accepted: true })
})

describe("FitGuide application", () => {
  it("shows the wellness disclaimer on the landing view", async () => {
    render(<App />)
    expect(screen.getByRole("heading", { name: /find a workout that works for you/i })).toBeInTheDocument()
    expect(screen.getByText(/not medical advice/i)).toBeInTheDocument()
    await waitFor(() => expect(api.getMetadata).toHaveBeenCalled())
  })

  it("opens the questionnaire with accessible required controls", async () => {
    const user = userEvent.setup()
    render(<App />)
    await waitFor(() => expect(api.getMetadata).toHaveBeenCalled())
    await user.click(screen.getByRole("button", { name: /build my routine/i }))
    expect(screen.getByLabelText(/main goal/i)).toBeInTheDocument()
    expect(screen.getByRole("group", { name: /available equipment/i })).toBeInTheDocument()
    expect(screen.getByRole("heading", { name: /choose movements to avoid/i })).toBeInTheDocument()
  })

  it("validates empty multi-choice requirements", async () => {
    const user = userEvent.setup()
    render(<App />)
    await waitFor(() => expect(api.getMetadata).toHaveBeenCalled())
    await user.click(screen.getByRole("button", { name: /build my routine/i }))
    await user.click(screen.getByText("None"))
    await user.click(screen.getByText("Cardio"))
    await user.click(screen.getByText("Strength"))
    await user.click(screen.getByText("Mobility"))
    await user.click(screen.getByText("Full Body"))
    await user.click(screen.getByRole("button", { name: /create my routine/i }))
    expect(screen.getByRole("alert")).toHaveTextContent(/choose at least one exercise type/i)
    expect(api.getRecommendations).not.toHaveBeenCalled()
  })

  it("submits the profile and displays a successful recommendation", async () => {
    const user = userEvent.setup()
    render(<App />)
    await waitFor(() => expect(api.getMetadata).toHaveBeenCalled())
    await user.click(screen.getByRole("button", { name: /build my routine/i }))
    await user.click(screen.getByRole("button", { name: /create my routine/i }))
    expect(await screen.findByRole("heading", { name: "Walking in Place" })).toBeInTheDocument()
    expect(screen.getByText(/24 exercises matched your basic requirements/i)).toBeInTheDocument()
    expect(api.getRecommendations).toHaveBeenCalledTimes(1)
  })

  it("displays the empty state without weakening restrictions", async () => {
    vi.mocked(api.getRecommendations).mockResolvedValue({ ...result, recommendations: [], eligible_count: 0, warning: "No exercises satisfy every hard restriction." })
    const user = userEvent.setup()
    render(<App />)
    await waitFor(() => expect(api.getMetadata).toHaveBeenCalled())
    await user.click(screen.getByRole("button", { name: /build my routine/i }))
    await user.click(screen.getByRole("button", { name: /create my routine/i }))
    expect(await screen.findByRole("heading", { name: /could not find a suitable routine/i })).toBeInTheDocument()
    expect(screen.getByText(/kept all the limits you selected/i)).toBeInTheDocument()
  })

  it("displays an API error and offers recovery", async () => {
    vi.mocked(api.getRecommendations).mockRejectedValue(new Error("Backend unavailable"))
    const user = userEvent.setup()
    render(<App />)
    await waitFor(() => expect(api.getMetadata).toHaveBeenCalled())
    await user.click(screen.getByRole("button", { name: /build my routine/i }))
    await user.click(screen.getByRole("button", { name: /create my routine/i }))
    expect(await screen.findByRole("alert")).toHaveTextContent("Backend unavailable")
    expect(screen.getByRole("button", { name: /edit preferences/i })).toBeInTheDocument()
  })

  it("allows results to return to editable preferences", async () => {
    const user = userEvent.setup()
    render(<App />)
    await waitFor(() => expect(api.getMetadata).toHaveBeenCalled())
    await user.click(screen.getByRole("button", { name: /build my routine/i }))
    await user.click(screen.getByRole("button", { name: /create my routine/i }))
    await screen.findByRole("heading", { name: "Walking in Place" })
    await user.click(screen.getByRole("button", { name: /edit preferences/i }))
    expect(screen.getByRole("heading", { name: /build a routine around your preferences/i })).toBeInTheDocument()
  })

  it("shows the data and limitation explanation", async () => {
    const user = userEvent.setup()
    render(<App />)
    await user.click(screen.getByRole("button", { name: /how it works/i }))
    expect(screen.getByRole("heading", { name: /simple recommender you can understand/i })).toBeInTheDocument()
    expect(screen.getByText(/uses 80 exercise records created for this project/i)).toBeInTheDocument()
  })
})
