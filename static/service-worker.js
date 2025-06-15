self.addEventListener("install", e => {
  console.log("Service Worker Installed");
  e.waitUntil(
    caches.open("cat-tracker-cache").then(cache => {
      return cache.addAll([
        "/",
        "/static/style.css",
        "/static/icons/anh nhi.png",
        "/static/icons/si lun.png"
      ]);
    })
  );
});

self.addEventListener("fetch", e => {
  e.respondWith(
    caches.match(e.request).then(response => {
      return response || fetch(e.request);
    })
  );
});
