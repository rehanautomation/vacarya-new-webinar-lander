import { stripe, VIP, json } from './_stripe.js';

const clean = (v, max = 200) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

export async function POST(request) {
  let body;
  try { body = await request.json(); } catch { return json({ error: 'Bad request.' }, 400); }

  const firstName = clean(body.firstName, 80);
  const lastName = clean(body.lastName, 80);
  const email = clean(body.email, 200).toLowerCase();
  const address = clean(body.address, 300);
  const method = body.method === 'wallet' ? 'wallet' : 'card';

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return json({ error: 'Please enter a valid email.' }, 400);
  }
  const name = [firstName, lastName].filter(Boolean).join(' ');

  try {
    let customer;
    try {
      customer = await stripe.customers.create({
        email,
        name: name || undefined,
        address: address ? { line1: address } : undefined,
        metadata: { source: 'vip-upsell' },
      });
    } catch (e) {
      console.error('customer create failed', e.message);
    }

    const pi = await stripe.paymentIntents.create({
      amount: VIP.amount,
      currency: VIP.currency,
      description: VIP.description,
      payment_method_types: ['card'], // card + Apple Pay + Google Pay
      customer: customer ? customer.id : undefined,
      receipt_email: email,
      metadata: { product: 'vip', first_name: firstName, last_name: lastName, email, method },
    });

    return json({ clientSecret: pi.client_secret });
  } catch (e) {
    console.error('payment intent failed', e.type, e.message);
    return json({ error: 'Checkout is having trouble. Please try again in a minute.' }, 500);
  }
}

// CORS preflight: the GHL pages on event.hostvacarya.com call this API (headers come from vercel.json)
export function OPTIONS() { return new Response(null, { status: 204 }); }
