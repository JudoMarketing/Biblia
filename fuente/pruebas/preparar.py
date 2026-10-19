"""Copia de prueba del website con el audio en MP3, porque el Chromium de Playwright no reproduce AAC.

  python3 -I fuente/pruebas/preparar.py sitio <carpeta de prueba>

Copia la página, contenido.json, el manifiesto y los íconos; pasa cada audio .mp4 a .mp3 (solo los que faltan
o cambiaron) y hace que la página pida .mp3. Después, desde fuente/pruebas (con npm install hecho):
  python3 -I ../scripts/servidor.py <carpeta de prueba> 8801 &
  KV_REST_API_URL=http://127.0.0.1:8803 KV_REST_API_TOKEN=prueba PROGRESO_SECRETO=secreto-solo-de-prueba node servidor-prueba.mjs ../../sitio/api/progreso.js
y en otra terminal: node biblia-3.mjs, node libro.mjs (8802), node avance.mjs, node salto.mjs, node biblia-volver.mjs.
"""
import sys, os, shutil
from multiprocessing import Pool
import numpy as np, av, lameenc

SITIO, PRUEBA = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(PRUEBA, "audio"), exist_ok=True)

def a_mp3(nombre):
    origen = os.path.join(SITIO, "audio", nombre)
    destino = os.path.join(PRUEBA, "audio", nombre[:-4] + ".mp3")
    if os.path.exists(destino) and os.path.getmtime(destino) >= os.path.getmtime(origen): return 0
    with av.open(origen) as f:
        pcm = np.concatenate([fr.to_ndarray().reshape(-1) for fr in f.decode(audio=0)])
        sr = f.streams.audio[0].rate
    if pcm.dtype != np.int16: pcm = (np.clip(pcm, -1, 1) * 32767).astype(np.int16)
    e = lameenc.Encoder(); e.set_bit_rate(32); e.set_in_sample_rate(sr); e.set_channels(1); e.set_quality(5)
    datos = e.encode(pcm.tobytes()) + e.flush()
    with open(destino + ".tmp", "wb") as s: s.write(datos)
    os.replace(destino + ".tmp", destino)
    return 1

if __name__ == "__main__":
    for x in ("contenido.json", "manifest.webmanifest", "icono-192.png", "icono-512.png"):
        if os.path.exists(os.path.join(SITIO, x)): shutil.copy(os.path.join(SITIO, x), PRUEBA)
    pagina = open(os.path.join(SITIO, "index.html"), encoding="utf8").read()
    assert pagina.count("audio/${id}.mp4") == 1, "la página ya no pide audio/${id}.mp4: revisa este script"
    open(os.path.join(PRUEBA, "index.html"), "w", encoding="utf8").write(pagina.replace("audio/${id}.mp4", "audio/${id}.mp3"))
    audios = sorted(n for n in os.listdir(os.path.join(SITIO, "audio")) if n.endswith(".mp4"))
    with Pool(os.cpu_count()) as p: hechos = sum(p.map(a_mp3, audios))
    print(f"{len(audios)} audios, {hechos} pasados a MP3 ahora, en {PRUEBA}")
