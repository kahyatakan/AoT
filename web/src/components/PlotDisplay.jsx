import { useEffect, useRef } from 'react'
import Plotly from 'plotly.js-dist-min'

export default function PlotDisplay({ plotJson, plotWarning, plotInfo }) {
  const containerRef = useRef(null)

  useEffect(() => {
    // BUG 1: ref'i değişken olarak yakala — cleanup sırasında null olabilir
    const container = containerRef.current
    if (!container || !plotJson) return

    const { data, layout } = plotJson
    const mergedLayout = {
      ...layout,
      autosize: true,
      margin: { l: 50, r: 20, t: 40, b: 50 },
      paper_bgcolor: 'transparent',
      plot_bgcolor: '#f9fafb',
    }

    Plotly.react(container, data, mergedLayout, {
      responsive: true,
      displaylogo: false,
    })

    // BUG 1: Plotly.purge için yakalanan container değişkenini kullan
    return () => {
      if (container) Plotly.purge(container)
    }
  }, [plotJson])

  // BUG 2: Grafik yok ama uyarı var
  if (!plotJson) {
    if (plotInfo) {
      return (
        <div className="space-y-1">
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Grafik</p>
          <div className="flex items-start gap-2 p-3 bg-indigo-50 border border-indigo-200 rounded-lg text-sm text-indigo-700">
            <span>ℹ</span>
            <span>{plotInfo}</span>
          </div>
        </div>
      )
    }
    if (plotWarning) {
      return (
        <div className="space-y-1">
          <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Grafik</p>
          <div className="flex items-start gap-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg text-sm text-yellow-700">
            <span>⚠</span>
            <span>{plotWarning}</span>
          </div>
        </div>
      )
    }
    return null
  }

  return (
    <div className="space-y-1">
      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Grafik</p>
      <div
        ref={containerRef}
        style={{ width: '100%', height: '420px' }}
        className="border border-gray-200 rounded-lg overflow-hidden"
      />
    </div>
  )
}
