// Prueba completa del lector de Génesis, Éxodo y Levítico con todo el contenido y el audio (servidor local en :8801).
import { chromium } from "playwright";
const BASE = process.env.BASE ?? "http://127.0.0.1:8801/index.html";
const DIR = process.env.DIR ?? "shots-biblia3";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--autoplay-policy=no-user-gesture-required"] });
const errores = [];
const fallos = [];
const comprobar = (ok, que) => { console.log((ok ? "  ok  " : "  MAL ") + que); if (!ok) fallos.push(que); };
async function pagina(ancho, alto, tema, ctxPrevio) {
  const ctx = ctxPrevio ?? (await b.newContext({ viewport: { width: ancho, height: alto }, colorScheme: tema, reducedMotion: "reduce" }));
  const p = await ctx.newPage();
  p.setDefaultTimeout(20000);
  p.on("pageerror", (e) => errores.push("pageerror " + e.message));
  p.on("console", (m) => { if (m.type() === "error") errores.push("console " + m.text()); });
  p.on("response", (r) => { if (r.status() >= 400 && !r.url().endsWith("favicon.ico")) errores.push(`HTTP ${r.status()} ${r.url()}`); });
  await p.goto(BASE, { waitUntil: "networkidle" });
  return { ctx, p };
}
const estadoAudio = (p) => p.evaluate(() => {
  const a = window.__audio;
  return a ? { src: a.dataset.archivo || a.src.split("/").pop(), t: a.currentTime, d: a.duration, pausado: a.paused } : null;
});

// Expone el elemento de audio para la prueba sin tocar la página: se intercepta new Audio().
const espia = () => {
  const Original = window.Audio;
  window.Audio = function (...a) { const x = new Original(...a); window.__audio = x; return x; };
  window.Audio.prototype = Original.prototype;
};

if (!process.env.SOLO_CAPTURAS) {
const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, colorScheme: "dark", reducedMotion: "reduce" });
await ctx.addInitScript(espia);
const { p } = await pagina(390, 844, "dark", ctx);
await p.getByRole("heading", { name: "Génesis, Éxodo y Levítico" }).waitFor();
comprobar(!(await p.getByRole("button", { name: /Continuar/ }).count()), "la primera visita no muestra Continuar");
await p.screenshot({ path: `${DIR}/portada-390-noche.png` });

// 1. Escuchar desde el principio: empieza la introducción de Génesis, con la voz del guía (la portada ya no tiene audio).
await p.getByRole("button", { name: "Escuchar desde el principio" }).click();
await p.waitForTimeout(2500);
let a = await estadoAudio(p);
comprobar(a && a.src === "INTRO-GEN.mp3" && !a.pausado && a.t > 0.5, `suena INTRO-GEN.mp3 (${JSON.stringify(a)})`);
comprobar((await p.locator("#punto-voz").getAttribute("class")).includes("guia"), "el punto del reproductor es el del guía");
comprobar((await p.locator("#donde").innerText()) === "Introducción a Génesis", `la vista sigue al audio: ${await p.locator("#donde").innerText()}`);
comprobar(!(await p.getByText("Antes de empezar").count()), "la introducción general ya no está en la página");

// 2. Avance automático: al terminar la introducción de Génesis sigue Génesis 1 y la página lo muestra.
await p.evaluate(() => { const x = window.__audio; x.currentTime = x.duration - 1.2; });
await p.waitForTimeout(3500);
a = await estadoAudio(p);
comprobar(a.src === "GEN-01.mp3", `después de la introducción de Génesis viene GEN-01 (${a.src})`);
comprobar((await p.locator("#donde").innerText()) === "Génesis 1", "la vista muestra Génesis 1");
await p.waitForTimeout(1500);
const resaltado = await p.locator(".sonando").getAttribute("data-k");
comprobar(resaltado === "c" || resaltado === "v1", `se resalta lo que suena al empezar el capítulo (${resaltado})`);

// 3. Tocar un versículo, una nota y una pausa.
await p.locator('.v[data-k="v26"]').click();
await p.waitForTimeout(1500);
comprobar((await p.locator("#que-suena").innerText()) === "Génesis 1:26", `tocar el versículo 26: ${await p.locator("#que-suena").innerText()}`);
comprobar((await p.locator(".sonando").getAttribute("data-k")) === "v26", "se resalta el 26");
await p.locator(".nota").first().click();
await p.waitForTimeout(1500);
comprobar((await p.locator("#que-suena").innerText()).startsWith("Nota · Génesis 1:"), `tocar una nota: ${await p.locator("#que-suena").innerText()}`);
comprobar((await p.locator("#punto-voz").getAttribute("class")).includes("guia"), "la nota la dice el guía");

// 4. Ir por el índice a una pausa de otro capítulo.
await p.getByRole("button", { name: "Índice" }).click();
await p.locator("#indice[open]").waitFor();
const pausasGen = await p.locator("#cuerpo-indice .lista-pausas li").count();
console.log("  pausas de Génesis en el índice (con la introducción):", pausasGen);
await p.screenshot({ path: `${DIR}/indice-390-noche.png` });
await p.locator("#cuerpo-indice .lista-pausas button[data-clave]").nth(4).click();
await p.waitForTimeout(800);
const donde = await p.locator("#donde").innerText();
const pausaVisible = await p.evaluate(() => {
  const el = [...document.querySelectorAll(".pausa")].find((e) => { const r = e.getBoundingClientRect(); return r.top < innerHeight && r.bottom > 0; });
  return el ? el.querySelector("h2").textContent : null;
});
comprobar(Boolean(pausaVisible), `el índice lleva a la pausa (${donde}: ${pausaVisible})`);
await p.screenshot({ path: `${DIR}/pausa-390-noche.png` });
await p.locator(".pausa h2", { hasText: pausaVisible }).click();
await p.waitForTimeout(1800);
comprobar((await p.locator("#que-suena").innerText()) === `Pausa · ${pausaVisible}`, `tocar la pausa la reproduce: ${await p.locator("#que-suena").innerText()}`);
await p.screenshot({ path: `${DIR}/pausa-sonando-390-noche.png` });

// 5. Fin de libro: Génesis 50 sigue con la introducción de Éxodo; Éxodo 40 con la de Levítico; Levítico 27 se detiene.
for (const [desde, hacia] of [["GEN-50", "INTRO-EXO"], ["EXO-40", "INTRO-LEV"], ["LEV-27", null]]) {
  await p.getByRole("button", { name: "Índice" }).click();
  const [libro, n] = desde.split("-");
  const nombre = { GEN: "Génesis", EXO: "Éxodo", LEV: "Levítico" }[libro];
  await p.locator(`#pestanas [data-pestana="${libro}"]`).click();
  await p.locator(`#cuerpo-indice .capitulos button[aria-label="${nombre} ${Number(n)}"]`).click();
  await p.getByRole("button", { name: "Escuchar el capítulo" }).click();
  await p.waitForTimeout(1500);
  await p.evaluate(() => { const x = window.__audio; x.currentTime = x.duration - 1.2; });
  await p.waitForTimeout(3500);
  a = await estadoAudio(p);
  if (hacia) comprobar(a.src === `${hacia}.mp3` && !a.pausado, `${desde} termina y sigue ${hacia} (${a.src})`);
  else comprobar(a.src === `${desde}.mp3` && a.pausado, `${desde} es el final: se detiene (${a.src}, pausado ${a.pausado})`);
}

// 5b. Los capítulos que terminaron quedan marcados en el índice.
await p.getByRole("button", { name: "Índice" }).click();
await p.locator('#pestanas [data-pestana="GEN"]').click();
const marcados = await p.locator("#cuerpo-indice .capitulos button.oido").evaluateAll((bs) => bs.map((x) => x.getAttribute("aria-label")));
comprobar(marcados.includes("Génesis 50, ya escuchado"), `capítulos marcados como escuchados: ${marcados.join(", ")}`);
comprobar(await p.locator("#cuerpo-indice .leyenda").count() === 1, `leyenda: ${await p.locator("#cuerpo-indice .leyenda").innerText().catch(() => "no hay")}`);
await p.screenshot({ path: `${DIR}/indice-escuchados-390-noche.png` });
await p.getByRole("button", { name: "Cerrar" }).click();

// 6. Velocidad y Continuar después de recargar.
await p.getByRole("button", { name: "Velocidad de lectura" }).click();
comprobar((await p.locator("#velocidad").innerText()) === "1,15×", `velocidad: ${await p.locator("#velocidad").innerText()}`);
await p.getByRole("button", { name: "Índice" }).click();
await p.locator('#pestanas [data-pestana="GEN"]').click();
await p.locator('#cuerpo-indice .capitulos button[aria-label="Génesis 3"]').click();
await p.locator('.v[data-k="v8"]').click();
await p.waitForTimeout(5000);
await p.getByRole("button", { name: "Pausar" }).click();
await p.reload({ waitUntil: "networkidle" });
const seguir = p.getByRole("button", { name: /Continuar/ });
comprobar(await seguir.count() === 1 && (await seguir.innerText()).includes("Génesis 3"), `tras recargar: ${await seguir.count() ? await seguir.innerText() : "sin Continuar"}`);
comprobar((await p.locator("#velocidad").innerText()) === "1,15×", "la velocidad elegida se recuerda");
comprobar((await p.locator(".libro-tarjeta").first().innerText()).includes("escuchados"), `la tarjeta de Génesis cuenta lo escuchado: ${(await p.locator(".libro-tarjeta").first().innerText()).replace(/\n/g, " ")}`);
await seguir.click();
await p.waitForTimeout(2000);
a = await estadoAudio(p);
comprobar(a.src === "GEN-03.mp3" && !a.pausado && a.t > 1, `Continuar retoma GEN-03 en ${a.t.toFixed(1)} s`);
const ancho = await p.evaluate(() => document.documentElement.scrollWidth);
comprobar(ancho <= 390, `sin desborde horizontal a 390 (${ancho})`);
await ctx.close();

}
// 7. Capturas en otros anchos y en los dos temas.
for (const [w, h, tema] of [[360, 740, "dark"], [360, 740, "light"], [390, 844, "light"], [768, 1024, "dark"], [1440, 900, "dark"], [1440, 900, "light"]]) {
  const c = await b.newContext({ viewport: { width: w, height: h }, colorScheme: tema, reducedMotion: "reduce" });
  const { p } = await pagina(w, h, tema, c);
  const t = tema === "dark" ? "noche" : "dia";
  await p.screenshot({ path: `${DIR}/portada-${w}-${t}.png` });
  await p.locator(".libro-tarjeta").first().click();
  await p.locator('.pie-cap [data-ir="GEN-01"]').click();
  await p.locator('.v[data-k="v3"]').click();
  await p.waitForTimeout(1200);
  await p.screenshot({ path: `${DIR}/capitulo-${w}-${t}.png` });
  await p.locator('.pie-cap [data-ir="GEN-02"]').click();
  await p.locator(".pausa").first().scrollIntoViewIfNeeded();
  await p.screenshot({ path: `${DIR}/pausa-${w}-${t}.png` });
  const ancho = await p.evaluate(() => document.documentElement.scrollWidth);
  comprobar(ancho <= w, `sin desborde horizontal a ${w} ${t} (${ancho})`);
  await c.close();
}
console.log("errores de la página:", errores.length, errores.slice(0, 8));
console.log(fallos.length ? `FALLAN ${fallos.length}: ${fallos.join(" | ")}` : "todo bien");
await b.close();
