"""Texto para la voz: lo que se pronuncia, sin tocar lo que se muestra."""
import re

def para_voz(t: str) -> str:
    t = t.replace("[", "").replace("]", "")
    # Palabras en mayúsculas de la 1909 ("EN el principio", "JEHOVÁ", "YO SOY EL QUE SOY"): el lector las deletrearía.
    t = re.sub(r"\b([A-ZÁÉÍÓÚÑÜ]{2,})\b", lambda m: m.group(1).capitalize(), t)
    # Ortografía de 1909: "á" y "ó" sueltas, "é" conjunción, ê circunflejo.
    t = re.sub(r"(?<!\w)[áÁ](?!\w)", "a", t)
    t = re.sub(r"(?<!\w)[óÓ](?!\w)", "o", t)
    t = re.sub(r"(?<!\w)[éÉ](?!\w)", "e", t)
    t = t.replace("ê", "e").replace("Ê", "E").replace("â", "a").replace("ô", "o")
    # Guiones dentro de nombres (Beth-lehem, El-Beth-el): una pausa breve, no la palabra "guion".
    t = re.sub(r"(?<=\w)-(?=\w)", " ", t)
    # La letra hebrea he se dice "je": escrita "he", el lector se come la h y dice "e".
    t = t.replace("yod, he, vav y he", "yod, je, vav y je")
    t = re.sub(r"\s+", " ", t).strip()
    return t

if __name__ == "__main__":
    for x in ["EN el principio crió Dios los cielos y la tierra.", "Así murió Rachêl, y fué sepultada en el camino de Ephrata, la cual es Beth-lehem.",
              "SANTIDAD Á JEHOVÁ.", "Y respondió Dios á Moisés: YO SOY EL QUE SOY.", "y tráeme[lo], y comeré", "Sem, Châm, y Japhet ó Isaac é Ismael"]:
        print(para_voz(x))
