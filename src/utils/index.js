export function getDateString() {
  const date = new Date();
  const [y, m, d] = [date.getFullYear(), date.getMonth() + 1, date.getDate()];
  const f = (num, digits) => {
    const s = num.toString();
    return '0'.repeat(digits - s.length) + s;
  };
  return `${f(y, 4)}/${f(m, 2)}/${f(d, 2)}`;
}

export function getValueString(value) {
  const prefix = value < 10 ? ' ' : '';
  const postfix = Number.isInteger(value) ? '.00' : '';
  let s = `${prefix}${String(value)}${postfix}`;
  if (s.length < 5) s += '0';
  return s;
}