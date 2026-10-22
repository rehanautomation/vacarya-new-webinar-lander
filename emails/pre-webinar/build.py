#!/usr/bin/env python3
"""Build the pre-webinar emails from copy_data.py.

  python3 build.py

Writes:
  templates/email-NN.html  real GHL Code-editor templates (merge fields kept raw)
  manifest.json            name / subject / preview / fromName / file per email (used for the API push)
  preview.html             approval page (artifact) showing every email + SMS
"""
import html, json, pathlib, re
from copy_data import EMAILS, SMS, CASE_STUDIES, CASE_LINKS, CAL_BUTTON_EMAILS, CHANGES

ROOT = pathlib.Path(__file__).resolve().parent
API = 'https://new-webinar-lander.vercel.app'
URLS_GHL = {
    'WJ': '{{contact.webinar_link}}',
    'GCAL': '{{contact.webinar_calendar_link}}',   # direct Google Calendar link, written per contact by n8n WJ2 (n8n-calendar-link.js)
    'ICS': API + '/api/ics?link={{contact.webinar_link}}',
}
BLUE, DARK = '#0096D1', '#0072B5'
TINT, LINE = '#EAF6FC', '#B8E4F7'   # email background tint + divider
SUPPORT = '{{ custom_values.support_email }}'
LOGO = 'https://hostvacarya.com/wp-content/uploads/2026/10/vacarya-logo-header-dark.png'  # same dark wordmark as the webinar landing page (index.html)
FONT = 'Arial,Helvetica,sans-serif'
P = 'margin:0 0 16px;'   # font/size/colour come from the wrapping cell


def cs_value(name):
    return '{{ custom_values.case_study_%s }}' % name


def url_for(key, mode):
    if key.startswith('CS:'):
        return cs_value(key[3:]) if mode == 'ghl' else (CASE_LINKS.get(key[3:]) or '#needed')
    if mode == 'ghl':
        return URLS_GHL[key]
    return {'WJ': '#', 'GCAL': API + '/api/gcal', 'ICS': API + '/api/ics'}[key]


def chip(label):
    return f'<span class="mf" title="Filled in by GHL">{html.escape(label)}</span>'


MERGE_LABELS = {'{{contact.first_name}}': 'first name', '{{contact.webinar_link}}': 'their join link'}


def inline(text, mode):
    """Escape, then apply [text](URL), **bold**, merge-field chips (preview only), line breaks."""
    out, pos = [], 0
    for m in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', text):
        out.append(('t', text[pos:m.start()]))
        out.append(('a', m.group(1), m.group(2)))
        pos = m.end()
    out.append(('t', text[pos:]))

    def esc(s):
        s = html.escape(s, quote=False)
        s = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', s)
        s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
        s = re.sub(r'(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])', r'<em>\1</em>', s)
        if mode == 'preview':
            for k, v in MERGE_LABELS.items():
                s = s.replace(html.escape(k, quote=False), chip(v))
        return s.replace('\n', '<br>')

    parts = []
    for item in out:
        if item[0] == 't':
            parts.append(esc(item[1]))
            continue
        _, label, key = item
        href = url_for(key, mode)
        if mode == 'ghl':
            parts.append(f'<a href="{href}" style="color:{DARK};text-decoration:underline;">{esc(label)}</a>')
        elif key.startswith('CS:') and not CASE_LINKS.get(key[3:]):
            parts.append(f'<a href="#needed" class="need" title="Case study link still needed">{esc(label)}</a>')
        elif key == 'WJ':
            parts.append(f'<a href="#" class="wj" title="Opens their own WebinarJam link" onclick="return false">{esc(label)}</a>')
        else:
            parts.append(f'<a href="{href}" target="_blank" rel="noopener" style="color:{DARK};">{esc(label)}</a>')
    return ''.join(parts)


def button(label, key, mode):
    href = url_for(key, mode)
    extra = ' onclick="return false" title="Opens their own WebinarJam link"' if (mode == 'preview' and key == 'WJ') else ''
    tgt = ' target="_blank" rel="noopener"' if (mode == 'preview' and href.startswith('http')) else ''
    return (f'<table role="presentation" align="center" cellpadding="0" cellspacing="0" border="0" style="margin:12px auto 20px;"><tr>'
            f'<td style="background:{BLUE};border-radius:6px;">'
            f'<a href="{href}"{tgt}{extra} style="display:inline-block;padding:14px 28px;font-family:{FONT};font-size:16px;'
            f'font-weight:bold;letter-spacing:0.3px;color:#ffffff;text-decoration:none;">{html.escape(label)}</a>'
            f'</td></tr></table>')


def blocks(body, mode):
    rows = []
    for b in body:
        if b.startswith('BTN:'):
            label, key = b[4:].split('|')
            rows.append(button(label, key, mode))
        elif b.startswith('CTA:'):
            label, key = b[4:].split('|')
            rows.append(f'<p style="margin:4px 0 20px;text-align:center;font-family:{FONT};font-size:16px;line-height:1.5;">'
                        + inline(f'[>> {label} <<]({key})', mode).replace('<a ', '<a data-cta="1" ', 1)
                        .replace(f'style="color:{DARK};text-decoration:underline;"', f'style="color:{DARK};font-weight:bold;text-decoration:underline;"')
                        + '</p>')
        elif b.startswith('SMALL:'):
            rows.append(f'<p style="margin:0 0 16px;text-align:center;font-family:{FONT};font-size:14px;line-height:1.5;color:#4A5A6A;">{inline(b[6:], mode)}</p>')
        elif b.startswith('LIST:'):
            items = ''.join(f'<li style="margin:0 0 8px;">{inline(x, mode)}</li>' for x in b[5:].split('||'))
            rows.append(f'<ul style="margin:0 0 16px;padding-left:22px;font-family:{FONT};font-size:16px;line-height:1.6;color:#1a1a1a;">{items}</ul>')
        else:
            rows.append(f'<p style="{P}">{inline(b, mode)}</p>')
    return '\n'.join(rows)


def body_of(e):
    body = list(e['body'])
    if e['n'] in CAL_BUTTON_EMAILS:
        body += ['BTN:ADD EVENT TO CALENDAR|GCAL', 'SMALL:Using Apple Calendar or Outlook? [Add it here](ICS).']
    return body


def footer(mode):
    mail = chip('support email') if mode == 'preview' else SUPPORT
    href = '#' if mode == 'preview' else 'mailto:' + SUPPORT
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:12px 0 0;"><tr>'
            f'<td style="border-top:1px solid {LINE};font-size:0;line-height:0;">&nbsp;</td></tr></table>'
            f'<p style="margin:20px 0 6px;text-align:center;font-family:{FONT};font-size:14px;line-height:1.5;color:#1a1a1a;"><strong>Need Help? Contact Us:</strong></p>'
            f'<p style="margin:0 0 20px;text-align:center;font-family:{FONT};font-size:14px;line-height:1.5;">'
            f'<a href="{href}" style="color:{DARK};text-decoration:underline;">{mail}</a></p>'
)


def header(mode):
    if mode == 'preview':
        return '<p style="margin:0 0 28px;text-align:center;"><span class="logo">VACARYA logo</span></p>'
    return (f'<p style="margin:0 0 28px;text-align:center;"><img src="{LOGO}" width="160" alt="Vacarya" '
            f'style="display:inline-block;width:160px;max-width:160px;height:auto;border:0;"></p>')


def ghl_template(e):
    inner = header('ghl') + '\n' + blocks(body_of(e), 'ghl') + '\n' + footer('ghl')
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(e['subject'])}</title>
</head>
<body style="margin:0;padding:0;background:{TINT};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{TINT};">
<tr><td align="center" style="padding:28px 20px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:600px;">
<tr><td align="left" style="font-family:{FONT};font-size:16px;line-height:1.6;color:#1a1a1a;">
{inner}
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>
'''


def template_name(e):
    return f"{e['n']:02d} - {e['timing']} - {e['purpose']}"   # inside the "Pre-Webinar" folder


# ---------- SMS sizing ----------
GSM = set("@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !\"#¤%&'()*+,-./0123456789:;<=>?¡ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà")
GSM_EXT = set('^{}\\[~]|€')
SAMPLE = {'{{contact.first_name}}': 'Jessica', '{{contact.webinar_link}}': 'https://event.webinarjam.com/go/live/4/abcd1234efgh5678'}


def sms_size(text):
    t = text
    for k, v in SAMPLE.items():
        t = t.replace(k, v)
    if all(c in GSM or c in GSM_EXT for c in t):
        n = sum(2 if c in GSM_EXT else 1 for c in t)
        seg = 1 if n <= 160 else -(-n // 153)
        return n, seg, 'GSM-7'
    n = len(t)
    seg = 1 if n <= 70 else -(-n // 67)
    return n, seg, 'UCS-2'


# ---------- preview page ----------
def preview_page():
    days = []
    for d in ['Registration', 'Monday', 'Tuesday', 'Wednesday']:
        days.append((d, [e for e in EMAILS if e['day'] == d]))

    cards = []
    for d, es in days:
        anchor = d.lower()
        items = []
        for e in es:
            items.append(f'''
      <article class="mail" id="email-{e['n']}">
        <div class="meta">
          <div class="num">Email {e['n']}</div>
          <div class="when">{html.escape(e['when'])}</div>
          <dl>
            <dt>From</dt><dd>{html.escape(e['sender'])}<br><span class="mono">{html.escape(e['sender_email'])}</span></dd>
            <dt>Subject</dt><dd class="subj">{html.escape(e['subject'])}</dd>
            <dt>Preview</dt><dd>{html.escape(e['preview'])}</dd>
            <dt>Template</dt><dd class="mono">{html.escape(template_name(e))}</dd>
          </dl>
        </div>
        <div class="paper"><div class="inbox"><span class="from">{html.escape(e['sender'])} <span class="pv">&lt;{html.escape(e['sender_email'])}&gt;</span></span><span class="line"><b>{html.escape(e['subject'])}</b> <span class="pv">– {html.escape(e['preview'])}</span></span></div>
          <div class="body">{header('preview')}{blocks(body_of(e), 'preview')}{footer('preview')}</div>
        </div>
      </article>''')
        cards.append(f'''
    <section class="day" id="{anchor}">
      <h2>{d}</h2>
      {''.join(items)}
    </section>''')

    sms_groups = {}
    for s in SMS:
        sms_groups.setdefault(s['group'], []).append(s)
    sms_html = []
    for g, items in sms_groups.items():
        rows = []
        for s in items:
            n, seg, enc = sms_size(s['text'])
            body = html.escape(s['text'], quote=False)
            for k, v in MERGE_LABELS.items():
                body = body.replace(html.escape(k, quote=False), chip(v))
            body = body.replace('\n', '<br>')
            rows.append(f'''
        <div class="sms">
          <div class="smeta"><span class="num">{s['label']}</span><span class="when">{html.escape(s['when'])}</span><span class="size">~{n} chars · {seg} segment{'s' if seg > 1 else ''} · {enc}</span></div>
          <div class="bubble">{body}</div>
        </div>''')
        sms_html.append(f'<div class="sgroup"><h3>{html.escape(g)}</h3>{"".join(rows)}</div>')

    missing = [k for k in CASE_STUDIES if not CASE_LINKS.get(k)]
    needed = ''.join(f'<li><code>case_study_{k}</code> <span>{html.escape(CASE_STUDIES[k])}</span></li>' for k in missing)
    found = ''.join(f'<li><code>case_study_{k}</code> <span>{html.escape(CASE_STUDIES[k])}: <a href="{CASE_LINKS[k]}" target="_blank" rel="noopener">found in Aiden\'s old emails</a></span></li>' for k in CASE_STUDIES if CASE_LINKS.get(k))
    changes = ''.join(f'<li>{c}</li>' for c in CHANGES)

    return f'''<title>Pre-Webinar Sequence</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: approval sheet. Each email = meta column beside a white "inbox paper" copy of the real email; days are the sections. */
:root {{
  --bg:#F4F7FA; --surface:#FFFFFF; --fg:#0C2440; --muted:#5A6B80; --line:#D9E3EC;
  --accent:#0072B5; --accent-soft:#E6F6FD; --warn:#8A5A00; --warn-bg:#FFF1CC;
  --bubble:#E9EEF4; --bubble-fg:#0C2440;
  --display:"Manrope", "Segoe UI", system-ui, sans-serif;
  --mono:"IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
  --paper:#FFFFFF; --paper-line:#E3E8EE;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#0B1622; --surface:#112131; --fg:#E4EDF6; --muted:#93A6BA; --line:#22384D;
  --accent:#4CC3F0; --accent-soft:#12324A; --warn:#FFD27A; --warn-bg:#3A2C0C;
  --bubble:#1A3046; --bubble-fg:#E4EDF6; --paper-line:#22384D; color-scheme:dark }} }}
:root[data-theme="dark"] {{
  --bg:#0B1622; --surface:#112131; --fg:#E4EDF6; --muted:#93A6BA; --line:#22384D;
  --accent:#4CC3F0; --accent-soft:#12324A; --warn:#FFD27A; --warn-bg:#3A2C0C;
  --bubble:#1A3046; --bubble-fg:#E4EDF6; --paper-line:#22384D; color-scheme:dark }}
* {{ box-sizing:border-box }}
body {{ background:var(--bg); color:var(--fg); font-family:var(--display); font-size:15px; line-height:1.55;
  padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); padding-block:28px 64px }}
.wrap {{ max-width:1120px; margin:0 auto; display:flex; flex-direction:column; gap:28px }}
header {{ display:flex; flex-direction:column; gap:10px }}
.eyebrow {{ font-family:var(--mono); font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--muted) }}
h1 {{ font-size:clamp(28px, 5vw, 40px); font-weight:800; line-height:1.1; margin:0; text-wrap:balance; letter-spacing:-.01em }}
.sub {{ color:var(--muted); margin:0; max-width:65ch }}
nav.days {{ display:flex; flex-wrap:wrap; gap:8px }}
nav.days a {{ font-family:var(--mono); font-size:13px; color:var(--accent); text-decoration:none; border:1px solid var(--line); background:var(--surface); padding:6px 12px; border-radius:999px }}
nav.days a:hover, nav.days a:focus-visible {{ border-color:var(--accent); outline:none }}
.notes {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(300px, 1fr)); gap:16px; align-items:start }}
.note {{ background:var(--surface); border:1px solid var(--line); border-radius:10px; padding:18px 20px; min-width:0 }}
.note h2 {{ font-size:16px; margin:0 0 10px; font-weight:800 }}
.note.warn {{ background:var(--warn-bg); border-color:transparent; color:var(--fg) }}
.note.warn h2 {{ color:var(--warn) }}
.note ul {{ margin:0; padding-left:18px; display:flex; flex-direction:column; gap:6px }}
.note li span {{ color:var(--muted) }}
.note.warn li span {{ color:var(--fg) }}
.note p {{ margin:10px 0 0; color:var(--muted); font-size:14px }}
.note.warn p {{ color:var(--fg) }}
code, .mono {{ font-family:var(--mono); font-size:12.5px; overflow-wrap:anywhere }}
details summary {{ cursor:pointer; font-weight:800; font-size:16px }}
details[open] summary {{ margin-bottom:10px }}
.day {{ display:flex; flex-direction:column; gap:20px; scroll-margin-top:16px }}
.day h2 {{ font-size:22px; font-weight:800; margin:8px 0 0; padding-bottom:8px; border-bottom:2px solid var(--fg) }}
.mail {{ display:grid; grid-template-columns:270px minmax(0, 1fr); gap:20px; align-items:start; scroll-margin-top:16px }}
.meta {{ position:sticky; top:16px; display:flex; flex-direction:column; gap:6px; min-width:0 }}
.num {{ font-family:var(--mono); font-size:12px; letter-spacing:.06em; text-transform:uppercase; color:var(--accent); font-weight:500 }}
.when {{ font-weight:800; font-size:17px }}
dl {{ margin:6px 0 0; display:grid; grid-template-columns:72px minmax(0, 1fr); gap:6px 10px; font-size:13.5px }}
dt {{ color:var(--muted); font-family:var(--mono); font-size:11.5px; text-transform:uppercase; letter-spacing:.05em; padding-top:2px }}
dd {{ margin:0; min-width:0; overflow-wrap:anywhere }}
dd.subj {{ font-weight:700 }}
.paper {{ background:#EAF6FC; border:1px solid var(--paper-line); border-radius:10px; overflow:hidden; min-width:0; color:#1a1a1a }}
.inbox {{ display:flex; flex-direction:column; gap:2px; padding:12px 20px; border-bottom:1px solid #D4E6F0; background:#FFFFFF; font-family:Arial, Helvetica, sans-serif; font-size:13.5px; color:#1a1a1a }}
.inbox .from {{ font-weight:700 }}
.inbox .pv {{ color:#667085 }}
.body {{ padding:28px 20px 24px; max-width:640px; margin:0 auto }}
.body a {{ color:#0072B5 }}
.mf {{ display:inline-block; font-family:var(--mono); font-size:.78em; line-height:1.3; padding:1px 6px; border-radius:4px; background:#E6F6FD; color:#0072B5; border:1px solid #B8E4F7; vertical-align:1px }}
.body a.need, .body a.need:visited {{ background:#FFF1CC; color:#8A5A00; text-decoration:none; border-bottom:2px dashed #C98A00; padding:0 2px }}
.body a.need::after {{ content:" ⚑ link needed"; font-family:var(--mono); font-size:11px }}
.body a.wj {{ cursor:help }}
.body a[data-cta] {{ font-weight:700 }}
.logo {{ display:inline-block; font-family:Arial, Helvetica, sans-serif; font-weight:700; letter-spacing:.18em; font-size:13px; color:#062F65; border:1px dashed #9CC9E2; padding:6px 12px; border-radius:4px }}
.smsw {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:24px }}
.sgroup {{ display:flex; flex-direction:column; gap:14px; min-width:0 }}
.sgroup h3 {{ margin:0; font-size:16px; font-weight:800 }}
.sms {{ display:flex; flex-direction:column; gap:6px }}
.smeta {{ display:flex; flex-wrap:wrap; gap:4px 10px; align-items:baseline; font-size:13px }}
.smeta .when {{ font-size:13.5px }}
.smeta .size {{ font-family:var(--mono); font-size:11.5px; color:var(--muted); font-variant-numeric:tabular-nums }}
.bubble {{ background:var(--bubble); color:var(--bubble-fg); border-radius:16px 16px 16px 4px; padding:12px 14px; max-width:420px; font-size:14.5px; line-height:1.45; overflow-wrap:anywhere }}
.bubble .mf {{ background:var(--accent-soft); color:var(--accent); border-color:var(--line) }}
footer {{ color:var(--muted); font-size:13px }}
@media (max-width: 760px) {{
  .mail {{ grid-template-columns:minmax(0, 1fr) }}
  .meta {{ position:static }}
  .body {{ padding:20px 16px 4px }}
}}
@media (prefers-reduced-motion: no-preference) {{ html {{ scroll-behavior:smooth }} }}
</style>

<div class="wrap">
  <header>
    <div class="eyebrow">Webinar sub-account · draft for approval · nothing is in GHL yet</div>
    <h1>Pre-Webinar Sequence</h1>
    <p class="sub">12 emails and 9 texts from Aiden's doc, ready to load into GHL once approved. Each email below is the real template. Blue tags are filled in by GHL for each person.</p>
    <nav class="days" aria-label="Jump to">
      <a href="#registration">Registration</a><a href="#monday">Monday</a><a href="#tuesday">Tuesday</a><a href="#wednesday">Wednesday</a><a href="#sms">SMS</a>
    </nav>
  </header>

  <div class="notes">
    <div class="note warn" id="needed">
      <h2>{len(missing)} case study links needed</h2>
      <ul>{needed}</ul>
      <p><strong>Already have:</strong></p>
      <ul>{found}</ul>
      <p>Each one will be a GHL custom value, so the links can be added later in one place without touching the emails. Until filled, these links go nowhere, so fill them before the switch.</p>
    </div>
    <div class="note">
      <details open>
        <summary>What I changed from Aiden's doc</summary>
        <ul>{changes}</ul>
      </details>
    </div>
  </div>

  {''.join(cards)}

  <section class="day" id="sms">
    <h2>SMS</h2>
    <div class="smsw">{''.join(sms_html)}</div>
  </section>

  <footer>Send times are Toronto time. Segment counts assume a 7-letter first name and a typical WebinarJam link.</footer>
</div>
'''


def main():
    manifest = []
    for e in EMAILS:
        f = ROOT / 'templates' / f"email-{e['n']:02d}.html"
        f.write_text(ghl_template(e))
        manifest.append({'n': e['n'], 'name': template_name(e), 'subjectLine': e['subject'], 'previewText': e['preview'],
                         'fromName': e['sender'], 'fromEmail': e['sender_email'], 'file': str(f.relative_to(ROOT)), 'when': e['when']})
    (ROOT / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    (ROOT / 'preview.html').write_text(preview_page())  # published as artifact 'Pre-Webinar Sequence' (not committed)
    for s in SMS:
        n, seg, enc = sms_size(s['text'])
        print(f"{s['group'][:12]:12} {s['label']}: {n:4} chars {seg} seg {enc}")
    print('emails:', len(EMAILS))


if __name__ == '__main__':
    main()
