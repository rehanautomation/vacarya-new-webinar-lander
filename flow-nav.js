/* Review-only Back / Next buttons to walk the buyer flow.
   Shows on *.vercel.app and localhost only, so real visitors on our own domain never see it.
   × shrinks it to a small Nav button; tap that to bring it back. */
(function () {
  var host = location.hostname;
  var q = new URLSearchParams(location.search);
  try {
    if (q.get('nav') === '0') sessionStorage.setItem('vcFlowNav', 'off');
    if (q.get('nav') === '1') sessionStorage.removeItem('vcFlowNav');
  } catch (e) {}
  if (!/\.vercel\.app$/.test(host) && host !== 'localhost' && host !== '127.0.0.1') return;

  /* buyer flow: register -> VIP checkout -> VIP application -> VIP confirmed */
  var path = location.pathname.replace(/\.html$/, '').replace(/\/index$/, '/') || '/';
  var vipBuyer = q.get('vip') === '1';
  var STEPS = {
    '/':                 { n: 'Register',        back: null,                next: '/vip' },
    '/vip':              { n: 'VIP checkout',    back: '/',                 next: '/vip-application' },
    '/vip-application':  { n: 'VIP application', back: '/vip',              next: '/vip-confirmed' },
    '/vip-confirmed':    { n: 'VIP confirmed',   back: '/vip-application',  next: null },
    '/confirmed':        { n: vipBuyer ? 'Confirmed (VIP)' : 'Confirmed (free seat)', back: vipBuyer ? '/vip-application' : '/vip', next: null }
  };
  var s = STEPS[path];
  if (!s) return;
  var local = /\.html$/.test(location.pathname); /* local test server has no clean URLs */
  function href(p) { return local ? (p === '/' ? '/index.html' : p + '.html') : p; }

  var css = '#vc-flow{position:fixed;left:50%;bottom:12px;transform:translateX(-50%);z-index:2147483600;display:flex;align-items:center;gap:6px;padding:6px;' +
    'background:rgba(10,10,10,.88);border-radius:999px;box-shadow:0 6px 20px rgba(0,0,0,.25);font:600 13px/1 system-ui,-apple-system,"Segoe UI",sans-serif;-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px)}' +
    '#vc-flow a,#vc-flow span{display:inline-flex;align-items:center;height:32px;padding:0 14px;border-radius:999px;color:#fff;text-decoration:none;white-space:nowrap}' +
    '#vc-flow a{background:#00ABE5}#vc-flow a:hover{background:#0096D1}' +
    '#vc-flow a.off{background:#333;color:#777;pointer-events:none}' +
    '#vc-flow span{padding:0 8px;color:#cfd3d8;font-weight:500}' +
    '#vc-flow button{width:26px;height:26px;border:0;border-radius:50%;background:transparent;color:#999;font:16px/1 system-ui;cursor:pointer}' +
    '#vc-flow button:hover{color:#fff}';
  function mount() {
    var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
    var bar = document.createElement('div'); bar.id = 'vc-flow';
    bar.innerHTML =
      '<a ' + (s.back ? 'href="' + href(s.back) + '"' : 'class="off"') + '>&#8592; Back</a>' +
      '<span>' + s.n + '</span>' +
      '<a ' + (s.next ? 'href="' + href(s.next) + '"' : 'class="off"') + '>Next &#8594;</a>' +
      '<button type="button" title="Hide (this tab)" aria-label="Hide">&times;</button>';
    var full = bar.innerHTML, mini = '<button type="button" title="Show Back/Next" style="width:auto;padding:0 12px;height:32px;color:#fff">&#8596; Nav</button>';
    function set(off) { try { off ? sessionStorage.setItem('vcFlowNav', 'off') : sessionStorage.removeItem('vcFlowNav'); } catch (e) {}
      bar.innerHTML = off ? mini : full; bar.querySelector('button').onclick = function () { set(!off); }; }
    var startOff = false; try { startOff = sessionStorage.getItem('vcFlowNav') === 'off'; } catch (e) {}
    set(startOff);
    document.body.appendChild(bar);
    /* sit above the page's own sticky CTA bar when it shows */
    function lift() {
      var sticky = document.querySelector('.vc-sticky'), off = 12;
      if (sticky) { var r = sticky.getBoundingClientRect(), cs = getComputedStyle(sticky);
        if (cs.display !== 'none' && cs.visibility !== 'hidden' && r.height && r.top < innerHeight && r.bottom > innerHeight - 2) off = innerHeight - r.top + 8; }
      bar.style.bottom = off + 'px';
    }
    lift(); addEventListener('scroll', lift, { passive: true }); addEventListener('resize', lift); setInterval(lift, 500);
  }
  if (document.body) mount(); else document.addEventListener('DOMContentLoaded', mount);
})();
