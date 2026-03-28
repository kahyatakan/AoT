const SYMBOLIC_DEFAULTS = {
  1: ['a'],
  2: ['a_1', 'a_2'],
  3: ['a_1', 'a_2', 'a_3'],
}

export default function PointInput({ point, pointMode, onChange, onModeChange }) {
  const dim = point.length

  const handleNumericChange = (index, raw) => {
    const val = parseFloat(raw)
    const next = [...point]
    next[index] = isNaN(val) ? 0 : val
    onChange(next)
  }

  const handleSymbolicChange = (index, raw) => {
    const next = [...point]
    next[index] = raw
    onChange(next)
  }

  const handleDimChange = (newDim) => {
    if (pointMode === 'symbolic') {
      onChange([...SYMBOLIC_DEFAULTS[newDim]])
    } else {
      onChange(Array.from({ length: newDim }, (_, i) =>
        typeof point[i] === 'number' ? point[i] : 0
      ))
    }
  }

  const handleModeChange = (newMode) => {
    onModeChange(newMode)
    if (newMode === 'symbolic') {
      onChange([...SYMBOLIC_DEFAULTS[dim]])
    } else {
      onChange(Array.from({ length: dim }, () => 0))
    }
  }

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-2 flex-wrap">
        <label className="text-sm font-medium text-gray-700">Açılım noktası</label>

        {/* Boyut seçici */}
        <select
          value={dim}
          onChange={(e) => handleDimChange(Number(e.target.value))}
          className="text-sm border border-gray-300 rounded px-2 py-1"
        >
          <option value={1}>1D</option>
          <option value={2}>2D</option>
          <option value={3}>3D</option>
        </select>

        {/* Mod geçişi: Sembolik | Sayısal */}
        <div className="flex rounded border border-gray-300 overflow-hidden text-xs">
          <button
            type="button"
            onClick={() => handleModeChange('symbolic')}
            className={`px-2 py-1 transition-colors ${
              pointMode === 'symbolic'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-50'
            }`}
          >
            Sembolik
          </button>
          <button
            type="button"
            onClick={() => handleModeChange('numeric')}
            className={`px-2 py-1 transition-colors ${
              pointMode === 'numeric'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-50'
            }`}
          >
            Sayısal
          </button>
        </div>
      </div>

      {/* Koordinat giriş alanları */}
      <div className="flex gap-2 flex-wrap">
        {point.map((v, i) => (
          <div key={i} className="flex items-center gap-1">
            <span className="text-xs text-gray-500">
              {dim === 1 ? 'x' : `x${i + 1}`} =
            </span>
            {pointMode === 'numeric' ? (
              <input
                type="number"
                step="any"
                value={v}
                onChange={(e) => handleNumericChange(i, e.target.value)}
                className="w-20 border border-gray-300 rounded px-2 py-1 text-sm"
              />
            ) : (
              <input
                type="text"
                value={v}
                onChange={(e) => handleSymbolicChange(i, e.target.value)}
                placeholder={SYMBOLIC_DEFAULTS[dim][i]}
                className="w-20 border border-indigo-300 rounded px-2 py-1 text-sm font-mono"
              />
            )}
          </div>
        ))}
      </div>

      {pointMode === 'symbolic' && (
        <p className="text-xs text-indigo-600">
          Sembolik mod: <span className="font-mono">a</span>, <span className="font-mono">a_1</span>, <span className="font-mono">a_2</span> gibi değerler girin. Grafik çizilmez; formül sembolik olarak gösterilir.
        </p>
      )}
    </div>
  )
}
