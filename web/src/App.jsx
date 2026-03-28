import { useState, useCallback } from 'react'
import FunctionInput from './components/FunctionInput'
import PointInput from './components/PointInput'
import OrderInput from './components/OrderInput'
import ResultDisplay from './components/ResultDisplay'
import PlotDisplay from './components/PlotDisplay'
import ErrorDisplay from './components/ErrorDisplay'
import { expandTaylor } from './api/client'

export default function App() {
  const [latex, setLatex] = useState('\\sin(x)')
  const [point, setPoint] = useState([0])
  const [pointMode, setPointMode] = useState('numeric')
  const [order, setOrder] = useState(5)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handlePointChange = useCallback((newPoint) => {
    setPoint(newPoint)
    // BUG 1: Boyut değişince order'ı kliple — 2D/3D için max 2
    if (newPoint.length > 1) {
      setOrder((prev) => Math.min(prev, 2))
    }
  }, [])

  // Örnek buton seçildiğinde latex + point + pointMode birlikte set et
  const handleSelect = useCallback((latex, point, pointMode) => {
    setLatex(latex)
    setPoint(point)
    setPointMode(pointMode)
    setOrder(point.length === 1 ? 5 : 2)
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!latex.trim()) return

    // BUG 1: Her yeni hesaplamada eski sonucu tamamen temizle
    setLoading(true)
    setResult(null)
    setError(null)

    try {
      const data = await expandTaylor(latex, point, order, pointMode)
      if (data.status === 'ok') {
        setResult(data)
      } else {
        setError(data)
      }
    } catch (err) {
      setError({ error_type: 'math_error', message: err.message, hint: null })
    } finally {
      setLoading(false)
    }
  }

  const dimension = point.length

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <span className="text-xl font-bold text-indigo-700">AOT</span>
          <span className="text-gray-400">·</span>
          <span className="text-gray-600 text-sm">Anvil of Taylor — Taylor Serisi Hesaplayıcı</span>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8 space-y-6">
        {/* Input form */}
        <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-5">
          <FunctionInput value={latex} onChange={setLatex} onSelect={handleSelect} />

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <PointInput
              point={point}
              pointMode={pointMode}
              onChange={handlePointChange}
              onModeChange={setPointMode}
            />
            <OrderInput order={order} onChange={setOrder} dimension={dimension} />
          </div>

          <button
            type="submit"
            disabled={loading || !latex.trim()}
            className="w-full sm:w-auto px-6 py-2.5 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
                </svg>
                Hesaplanıyor…
              </>
            ) : (
              'Hesapla'
            )}
          </button>
        </form>

        {/* Error */}
        <ErrorDisplay error={error} />

        {/* Results */}
        {result && (
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-6">
            <ResultDisplay data={result} />
            <PlotDisplay
              plotJson={result.plot_json}
              plotWarning={result.plot_warning}
              plotInfo={result.plot_info}
            />
          </div>
        )}
      </main>
    </div>
  )
}
