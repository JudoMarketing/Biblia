"""Arma el website independiente (fuera de Claude), listo para Vercel.

  python3 -I scripts/sitio.py fuente sitio      (desde la raíz del repositorio)

Toma pagina/genesis-exodo-levitico.html, salida/contenido.json y salida/audio/*.mp4. Si no hay salida/ (no está en
el repositorio porque se rehace con voz/generar.py), conserva el contenido.json y los audios que ya tiene sitio/,
así un cambio en la página no obliga a volver a generar el audio. Agrega lo que el artifact
ponía solo (doctype, charset, viewport, reset) y lo que necesita una web propia: manifiesto para instalarla en el
teléfono, íconos para la pantalla bloqueada y vercel.json con encabezados de seguridad y de caché.
"""
import json, os, shutil, sys
from PIL import Image, ImageDraw

B = sys.argv[1]
S = sys.argv[2]
SALIDA = os.path.join(B, "salida")
CON_SALIDA = os.path.isdir(os.path.join(SALIDA, "audio"))
# Los audios que ya están en el sitio nunca se borran: los de salida/audio se agregan o reemplazan encima.
# Así, generar solo los libros nuevos no hace perder los anteriores.
os.makedirs(os.path.join(S, "audio"), exist_ok=True)
for f in os.listdir(S):
    if f not in ("audio", "contenido.json"):
        r = os.path.join(S, f)
        shutil.rmtree(r) if os.path.isdir(r) else os.remove(r)

NOMBRE = "La Biblia en voz alta"
FONDO, TINTA, CARMESI, ORO = "#2e1d12", "#f4ecd9", "#9c2b1f", "#d9b56c"   # mesa, papel, rúbrica, oro

cuerpo = open(os.path.join(B, "pagina", "genesis-exodo-levitico.html"), encoding="utf8").read()
cabeza = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="La Biblia en voz alta, en la Reina Valera 1909, con notas y pausas de contexto histórico: de Génesis a Josué.">
<meta name="robots" content="noindex">
<meta name="progreso-servidor" content="api/progreso">
<meta name="theme-color" content="{FONDO}">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="La Biblia">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="192x192" href="icono-192.png">
<link rel="apple-touch-icon" href="icono-512.png">
<style>:root{{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}}body{{margin:0;font:14px system-ui}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
</head>
<body>
"""
open(os.path.join(S, "index.html"), "w", encoding="utf8").write(cabeza + cuerpo + "\n</body>\n</html>\n")

json.dump({
    "name": NOMBRE, "short_name": "La Biblia", "lang": "es", "start_url": "./", "scope": "./",
    "display": "standalone", "background_color": FONDO, "theme_color": FONDO,
    "icons": [{"src": "icono-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "icono-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}],
}, open(os.path.join(S, "manifest.webmanifest"), "w", encoding="utf8"), ensure_ascii=False, indent=1)

# Ícono: un libro abierto sobre el azul de la página, con el punto carmesí de la voz que lee.
def icono(tam):
    im = Image.new("RGB", (tam, tam), FONDO)
    d = ImageDraw.Draw(im)
    u = tam / 100
    d.polygon([(50 * u, 34 * u), (20 * u, 28 * u), (20 * u, 70 * u), (50 * u, 76 * u)], fill=TINTA)
    d.polygon([(50 * u, 34 * u), (80 * u, 28 * u), (80 * u, 70 * u), (50 * u, 76 * u)], fill=TINTA)
    d.line([(50 * u, 34 * u), (50 * u, 76 * u)], fill=FONDO, width=max(1, round(2 * u)))
    d.line([(20 * u, 74 * u), (50 * u, 80 * u), (80 * u, 74 * u)], fill=ORO, width=max(1, round(2.5 * u)))
    d.ellipse([44 * u, 14 * u, 56 * u, 26 * u], fill=CARMESI)
    return im
for tam in (192, 512):
    icono(tam).save(os.path.join(S, f"icono-{tam}.png"), optimize=True)

if os.path.exists(os.path.join(SALIDA, "contenido.json")):
    shutil.copy(os.path.join(SALIDA, "contenido.json"), S)
# Función del servidor que guarda el avance con el número de teléfono (ver sitio-api/progreso.js).
os.makedirs(os.path.join(S, "api"))
shutil.copy(os.path.join(B, "sitio-api", "progreso.js"), os.path.join(S, "api", "progreso.js"))
json.dump({"name": "biblia-gel", "private": True, "type": "module"}, open(os.path.join(S, "package.json"), "w"), indent=1)
for f in sorted(os.listdir(os.path.join(SALIDA, "audio")) if CON_SALIDA else []):
    if f.endswith(".mp4"):
        shutil.copy2(os.path.join(SALIDA, "audio", f), os.path.join(S, "audio", f))

csp = ("default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src https://fonts.gstatic.com; img-src 'self' data:; media-src 'self'; connect-src 'self'; manifest-src 'self'; "
       "base-uri 'none'; form-action 'none'; frame-ancestors 'none'; object-src 'none'")
json.dump({
    "headers": [
        {"source": "/(.*)", "headers": [
            {"key": "Content-Security-Policy", "value": csp},
            {"key": "X-Content-Type-Options", "value": "nosniff"},
            {"key": "Referrer-Policy", "value": "no-referrer"},
            {"key": "X-Frame-Options", "value": "DENY"},
            {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=(), payment=()"},
            {"key": "X-Robots-Tag", "value": "noindex, nofollow"}]},
        {"source": "/audio/(.*)", "headers": [
            {"key": "Content-Type", "value": "audio/mp4"},
            {"key": "Cache-Control", "value": "public, max-age=604800"}]},
        {"source": "/contenido.json", "headers": [{"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"}]},
    ]
}, open(os.path.join(S, "vercel.json"), "w", encoding="utf8"), indent=1)
open(os.path.join(S, "robots.txt"), "w").write("User-agent: *\nDisallow: /\n")

total = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(S) for f in fs)
print(f"sitio listo en {S}: {sum(len(fs) for _, _, fs in os.walk(S))} archivos, {total / 1e6:.1f} MB")
