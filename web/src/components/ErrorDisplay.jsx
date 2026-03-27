const TYPE_LABELS = {
  parse_error: 'LaTeX Sözdizimi Hatası',
  math_error: 'Matematiksel Hata',
  validation_error: 'Doğrulama Hatası',
}

export default function ErrorDisplay({ error }) {
  if (!error) return null

  const label = TYPE_LABELS[error.error_type] ?? 'Hata'

  return (
    <div className="rounded-lg border border-red-200 bg-red-50 p-4 space-y-1">
      <p className="text-sm font-semibold text-red-700">{label}</p>
      <p className="text-sm text-red-600">{error.message}</p>
      {error.hint && (
        <p className="text-xs text-red-500 mt-1">
          <span className="font-medium">İpucu:</span> {error.hint}
        </p>
      )}
    </div>
  )
}
