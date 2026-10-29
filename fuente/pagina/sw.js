// Carga adelantada del audio, como en YouTube. Guarda completos el capítulo que suena y el siguiente, y los
// entrega por partes (rangos de bytes, que Safari exige para el audio): así se adelanta sin esperar, el
// capítulo siguiente empieza enseguida y un corte de internet no detiene lo que ya está guardado.
// Solo atiende los pedidos de audio/; la página, el contenido y el avance van siempre a la red.
const CACHE = "audio-v1";
const MAXIMO = 6;   // archivos guardados a la vez: unos 25 MB como mucho
const enCurso = new Map();

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil((async () => {
  for (const k of await caches.keys()) if (k.startsWith("audio-") && k !== CACHE) await caches.delete(k);
  await self.clients.claim();
})()));

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== self.location.origin || !/\/audio\/[\w-]+\.(mp4|mp3)$/.test(url.pathname)) return;
  e.respondWith(responder(e, url.origin + url.pathname));
});

async function responder(e, clave) {
  const cache = await caches.open(CACHE);
  const enCache = await cache.match(clave);
  if (enCache) return rango(e.request, { cuerpo: await enCache.blob(), tipo: enCache.headers.get("Content-Type") });
  const bajando = guardar(cache, clave);
  e.waitUntil(bajando);
  // Si el reproductor pide un rango de algo que todavía no está guardado, va a la red para empezar enseguida;
  // el archivo completo se termina de guardar en paralelo para lo que sigue.
  if (e.request.headers.has("range")) return fetch(e.request).catch(async () => { const g = await bajando; return g ? rango(e.request, g) : Response.error(); });
  const guardado = await bajando;
  return guardado ? rango(e.request, guardado) : fetch(e.request);
}

function guardar(cache, clave) {
  if (!enCurso.has(clave)) {
    enCurso.set(clave, (async () => {
      try {
        const r = await fetch(clave);
        if (r.status !== 200) return null;
        const cuerpo = await r.blob(), tipo = r.headers.get("Content-Type") || "audio/mp4";
        await cache.put(clave, new Response(cuerpo, { headers: { "Content-Type": tipo, "Content-Length": String(cuerpo.size) } }));
        await recortar(cache, clave);
        return { cuerpo, tipo };   // un Blob se puede leer muchas veces; una Response, una sola
      } catch {
        return null;
      } finally {
        enCurso.delete(clave);
      }
    })());
  }
  return enCurso.get(clave);
}

// Deja solo los últimos MAXIMO archivos guardados (cache.keys() los da en el orden en que entraron).
async function recortar(cache, nueva) {
  const claves = await cache.keys();
  for (const k of claves.slice(0, Math.max(0, claves.length - MAXIMO))) if (k.url !== nueva) await cache.delete(k);
}

function rango(req, { cuerpo, tipo }) {
  const total = cuerpo.size;
  tipo = tipo || "audio/mp4";
  const m = /^bytes=(\d*)-(\d*)$/.exec(req.headers.get("range") || "");
  if (!m || (m[1] === "" && m[2] === "")) return new Response(cuerpo, { status: 200, headers: { "Content-Type": tipo, "Content-Length": String(total), "Accept-Ranges": "bytes" } });
  const desde = m[1] === "" ? Math.max(0, total - Number(m[2])) : Number(m[1]);
  const hasta = m[1] === "" || m[2] === "" ? total - 1 : Math.min(Number(m[2]), total - 1);
  if (desde >= total || desde > hasta) return new Response(null, { status: 416, headers: { "Content-Range": `bytes */${total}` } });
  return new Response(cuerpo.slice(desde, hasta + 1), { status: 206, headers: {
    "Content-Type": tipo, "Content-Length": String(hasta - desde + 1), "Content-Range": `bytes ${desde}-${hasta}/${total}`, "Accept-Ranges": "bytes" } });
}
