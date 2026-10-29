// Carga adelantada con el service worker (sw.js), como en YouTube (servidor de prueba en :8802, que manda los
// mismos encabezados que Vercel, con la política de seguridad):
// 1. Al escuchar un capítulo, quedan guardados enteros ese capítulo y el siguiente, y la barra se llena.
// 2. Sin internet, adelantar dentro del capítulo funciona y el audio sigue.
// 3. Sin internet, al terminar el capítulo empieza el siguiente enseguida.
// 4. Nada choca con la política de seguridad.
import { chromium } from "playwright";
const BASE = process.env.BASE ?? "http://127.0.0.1:8802/index.html";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--autoplay-policy=no-user-gesture-required"] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: "reduce", serviceWorkers: "allow" });
await ctx.addInitScript(() => { const O = window.Audio; window.Audio = function (...a) { const x = new O(...a); window.__audio = x; return x; }; window.Audio.prototype = O.prototype; });
const p = await ctx.newPage(); p.setDefaultTimeout(30000);
const errores = [];
p.on("pageerror", (e) => errores.push(e.message));
p.on("console", (m) => { if (m.type() === "error" || /Content Security Policy/.test(m.text())) errores.push(m.text().slice(0, 160)); });
const fallos = [];
const ok = (c, q) => { console.log((c ? "  ok  " : "  MAL ") + q); if (!c) fallos.push(q); };
const guardados = () => p.evaluate(async () => (await (await caches.open("audio-v1")).keys()).map((r) => r.url.split("/").pop()));
const estado = () => p.evaluate(() => ({ archivo: window.__audio.dataset.archivo, t: window.__audio.currentTime, d: window.__audio.duration, pausado: window.__audio.paused, aviso: document.getElementById("que-suena").textContent }));

await p.goto(BASE + "?carga#GEN-01", { waitUntil: "load" });
await p.waitForFunction(() => navigator.serviceWorker && navigator.serviceWorker.controller, null, { timeout: 15000 }).catch(() => {});
ok(await p.evaluate(() => Boolean(navigator.serviceWorker.controller)), "el service worker atiende la página");

// 1. Escuchar Génesis 1: quedan guardados Génesis 1 y Génesis 2.
await p.getByRole("button", { name: "Escuchar el capítulo" }).click();
await p.waitForFunction(() => window.__audio && !window.__audio.paused && window.__audio.currentTime > 0.3);
await p.evaluate(() => { window.__audio.currentTime = 12; });
let g = [];
for (let i = 0; i < 60 && !(g.includes("GEN-01.mp3") && g.includes("GEN-02.mp3")); i++) { await p.waitForTimeout(500); g = await guardados(); }
ok(g.includes("GEN-01.mp3") && g.includes("GEN-02.mp3"), `guardados enteros: ${g.join(", ")}`);
await p.waitForFunction(() => getComputedStyle(document.getElementById("barra-tiempo")).getPropertyValue("--cargado").trim() === "100%", null, { timeout: 10000 }).catch(() => {});
ok((await p.evaluate(() => document.getElementById("barra-tiempo").style.getPropertyValue("--cargado"))) === "100%", "la barra muestra el capítulo entero cargado");

// 2. Sin internet: adelantar casi al final y que siga sonando.
await ctx.setOffline(true);
await p.evaluate(() => { window.__audio.currentTime = window.__audio.duration - 40; });
await p.waitForTimeout(2500);
let e = await estado();
ok(e.archivo === "GEN-01.mp3" && !e.pausado && e.t > e.d - 39 && !e.aviso.startsWith("Sin señal"), `sin internet, adelantar funciona y sigue sonando (${e.t.toFixed(1)} de ${e.d.toFixed(1)} s)`);

// 3. Sin internet: el capítulo termina y Génesis 2 empieza enseguida.
await p.evaluate(() => { window.__audio.currentTime = window.__audio.duration - 1; });
const t0 = Date.now();
await p.waitForFunction(() => window.__audio.dataset.archivo === "GEN-02.mp3" && !window.__audio.paused && window.__audio.currentTime > 0.2, null, { timeout: 15000 }).catch(() => {});
e = await estado();
ok(e.archivo === "GEN-02.mp3" && !e.pausado, `sin internet, Génesis 2 empieza en ${((Date.now() - t0) / 1000).toFixed(1)} s (${e.archivo}, ${e.aviso})`);
await p.evaluate(() => { window.__audio.currentTime = window.__audio.duration / 2; });
await p.waitForTimeout(2000);
e = await estado();
ok(!e.pausado && e.t > e.d / 2, "sin internet, adelantar en Génesis 2 también funciona");
await ctx.setOffline(false);

// 4. Nada choca con la política de seguridad.
ok(!errores.some((x) => /Content Security Policy/.test(x)), "la política de seguridad no bloquea nada");
console.log("errores de la página:", errores);
console.log(fallos.length ? `FALLAN ${fallos.length}: ${fallos.join(" | ")}` : "todo bien");
await b.close();
