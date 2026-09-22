const abs = (n) => Math.abs(n).toLocaleString('en-US')

export function signed(n, digits = 0) {
  const v = digits ? Math.abs(n).toFixed(digits) : abs(Math.round(n))
  if (n < 0) return '−' + v
  if (n > 0) return '+' + v
  return digits ? Number(0).toFixed(digits) : '0'
}

export function dollars(n) {
  const v = abs(Math.round(n))
  if (n < 0) return '−$' + v
  if (n > 0) return '+$' + v
  return '$0'
}

export function billions(n, digits = 0) {
  const v = Math.abs(n).toFixed(digits)
  if (n < 0) return '−$' + v + 'bn'
  if (n > 0) return '+$' + v + 'bn'
  return '$0'
}
