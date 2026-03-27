export default function PointInput({ point, onChange }) {
  const dim = point.length

  const handleChange = (index, raw) => {
    const val = raw === '' || raw === '-' ? raw : parseFloat(raw)
    const next = [...point]
    next[index] = isNaN(val) ? 0 : val
    onChange(next)
  }

  const handleDimChange = (newDim) => {
    const next = Array.from({ length: newDim }, (_, i) => point[i] ?? 0)
    onChange(next)
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-3">
        <label className="text-sm font-medium text-gray-700">Açılım noktası</label>
        <select
          value={dim}
          onChange={(e) => handleDimChange(Number(e.target.value))}
          className="text-sm border border-gray-300 rounded px-2 py-1"
        >
          <option value={1}>1D</option>
          <option value={2}>2D</option>
          <option value={3}>3D</option>
        </select>
      </div>
      <div className="flex gap-2">
        {point.map((v, i) => (
          <div key={i} className="flex items-center gap-1">
            <span className="text-xs text-gray-500">
              {dim === 1 ? 'x' : `x${i + 1}`} =
            </span>
            <input
              type="number"
              step="any"
              value={v}
              onChange={(e) => handleChange(i, e.target.value)}
              className="w-20 border border-gray-300 rounded px-2 py-1 text-sm"
            />
          </div>
        ))}
      </div>
    </div>
  )
}
