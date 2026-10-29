"""Une el texto RV1909 con el comentario: contenido.json (para la página) y trabajos.json (para la voz).

  python3 -I scripts/armar.py <carpeta biblia> [--tiempos]   (--tiempos agrega los segundos de cada parte ya generados)
"""
import json, os, sys, glob
B = sys.argv[1]
texto = json.load(open(f"{B}/texto-final.json", encoding="utf8"))
intro_general = json.load(open(f"{B}/intro-general.json", encoding="utf8"))
comentarios = [json.load(open(f, encoding="utf8")) for f in sorted(glob.glob(f"{B}/comentario/*.json"))]

notas, pausas, intros = {}, {}, {}
for c in comentarios:
    for n in c.get("notas", []):
        notas.setdefault((c["libro"], n["cap"], n["v"]), []).append(n["texto"])
    for p in c.get("pausas", []):
        pausas.setdefault((c["libro"], p["cap"], p["v"]), []).append(p)
    if c.get("introduccion"): intros[c["libro"]] = c["introduccion"]

libros, trabajos = [], []
contador_pausas = 0
for codigo in [c for c in ["GEN", "EXO", "LEV", "NUM", "DEU", "JOS", "JDG", "RUT"] if c in texto]:
    libro = texto[codigo]
    caps = []
    if codigo in intros:
        trabajos.append({"id": f"INTRO-{codigo}", "partes": [
            {"clave": "i", "voz": "guia", "campana": True, "textos": [f"Introducción al libro de {libro['nombre']}. {intros[codigo]['titulo']}."] + intros[codigo]["texto"].split("\n\n")}]})
    for c in range(1, len(libro["capitulos"]) + 1):
        items, partes = [], [{"clave": "c", "voz": "biblia", "textos": [f"{libro['nombre']}, capítulo {c}."], "pausa_larga": True}]
        for v_txt, x in libro["capitulos"][str(c)].items():
            v = int(v_txt)
            items.append({"t": "v", "k": f"v{v}", "n": v, "x": x})
            partes.append({"clave": f"v{v}", "voz": "biblia", "textos": [x]})
            for i, nota in enumerate(notas.get((codigo, c, v), []), 1):
                k = f"n{v}-{i}"
                items.append({"t": "nota", "k": k, "x": nota})
                partes.append({"clave": k, "voz": "guia", "campana": True, "textos": [f"Nota. {nota}"]})
            for p in pausas.get((codigo, c, v), []):
                contador_pausas += 1
                k = f"p{v}-{contador_pausas}"
                items.append({"t": "pausa", "k": k, "titulo": p["titulo"], "epoca": p["epoca"], "lugar": p["lugar"], "x": p["texto"], "preguntas": p.get("preguntas", [])})
                dichos = [f"Pausa para el contexto. {p['titulo']}.", f"Época: {p['epoca'].rstrip('.')}. Lugar: {p['lugar'].rstrip('.')}."] + p["texto"].split("\n\n")
                if p.get("preguntas"): dichos.append("Para pensar. " + " ".join(p["preguntas"]))
                partes.append({"clave": k, "voz": "guia", "campana": True, "textos": dichos})
        caps.append({"n": c, "items": items})
        trabajos.append({"id": f"{codigo}-{c:02d}", "partes": partes})
    libros.append({"id": codigo, "nombre": libro["nombre"], "intro": intros.get(codigo), "capitulos": caps})

trabajos.insert(0, {"id": "INTRO", "partes": [{"clave": "i", "voz": "guia", "campana": True, "textos": [intro_general["titulo"] + "."] + intro_general["texto"].split("\n\n")}]})
contenido = {"intro": intro_general, "libros": libros, "correcciones": json.load(open(f"{B}/correcciones.json", encoding="utf8"))}

if "--tiempos" in sys.argv:
    def tiempos(ide):
        f = f"{B}/salida/tiempos/{ide}.json"
        return json.load(open(f, encoding="utf8")) if os.path.exists(f) else None
    contenido["intro"]["audio"] = tiempos("INTRO")
    for l in libros:
        if l["intro"]: l["intro"]["audio"] = tiempos(f"INTRO-{l['id']}")
        for c in l["capitulos"]: c["audio"] = tiempos(f"{l['id']}-{c['n']:02d}")

os.makedirs(f"{B}/salida", exist_ok=True)
json.dump(contenido, open(f"{B}/salida/contenido.json", "w", encoding="utf8"), ensure_ascii=False, separators=(",", ":"))
json.dump(trabajos, open(f"{B}/salida/trabajos.json", "w", encoding="utf8"), ensure_ascii=False)
palabras = lambda ps: sum(len(t.split()) for p in ps for t in p["textos"])
guia = sum(len(t.split()) for tr in trabajos for p in tr["partes"] if p["voz"] == "guia" for t in p["textos"])
biblia = sum(len(t.split()) for tr in trabajos for p in tr["partes"] if p["voz"] == "biblia" for t in p["textos"])
print(f"{len(comentarios)} tramos de comentario · {sum(len(v) for v in notas.values())} notas · {contador_pausas} pausas · {len(trabajos)} audios")
print(f"palabras: Biblia {biblia} · guía {guia} · tamaño de contenido.json {os.path.getsize(f'{B}/salida/contenido.json')/1e6:.2f} MB")
