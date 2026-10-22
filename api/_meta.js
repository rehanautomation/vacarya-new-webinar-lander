import { createHash } from 'node:crypto';

// Meta Conversions API: server half of the VIP "Purchase" event (split Test A).
// The browser half fires on /vip-application with the same event id (the payment_intent id),
// so Meta keeps one of the two. Off until META_PIXEL_ID + META_CAPI_TOKEN are set in Vercel.
// Optional: META_TEST_EVENT_CODE (shows events in Events Manager > Test events), META_GRAPH_VERSION.

const VERSION = process.env.META_GRAPH_VERSION || 'v26.0';

const sha = (v) => createHash('sha256').update(v, 'utf8').digest('hex');
const hashed = (v) => {
  const n = typeof v === 'string' ? v.trim().toLowerCase() : '';
  return n ? [sha(n)] : undefined;
};

export async function sendPurchase({ eventId, eventTime, value, currency, email, firstName, lastName, ip, ua, fbp, fbc, url }) {
  const pixel = process.env.META_PIXEL_ID;
  const token = process.env.META_CAPI_TOKEN;
  if (!pixel || !token) {
    console.log('CAPI off: META_PIXEL_ID / META_CAPI_TOKEN not set', eventId);
    return;
  }

  const user_data = {
    em: hashed(email),
    fn: hashed(firstName),
    ln: hashed(lastName),
    client_ip_address: ip || undefined,
    client_user_agent: ua || undefined,
    fbp: fbp || undefined,
    fbc: fbc || undefined,
  };

  const body = {
    data: [{
      event_name: 'Purchase',
      event_time: eventTime,
      event_id: eventId,
      action_source: 'website',
      event_source_url: url || 'https://event.hostvacarya.com/vip',
      user_data,
      custom_data: { value, currency: String(currency || 'usd').toUpperCase(), content_name: 'VIP Access', order_id: eventId },
    }],
    access_token: token, // in the body, not the URL, so it never shows in logs
  };
  if (process.env.META_TEST_EVENT_CODE) body.test_event_code = process.env.META_TEST_EVENT_CODE;

  const r = await fetch(`https://graph.facebook.com/${VERSION}/${pixel}/events`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(8000),
  });
  const text = await r.text();
  if (!r.ok) console.error('CAPI Purchase failed', r.status, eventId, text.slice(0, 500));
  else console.log('CAPI Purchase sent', eventId, text.slice(0, 200));
}
