const CACHE_NAME = 'nexa-v3';
const urlsToCache = [
  './',
  'index.html',
  'manifest.json',
  'data/baleno_6_airbag.json',
  'data/ciaz.json',
  'data/grand_vitara_6_airbag.json',
  'data/ignis.json',
  'data/invicto.json',
  'data/jimny.json',
  'data/new_fronx_6_airbag.json',
  'data/new_xl6_6_airbag.json',
  'data/baleno_features.json',
  'data/ciaz_features.json',
  'data/grand_vitara_features.json',
  'data/ignis_features.json',
  'data/invicto_features.json',
  'data/jimny_features.json',
  'data/fronx_features.json',
  'data/xl6_features.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
      .catch(() => caches.match('index.html'))
  );
});
