import { useEffect, useRef } from 'react'
import katex from 'katex'
import 'katex/dist/katex.min.css'

function LatexBlock({ label, latex }) {
  const ref = useRef(null)

  useEffect(() => {
    if (!ref.current || !latex) return
    try {
      katex.render(latex, ref.current, {
        displayMode: true,
        throwOnError: false,
        trust: false,
      })
    } catch {
      ref.current.textContent = latex
    }
  }, [latex])

  if (!latex) return null

  return (
    <div className="space-y-1">
      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide">{label}</p>
      <div
        ref={ref}
        className="overflow-x-auto p-3 bg-gray-50 border border-gray-200 rounded-lg"
      />
    </div>
  )
}

export default function ResultDisplay({ data }) {
  if (!data) return null

  return (
    <div className="space-y-4">
      <h2 className="text-base font-semibold text-gray-800">Sonuç</h2>
      <LatexBlock label="Taylor açılımı" latex={data.symbolic_latex} />
      {data.gradient_latex && (
        <LatexBlock label="Gradient ∇f" latex={data.gradient_latex} />
      )}
      {data.hessian_latex && (
        <LatexBlock label="Hessian H" latex={data.hessian_latex} />
      )}
      <p className="text-xs text-gray-400">
        Boyut: {data.dimension}D &nbsp;·&nbsp; Değişkenler:{' '}
        {data.variables?.join(', ')}
      </p>
    </div>
  )
}
