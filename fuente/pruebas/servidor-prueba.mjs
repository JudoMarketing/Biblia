// Servidor de prueba: Redis falso (8803) y la función real de api/progreso.js; lo demás va al servidor estático de 8801.
import http from "node:http";
const datos = new Map();
http.createServer((req, res) => {
  let b = ""; req.on("data", (c) => (b += c)); req.on("end", () => {
    const [cmd, k, v] = JSON.parse(b); let result = null;
    if (cmd === "GET") result = datos.get(k) ?? null;
    else if (cmd === "SET") { datos.set(k, v); result = "OK"; }
    else if (cmd === "INCR") { result = Number(datos.get(k) || 0) + 1; datos.set(k, String(result)); }
    else if (cmd === "EXPIRE") result = 1;
    res.setHeader("Content-Type", "application/json"); res.end(JSON.stringify({ result }));
  });
}).listen(8803);
http.createServer((req, res) => { if (req.url === "/__claves") { res.end(JSON.stringify([...datos.entries()])); } }).listen(8804);
const { POST } = await import(process.argv[2]);
http.createServer(async (req, res) => {
  if (req.url.startsWith("/api/progreso")) {
    let b = ""; req.on("data", (c) => (b += c)); await new Promise((r) => req.on("end", r));
    const r = await POST(new Request("http://x/api/progreso", { method: "POST", headers: { ...req.headers, "x-forwarded-for": req.headers["x-prueba-ip"] || "10.0.0.1" }, body: b }));
    res.writeHead(r.status, Object.fromEntries(r.headers)); res.end(await r.text()); return;
  }
  const p = http.request({ host: "127.0.0.1", port: 8801, path: req.url, method: req.method, headers: req.headers }, (r) => { res.writeHead(r.statusCode, r.headers); r.pipe(res); });
  req.pipe(p);
}).listen(8802);
console.log("listo");
