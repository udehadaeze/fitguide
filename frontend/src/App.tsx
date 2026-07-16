import { useEffect, useState } from "react"

import { getMetadata, getRecommendations } from "./api"
import About from "./components/About"
import EmptyView from "./components/EmptyView"
import ErrorView from "./components/ErrorView"
import Header from "./components/Header"
import Landing from "./components/Landing"
import LoadingView from "./components/LoadingView"
import Questionnaire from "./components/Questionnaire"
import Results from "./components/Results"
import type { Metadata, RecommendationResponse, UserProfile } from "./types"

type View = "landing" | "questionnaire" | "loading" | "results" | "empty" | "error" | "about"

const initialProfile: UserProfile = {
  goal: "general_fitness",
  fitness_level: "beginner",
  workout_location: "home",
  available_equipment: ["none"],
  preferred_duration_minutes: 10,
  preferred_intensity: "low",
  preferred_categories: ["cardio", "strength", "mobility"],
  target_body_areas: ["full_body"],
  movement_restrictions: [],
  exercises_to_avoid: [],
  low_impact_required: false,
  maximum_recommendations: 5
}

export default function App() {
  const [view, setView] = useState<View>("landing")
  const [metadata, setMetadata] = useState<Metadata | null>(null)
  const [profile, setProfile] = useState<UserProfile>(initialProfile)
  const [result, setResult] = useState<RecommendationResponse | null>(null)
  const [error, setError] = useState("")
  useEffect(() => { getMetadata().then(setMetadata).catch(() => setError("The preference options could not be loaded. Make sure the FitGuide backend is running.")) }, [])
  const start = () => {
    if (!metadata) { setError("The preference options are not available yet. Make sure the FitGuide backend is running."); setView("error"); return }
    setView("questionnaire")
  }
  const submit = async (nextProfile: UserProfile) => {
    setProfile(nextProfile); setView("loading"); setError("")
    try { const nextResult = await getRecommendations(nextProfile); setResult(nextResult); setView(nextResult.recommendations.length ? "results" : "empty") }
    catch (requestError) { setError(requestError instanceof Error ? requestError.message : "An unexpected request error occurred."); setView("error") }
  }
  const reset = () => { setProfile(initialProfile); setResult(null); setError(""); setView("landing") }
  return (
    <div className="app-frame">
      <a className="skip-link" href="#main-content">Skip to main content</a>
      <Header active={view === "about" ? "about" : "home"} onHome={reset} onAbout={() => setView("about")} />
      <div id="main-content">
        {view === "landing" ? <Landing onStart={start} onAbout={() => setView("about")} /> : null}
        {view === "questionnaire" && metadata ? <Questionnaire metadata={metadata} initialProfile={profile} onSubmit={submit} onCancel={() => setView("landing")} /> : null}
        {view === "loading" ? <LoadingView /> : null}
        {view === "results" && result ? <Results result={result} profile={profile} onEdit={() => setView("questionnaire")} onRegenerate={() => submit(profile)} onReset={reset} /> : null}
        {view === "empty" && result ? <EmptyView warning={result.warning ?? "No compatible exercises were found."} onEdit={() => setView("questionnaire")} onReset={reset} /> : null}
        {view === "error" ? <ErrorView message={error} onRetry={() => metadata ? submit(profile) : window.location.reload()} onEdit={() => metadata ? setView("questionnaire") : setView("landing")} /> : null}
        {view === "about" ? <About onStart={start} /> : null}
      </div>
      <footer><span>FitGuide Recommender</span><span>General wellness prototype · Synthetic exercise data · Transparent routine ranking</span></footer>
    </div>
  )
}
