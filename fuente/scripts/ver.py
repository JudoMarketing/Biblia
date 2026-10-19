"""Muestra el texto RV1909 de un tramo: python3 -I scripts/ver.py GEN 1 11 (libro, capítulo inicial, capítulo final)."""
import json, sys, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
t = json.load(open(os.path.join(BASE, "texto-final.json"), encoding="utf8"))
libro, desde, hasta = sys.argv[1], int(sys.argv[2]), int(sys.argv[3] if len(sys.argv) > 3 else sys.argv[2])
for c in range(desde, hasta + 1):
    print(f"\n### {t[libro]['nombre']} {c}")
    for v, x in t[libro]["capitulos"][str(c)].items(): print(f"{c}:{v} {x}")
