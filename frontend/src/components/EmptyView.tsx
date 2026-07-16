export default function EmptyView({ warning, onEdit, onReset }: { warning: string; onEdit: () => void; onReset: () => void }) {
  return <main className="state-view page-shell"><div className="state-symbol" aria-hidden="true">0</div><div className="step-kicker">Your choices were kept</div><h1>We could not find a suitable routine.</h1><p>{warning}</p><p className="state-note">FitGuide kept all the limits you selected instead of ignoring one just to fill the routine.</p><div className="state-actions"><button className="button primary" type="button" onClick={onEdit}>Change my choices</button><button className="button secondary" type="button" onClick={onReset}>Start over</button></div></main>
}

