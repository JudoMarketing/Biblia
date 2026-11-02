"""Qué audios faltan y cuáles caben este mes en la cuota gratis de Google.

  python3 -I scripts/pendientes.py <carpeta fuente>

Imprime en la salida los ids que conviene generar ahora, listos para voz/generar.py, y en stderr el detalle.
Primero van los capítulos ya grabados cuyo texto cambió (voz/rehacer.txt, o la huella guardada en salida/tiempos
que ya no coincide con el texto); después, los libros que todavía no tienen voz, enteros y en orden de lectura,
mientras quepan en lo que le queda al mes. Si un libro no cabe, se detiene ahí: los que siguen esperan al mes
siguiente. Cuenta igual que voz/generar.py (lo que no está en la caché de voz) y no pide nada a Google.
Necesita salida/trabajos.json (python3 -I scripts/armar.py <carpeta>).
"""
import sys, os, json
B = sys.argv[1]
sys.path.insert(0, os.path.join(B, "voz"))
import generar as g   # mismas cuentas, mismas voces y la misma caché que al generar

trabajos = json.load(open(os.path.join(B, "salida", "trabajos.json"), encoding="utf8"))
SITIO = os.path.join(B, "..", "sitio", "audio")
tiene_audio = lambda i: os.path.exists(os.path.join(SITIO, f"{i}.mp4")) or os.path.exists(os.path.join(B, "salida", "audio", f"{i}.mp4"))

def cambiado(t):
    try: guardada = json.load(open(os.path.join(B, "salida", "tiempos", f"{t['id']}.json"), encoding="utf8")).get("huella")
    except FileNotFoundError: return False
    return bool(guardada) and guardada != g.huella(t, g.VOCES, g.RITMO)

rehacer = set(open(g.REHACER, encoding="utf8").read().split()) if os.path.exists(g.REHACER) else set()
arreglos = [t for t in trabajos if tiene_audio(t["id"]) and (t["id"] in rehacer or cambiado(t))]
# Libros sin voz, en orden de lectura. La introducción de cada libro va con su libro.
libro_de = lambda i: i.split("-")[1] if i.startswith("INTRO-") else i.split("-")[0]
libros = {}
for t in trabajos:
    if t["id"] != "INTRO" and not tiene_audio(t["id"]): libros.setdefault(libro_de(t["id"]), []).append(t)

mes = g.mes_google()
usado = g.leer_consumo()["meses"].get(mes, {}).get("caracteres", 0)
elegidos, total = [], 0
n = g.por_pedir(arreglos)
if arreglos and usado + n <= g.TOPE:
    elegidos += arreglos; total += n
    print(f"arreglos: {', '.join(t['id'] for t in arreglos)} ({n:,} caracteres)", file=sys.stderr)
elif arreglos:
    print(f"arreglos que no caben este mes: {', '.join(t['id'] for t in arreglos)} ({n:,} caracteres)", file=sys.stderr)
for libro, lista in libros.items():
    n = g.por_pedir(elegidos + lista) - g.por_pedir(elegidos)
    if usado + total + n > g.TOPE:
        print(f"{libro}: {n:,} caracteres, no cabe en {mes} (quedarían {g.TOPE - usado - total:,}); espera al mes siguiente", file=sys.stderr)
        break
    elegidos += lista; total += n
    print(f"{libro}: {len(lista)} audios, {n:,} caracteres", file=sys.stderr)
print(f"{mes}: ya usados {usado:,}; con esto, {usado + total:,} de un tope de {g.TOPE:,}", file=sys.stderr)
print(" ".join(t["id"] for t in elegidos))
