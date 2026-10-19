// Guarda el avance de cada persona (dónde va, capítulos escuchados y velocidad) con su número de teléfono.
// El número no se guarda: la clave en Redis es un HMAC del número con un secreto que solo tiene el servidor.
// Necesita en Vercel: Upstash Redis conectado al proyecto (KV_REST_API_URL y KV_REST_API_TOKEN) y PROGRESO_SECRETO.

const ID = /^(INTRO(-(GEN|EXO|LEV|NUM|DEU|JOS))?|GEN-(0[1-9]|[1-4]\d|50)|EXO-(0[1-9]|[1-3]\d|40)|LEV-(0[1-9]|1\d|2[0-7])|NUM-(0[1-9]|[12]\d|3[0-6])|DEU-(0[1-9]|[12]\d|3[0-4])|JOS-(0[1-9]|1\d|2[0-4]))$/;
const VELOCIDADES = [1, 1.15, 1.3, 1.5, 0.85];
const DOS_ANOS = 60 * 60 * 24 * 730;

const respuesta = (cuerpo, estado = 200) =>
  new Response(JSON.stringify(cuerpo), { status: estado, headers: { "Content-Type": "application/json; charset=utf-8", "Cache-Control": "no-store" } });

async function redis(...comando) {
  const url = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL;
  const token = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN;
  const r = await fetch(url, { method: "POST", headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" }, body: JSON.stringify(comando) });
  if (!r.ok) throw new Error(`Redis respondió ${r.status}`);
  return (await r.json()).result;
}

// Solo números de Estados Unidos: 10 dígitos, con o sin el 1 delante.
function normalizar(tel) {
  let d = String(tel ?? "").replace(/\D/g, "");
  if (d.length === 11 && d[0] === "1") d = d.slice(1);
  return /^[2-9]\d{2}[2-9]\d{6}$/.test(d) ? "+1" + d : null;
}

async function hmac(texto) {
  const codificar = (x) => new TextEncoder().encode(x);
  const llave = await crypto.subtle.importKey("raw", codificar(process.env.PROGRESO_SECRETO), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return Buffer.from(await crypto.subtle.sign("HMAC", llave, codificar(texto))).toString("hex");
}

// Ventana fija por conexión: evita que alguien recorra números ajenos o llene la base.
async function dentroDelLimite(nombre, maximo, segundos) {
  const n = await redis("INCR", nombre);
  if (n === 1) await redis("EXPIRE", nombre, segundos);
  return n <= maximo;
}

const hora = (x) => (Number.isFinite(x) ? Math.min(Math.max(0, x), Date.now()) : 0);

// Solo se acepta lo que la página sabe mandar; lo demás se descarta.
function limpiar(d) {
  const s = {};
  if (d?.pos && ID.test(d.pos.id) && Number.isFinite(d.pos.t) && d.pos.t >= 0 && d.pos.t < 36000)
    s.pos = { id: d.pos.id, t: Math.round(d.pos.t * 10) / 10, ts: hora(d.pos.ts) };
  if (Array.isArray(d?.oidos)) s.oidos = [...new Set(d.oidos.filter((x) => typeof x === "string" && ID.test(x)))];
  if (VELOCIDADES.includes(d?.vel)) { s.vel = d.vel; s.velTs = hora(d.velTs); }
  return s;
}

// Capítulos escuchados de los dos lados; posición y velocidad, la más reciente.
function unir(a, b) {
  const s = { oidos: [...new Set([...(a.oidos || []), ...(b.oidos || [])])] };
  const pos = [a.pos, b.pos].filter(Boolean).sort((x, y) => (y.ts || 0) - (x.ts || 0))[0];
  if (pos) s.pos = pos;
  const vel = [a, b].filter((x) => x.vel).sort((x, y) => (y.velTs || 0) - (x.velTs || 0))[0];
  if (vel) { s.vel = vel.vel; s.velTs = vel.velTs || 0; }
  return s;
}

export async function POST(request) {
  if (!(process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL) || !process.env.PROGRESO_SECRETO)
    return respuesta({ error: "El guardado del avance todavía no está configurado." }, 503);
  if (Number(request.headers.get("content-length") || 0) > 8000) return respuesta({ error: "Petición demasiado grande." }, 413);
  let cuerpo;
  try { cuerpo = await request.json(); } catch { return respuesta({ error: "Petición inválida." }, 400); }
  const tel = normalizar(cuerpo?.telefono);
  if (!tel) return respuesta({ error: "Escribe un número de Estados Unidos de 10 dígitos, por ejemplo (555) 123-4567." }, 400);
  if (cuerpo.accion !== "leer" && cuerpo.accion !== "guardar") return respuesta({ error: "Acción desconocida." }, 400);

  try {
    const ip = await hmac("ip:" + ((request.headers.get("x-forwarded-for") || "").split(",")[0].trim() || "desconocida"));
    if (!(await dentroDelLimite(`limite:${ip}`, 120, 60))) return respuesta({ error: "Demasiadas peticiones. Espera un minuto." }, 429);
    if (cuerpo.accion === "leer" && !(await dentroDelLimite(`limite-leer:${ip}`, 20, 600)))
      return respuesta({ error: "Demasiados intentos con números distintos. Espera unos minutos." }, 429);

    const clave = "avance:" + (await hmac(tel));
    const guardado = JSON.parse((await redis("GET", clave)) || "{}");
    if (cuerpo.accion === "leer") return respuesta(guardado);

    const nuevo = unir(guardado, limpiar(cuerpo.datos));
    await redis("SET", clave, JSON.stringify(nuevo), "EX", DOS_ANOS);
    return respuesta(nuevo);
  } catch (e) {
    console.error("progreso:", e.message);
    return respuesta({ error: "No se pudo guardar ahora. Se intentará de nuevo." }, 502);
  }
}
