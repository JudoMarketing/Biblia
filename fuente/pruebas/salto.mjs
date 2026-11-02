// Mide cuánto tarda en empezar el capítulo siguiente con una conexión lenta (3 s de espera por audio), con la
// carga adelantada del service worker: el siguiente ya está guardado cuando termina el capítulo.
import { chromium } from "playwright";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--autoplay-policy=no-user-gesture-required"] });
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, reducedMotion: "reduce", serviceWorkers: "allow" });
await ctx.addInitScript(() => { const O = window.Audio; window.Audio = function (...a) { const x = new O(...a); window.__audio = x; return x; }; window.Audio.prototype = O.prototype; });
const p = await ctx.newPage(); const errores = []; p.on("pageerror", (e) => errores.push(e.message));
// En el contexto, no en la página: así la espera también alcanza a lo que baja el service worker.
await ctx.route("**/audio/*", async (r) => { await new Promise((ok) => setTimeout(ok, 3000)); await r.continue(); });
await p.goto("http://127.0.0.1:8802/index.html?x#GEN-30", { waitUntil: "load" });
await p.waitForFunction(() => navigator.serviceWorker && navigator.serviceWorker.controller, null, { timeout: 15000 });
await p.getByRole("button", { name: "Escuchar el capítulo" }).click();
await p.waitForFunction(() => window.__audio && window.__audio.currentTime > 0.5, null, { timeout: 30000 });
await p.evaluate(() => { window.__audio.currentTime = 12; });
await p.waitForTimeout(9000);   // tiempo para que la precarga termine
await p.evaluate(() => { window.__audio.currentTime = window.__audio.duration - 1; });
await p.waitForFunction(() => window.__audio.dataset.archivo === "GEN-31.mp3", null, { timeout: 30000 });
const t0 = Date.now();
await p.waitForFunction(() => !window.__audio.paused && window.__audio.currentTime > 0.2, null, { timeout: 30000 });
const conPrecarga = Date.now() - t0;
const guardado = await p.evaluate(async () => Boolean(await (await caches.open("audio-v1")).match(new URL("audio/GEN-31.mp3", location.href).href)));
// Sin precarga: saltar directo al final, antes de que alcance a bajar el siguiente.
await p.evaluate(() => { window.__audio.currentTime = window.__audio.duration - 1; });
await p.waitForFunction(() => window.__audio.dataset.archivo === "GEN-32.mp3", null, { timeout: 30000 });
const t1 = Date.now();
await p.waitForFunction(() => !window.__audio.paused && window.__audio.currentTime > 0.2, null, { timeout: 30000 });
const sinPrecarga = Date.now() - t1;
console.log(`GEN-30 a GEN-31 con precarga: ${(conPrecarga / 1000).toFixed(2)} s (ya guardado: ${guardado})`);
console.log(`GEN-31 a GEN-32 sin precarga, como antes: ${(sinPrecarga / 1000).toFixed(2)} s`);
console.log("errores:", errores);
await b.close();
