"""Servidor local con Range (como el del artifact) para probar el audio: python3 -I servidor.py <carpeta> <puerto>

Si la carpeta tiene vercel.json, manda los mismos encabezados que Vercel (la política de seguridad, la caché),
para que las pruebas vean lo mismo que el sitio publicado. El tipo de archivo lo pone este servidor.
"""
import os, sys, re, json
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
REGLAS = []
if os.path.exists(os.path.join(sys.argv[1], "vercel.json")):
    for r in json.load(open(os.path.join(sys.argv[1], "vercel.json"), encoding="utf8")).get("headers", []):
        REGLAS.append((re.compile(r["source"]), [(h["key"], h["value"]) for h in r["headers"] if h["key"].lower() != "content-type"]))
class Rango(SimpleHTTPRequestHandler):
    def end_headers(self):
        ruta = self.path.split("?")[0]
        for patron, encabezados in REGLAS:
            if patron.fullmatch(ruta):
                for k, v in encabezados: self.send_header(k, v)
        super().end_headers()
    def send_head(self):
        rango = self.headers.get("Range")
        ruta = self.translate_path(self.path)
        if not rango or not os.path.isfile(ruta): return super().send_head()
        m = re.match(r"bytes=(\d*)-(\d*)", rango); tam = os.path.getsize(ruta)
        a = int(m.group(1)) if m.group(1) else 0; z = int(m.group(2)) if m.group(2) else tam - 1
        z = min(z, tam - 1)
        f = open(ruta, "rb"); f.seek(a)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(ruta)); self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", f"bytes {a}-{z}/{tam}"); self.send_header("Content-Length", str(z - a + 1)); self.end_headers()
        self._resto = z - a + 1
        return f
    def copyfile(self, origen, destino):
        if hasattr(self, "_resto"):
            destino.write(origen.read(self._resto)); del self._resto
        else: super().copyfile(origen, destino)
    def log_message(self, *a): pass
ThreadingHTTPServer(("127.0.0.1", int(sys.argv[2])), partial(Rango, directory=sys.argv[1])).serve_forever()
