// StatFlight Service Worker — offline cache
const CACHE_NAME = 'statflight-v1';
const ASSETS = [
  './',
  './index.html',
  './ob.html',
  './peds.html',
  './manifest.json',
  './icon.svg'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  // Only handle GET
  if (e.request.method !== 'GET') return;

  e.respondWith(
    caches.match(e.request).then((cached) => {
      if (cached) return cached;
      return fetch(e.request).then((response) => {
        // Cache successful responses for same-origin & known CDNs
        const url = new URL(e.request.url);
        const cacheable =
          url.origin === self.location.origin ||
          url.host.includes('fonts.googleapis.com') ||
          url.host.includes('fonts.gstatic.com');
        if (cacheable && response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((c) => c.put(e.request, clone));
        }
        return response;
      }).catch(() => {
        // Offline: fall back to launcher for navigation
        if (e.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
      });
    })
  );
});
