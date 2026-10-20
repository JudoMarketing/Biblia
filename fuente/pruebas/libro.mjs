// Prueba del diseño de libro: la Biblia que se abre al entrar, los separadores, las hojas que pasan,
// la página izquierda en pantallas anchas, y que el avance guardado sigue igual (servidor de prueba en :8802).
import { chromium } from "playwright";
const BASE = process.env.BASE ?? "http://127.0.0.1:8802/index.html";
const b = await chromium.launch({ executablePath: "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" });
const fallos = [], errores = [];
const ok = (c, q) => { console.log((c ? "  ok  " : "  MAL ") + q); if (!c) fallos.push(q); };
async function pagina(opciones, url = BASE) {
  const ctx = await b.newContext(opciones);
  const p = await ctx.newPage(); p.setDefaultTimeout(15000);
  p.on("pageerror", (e) => errores.push(e.message));
  p.on("console", (m) => { if (m.type() === "error") errores.push(m.text()); });
  await p.goto(url, { waitUntil: "load" });
  return { ctx, p };
}

// 1. La apertura se ve al entrar, dura unos 4 segundos y se quita sola.
//    (La de antes dejaba la tapa abierta fuera de la pantalla en el teléfono.)
let { ctx, p } = await pagina({ viewport: { width: 390, height: 844 } });
ok(await p.locator("#apertura").isVisible(), "al entrar se ve la Biblia cerrada");
await p.waitForTimeout(2000);
ok(await p.locator("#apertura").count() === 1, "a los 2 segundos sigue la apertura");
// Abierta, en el teléfono se ven las dos páginas: la tapa (por dentro) y la primera hoja, enteras en la pantalla.
// Se mide en el segundo 2,8 de la animación, no del reloj: el script puede empezar un poco después de cargar.
const medir = () => { for (const x of document.getAnimations()) x.currentTime = 2800; return ["tapa-dorso", "tomo-hojas"].map((c) => { const r = document.querySelector("." + c).getBoundingClientRect(); return { c, izq: Math.round(r.left), der: Math.round(r.right), ancho: Math.round(r.width) }; }); };
const dentro = await p.evaluate(medir);
ok(dentro.every((r) => r.izq >= 0 && r.der <= 390 && r.ancho > 120), `la Biblia abierta cabe en la pantalla: ${JSON.stringify(dentro)}`);
await p.waitForTimeout(2800);
ok(await p.locator("#apertura").count() === 0, "a los 4,8 segundos la apertura ya no está");
// 1b. En el website está el enlace a godshome.app, y abre en otra pestaña para que el audio siga.
const sentir = p.locator("#sentir");
ok(await sentir.isVisible() && (await sentir.getAttribute("href")) === "https://www.godshome.app/" && (await sentir.getAttribute("target")) === "_blank", `enlace: ${(await sentir.innerText()).replace(/\n/g, " ")}`);
// 2. Separadores: el de Inicio está marcado; tocar Éxodo pasa varias hojas y lleva a su introducción.
ok((await p.locator('.separador[aria-current="true"]').innerText()).trim() === "Inicio", "el separador marcado es Inicio");
await p.locator(".separador.sep-EXO").click();
await p.waitForTimeout(150);
ok(await p.locator(".vuelo .hoja-vuelo").count() === 5, `al tocar un separador pasan ${await p.locator(".vuelo .hoja-vuelo").count()} hojas`);
await p.waitForTimeout(1500);
ok(await p.locator(".vuelo").count() === 0, "las hojas se quitan al terminar");
ok((await p.locator("#donde").innerText()) === "Introducción a Éxodo", `lleva a: ${await p.locator("#donde").innerText()}`);
ok((await p.locator('.separador[aria-current="true"]').innerText()).trim() === "Éxodo", "queda marcado Éxodo");
// 3. Ir al capítulo siguiente pasa una sola hoja.
await p.locator('.pie-cap [data-ir="EXO-01"]').click();
await p.waitForTimeout(150);
ok(await p.locator(".vuelo .hoja-vuelo").count() === 1, "al capítulo de al lado pasa una hoja");
await p.waitForTimeout(1200);
ok((await p.locator("#donde").innerText()) === "Éxodo 1", "llega a Éxodo 1");
const ancho = await p.evaluate(() => document.documentElement.scrollWidth);
ok(ancho <= 390, `sin desborde a 390 (${ancho})`);
await ctx.close();

// 3b. En un teléfono más chico también cabe abierta.
({ ctx, p } = await pagina({ viewport: { width: 360, height: 640 } }));
await p.waitForTimeout(300);
const chico = await p.evaluate(medir);
ok(chico.every((r) => r.izq >= 0 && r.der <= 360), `a 360 de ancho también cabe abierta: ${JSON.stringify(chico)}`);
await ctx.close();

// 4. Saltar: tocar la pantalla quita la apertura enseguida.
({ ctx, p } = await pagina({ viewport: { width: 390, height: 844 } }));
await p.getByRole("button", { name: "Saltar" }).click();
await p.waitForTimeout(600);
ok(await p.locator("#apertura").count() === 0, "Saltar quita la apertura");
await ctx.close();

// 5. Con "reducir movimiento" no hay apertura ni hojas que pasen.
({ ctx, p } = await pagina({ viewport: { width: 390, height: 844 }, reducedMotion: "reduce" }));
ok(await p.locator("#apertura").count() === 0, "con reducir movimiento no hay apertura");
await p.locator(".separador.sep-GEN").click();
ok(await p.locator(".vuelo").count() === 0 && (await p.locator("#donde").innerText()) === "Introducción a Génesis", "con reducir movimiento el separador lleva directo");
await ctx.close();

// 5b. Portada limpia: los libros una sola vez, sin la introducción general, con el crédito al final.
({ ctx, p } = await pagina({ viewport: { width: 390, height: 844 }, reducedMotion: "reduce" }, BASE + "?limpia"));
ok(await p.locator(".libro-tarjeta").count() === 3, "la portada muestra los 3 libros una vez");
ok(!(await p.getByText("Antes de empezar").count()) && !(await p.getByRole("button", { name: "Ir a Génesis 1" }).count()), "sin la introducción general ni botones repetidos");
const credito = p.locator(".credito a");
ok((await credito.innerText()) === "Judo Marketing" && (await credito.getAttribute("href")) === "https://www.judomarketing.net", `crédito: ${await p.locator(".credito").innerText()}`);
await ctx.close();

// 6. Pantalla ancha: la página izquierda muestra los capítulos; el avance guardado se respeta.
({ ctx, p } = await pagina({ viewport: { width: 1440, height: 900 }, reducedMotion: "reduce" }, BASE + "?ancho#GEN-01"));
await p.evaluate(() => { localStorage.setItem("gel:oidos", JSON.stringify(["GEN-01", "GEN-02"])); localStorage.setItem("gel:pos", JSON.stringify({ id: "GEN-02", t: 30, ts: Date.now() })); });
await p.reload({ waitUntil: "load" });
await p.locator("#pagina-izq .capitulos button").first().waitFor();
ok(await p.locator("#pagina-izq .capitulos button").count() === 50, "la página izquierda tiene los 50 capítulos de Génesis");
ok(await p.locator("#pagina-izq .capitulos button.oido").count() === 2, "marca los 2 capítulos ya escuchados (avance anterior intacto)");
await p.locator('#pagina-izq .capitulos button[data-ir="GEN-03"]').click();
ok((await p.locator("#donde").innerText()) === "Génesis 3", "tocar el 3 en la página izquierda lleva a Génesis 3");
ok(await p.locator("#pagina-izq .capitulos button.actual").innerText() === "3", "el 3 queda marcado como actual");
await p.goto(BASE + "?ancho2", { waitUntil: "load" });
ok((await p.getByRole("button", { name: /Continuar/ }).innerText()).includes("Génesis 2"), "Continuar sigue ofreciendo Génesis 2");
ok((await p.locator("#pagina-izq .epigrafe").innerText()).includes("EN el principio crió Dios"), "en la portada, la página izquierda lleva Génesis 1, versículo 1");
const anchoAncho = await p.evaluate(() => document.documentElement.scrollWidth);
ok(anchoAncho <= 1440, `sin desborde a 1440 (${anchoAncho})`);
await ctx.close();

console.log("errores de la página:", errores);
console.log(fallos.length ? `FALLAN ${fallos.length}: ${fallos.join(" | ")}` : "todo bien");
await b.close();
