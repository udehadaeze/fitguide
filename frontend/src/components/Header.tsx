import BrandMark from "./BrandMark"

type HeaderProps = { active: "home" | "about"; onHome: () => void; onAbout: () => void }

export default function Header({ active, onHome, onAbout }: HeaderProps) {
  return (
    <header className="site-header">
      <button className="brand" type="button" onClick={onHome} aria-label="FitGuide home"><BrandMark /><span>FitGuide</span></button>
      <nav aria-label="Main navigation">
        <button className={active === "home" ? "nav-active" : ""} type="button" onClick={onHome}>Plan</button>
        <button className={active === "about" ? "nav-active" : ""} type="button" onClick={onAbout}>How it works</button>
      </nav>
    </header>
  )
}

