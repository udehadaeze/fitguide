import { useState, type FormEvent } from "react"

import type { Metadata, UserProfile } from "../types"
import ChoiceGroup from "./ChoiceGroup"
import SelectField from "./SelectField"

type QuestionnaireProps = { metadata: Metadata; initialProfile: UserProfile; onSubmit: (profile: UserProfile) => void; onCancel: () => void }

export default function Questionnaire({ metadata, initialProfile, onSubmit, onCancel }: QuestionnaireProps) {
  const [profile, setProfile] = useState(initialProfile)
  const [error, setError] = useState("")
  const update = <K extends keyof UserProfile>(key: K, value: UserProfile[K]) => setProfile(current => ({ ...current, [key]: value }))
  const submit = (event: FormEvent) => {
    event.preventDefault()
    if (!profile.preferred_categories.length || !profile.target_body_areas.length || !profile.available_equipment.length) {
      setError("Please choose at least one exercise type, body area and equipment option.")
      return
    }
    setError("")
    onSubmit(profile)
  }
  return (
    <main className="questionnaire page-shell">
      <div className="step-kicker">Tell us what suits you</div>
      <h1>Let’s build a routine around your preferences.</h1>
      <p className="page-intro">FitGuide checks the movements you want to avoid before it ranks any exercise. A better score will never override those choices.</p>
      <form onSubmit={submit} noValidate>
        {error ? <div className="form-error" role="alert">{error}</div> : null}
        <section className="form-section" aria-labelledby="essentials-title">
          <div className="section-number">01</div>
          <div className="section-content">
            <h2 id="essentials-title">Start with the basics</h2>
            <div className="field-row">
              <SelectField id="goal" labelText="Main goal" value={profile.goal} options={metadata.goals} onChange={value => update("goal", value)} />
              <SelectField id="level" labelText="Current fitness level" value={profile.fitness_level} options={metadata.levels} onChange={value => update("fitness_level", value)} />
              <SelectField id="location" labelText="Workout setting" value={profile.workout_location} options={metadata.locations} onChange={value => update("workout_location", value)} />
              <SelectField id="intensity" labelText="Preferred intensity" value={profile.preferred_intensity} options={metadata.intensities} onChange={value => update("preferred_intensity", value)} />
            </div>
            <label className="form-field range-field" htmlFor="duration"><span>Maximum time for one exercise: <strong>{profile.preferred_duration_minutes} minutes</strong></span><input id="duration" type="range" min="3" max="30" value={profile.preferred_duration_minutes} onChange={event => update("preferred_duration_minutes", Number(event.target.value))} /></label>
          </div>
        </section>
        <section className="form-section" aria-labelledby="preferences-title">
          <div className="section-number">02</div>
          <div className="section-content">
            <h2 id="preferences-title">Choose what you enjoy</h2>
            <ChoiceGroup legend="Available equipment" options={metadata.equipment} selected={profile.available_equipment} onChange={value => update("available_equipment", value)} required />
            <ChoiceGroup legend="Exercise categories" hint="Pick the types of exercise you would like in your routine." options={metadata.categories} selected={profile.preferred_categories} onChange={value => update("preferred_categories", value)} required />
            <ChoiceGroup legend="Body areas of interest" options={metadata.body_areas} selected={profile.target_body_areas} onChange={value => update("target_body_areas", value)} required />
          </div>
        </section>
        <section className="form-section safety-section" aria-labelledby="boundaries-title">
          <div className="section-number">03</div>
          <div className="section-content">
            <h2 id="boundaries-title">Choose movements to avoid</h2>
            <p className="section-note">These choices simply help FitGuide remove unsuitable movements. They are not a medical assessment.</p>
            <label className={profile.low_impact_required ? "impact-toggle selected" : "impact-toggle"}>
              <input type="checkbox" checked={profile.low_impact_required} onChange={event => update("low_impact_required", event.target.checked)} />
              <span><strong>Low-impact routine required</strong><small>FitGuide will only show exercises labelled as low impact.</small></span>
            </label>
            <ChoiceGroup legend="Movements to avoid" options={metadata.movement_restrictions} selected={profile.movement_restrictions} onChange={value => update("movement_restrictions", value)} />
            <label className="form-field" htmlFor="avoid-exercises"><span>Specific exercise names to avoid</span><span className="field-hint">Use commas if you want to enter more than one exercise.</span><input id="avoid-exercises" type="text" value={profile.exercises_to_avoid.join(", ")} onChange={event => update("exercises_to_avoid", event.target.value.split(",").map(value => value.trim()).filter(Boolean))} placeholder="Example: Jumping Jacks" /></label>
          </div>
        </section>
        <div className="form-actions"><button className="button secondary" type="button" onClick={onCancel}>Back</button><button className="button primary" type="submit">Create my routine <span aria-hidden="true">→</span></button></div>
      </form>
    </main>
  )
}
