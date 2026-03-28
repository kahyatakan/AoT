const API_BASE = ''  // Vite proxy forwards /api → localhost:8000

/**
 * Taylor açılımı hesapla.
 * @param {string} latex - LaTeX string
 * @param {Array<number|string>} point - Açılım noktası (sayısal veya sembolik)
 * @param {number} order - Açılım mertebesi
 * @param {string} pointMode - "numeric" veya "symbolic"
 * @returns {Promise<object>} - ExpandResponse veya ErrorResponse
 */
export async function expandTaylor(latex, point, order, pointMode = 'numeric') {
  const resp = await fetch(`${API_BASE}/api/expand`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ latex, point, order, point_mode: pointMode }),
  })

  if (!resp.ok) {
    const text = await resp.text()
    let detail = text
    try {
      const json = JSON.parse(text)
      detail = json.detail ?? json.message ?? text
    } catch {}
    throw new Error(`HTTP ${resp.status}: ${detail}`)
  }

  return resp.json()
}
