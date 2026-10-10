import Stripe from 'stripe';

// Pinned to the same API version as the Stripe webhook destination.
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY, {
  apiVersion: '2025-04-30.basil',
});

// Price lives on the server only, so nobody can change it in the browser.
export const VIP = {
  amount: 2700,          // $27.00 (placeholder until Aiden confirms)
  currency: 'usd',
  description: 'Vacarya VIP Access',
};

export function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'content-type': 'application/json', 'cache-control': 'no-store' },
  });
}
