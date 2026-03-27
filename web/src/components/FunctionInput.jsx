import { useRef, useEffect } from 'react'
import 'mathlive'

const EXAMPLES = [
  { label: '\\sin(x)', value: '\\sin(x)' },
  { label: 'e^{x^2}', value: 'e^{x^2}' },
  { label: '\\frac{e^{x_1^2+x_2^2}}{\\sin(x_1)\\cdot\\cos(x_2)}', value: '\\frac{e^{x_1^2+x_2^2}}{\\sin(x_1)\\cdot\\cos(x_2)}' },
  { label: 'x_1\\cdot x_2\\cdot x_3', value: 'x_1\\cdot x_2\\cdot x_3' },
]

export default function FunctionInput({ value, onChange }) {
  const mfRef = useRef(null)

  useEffect(() => {
    const mf = mfRef.current
    if (!mf) return

    const handler = () => {
      onChange(mf.getValue('latex'))
    }
    mf.addEventListener('input', handler)
    return () => mf.removeEventListener('input', handler)
  }, [onChange])

  // Keep math-field in sync when parent sets value programmatically (example buttons)
  useEffect(() => {
    const mf = mfRef.current
    if (!mf) return
    if (mf.getValue('latex') !== value) {
      mf.setValue(value)
    }
  }, [value])

  return (
    <div className="space-y-2">
      <label className="block text-sm font-medium text-gray-700">
        Fonksiyon <span className="text-gray-400">(LaTeX)</span>
      </label>
      <math-field ref={mfRef} />
      <div className="flex flex-wrap gap-2 mt-1">
        {EXAMPLES.map((ex) => (
          <button
            key={ex.value}
            type="button"
            onClick={() => onChange(ex.value)}
            className="px-2 py-1 text-xs bg-gray-100 hover:bg-indigo-100 border border-gray-200 rounded font-mono"
            title={ex.value}
          >
            {ex.label}
          </button>
        ))}
      </div>
    </div>
  )
}
