// GET /api/gcal -> redirects to Google Calendar "add event" for the NEXT live training.
// Used in emails, where the date can't be worked out in advance.
// Optional ?link=<their WebinarJam join link> (last param) puts the personal link in the event.
import { nextWebinar, stamp, joinLink, details, TITLE, LENGTH_MIN } from './_webinar.js';

export default function handler(req, res) {
  const start = nextWebinar(), end = new Date(start.getTime() + LENGTH_MIN * 60000);
  const link = joinLink(req);
  const q = new URLSearchParams({ action: 'TEMPLATE', text: TITLE, dates: stamp(start) + '/' + stamp(end), details: details(link) });
  if (link) q.set('location', link);
  res.statusCode = 302;
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Location', 'https://calendar.google.com/calendar/render?' + q.toString());
  res.end();
}
