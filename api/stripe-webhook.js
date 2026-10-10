import { stripe, json } from './_stripe.js';

export async function POST(request) {
  const sig = request.headers.get('stripe-signature');
  const raw = await request.text();

  let event;
  try {
    event = await stripe.webhooks.constructEventAsync(raw, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (e) {
    console.error('webhook signature failed', e.message);
    return json({ error: 'Invalid signature' }, 400);
  }

  if (event.type === 'payment_intent.succeeded') {
    const pi = event.data.object;
    const m = pi.metadata || {};
    console.log('VIP paid', pi.id, m.email, pi.amount);

    // Optional: tag the buyer in GHL. Set GHL_VIP_WEBHOOK_URL in Vercel to turn on.
    const ghl = process.env.GHL_VIP_WEBHOOK_URL;
    if (ghl && m.product === 'vip') {
      try {
        await fetch(ghl, {
          method: 'POST',
          headers: { 'content-type': 'application/json' },
          body: JSON.stringify({
            email: m.email || pi.receipt_email,
            first_name: m.first_name,
            last_name: m.last_name,
            amount: pi.amount / 100,
            currency: pi.currency,
            payment_intent: pi.id,
            product: 'VIP Access',
          }),
        });
      } catch (e) {
        console.error('GHL forward failed', e.message);
      }
    }
  }

  return json({ received: true });
}
