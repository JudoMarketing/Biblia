"""Audio de cada capítulo (y de las introducciones) con dos voces y la hora exacta de cada parte.

Entrada: contenido.json (lo arma scripts/armar.py). Salida: salida/audio/<id>.mp4 y salida/tiempos/<id>.json.
  python3 -I voz/generar.py <carpeta biblia> [ids...]     (sin ids: todo lo que falta)
  python3 -I voz/generar.py <carpeta biblia> --calentar   (solo sintetiza la lectura de la Biblia y la guarda)

Cada texto dicho se guarda en voz/cache (por voz, ritmo y texto): el texto bíblico no cambia, así que se
sintetiza una sola vez, y al corregir una nota solo se vuelve a decir esa nota.
"""
import sys, os, json, wave, io, math, time, hashlib
from multiprocessing import Pool
import numpy as np
B = sys.argv[1]
sys.path.insert(0, os.path.join(B, "voz"))
from hablar import para_voz

SR = 24000
VOZ_BIBLIA = "es-US-Chirp3-HD-" + os.environ.get("VOZ_BIBLIA", "Iapetus")
VOZ_GUIA = "es-US-Chirp3-HD-" + os.environ.get("VOZ_GUIA", "Vindemiatrix")
RITMO = {VOZ_BIBLIA: 0.95, VOZ_GUIA: 1.0}   # speakingRate de Google
KBPS = int(os.environ.get("KBPS", "30"))   # AAC en .mp4: a 24 kbps el MP3 cortaba todo arriba de 6000 Hz

def codificar(pcm, ruta):
    """PCM mono de 24000 Hz a AAC en contenedor MP4 (.mp4), con el índice al principio para empezar a sonar rápido."""
    import av
    temporal = f"{ruta}.{os.getpid()}.tmp"
    with av.open(temporal, "w", format="mp4", options={"movflags": "+faststart"}) as sal:
        flujo = sal.add_stream("aac", rate=SR, layout="mono")
        flujo.bit_rate = KBPS * 1000
        for i in range(0, len(pcm), SR):
            cuadro = av.AudioFrame.from_ndarray(pcm[i:i + SR].reshape(1, -1), format="s16", layout="mono")
            cuadro.sample_rate = SR
            for paquete in flujo.encode(cuadro): sal.mux(paquete)
        for paquete in flujo.encode(None): sal.mux(paquete)
    os.replace(temporal, ruta)
SILENCIO = {"entre_versos": 0.45, "antes_guia": 0.55, "despues_guia": 0.7, "titulo": 0.9, "parrafo": 0.6}

URL = "https://texttospeech.googleapis.com/v1/text:synthesize"

def voz(nombre, dicho):
    """Google Cloud Text-to-Speech (Chirp 3 HD). La clave va solo en el encabezado X-Goog-Api-Key."""
    import urllib.request, urllib.error, base64, random
    assert len(dicho.encode("utf8")) < 5000, dicho[:80]
    cuerpo = json.dumps({"input": {"text": dicho},
                         "voice": {"languageCode": "es-US", "name": nombre},
                         "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": SR, "speakingRate": RITMO[nombre]}}).encode("utf8")
    espera = 2.0
    for intento in range(10):
        req = urllib.request.Request(URL, data=cuerpo, method="POST", headers={
            "Content-Type": "application/json; charset=utf-8", "X-Goog-Api-Key": os.environ["GOOGLE_TTS_API_KEY"]})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                datos = base64.b64decode(json.load(r)["audioContent"])
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 and e.code < 500: raise RuntimeError(f"Google {e.code}: {e.read()[:300]!r}") from None
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            pass
        time.sleep(espera + random.random()); espera = min(espera * 2, 60)
    else:
        raise RuntimeError("Google no respondió tras 10 intentos")
    with wave.open(io.BytesIO(datos), "rb") as w:
        assert w.getframerate() == SR and w.getnchannels() == 1 and w.getsampwidth() == 2
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)

CACHE = os.path.join(B, "voz", "cache")

def decir(texto, nombre):
    dicho = para_voz(texto)
    clave = hashlib.sha1(f"{nombre}|{RITMO[nombre]}|{dicho}".encode("utf8")).hexdigest()
    ruta = os.path.join(CACHE, clave[:2], clave + ".pcm")
    if os.path.exists(ruta):
        return np.fromfile(ruta, dtype=np.int16)
    pcm = voz(nombre, dicho)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    temporal = f"{ruta}.{os.getpid()}.tmp"
    pcm.tofile(temporal); os.replace(temporal, ruta)
    return pcm

def calentar(texto):
    t0 = time.time()
    return len(decir(texto, VOZ_BIBLIA)) / SR, time.time() - t0

def silencio(seg): return np.zeros(int(SR * seg), dtype=np.int16)

def campana():
    """Dos notas suaves antes de cada explicación: avisa que cambia la voz."""
    partes = []
    for f, d in [(659.25, 0.16), (987.77, 0.30)]:
        t = np.arange(int(SR * d)) / SR
        env = np.minimum(1, t / 0.01) * np.exp(-t * 7)
        onda = 0.18 * env * (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(4 * np.pi * f * t))
        partes.append((onda * 32767).astype(np.int16))
    return np.concatenate(partes)
CAMPANA = None

def generar(trabajo):
    """trabajo = {"id": "GEN-01", "partes": [{"clave": "v1", "voz": "biblia"|"guia", "textos": [...], "campana": bool}]}"""
    global CAMPANA
    if CAMPANA is None: CAMPANA = campana()
    salida_audio = os.path.join(B, "salida", "audio", f"{trabajo['id']}.mp4")
    salida_t = os.path.join(B, "salida", "tiempos", f"{trabajo['id']}.json")
    t0 = time.time()
    trozos, tiempos, pos = [], [], 0
    def poner(x):
        nonlocal pos
        trozos.append(x); pos += len(x)
    previa = None
    for p in trabajo["partes"]:
        es_guia = p["voz"] == "guia"
        if previa is not None:
            poner(silencio(SILENCIO["antes_guia"] if es_guia else (SILENCIO["despues_guia"] if previa == "guia" else SILENCIO["entre_versos"])))
        inicio = pos / SR
        if p.get("campana"):
            poner(CAMPANA); poner(silencio(0.25))
        for i, texto in enumerate(p["textos"]):
            if i: poner(silencio(SILENCIO["parrafo"]))
            poner(decir(texto, VOZ_GUIA if es_guia else VOZ_BIBLIA))
        if p.get("pausa_larga"): poner(silencio(SILENCIO["titulo"] - SILENCIO["entre_versos"]))
        tiempos.append({"clave": p["clave"], "t": round(inicio, 2)})
        previa = p["voz"]
    poner(silencio(1.0))
    pcm = np.concatenate(trozos)
    os.makedirs(os.path.dirname(salida_audio), exist_ok=True); os.makedirs(os.path.dirname(salida_t), exist_ok=True)
    codificar(pcm, salida_audio)
    peso = os.path.getsize(salida_audio)
    dur = len(pcm) / SR
    json.dump({"id": trabajo["id"], "duracion": round(dur, 2), "partes": tiempos}, open(salida_t, "w", encoding="utf8"), ensure_ascii=False)
    return trabajo["id"], dur, peso, time.time() - t0

if __name__ == "__main__":
    trabajos = json.load(open(os.path.join(B, "salida", "trabajos.json"), encoding="utf8"))
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    if "--calentar" in sys.argv:
        textos = sorted({t for tr in trabajos for p in tr["partes"] if p["voz"] == "biblia" for t in p["textos"]}, key=len, reverse=True)
        print(f"{len(textos)} textos de la Biblia por decir (los que ya están guardados salen al instante)", flush=True)
        total = 0.0
        with Pool(int(os.environ.get("PROCESOS", "6"))) as pool:
            for i, (dur, seg) in enumerate(pool.imap_unordered(calentar, textos, chunksize=4), 1):
                total += dur
                if i % 250 == 0 or i == len(textos):
                    print(f"  {i}/{len(textos)} · {total/3600:.2f} h de lectura", flush=True)
        sys.exit(0)
    pedidos = set(sys.argv[2:])
    hechos = lambda t: os.path.exists(os.path.join(B, "salida", "audio", f"{t['id']}.mp4"))
    lista = [t for t in trabajos if (t["id"] in pedidos if pedidos else not hechos(t))]
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    print(f"{len(lista)} audios por generar", flush=True)
    with Pool(int(os.environ.get("PROCESOS", "6"))) as pool:
        for i, (ide, dur, peso, seg) in enumerate(pool.imap_unordered(generar, lista), 1):
            print(f"  {i}/{len(lista)} {ide}: {dur/60:.1f} min de audio, {peso/1e6:.2f} MB, en {seg:.0f} s", flush=True)
