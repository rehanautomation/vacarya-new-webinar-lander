// Shared by /api/ics and /api/gcal: the NEXT live training (Wednesday 7:00 PM Toronto time),
// worked out fresh on every request so links in old emails roll over to the next week by themselves.
const TZ = 'America/Toronto';
const WEEKDAY = 3, HOUR = 19, MIN = 0, CUTOFF_MIN = 30;
export const LENGTH_MIN = 60;
export const TITLE = 'Vacarya Live Training with Aiden Weir';

function parts(date) {
  const p = {};
  new Intl.DateTimeFormat('en-US', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23', weekday: 'short' })
    .formatToParts(date).forEach((x) => { p[x.type] = x.value; });
  return p;
}
function tzOffset(date) {
  const p = parts(date);
  return Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second) - Math.floor(date.getTime() / 1000) * 1000;
}
function zoned(y, m, d, h, mi) {
  const guess = Date.UTC(y, m, d, h, mi);
  const t = guess - tzOffset(new Date(guess));
  return new Date(guess - tzOffset(new Date(t)));
}
export function nextWebinar() {
  const now = new Date(), p = parts(now);
  const days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
  const add = (WEEKDAY - days[p.weekday] + 7) % 7;
  let t;
  for (let k = 0; k < 2; k++) {
    const base = new Date(Date.UTC(+p.year, +p.month - 1, +p.day + add + 7 * k));
    t = zoned(base.getUTCFullYear(), base.getUTCMonth(), base.getUTCDate(), HOUR, MIN);
    if (now.getTime() < t.getTime() + CUTOFF_MIN * 60000) return t;  // sign-ups until 7:30 PM count for tonight
  }
  return t;
}
export const stamp = (d) => d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');

// Person's own WebinarJam join link, passed as the LAST query param (?link=...).
// GHL merge fields aren't URL-encoded, so everything after "link=" is taken as-is.
// Only https WebinarJam links are accepted; anything else is ignored.
export function joinLink(req) {
  const raw = String(req.url || '');
  const i = raw.indexOf('link=');
  if (i < 0) return '';
  let v = raw.slice(i + 5);
  try { v = decodeURIComponent(v); } catch { /* keep raw */ }
  // drop tracking params that email tools or proxies tack onto the end (utm_*, fbclid, gclid, mc_*, _vercel*)
  v = v.replace(/[&?](utm_[^=&]*|fbclid|gclid|mc_[^=&]*|_vercel[^=&]*)=[^&]*/gi, '').trim();
  try {
    const u = new URL(v);
    if (u.protocol === 'https:' && /(^|\.)webinarjam\.(com|net)$/.test(u.hostname)) return u.href;
  } catch { /* not a URL */ }
  return '';
}

export function details(link) {
  return link
    ? 'Free live training with Aiden Weir.\n\nYour personal join link:\n' + link
    : 'Free live training. Your join link is in your confirmation email.';
}
