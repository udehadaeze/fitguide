export function label(value: string): string {
  return value.replaceAll("_", " ").replace(/\b\w/g, character => character.toUpperCase())
}

export function scorePercent(score: number): string {
  return `${Math.round(score * 100)}%`
}
