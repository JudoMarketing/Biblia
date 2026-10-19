"""Revisa un archivo de comentario contra la guía (GUIA.md)."""
import json, re, sys, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
texto = json.load(open(os.path.join(BASE, "texto-final.json"), encoding="utf8"))
archivo = sys.argv[1]
d = json.load(open(archivo, encoding="utf8"))
errores, avisos = [], []
libro = d.get("libro"); caps = texto[libro]["capitulos"]
def existe(c, v): return str(c) in caps and str(v) in caps[str(c)]
def orden(c, v): return (c, v)
desde, hasta = d["desde"], d["hasta"]
if not existe(desde["cap"], desde["v"]) or not existe(hasta["cap"], hasta["v"]): errores.append("desde/hasta no existe")
PROHIBIDO = [(r"[—–]", "raya"), (r"\s-\s", "guion de pausa"), (r"\ba\.\s?C\.|\bd\.\s?C\.", "abreviatura a. C./d. C."),
             (r"\baprox\.", "abreviatura aprox."), (r"\bkm\b|\bmts?\b", "abreviatura de medida"),
             (r"\b\d+:\d+", "cita con dos puntos (escríbela en palabras)"), (r"\bcap\.|\bv\.\s?\d", "abreviatura de capítulo o versículo"),
             (r"RVR|NVI|Reina[- ]Valera 1960", "otra traducción"), (r"[%&]|/", "símbolo"),
             (r"esto nos enseña|nos enseña que|debemos |el mensaje es", "conclusión impuesta")]
# La voz no sabe leer números romanos ni siglas: "Ramsés II" saldría "Ramsés Ii".
ROMANO = re.compile(r"M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})")
MAYUSCULAS_BIBLIA = {w for c in caps.values() for v in c.values() for w in re.findall(r"\b[A-ZÁÉÍÓÚÑÜ]{2,}\b", v)}
def revisar_texto(t, donde, minp, maxp):
    n = len(t.split())
    if n < minp or n > maxp: avisos.append(f"{donde}: {n} palabras (se esperan {minp} a {maxp})")
    for patron, que in PROHIBIDO:
        m = re.search(patron, t, re.I if que == "conclusión impuesta" else 0)
        if m: errores.append(f"{donde}: {que} («{t[max(0, m.start()-25):m.end()+25]}»)")
    for m in re.finditer(r"\b[A-ZÁÉÍÓÚÑÜ]+\b", t):
        w = m.group()
        if ROMANO.fullmatch(w):
            errores.append(f"{donde}: número romano «{w}»; la voz no lo lee bien (reyes: «Ramsés segundo»; siglos: «el siglo 13»)")
        elif len(w) >= 2 and w not in MAYUSCULAS_BIBLIA:
            errores.append(f"{donde}: sigla o palabra en mayúsculas «{w}»; la voz no la lee bien, escríbela como se dice")
for i, n in enumerate(d.get("notas", []), 1):
    donde = f"nota {i} ({n.get('cap')}:{n.get('v')})"
    if not existe(n["cap"], n["v"]): errores.append(f"{donde}: el versículo no existe")
    elif not (orden(desde["cap"], desde["v"]) <= orden(n["cap"], n["v"]) <= orden(hasta["cap"], hasta["v"])): errores.append(f"{donde}: fuera del tramo")
    revisar_texto(n["texto"], donde, 10, 85)
for i, p in enumerate(d.get("pausas", []), 1):
    donde = f"pausa {i} ({p.get('cap')}:{p.get('v')} {p.get('titulo')})"
    if not existe(p["cap"], p["v"]): errores.append(f"{donde}: el versículo no existe")
    for k in ["titulo", "epoca", "lugar", "texto"]:
        if not p.get(k): errores.append(f"{donde}: falta {k}")
    revisar_texto(p.get("texto", ""), donde, 330, 750)
    for k in ["titulo", "epoca", "lugar"]: revisar_texto(p.get(k, ""), f"{donde} {k}", 1, 40)
    for q in p.get("preguntas", []): revisar_texto(q, f"{donde} pregunta", 3, 40)
    if len(p.get("preguntas", [])) > 2: errores.append(f"{donde}: más de 2 preguntas")
if "introduccion" in d:
    revisar_texto(d["introduccion"]["texto"], "introducción", 550, 950)
notas = sorted((n["cap"], n["v"]) for n in d.get("notas", []))
versos = sum(1 for c, vs in caps.items() for v in vs if orden(desde["cap"], desde["v"]) <= orden(int(c), int(v)) <= orden(hasta["cap"], hasta["v"]))
print(f"{archivo}: {len(d.get('notas', []))} notas · {len(d.get('pausas', []))} pausas · {versos} versículos en el tramo · una nota cada {versos / max(1, len(d.get('notas', []))):.1f} versículos")
for a in avisos: print("  ⚠", a)
for e in errores: print("  ✗", e)
print(f"{len(errores)} error(es), {len(avisos)} aviso(s)")
sys.exit(1 if errores else 0)
