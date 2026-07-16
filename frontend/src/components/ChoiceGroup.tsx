import { label } from "../format"

type ChoiceGroupProps = { legend: string; hint?: string; options: string[]; selected: string[]; onChange: (values: string[]) => void; required?: boolean }

export default function ChoiceGroup({ legend, hint, options, selected, onChange, required = false }: ChoiceGroupProps) {
  const toggle = (value: string) => onChange(selected.includes(value) ? selected.filter(item => item !== value) : [...selected, value])
  return (
    <fieldset className="form-field choice-field">
      <legend>{legend}{required ? <span aria-hidden="true"> *</span> : null}</legend>
      {hint ? <p className="field-hint">{hint}</p> : null}
      <div className="choice-grid">
        {options.map(option => (
          <label className={selected.includes(option) ? "choice selected" : "choice"} key={option}>
            <input type="checkbox" checked={selected.includes(option)} onChange={() => toggle(option)} />
            <span>{label(option)}</span>
          </label>
        ))}
      </div>
    </fieldset>
  )
}

