// Cortes de señal al pasar de un capítulo al siguiente (servidor de prueba en :8802, como salto.mjs), sin el
// service worker: así se prueba lo que hace la página en un navegador que no lo tenga (carga.mjs prueba el otro caso).
// 1. Con la pantalla bloqueada (página oculta) el capítulo siguiente suena igual.
// 3. Si fallan las dos primeras cargas, reintenta sola y sigue.
// 4. Sin conexión espera, y cuando vuelve la señal sigue sola.
// 5. Si falla al empezar en un versículo, retoma en ese versículo y no en el 0.
// 6. Si la persona pausó, que vuelva la señal no la hace sonar.
import { chromium } from "playwright";
const BASE = process.env.BASE ?? "http://127.0.0.1:8802/index.html";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--autoplay-policy=no-user-gesture-required"] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: "reduce", serviceWorkers: "block" });
await ctx.addInitScript(() => {
  const O = window.Audio; window.Audio = function (...a) { const x = new O(...a); window.__audio = x; return x; }; window.Audio.prototype = O.prototype;
  Object.defineProperty(Document.prototype, "visibilityState", { configurable: true, get() { return window.__oculto ? "hidden" : "visible"; } });
});
const p = await ctx.newPage(); p.setDefaultTimeout(30000);
const errores = []; p.on("pageerror", (e) => errores.push(e.message));
const fallos = [];
const ok = (c, q) => { console.log((c ? "  ok  " : "  MAL ") + q); if (!c) fallos.push(q); };
// Hace fallar las cargas del audio que se pida, contando solo las del reproductor (no la precarga).
let romper = { archivo: null, veces: 0, precarga: false };
await p.route("**/audio/*", async (r) => {
  const archivo = r.request().url().split("/").pop();
  const media = r.request().resourceType() === "media";
  if (archivo === romper.archivo && ((media && romper.veces > 0) || (!media && romper.precarga))) {
    if (media) romper.veces--;
    return r.abort("internetdisconnected");
  }
  return r.continue();
});
const estado = () => p.evaluate(() => ({ archivo: window.__audio.dataset.archivo, blob: window.__audio.src.startsWith("blob:"), sonando: !window.__audio.paused && window.__audio.readyState >= 2, t: window.__audio.currentTime, aviso: document.getElementById("que-suena").textContent }));
const alFinal = (seg) => p.evaluate((s) => { window.__audio.currentTime = window.__audio.duration - s; }, seg);
const esperarSonando = (archivo) => p.waitForFunction((a) => window.__audio.dataset.archivo === a && !window.__audio.paused && window.__audio.currentTime > 0.3, archivo);

await p.goto(BASE + "?corte#GEN-30", { waitUntil: "load" });
await p.getByRole("button", { name: "Escuchar el capítulo" }).click();
await esperarSonando("GEN-30.mp3");

// 1. Pantalla bloqueada: el siguiente sale por su dirección.
await p.evaluate(() => { window.__audio.currentTime = 12; });
await p.waitForTimeout(400);
await alFinal(200);                       // entra en los últimos cinco minutos: precarga GEN-31
await p.waitForTimeout(2500);
await p.evaluate(() => { window.__oculto = true; document.dispatchEvent(new Event("visibilitychange")); });
await alFinal(1);
await esperarSonando("GEN-31.mp3");
let e = await estado();
ok(!e.blob && !e.aviso.startsWith("Sin señal"), `con la página oculta, GEN-31 suena (${e.archivo})`);
await p.evaluate(() => { window.__oculto = false; document.dispatchEvent(new Event("visibilitychange")); });

// 3. Las dos primeras cargas de GEN-32 fallan: reintenta y sigue.
romper = { archivo: "GEN-32.mp3", veces: 2, precarga: true };
await alFinal(1);
await p.waitForFunction(() => document.getElementById("que-suena").textContent.startsWith("Sin señal. Reintentando"), null, { timeout: 8000 });
ok(true, "avisa «Sin señal. Reintentando…»");
await esperarSonando("GEN-32.mp3");
ok(romper.veces === 0, "GEN-32 suena después de dos cargas fallidas, sin tocar nada");
romper = { archivo: null, veces: 0, precarga: false };

// 4. Sin conexión: espera y sigue sola cuando vuelve la señal.
await ctx.setOffline(true);
await alFinal(1);
await p.waitForFunction(() => window.__audio.dataset.archivo === "GEN-33.mp3");
await p.waitForFunction(() => document.getElementById("que-suena").textContent === "Sin señal. Seguirá cuando vuelva", null, { timeout: 20000 }).catch(() => {});
e = await estado();
ok(e.aviso === "Sin señal. Seguirá cuando vuelva", `sin conexión avisa que seguirá: «${e.aviso}»`);
await ctx.setOffline(false);
await esperarSonando("GEN-33.mp3");
ok(true, "vuelve la señal y GEN-33 suena solo");

// 5. Falla al empezar en el versículo 10 de GEN-34: retoma en el 10.
romper = { archivo: "GEN-34.mp3", veces: 1, precarga: true };
await p.getByRole("button", { name: "Pausar" }).click();
await p.locator('.pie-cap [data-ir="GEN-34"]').click();
await p.locator('.v[data-k="v10"]').click();
await esperarSonando("GEN-34.mp3");
await p.waitForTimeout(4500);   // el avance se guarda cada 4 segundos
e = await estado();
const t10 = await p.evaluate(() => fetch("contenido.json").then((r) => r.json()).then((c) => c.libros[0].capitulos[33].audio.partes.find((x) => x.clave === "v10").t));
ok(e.t >= t10 - 0.5, `retoma en el versículo 10 (${e.t.toFixed(1)} s; el 10 empieza en ${t10.toFixed(1)} s)`);
const pos = await p.evaluate(() => JSON.parse(localStorage.getItem("gel:pos")));
ok(pos.id === "GEN-34" && pos.t >= t10 - 3, `el avance guardado no volvió a 0 (${pos.id} en ${pos.t.toFixed(1)} s)`);
romper = { archivo: null, veces: 0, precarga: false };

// 6. Pausado a propósito: un corte y la vuelta de la señal no lo hacen sonar.
await p.getByRole("button", { name: "Pausar" }).click();
await ctx.setOffline(true); await p.waitForTimeout(500); await ctx.setOffline(false); await p.waitForTimeout(1500);
e = await estado();
ok(!e.sonando, "si la persona pausó, sigue en pausa");

console.log("errores de la página:", errores);
console.log(fallos.length ? `FALLAN ${fallos.length}: ${fallos.join(" | ")}` : "todo bien");
await b.close();
