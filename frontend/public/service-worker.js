const CACHE_NAME = 'jensy-cache-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/vite.svg'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);
  
  // Cache API requests related to dashboard and syllabus
  if (url.pathname.includes('/progress/dashboard') || url.pathname.includes('/syllabus')) {
    event.respondWith(
      caches.match(event.request)
        .then(response => {
          if (response) {
            // Fetch updated data in background
            fetch(event.request).then(res => {
              caches.open(CACHE_NAME).then(cache => {
                cache.put(event.request, res.clone());
              });
            });
            return response;
          }
          return fetch(event.request).then(
            response => {
              if(!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }
              var responseToCache = response.clone();
              caches.open(CACHE_NAME)
                .then(cache => {
                  cache.put(event.request, responseToCache);
                });
              return response;
            }
          );
        })
    );
  } else {
    // Network first, fallback to cache for static assets
    event.respondWith(
      fetch(event.request).catch(() => caches.match(event.request))
    );
  }
});

self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});
