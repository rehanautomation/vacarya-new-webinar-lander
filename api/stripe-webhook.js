import { stripe, json } from './_stripe.js';
import { sendPurchase } from './_meta.js';

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

    // Shared Stripe account: only our $27 VIP checkout goes to GHL + Meta.
    if (m.product === 'vip') {
      const email = m.email || pi.receipt_email;

      // Tag the buyer in GHL (workflow "VIP | Paid"). Set GHL_VIP_WEBHOOK_URL in Vercel to turn on.
      const ghl = process.env.GHL_VIP_WEBHOOK_URL;
      if (ghl) {
        try {
          await fetch(ghl, {
            method: 'POST',
            headers: { 'content-type': 'application/json' },
            body: JSON.stringify({
              email,
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

      // Meta Purchase (server half). event_id = payment_intent id, same as the browser event.
      try {
        await sendPurchase({
          eventId: pi.id,
          eventTime: event.created,
          value: pi.amount / 100,
          currency: pi.currency,
          email,
          firstName: m.first_name,
          lastName: m.last_name,
          ip: m.capi_ip,
          ua: m.capi_ua,
          fbp: m.capi_fbp,
          fbc: m.capi_fbc,
          url: m.capi_url,
        });
      } catch (e) {
        console.error('CAPI Purchase error', e.message);
      }
    }
  }

  return json({ received: true });
}
