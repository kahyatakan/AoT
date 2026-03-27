import { useEffect, useRef } from 'react'
import Plotly from 'plotly.js-dist-min'

export default function PlotDisplay({ plotJson }) {
  const containerRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current || !plotJson) return

    const { data, layout } = plotJson
    const mergedLayout = {
      ...layout,
      autosize: true,
      margin: { l: 50, r: 20, t: 40, b: 50 },
      paper_bgcolor: 'transparent',
      plot_bgcolor: '#f9fafb',
    }

    Plotly.react(containerRef.current, data, mergedLayout, {
      responsive: true,
      displaylogo: false,
    })

    return () => {
      Plotly.purge(containerRef.current)
    }
  }, [plotJson])

  if (!plotJson) return null

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
