// Prueba del avance guardado con el teléfono: dos "aparatos" (contextos sin nada en común) con el mismo número.
import { chromium } from "playwright";
const BASE = "http://127.0.0.1:8802/index.html";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome", args: ["--autoplay-policy=no-user-gesture-required"] });
const fallos = [], errores = [];
const ok = (c, q) => { console.log((c ? "  ok  " : "  MAL ") + q); if (!c) fallos.push(q); };
const espia = () => { const O = window.Audio; window.Audio = function (...a) { const x = new O(...a); window.__audio = x; return x; }; window.Audio.prototype = O.prototype; };
async function aparato(ancho) {
  const ctx = await b.newContext({ viewport: { width: ancho, height: 844 }, colorScheme: "dark" });
  await ctx.addInitScript(espia);
  const p = await ctx.newPage(); p.setDefaultTimeout(20000);
  p.on("pageerror", (e) => errores.push(e.message));
  p.on("console", (m) => { if (m.type() === "error") errores.push(m.text()); });
  await p.goto(BASE, { waitUntil: "networkidle" });
  return { ctx, p };
}
// Aparato 1: número inválido, luego válido; escucha Génesis 3 y termina Génesis 50.
const A = await aparato(390);
await A.p.locator("#tel").fill("12345");
await A.p.getByRole("button", { name: "Guardar mi avance" }).click();
ok(await A.p.locator("#error-tel").isVisible(), `número inválido: ${await A.p.locator("#error-tel").innerText()}`);
await A.p.screenshot({ path: "shots-biblia3/telefono-390.png" });
await A.p.locator("#tel").fill("(312) 555-0147");
await A.p.getByRole("button", { name: "Guardar mi avance" }).click();
await A.p.getByText("Tu avance se guarda con el (312) 555-0147").waitFor();
ok(true, "entra con el número y lo muestra");
await A.p.screenshot({ path: "shots-biblia3/telefono-guardado-390.png" });
await A.p.goto(BASE + "?1#GEN-50", { waitUntil: "networkidle" });
await A.p.getByRole("button", { name: "Escuchar el capítulo" }).click();
await A.p.waitForTimeout(1500);
await A.p.evaluate(() => { const x = window.__audio; x.currentTime = x.duration - 1.2; });
await A.p.waitForTimeout(3500);
await A.p.goto(BASE + "?2#GEN-03", { waitUntil: "networkidle" });
await A.p.getByRole("button", { name: "Escuchar el capítulo" }).click();
await A.p.waitForTimeout(1500);
await A.p.evaluate(() => { window.__audio.currentTime = 95; });
await A.p.waitForTimeout(2000);
await A.p.getByRole("button", { name: "Pausar" }).click();
await A.p.waitForTimeout(1500);
const claves = await (await fetch("http://127.0.0.1:8804/__claves")).json();
ok(!JSON.stringify(claves).includes("5550147") && !JSON.stringify(claves).includes("312"), "la base no tiene el número a la vista");
const guardado = JSON.parse(claves.find(([k]) => k.startsWith("avance:"))[1]);
ok(guardado.pos?.id === "GEN-03" && guardado.pos.t > 90 && guardado.oidos.includes("GEN-50"), `en el servidor: ${JSON.stringify(guardado)}`);
// Aparato 2: otro navegador, sin nada guardado. Entra con el mismo número.
const B = await aparato(1440);
ok(!(await B.p.getByRole("button", { name: /Continuar/ }).count()), "el aparato 2 empieza sin avance");
await B.p.locator("#tel").fill("312-555-0147");
await B.p.getByRole("button", { name: "Guardar mi avance" }).click();
await B.p.getByText("Tu avance se guarda con el (312) 555-0147").waitFor();
const seguir = B.p.getByRole("button", { name: /Continuar/ });
ok((await seguir.count()) === 1 && (await seguir.innerText()).includes("Génesis 3"), `aparato 2 ofrece: ${await seguir.innerText().catch(() => "nada")}`);
ok((await B.p.locator(".libro-tarjeta").first().innerText()).includes("1 de 50 escuchados"), "aparato 2 cuenta Génesis 50 como escuchado");
await B.p.screenshot({ path: "shots-biblia3/telefono-aparato2-1440.png" });
await seguir.click();
await B.p.waitForTimeout(2000);
const a = await B.p.evaluate(() => ({ src: window.__audio.dataset.archivo || window.__audio.src.split("/").pop(), t: window.__audio.currentTime }));
ok(a.src === "GEN-03.mp3" && a.t > 90, `aparato 2 sigue en GEN-03 en ${a.t.toFixed(1)} s`);
// Velocidad en el aparato 2 llega al aparato 1 al volver a abrir.
await B.p.getByRole("button", { name: "Velocidad de lectura" }).click();
await B.p.getByRole("button", { name: "Pausar" }).click();
await B.p.waitForTimeout(1500);
await A.p.goto(BASE, { waitUntil: "networkidle" });
await A.p.waitForTimeout(1500);
ok((await A.p.locator("#velocidad").innerText()) === "1,15×", `la velocidad pasa al aparato 1: ${await A.p.locator("#velocidad").innerText()}`);
// Usar otro número.
await A.p.getByRole("button", { name: "Usar otro número" }).click();
ok(await A.p.locator("#tel").isVisible(), "Usar otro número vuelve a pedir el número");
// Límite de intentos con números distintos.
let ultimo = 0;
for (let i = 0; i < 22; i++) ultimo = (await fetch("http://127.0.0.1:8802/api/progreso", { method: "POST", headers: { "x-prueba-ip": "10.9.9.9" }, body: JSON.stringify({ accion: "leer", telefono: `31255501${String(i).padStart(2, "0")}` }) })).status;
ok(ultimo === 429, `después de 20 números distintos responde ${ultimo}`);
const ancho = await B.p.evaluate(() => document.documentElement.scrollWidth);
ok(ancho <= 1440, "sin desborde");
console.log("errores de la página:", errores);
console.log(fallos.length ? `FALLAN ${fallos.length}: ${fallos.join(" | ")}` : "todo bien");
await b.close();
