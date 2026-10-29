"""Texto exacto de la Reina-Valera 1909 (dominio público): Génesis a Josué.

Fuente A: eBible.org (USFM de spaRV1909). Fuente B: BibleGateway (RVA).
Guarda texto.json con las dos y la lista de diferencias para revisarlas.
"""
import json, re, sys, time, html, os, urllib.request

BASE = sys.argv[1]
FU = os.path.join(BASE, "fuentes")
TODOS = [("GEN", "Gen", "Génesis", "02-GENspaRV1909.usfm", 50),
         ("EXO", "Exod", "Éxodo", "03-EXOspaRV1909.usfm", 40),
         ("LEV", "Lev", "Levítico", "04-LEVspaRV1909.usfm", 27),
         ("NUM", "Num", "Números", "05-NUMspaRV1909.usfm", 36),
         ("DEU", "Deut", "Deuteronomio", "06-DEUspaRV1909.usfm", 34),
         ("JOS", "Josh", "Josué", "07-JOSspaRV1909.usfm", 24)]
# python3 -I scripts/extraer.py <carpeta> [GEN EXO ...]: sin códigos, los tres primeros libros (como antes)
PEDIDOS = sys.argv[2:] or ["GEN", "EXO", "LEV"]
LIBROS = [l for l in TODOS if l[0] in PEDIDOS]

def usfm(archivo):
    t = open(os.path.join(FU, "ebible-usfm", archivo), encoding="utf8").read()
    caps = {}
    cap = None
    for linea in t.splitlines():
        m = re.match(r"\\c (\d+)", linea)
        if m:
            cap = int(m.group(1)); caps[cap] = {}; continue
        m = re.match(r"\\v (\d+)\s+(.*)", linea)
        if m and cap:
            x = m.group(2)
            x = re.sub(r"\\w (.*?)\|strong=\"[^\"]*\"\\w\*", r"\1", x)
            x = re.sub(r"\\add (.*?)\\add\*", r"[\1]", x)   # palabras añadidas: se marcan
            x = re.sub(r"\s+", " ", x).strip()
            assert "\\" not in x, (archivo, cap, m.group(1), x)
            caps[cap][int(m.group(1))] = x
    return caps

def hasta_cierre(t, i):
    prof = 1; j = i
    while prof and j < len(t):
        a = t.find("<span", j); c = t.find("</span>", j)
        if c < 0: return t[i:], len(t)
        if 0 <= a < c: prof += 1; j = a + 5
        else: prof -= 1; j = c + 7
    return t[i:j - 7], j

def limpiar(x):
    x = re.sub(r"<sup[^>]*class=['\"](?:versenum|crossreference|footnote)['\"][^>]*>.*?</sup>", "", x, flags=re.S)
    x = re.sub(r'<span class="chapternum">.*?</span>', "", x, flags=re.S)
    x = re.sub(r"<[^>]+>", "", x)
    return re.sub(r"\s+", " ", html.unescape(x)).strip()

def bg(osis, desde, hasta, cache):
    archivo = os.path.join(cache, f"{osis}-{desde}-{hasta}.html")
    if not os.path.exists(archivo):
        nombre = {"Gen": "Genesis", "Exod": "Exodus", "Lev": "Leviticus", "Num": "Numbers", "Deut": "Deuteronomy", "Josh": "Joshua"}[osis]
        url = f"https://www.biblegateway.com/passage/?search={nombre}%20{desde}-{hasta}&version=RVA"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (estudio biblico personal)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            open(archivo, "w", encoding="utf8").write(r.read().decode("utf8"))
        time.sleep(15.5)
    t = open(archivo, encoding="utf8").read()
    t = re.sub(r"<h[1-6][^>]*>.*?</h[1-6]>", "", t, flags=re.S)
    salida = {}
    for m in re.finditer(r'<span[^>]*class="text (' + osis + r')-(\d+)-(\d+)"[^>]*>', t):
        cap, v = int(m.group(2)), int(m.group(3))
        contenido, _ = hasta_cierre(t, m.end())
        salida.setdefault(cap, {}).setdefault(v, []).append(limpiar(contenido))
    return {c: {v: " ".join(p for p in partes if p) for v, partes in vs.items()} for c, vs in salida.items()}

cache = os.path.join(FU, "bg"); os.makedirs(cache, exist_ok=True)
resultado, diferencias = {}, []
for codigo, osis, nombre, archivo, ncap in LIBROS:
    a = usfm(archivo)
    b = {}
    for desde in range(1, ncap + 1, 8):
        hasta = min(ncap, desde + 7)
        parte = bg(osis, desde, hasta, cache)
        for c in range(desde, hasta + 1):
            b[c] = parte.get(c, {})
        print(f"{nombre} {desde}-{hasta}: {sum(len(parte.get(c, {})) for c in range(desde, hasta + 1))} versículos de BibleGateway", flush=True)
    assert len(a) == ncap, (nombre, len(a))
    resultado[codigo] = {"nombre": nombre, "capitulos": {}}
    for c in range(1, ncap + 1):
        resultado[codigo]["capitulos"][c] = a[c]
        for v in sorted(set(a[c]) | set(b.get(c, {}))):
            x = re.sub(r"[\[\]]", "", a[c].get(v, ""))
            y = b.get(c, {}).get(v, "")
            if x != y:
                diferencias.append({"libro": nombre, "cap": c, "v": v, "ebible": a[c].get(v), "bg": y})
json.dump(resultado, open(os.path.join(BASE, "texto.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
json.dump(diferencias, open(os.path.join(BASE, "diferencias.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
total = sum(len(vs) for l in resultado.values() for vs in l["capitulos"].values())
print(f"\n{total} versículos; {len(diferencias)} con diferencias entre las dos fuentes")
