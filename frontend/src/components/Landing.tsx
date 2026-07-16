import "../landing-simple.css"
import SafetyNotice from "./SafetyNotice"

export default function Landing({ onStart, onAbout }: { onStart: () => void; onAbout: () => void }) {
  return (
    <main>
      <section className="hero hero-simple page-shell">
        <div className="hero-copy">
          <div className="eyebrow">Exercise ideas that fit your routine</div>
          <h1>Find a workout that works for you.</h1>
          <p>Tell FitGuide what you want to work on, how much time you have, and which movements you would rather avoid. It will put together a short routine and explain why each exercise was chosen.</p>
          <div className="hero-actions"><button className="button primary" type="button" onClick={onStart}>Build my routine <span aria-hidden="true">→</span></button><button className="text-button" type="button" onClick={onAbout}>How does FitGuide choose?</button></div>
        </div>
      </section>
      <section className="page-shell"><SafetyNotice /></section>
      <section className="principles page-shell" aria-labelledby="principles-title">
        <div><span className="section-label">Why FitGuide works this way</span><h2 id="principles-title">Your limits are checked first.</h2></div>
        <div className="principle-grid">
          <article><span>01</span><h3>Tell us what to avoid</h3><p>Exercises that do not suit your equipment, location, time, level or movement choices are removed before anything is ranked.</p></article>
          <article><span>02</span><h3>Know why it was chosen</h3><p>Each recommendation comes with a short reason, so you can see how it connects to the choices you made.</p></article>
          <article><span>03</span><h3>Get a more balanced routine</h3><p>FitGuide mixes preparation, main exercises and recovery instead of giving you several versions of the same movement.</p></article>
        </div>
      </section>
    </main>
  )
}

