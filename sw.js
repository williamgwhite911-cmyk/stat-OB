// StatFlight Service Worker — offline cache
const CACHE_NAME = 'statflight-v48';
const ASSETS = [
  './',
  './index.html',
  './adult.html',
  './ob.html',
  './peds.html',
  './ketamine-chart.html',
  './manifest.json',
  './icon.svg',
  './icon-180.png',
  './icon-192.png',
  './icon-512.png'
];
// Optional precache (won't block install if missing) — any PHI protocol PDFs the user has dropped in
const OPTIONAL_ASSETS = [
  './protocols/PHI_Medical.pdf',
  './protocols/PHI_Resusc.pdf',
  './protocols/PHI_Trauma.pdf',
  './protocols/PHI_Neuro.pdf',
  './protocols/PHI_Tox.pdf',
  './protocols/PHI_Neonate.pdf',
  './protocols/PHI_Ob.pdf',
  './protocols/PHI_Safer.pdf',
  './protocols/PHI_Analgesia.pdf',
  './protocols/PHI_Drugs.pdf',
  './protocols/PHI_Cardiovascular.pdf',
  './protocols/PHI_Operations.pdf',
  './protocols/PHI_Appdex.pdf'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS).then(() => {
        // Try to precache optional assets (PDF), don't fail install if missing
        return Promise.all(OPTIONAL_ASSETS.map((url) =>
          fetch(url).then((r) => r.ok ? cache.put(url, r.clone()) : null).catch(() => null)
        ));
      }))
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
          url.host.includes('fonts.gstatic.com') ||
          url.host.includes('cdnjs.cloudflare.com');
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
