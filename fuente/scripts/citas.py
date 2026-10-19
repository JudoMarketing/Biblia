"""Lista las frases entre comillas del comentario que no están tal cual en la RV1909 de los tres libros.
Los significados de nombres ("casa del pan") y las traducciones literales del hebreo salen aquí y están bien;
lo que hay que mirar es si alguna se presenta como palabras de la Biblia.
  python3 -I scripts/citas.py <carpeta biblia> [archivos...]"""
import json, re, glob, sys, unicodedata
B = sys.argv[1]
texto = json.load(open(f"{B}/texto-final.json", encoding="utf8"))
def norm(s):
    s = unicodedata.normalize("NFD", s.replace("[", "").replace("]", "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-zñ0-9 ]+", " ", s).split()
todo = " " + " ".join(" ".join(norm(v)) for l in texto.values() for c in l["capitulos"].values() for v in c.values()) + " "
for f in sys.argv[2:] or sorted(glob.glob(f"{B}/comentario/*.json")):
    d = json.load(open(f, encoding="utf8"))
    textos = [(f"nota {n['cap']}:{n['v']}", n["texto"]) for n in d["notas"]] + [(f"pausa {p['cap']}:{p['v']}", p["texto"]) for p in d["pausas"]]
    if d.get("introduccion"): textos.append(("introducción", d["introduccion"]["texto"]))
    total, fuera = 0, []
    for donde, t in textos:
        for q in re.findall(r'["“«]([^"”»]{3,})["”»]', t):
            w = norm(q)
            if len(w) < 2: continue
            total += 1
            if " " + " ".join(w) + " " not in todo: fuera.append(f"{donde}: «{q}»")
    print(f"{f.split('/')[-1]}: {total} citas, {len(fuera)} no están tal cual en la RV1909")
    for x in fuera: print("    " + x)
