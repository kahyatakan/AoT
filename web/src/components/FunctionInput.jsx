import { useRef, useEffect } from 'react'
import 'mathlive'

// Her item: { name, latex, point, pointMode }
const CATEGORIES = [
  {
    label: '1D',
    items: [
      { name: 'sin(x)', latex: '\\sin(x)', point: ['a'], pointMode: 'symbolic' },
      { name: 'e^{x²}', latex: 'e^{x^2}', point: ['a'], pointMode: 'symbolic' },
      { name: '1/(1+x²)', latex: '\\frac{1}{1+x^2}', point: ['a'], pointMode: 'symbolic' },
    ],
  },
  {
    label: 'Klasik Yüzeyler',
    items: [
      { name: 'Gaussian', latex: 'e^{-(x_1^2+x_2^2)}', point: [1, 0], pointMode: 'numeric' },
      { name: 'Yumurta kartonu', latex: '\\sin(x_1)\\cdot\\sin(x_2)', point: [0, 0], pointMode: 'numeric' },
      { name: 'Dairesel dalga', latex: '\\cos(x_1^2+x_2^2)', point: [0, 0], pointMode: 'numeric' },
    ],
  },
  {
    label: 'Kesirli & Rasyonel',
    items: [
      { name: '2D Lorentzian', latex: '\\frac{1}{1+x_1^2+x_2^2}', point: ['a_1', 'a_2'], pointMode: 'symbolic' },
      { name: 'Eyer noktası', latex: '\\frac{x_1\\cdot x_2}{x_1^2+x_2^2+1}', point: [0, 0], pointMode: 'numeric' },
      { name: 'Trig+rasyonel', latex: '\\frac{\\sin(x_1\\cdot x_2)}{1+x_1^2+x_2^2}', point: ['a_1', 'a_2'], pointMode: 'symbolic' },
    ],
  },
  {
    label: 'Fizik',
    items: [
      { name: 'Log potansiyel', latex: '\\ln(1+x_1^2+x_2^2)', point: [0, 0], pointMode: 'numeric' },
      { name: 'Hiperboloid', latex: '\\sqrt{x_1^2+x_2^2+1}', point: ['a_1', 'a_2'], pointMode: 'symbolic' },
      { name: 'Laplace çözümü', latex: 'e^{x_1}\\cdot\\cos(x_2)', point: ['a_1', 'a_2'], pointMode: 'symbolic' },
    ],
  },
  {
    label: 'Vay Be',
    items: [
      { name: "AOT'un sebebi", latex: '\\frac{e^{x_1\\cdot x_2}}{\\cos(x_1)+\\cos(x_2)+2}', point: ['a_1', 'a_2'], pointMode: 'symbolic' },
      { name: 'Polar açı', latex: '\\arctan\\left(\\frac{x_2}{x_1}\\right)', point: [1, 0], pointMode: 'numeric' },
      { name: 'Üstel güç', latex: 'e^{x_2\\cdot\\ln(x_1)}', point: [1, 1], pointMode: 'numeric' },
    ],
  },
  {
    label: '3D',
    items: [
      { name: 'Üçlü etkileşim', latex: 'e^{x_1\\cdot x_2\\cdot x_3}', point: ['a_1', 'a_2', 'a_3'], pointMode: 'symbolic' },
      { name: '3D rasyonel', latex: '\\frac{x_1+x_2+x_3}{1+x_1^2+x_2^2+x_3^2}', point: [1, 1, 1], pointMode: 'numeric' },
      { name: 'Dalga+sönümleme', latex: '\\sin(x_1+x_2)\\cdot e^{-x_3^2}', point: ['a_1', 'a_2', 'a_3'], pointMode: 'symbolic' },
    ],
  },
]

export default function FunctionInput({ value, onChange, onSelect }) {
  const mfRef = useRef(null)

  useEffect(() => {
    const mf = mfRef.current
    if (!mf) return
    const handler = () => onChange(mf.getValue('latex'))
    mf.addEventListener('input', handler)
    return () => mf.removeEventListener('input', handler)
  }, [onChange])

  useEffect(() => {
    const mf = mfRef.current
    if (!mf) return
    if (mf.getValue('latex') !== value) {
      mf.setValue(value)
    }
  }, [value])

  const handleSelect = (item) => {
    onChange(item.latex)
    onSelect(item.latex, item.point, item.pointMode)
  }

  return (
    <div className="space-y-3">
      <label className="block text-sm font-medium text-gray-700">
        Fonksiyon <span className="text-gray-400">(LaTeX)</span>
      </label>
      <math-field ref={mfRef} />

      {/* Kategorili örnek butonlar */}
      <div className="space-y-2">
        {CATEGORIES.map((cat) => (
          <div key={cat.label} className="flex items-start gap-2">
            <span className="text-xs font-semibold text-gray-400 w-24 shrink-0 pt-1">
              {cat.label}
            </span>
            <div className="flex flex-wrap gap-1">
              {cat.items.map((item) => (
                <button
                  key={item.latex}
                  type="button"
                  onClick={() => handleSelect(item)}
                  title={item.latex}
                  className="px-2 py-0.5 text-xs bg-gray-100 hover:bg-indigo-100 border border-gray-200 hover:border-indigo-300 rounded transition-colors"
                >
                  {item.name}
                  {item.pointMode === 'symbolic' && (
                    <span className="ml-1 text-indigo-400 font-normal">∿</span>
                  )}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
      <p className="text-xs text-gray-400">
        <span className="text-indigo-400">∿</span> sembolik nokta, diğerleri sayısal
      </p>
    </div>
  )
}
