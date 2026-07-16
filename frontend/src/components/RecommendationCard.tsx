import { useState } from "react"

import { sendFeedback } from "../api"
import { label, scorePercent } from "../format"
import type { Recommendation } from "../types"

export default function RecommendationCard({ item }: { item: Recommendation }) {
  const [feedback, setFeedback] = useState<string>("")
  const [feedbackError, setFeedbackError] = useState(false)
  const choose = async (value: "like" | "dislike" | "unsuitable") => {
    setFeedbackError(false)
    try {
      await sendFeedback(item.exercise_id, value)
      setFeedback(value)
    } catch {
      setFeedbackError(true)
    }
  }
  return (
    <article className="recommendation-card">
      <div className="routine-index"><strong>{String(item.routine_position).padStart(2, "0")}</strong><span>{label(item.routine_role)}</span></div>
      <div className="recommendation-main">
        <div className="card-heading"><div><span className="category-label">{label(item.category)}</span><h2>{item.name}</h2></div><div className="score-badge" aria-label={`Compatibility score ${scorePercent(item.score)}`}><strong>{scorePercent(item.score)}</strong><span>match</span></div></div>
        <p>{item.description}</p>
        <div className="attribute-row"><span>{label(item.difficulty)}</span><span>{label(item.intensity)} intensity</span><span>{item.estimated_duration_minutes} min</span><span>{item.equipment.map(label).join(", ")}</span></div>
        <div className="reason-box"><strong>Why FitGuide chose this</strong><p>{item.explanation}</p></div>
        <details><summary>How to do it and what to keep in mind</summary><p>{item.instructions}</p><p className="safety-text">{item.safety_notes}</p><p><strong>Suggested format:</strong> {item.recommended_sets}, {item.recommended_repetitions}</p></details>
        <div className="feedback-row" aria-label={`Feedback for ${item.name}`}><span>Would you use this exercise?</span><button type="button" aria-pressed={feedback === "like"} onClick={() => choose("like")}>Yes</button><button type="button" aria-pressed={feedback === "dislike"} onClick={() => choose("dislike")}>Not for me</button><button type="button" aria-pressed={feedback === "unsuitable"} onClick={() => choose("unsuitable")}>Unsuitable</button>{feedback ? <small role="status">Thanks. Your feedback was saved for this session.</small> : null}{feedbackError ? <small role="alert">Sorry, your feedback could not be saved.</small> : null}</div>
      </div>
    </article>
  )
}

