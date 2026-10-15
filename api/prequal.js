// Pre-qualification answers (shown after VIP checkout) -> GHL.
// Same pattern as the VIP purchase: we forward to a GHL "Inbound Webhook" workflow trigger,
// and that workflow saves the answers onto the contact (matched by email).
// Turn on by setting GHL_PREQUAL_WEBHOOK_URL in Vercel.

const OPTIONS = {
  capital: ['Less than $50,000', '$50,000 - $100,000', '$100,000 - $250,000', '$250,000 - $500,000+'],
  situation: [
    'I am completely new to Airbnb',
    'I understand the basics but have not secured my first property',
    "I have at least one property in my portfolio and I'm looking to expand",
  ],
  timeline: ["I'm ready to start right away", 'Within 30 days', '30-60 days', '3-6 months', 'Just exploring for now'],
};

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });
}

const clean = (v, max) => String(v == null ? '' : v).trim().slice(0, max);

export async function POST(request) {
  let b;
  try { b = await request.json(); } catch { return json({ error: 'Bad request' }, 400); }

  const data = {
    email: clean(b.email, 200).toLowerCase(),
    first_name: clean(b.first_name, 80),
    last_name: clean(b.last_name, 80),
    goal: clean(b.goal, 3000),
    capital: clean(b.capital, 100),
    situation: clean(b.situation, 150),
    timeline: clean(b.timeline, 100),
    payment_intent: clean(b.payment_intent, 100),
  };

  // Email comes from checkout via the URL; the form never asks for it again.
  if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) data.email = '';
  if (!data.email) console.warn('prequal: submitted without email (page opened without checkout params)');
  if (data.goal.length < 3) return json({ error: 'Please answer the first question.' }, 400);
  for (const k of ['capital', 'situation', 'timeline']) {
    if (!OPTIONS[k].includes(data[k])) return json({ error: 'Please answer every question.' }, 400);
  }

  const hook = process.env.GHL_PREQUAL_WEBHOOK_URL;
  if (!hook) {
    // Not connected to GHL yet: never block a paying buyer. Answers are kept in the Vercel logs until the webhook is set.
    console.log('PREQUAL_UNSENT ' + JSON.stringify(data));
    return json({ ok: true, saved: 'logs' });
  }

  try {
    const r = await fetch(hook, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ ...data, source: 'VIP pre-qualification', submitted_at: new Date().toISOString() }),
    });
    if (!r.ok) throw new Error('GHL responded ' + r.status);
  } catch (e) {
    console.error('prequal: GHL forward failed', e.message, data.email);
    return json({ error: 'Something went wrong on our side. Please try again in a minute.' }, 502);
  }

  return json({ ok: true });
}
