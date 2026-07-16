import { label } from "../format"

type SelectFieldProps = { id: string; labelText: string; value: string; options: string[]; onChange: (value: string) => void }

export default function SelectField({ id, labelText, value, options, onChange }: SelectFieldProps) {
  return (
    <label className="form-field" htmlFor={id}>
      <span>{labelText} <span aria-hidden="true">*</span></span>
      <select id={id} value={value} onChange={event => onChange(event.target.value)}>
        {options.map(option => <option key={option} value={option}>{label(option)}{id === "goal" ? " Goal" : ""}</option>)}
      </select>
    </label>
  )
}

