// GET /api/ics -> calendar file for the NEXT live training (Wednesday 7:00 PM Toronto time).
// Worked out fresh on every request, so it rolls over to the next week by itself.
// A real file URL (not a data: link) is what Apple Calendar on iPhone and Outlook need to open it.
const TZ = 'America/Toronto';
const WEEKDAY = 3, HOUR = 19, MIN = 0, LENGTH_MIN = 60;
const TITLE = 'Vacarya Live Training with Aiden Weir';
const DETAILS = 'Free live training. Your join link is in your confirmation email.';

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
function nextWebinar() {
  const now = new Date(), p = parts(now);
  const days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
  const add = (WEEKDAY - days[p.weekday] + 7) % 7;
  let t;
  for (let k = 0; k < 2; k++) {
    const base = new Date(Date.UTC(+p.year, +p.month - 1, +p.day + add + 7 * k));
    t = zoned(base.getUTCFullYear(), base.getUTCMonth(), base.getUTCDate(), HOUR, MIN);
    if (t.getTime() > now.getTime()) return t;
  }
  return t;
}
const stamp = (d) => d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');

export default function handler(req, res) {
  const start = nextWebinar(), end = new Date(start.getTime() + LENGTH_MIN * 60000);
  const ics = [
    'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Vacarya//Live Training//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
    'BEGIN:VEVENT',
    'UID:live-training-' + stamp(start) + '@hostvacarya.com',
    'DTSTAMP:' + stamp(new Date()),
    'DTSTART:' + stamp(start), 'DTEND:' + stamp(end),
    'SUMMARY:' + TITLE, 'DESCRIPTION:' + DETAILS,
    'BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:' + TITLE + ' starts in 15 minutes', 'TRIGGER:-PT15M', 'END:VALARM',
    'END:VEVENT', 'END:VCALENDAR', ''
  ].join('\r\n');
  res.setHeader('Content-Type', 'text/calendar; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename="vacarya-live-training.ics"');
  res.setHeader('Cache-Control', 'no-store');
  res.status(200).send(ics);
}
