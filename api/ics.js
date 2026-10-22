// GET /api/ics -> calendar file for the NEXT live training (Wednesday 7:00 PM Toronto time).
// Optional ?link=<their WebinarJam join link> (last param) puts the personal link in the event.
// A real file URL (not a data: link) is what Apple Calendar on iPhone and Outlook need to open it.
import { nextWebinar, stamp, joinLink, details, TITLE, LENGTH_MIN } from './_webinar.js';

// iCalendar text: escape \ ; , and newlines
const esc = (s) => String(s).replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n');

export default function handler(req, res) {
  const start = nextWebinar(), end = new Date(start.getTime() + LENGTH_MIN * 60000);
  const link = joinLink(req);
  const ics = [
    'BEGIN:VCALENDAR', 'VERSION:2.0', 'PRODID:-//Vacarya//Live Training//EN', 'CALSCALE:GREGORIAN', 'METHOD:PUBLISH',
    'BEGIN:VEVENT',
    'UID:live-training-' + stamp(start) + '@hostvacarya.com',
    'DTSTAMP:' + stamp(new Date()),
    'DTSTART:' + stamp(start), 'DTEND:' + stamp(end),
    'SUMMARY:' + esc(TITLE), 'DESCRIPTION:' + esc(details(link)),
    ...(link ? ['LOCATION:' + esc(link), 'URL:' + link] : []),
    'BEGIN:VALARM', 'ACTION:DISPLAY', 'DESCRIPTION:' + esc(TITLE + ' starts in 15 minutes'), 'TRIGGER:-PT15M', 'END:VALARM',
    'END:VEVENT', 'END:VCALENDAR', ''
  ].join('\r\n');
  res.setHeader('Content-Type', 'text/calendar; charset=utf-8');
  res.setHeader('Content-Disposition', 'attachment; filename="vacarya-live-training.ics"');
  res.setHeader('Cache-Control', 'no-store');
  res.status(200).send(ics);
}
