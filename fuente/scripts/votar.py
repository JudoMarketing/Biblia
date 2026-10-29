"""Desempate de dos contra uno con wordproject.org para cada versículo en que eBible y BibleGateway difieren."""
import json, sys, re, html, os, time, urllib.request
B = sys.argv[1]
NUM = {"Génesis": "01", "Éxodo": "02", "Levítico": "03", "Números": "04", "Deuteronomio": "05", "Josué": "06", "Jueces": "07", "Rut": "08"}
COD = {"Génesis": "GEN", "Éxodo": "EXO", "Levítico": "LEV", "Números": "NUM", "Deuteronomio": "DEU", "Josué": "JOS", "Jueces": "JDG", "Rut": "RUT"}
dif = json.load(open(f"{B}/diferencias.json", encoding="utf8"))
texto = json.load(open(f"{B}/texto.json", encoding="utf8"))

def wp(libro, cap):
    archivo = f"{B}/fuentes/wp/{NUM[libro]}-{cap}.htm"
    if not os.path.exists(archivo):
        req = urllib.request.Request(f"https://www.wordproject.org/bibles/sp/{NUM[libro]}/{cap}.htm", headers={"User-Agent": "Mozilla/5.0 (estudio biblico personal)"})
        open(archivo, "wb").write(urllib.request.urlopen(req, timeout=30).read()); time.sleep(3)
    t = open(archivo, encoding="utf8", errors="replace").read()
    t = t.replace('<!--span class="verse" id="1">1 </span-->', '<span class="verse" id="1">1 </span>')
    partes = re.split(r'<span class="verse" id="(\d+)">\s*\d+\s*</span>', t)
    salida = {}
    for i in range(1, len(partes) - 1, 2):
        x = re.split(r"<br|</p>", partes[i + 1])[0]
        salida[int(partes[i])] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", x))).strip()
    return salida

n = lambda s: re.sub(r"\s+", " ", (s or "").replace("[", "").replace("]", "")).strip()
cache, decisiones = {}, {"eBible (con WP)": 0, "BG (con WP)": 0, "ninguna igual": 0}
revisar, cambios = [], []
for d in dif:
    clave = (d["libro"], d["cap"])
    if clave not in cache: cache[clave] = wp(*clave)
    w = cache[clave].get(d["v"], "")
    eb, bg = n(d["ebible"]), n(d["bg"])
    if n(w) == eb: decisiones["eBible (con WP)"] += 1
    elif n(w) == bg:
        decisiones["BG (con WP)"] += 1
        original = texto[COD[d["libro"]]]["capitulos"][str(d["cap"])][str(d["v"])]
        cambios.append({"ref": f'{d["libro"]} {d["cap"]}:{d["v"]}', "antes": original, "despues": d["bg"], "tenia_añadidas": "[" in original})
    else:
        decisiones["ninguna igual"] += 1
        revisar.append({"ref": f'{d["libro"]} {d["cap"]}:{d["v"]}', "eB": d["ebible"], "BG": d["bg"], "WP": w})
json.dump({"cambios": cambios, "revisar": revisar}, open(f"{B}/votacion.json", "w", encoding="utf8"), ensure_ascii=False, indent=1)
print(decisiones, "· capítulos consultados:", len(cache))
