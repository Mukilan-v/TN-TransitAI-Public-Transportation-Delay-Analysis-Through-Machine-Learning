// TN-TransitAI Service Worker - PWA Offline Support & Cache Management
// Version: v11.0 - Full Zero-WiFi / Offline Caching & Cross-Platform Support
const CACHE_NAME = 'tn-transit-ai-v11.0';

const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon-maskable.png',
  './Tamil_Nadu_Smart_Transport_AI_Technology_Stack.pdf',
  './Tamil_Nadu_Smart_Transport_AI_Technology_Stack.html',
  'https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Rajdhani:wght@600;700&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
  'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
  'https://cdn.jsdelivr.net/npm/chart.js'
];

// Pre-cache all essential static assets & CDN libraries on install
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.allSettled(
        ASSETS_TO_CACHE.map((url) =>
          cache.add(url).catch((err) => {
            console.warn('[PWA SW] Precache optional asset skipped:', url, err);
          })
        )
      );
    }).then(() => self.skipWaiting())
  );
});

// Purge obsolete cache stores and claim control immediately
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Intelligent fetch router: Cache-First for static/CDN libraries, Network-First for dynamic navigation
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Identify static assets and remote CDN scripts/stylesheets/fonts
  const isStaticOrCDN =
    url.hostname.includes('cdnjs.cloudflare.com') ||
    url.hostname.includes('unpkg.com') ||
    url.hostname.includes('cdn.jsdelivr.net') ||
    url.hostname.includes('fonts.googleapis.com') ||
    url.hostname.includes('fonts.gstatic.com') ||
    url.pathname.includes('/icons/') ||
    url.pathname.endsWith('.png') ||
    url.pathname.endsWith('.jpg') ||
    url.pathname.endsWith('.jpeg') ||
    url.pathname.endsWith('.svg') ||
    url.pathname.endsWith('.pdf') ||
    url.pathname.endsWith('.css') ||
    url.pathname.endsWith('.js');

  if (isStaticOrCDN) {
    // Cache-First strategy: serve cached instantly, otherwise fetch & cache for offline
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(event.request)
          .then((networkResponse) => {
            if (networkResponse && (networkResponse.status === 200 || networkResponse.type === 'opaque')) {
              const clone = networkResponse.clone();
              caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
            }
            return networkResponse;
          })
          .catch(() => cachedResponse);
      })
    );
    return;
  }

  // Network-First strategy with seamless offline cache fallback for app navigation
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const clone = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) return cachedResponse;
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html') || caches.match('./');
          }
        });
      })
  );
});
