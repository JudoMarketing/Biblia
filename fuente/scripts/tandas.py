"""Reparte contenido.json y los MP3 en tandas para publicar (64 MB y 255 archivos por publicación).

  python3 -I scripts/tandas.py <carpeta biblia>   → salida/tandas.json: [{"audio/GEN-01.mp4": "<ruta>", ...}, ...]
"""
import json, os, sys
B = sys.argv[1]
TOPE_MB, TOPE_ARCHIVOS = 60, 250
trabajos = json.load(open(f"{B}/salida/trabajos.json", encoding="utf8"))
orden = [t["id"] for t in trabajos]
archivos = [("contenido.json", f"{B}/salida/contenido.json")] + [(f"audio/{i}.mp4", f"{B}/salida/audio/{i}.mp4") for i in orden]
faltan = [r for _, r in archivos if not os.path.exists(r)]
if faltan: sys.exit(f"faltan {len(faltan)} archivos, por ejemplo {faltan[0]}")
tandas, actual, peso = [], {}, 0
for publicado, ruta in archivos:
    p = os.path.getsize(ruta)
    assert p < 15e6, f"{publicado} pesa {p/1e6:.1f} MB"
    if actual and (peso + p > TOPE_MB * 1e6 or len(actual) >= TOPE_ARCHIVOS):
        tandas.append(actual); actual, peso = {}, 0
    actual[publicado] = ruta; peso += p
tandas.append(actual)
json.dump(tandas, open(f"{B}/salida/tandas.json", "w", encoding="utf8"), indent=1)
total = sum(os.path.getsize(r) for _, r in archivos)
for i, t in enumerate(tandas, 1):
    print(f"tanda {i}: {len(t)} archivos, {sum(os.path.getsize(r) for r in t.values())/1e6:.1f} MB, de {next(iter(t))} a {list(t)[-1]}")
print(f"total {len(archivos)} archivos, {total/1e6:.1f} MB")
