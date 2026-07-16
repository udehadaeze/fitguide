export default function ErrorView({ message, onRetry, onEdit }: { message: string; onRetry: () => void; onEdit: () => void }) {
  return <main className="state-view page-shell"><div className="state-symbol error-symbol" aria-hidden="true">×</div><div className="step-kicker">Something went wrong</div><h1>FitGuide could not create your routine.</h1><p role="alert">{message}</p><div className="state-actions"><button className="button primary" type="button" onClick={onRetry}>Try again</button><button className="button secondary" type="button" onClick={onEdit}>Edit preferences</button></div></main>
}

