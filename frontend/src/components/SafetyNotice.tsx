export default function SafetyNotice({ compact = false }: { compact?: boolean }) {
  const titleId = compact ? "compact-safety-title" : "safety-title"
  return (
    <aside className={`safety-notice ${compact ? "safety-compact" : ""}`} aria-labelledby={titleId}>
      <span className="notice-icon" aria-hidden="true">!</span>
      <div>
        <h2 id={titleId}>Please put your safety first</h2>
        <p>FitGuide only offers general exercise ideas and is not medical advice. Stop if an exercise causes pain. If you are injured, pregnant, living with a chronic condition, concerned about your heart, or simply unsure, speak with a qualified professional before you exercise.</p>
      </div>
    </aside>
  )
}

