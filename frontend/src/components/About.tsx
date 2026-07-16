import SafetyNotice from "./SafetyNotice"

export default function About({ onStart }: { onStart: () => void }) {
  return (
    <main className="about page-shell">
      <div className="about-hero"><div className="step-kicker">How FitGuide works</div><h1>A simple recommender you can understand.</h1><p>FitGuide is a university project that explores how exercise suggestions can be matched to a person’s preferences. It is meant to help with everyday wellness choices, but it cannot replace advice from a healthcare or fitness professional.</p><button className="button primary" type="button" onClick={onStart}>Build a routine</button></div>
      <section className="about-grid" aria-label="How FitGuide works"><article><span>1</span><h2>First, it checks your limits</h2><p>FitGuide removes exercises that conflict with the movements you want to avoid, your equipment, location, level or available time.</p></article><article><span>2</span><h2>Then, it looks for good matches</h2><p>It compares the remaining exercises with the preferences you selected in the questionnaire.</p></article><article><span>3</span><h2>Finally, it builds the routine</h2><p>Suitable exercises are arranged into a short sequence with preparation, main movement and recovery roles.</p></article></section>
      <section className="about-text"><div><span className="section-label">Your data</span><h2>A made-up exercise catalogue and only a few personal choices</h2></div><div><p>FitGuide uses 80 exercise records created for this project. The catalogue has not been clinically validated and contains no patient data. The questionnaire does not ask for your name, date of birth, diagnosis, medication or medical records.</p><p>If you leave feedback, FitGuide only records the exercise and the option you selected. It is kept temporarily while the server is running and does not change future recommendations.</p></div></section>
      <section className="about-text"><div><span className="section-label">Limits</span><h2>What the score does not mean</h2></div><div><p>The score only shows how closely an exercise matches your answers compared with other exercises in this catalogue. It cannot tell whether an exercise is safe for you, whether your technique is correct or whether it will improve your health.</p><p>Because FitGuide uses your questionnaire answers, it can suggest exercises straight away. However, its features and scoring weights were chosen manually, and it does not learn from your long-term exercise habits.</p></div></section>
      <SafetyNotice />
    </main>
  )
}
