import { label } from "../format"
import type { RecommendationResponse, UserProfile } from "../types"
import RecommendationCard from "./RecommendationCard"
import SafetyNotice from "./SafetyNotice"

export default function Results({ result, profile, onEdit, onRegenerate, onReset }: { result: RecommendationResponse; profile: UserProfile; onEdit: () => void; onRegenerate: () => void; onReset: () => void }) {
  return (
    <main className="results page-shell">
      <div className="results-header"><div><div className="step-kicker">Your routine</div><h1>Here is your exercise plan.</h1><p>{result.eligible_count} exercises matched your basic requirements before FitGuide created this routine.</p></div><button className="button secondary" type="button" onClick={onEdit}>Edit preferences</button></div>
      <div className="profile-strip" aria-label="Profile summary"><span><small>Goal</small>{label(profile.goal)}</span><span><small>Level</small>{label(profile.fitness_level)}</span><span><small>Setting</small>{label(profile.workout_location)}</span><span><small>Intensity</small>{label(profile.preferred_intensity)}</span><span><small>Restrictions</small>{profile.movement_restrictions.length ? profile.movement_restrictions.map(label).join(", ") : "None selected"}</span></div>
      <SafetyNotice compact />
      <section className="routine-list" aria-label="Recommended routine">{result.recommendations.map(item => <RecommendationCard key={item.exercise_id} item={item} />)}</section>
      {result.warning ? <p className="result-warning">{result.warning}</p> : null}
      <div className="form-actions"><button className="button secondary" type="button" onClick={onReset}>Start over</button><button className="button primary" type="button" onClick={onRegenerate}>Try another routine</button></div>
    </main>
  )
}

