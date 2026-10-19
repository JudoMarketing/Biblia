"""Servidor local con Range (como el del artifact) para probar el audio: python3 -I servidor.py <carpeta> <puerto>"""
import os, sys, re
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
class Rango(SimpleHTTPRequestHandler):
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
