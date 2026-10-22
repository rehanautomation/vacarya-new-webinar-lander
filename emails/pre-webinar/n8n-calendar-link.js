// n8n Code node "Build calendar link" (Mode: Run Once for Each Item).
// Put it in WJ2 right after the WebinarJam register node, before the GHL contact update.
// Builds a direct Google Calendar link for the next Wednesday 7 PM Toronto, with the person's own join link inside.
// Then add a second custom field to the GHL contact update:
//   id: FcvelyyV3mNVqKZf571p (contact.webinar_calendar_link)   value: {{ $json.calendar_link }}
// (n8n Code nodes have no URLSearchParams, so the URL is built with encodeURIComponent.)

const joinLink = ($json.user && $json.user.live_room_url) || '';
const TZ = 'America/Toronto';

function parts(d) {
  const p = {};
  new Intl.DateTimeFormat('en-US', { timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hourCycle: 'h23', weekday: 'short' })
    .formatToParts(d).forEach((x) => { p[x.type] = x.value; });
  return p;
}
function offset(d) {
  const p = parts(d);
  return Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second) - Math.floor(d.getTime() / 1000) * 1000;
}
function zoned(y, m, d, h, mi) {
  const g = Date.UTC(y, m, d, h, mi);
  const t = g - offset(new Date(g));
  return new Date(g - offset(new Date(t)));
}

const now = new Date(), p = parts(now);
const days = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
const add = (3 - days[p.weekday] + 7) % 7;
let start;
for (let k = 0; k < 2; k++) {
  const b = new Date(Date.UTC(+p.year, +p.month - 1, +p.day + add + 7 * k));
  start = zoned(b.getUTCFullYear(), b.getUTCMonth(), b.getUTCDate(), 19, 0);
  if (start.getTime() > now.getTime()) break;
}
const end = new Date(start.getTime() + 60 * 60000);
const stamp = (d) => d.toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');

const q = {
  action: 'TEMPLATE',
  text: 'Vacarya Live Training with Aiden Weir',
  dates: stamp(start) + '/' + stamp(end),
  details: joinLink
    ? 'Free live training with Aiden Weir.\n\nYour personal join link:\n' + joinLink
    : 'Free live training. Your join link is in your confirmation email.',
};
if (joinLink) q.location = joinLink;
const calendar_link = 'https://calendar.google.com/calendar/render?' +
  Object.keys(q).map((k) => k + '=' + encodeURIComponent(q[k])).join('&');

return { json: { ...$json, calendar_link } };
