export default function OrderInput({ order, onChange, dimension }) {
  const is1D = dimension === 1

  return (
    <div className="space-y-1">
      <label className="block text-sm font-medium text-gray-700">
        Mertebe (order)
        {!is1D && (
          <span className="ml-2 text-xs text-gray-400">çok değişkenli: max 2</span>
        )}
      </label>
      {is1D ? (
        <div className="flex items-center gap-3">
          <input
            type="range"
            min={1}
            max={20}
            value={Math.min(order, 20)}
            onChange={(e) => onChange(Number(e.target.value))}
            className="w-40"
          />
          <input
            type="number"
            min={1}
            max={100}
            value={order}
            onChange={(e) => {
              const v = Math.max(1, Math.min(100, Number(e.target.value)))
              onChange(v)
            }}
            className="w-20 border border-gray-300 rounded px-2 py-1 text-sm"
          />
        </div>
      ) : (
        <div className="flex gap-2">
          {[1, 2].map((v) => (
            <button
              key={v}
              type="button"
              onClick={() => onChange(v)}
              className={`px-4 py-1.5 rounded border text-sm font-medium transition-colors ${
                order === v
                  ? 'bg-indigo-600 text-white border-indigo-600'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
              }`}
            >
              {v}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
