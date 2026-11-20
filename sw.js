/* 技术单词训练器 Service Worker
 * 目标：首次打开后整页落到手机本地，之后秒开，断网也能用。
 * 策略：
 *   - 导航请求（打开页面）：cache-first + 后台静默更新（stale-while-revalidate，体感最快）
 *   - 其它静态资源：cache-first
 *   - 离线且没缓存：回退到缓存的首页
 * 版本号：改动页面内容后把 CACHE 版本 +1，用户下次打开自动换新
 */
const CACHE = 'wordtrainer-v4';
const PAGE = './index.html';

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE)
      .then((c) => c.addAll([PAGE, './']).catch(() => c.add(PAGE)))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // 跨域不管

  // 页面导航：先给缓存（秒开），同时后台拉新版本写回缓存
  if (req.mode === 'navigate') {
    e.respondWith(
      caches.match(PAGE).then((hit) => {
        const net = fetch(req).then((res) => {
          if (res && res.ok) {
            const copy = res.clone();
            caches.open(CACHE).then((c) => c.put(PAGE, copy));
          }
          return res;
        }).catch(() => hit);
        return hit || net;
      })
    );
    return;
  }

  // 其它资源：cache-first，未命中则联网并写缓存
  e.respondWith(
    caches.match(req).then((hit) => {
      if (hit) return hit;
      return fetch(req).then((res) => {
        if (res && res.ok && res.type === 'basic') {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      }).catch(() => caches.match(PAGE));
    })
  );
});
