# Respaldo del proyecto "Génesis, Éxodo y Levítico"

Fuentes para rehacer el audio o seguir con otros libros en otra sesión.

- texto-final.json: Reina Valera 1909 de los tres libros, cotejada con tres fuentes. correcciones.json tiene las 4 palabras corregidas.
- comentario/*.json: notas, pausas e introducciones, ya revisadas. GUIA.md es la guía de estilo con la tabla de cronología.
- intro-general.json: el texto de "Antes de empezar".
- scripts/armar.py: une texto y comentario en contenido.json y trabajos.json (las partes que dice cada voz).
- voz/generar.py y voz/hablar.py: la voz con caché por texto, audio AAC en .mp4 (mono, 24000 Hz, 30 kbps, codificado con PyAV) y la hora de cada parte. Antes era MP3 de 24 kbps, que cortaba los agudos.
- Voces (octubre de 2026): Google Cloud Text-to-Speech, Chirp 3 HD en español de Estados Unidos: es-US-Chirp3-HD-Iapetus lee la Biblia (velocidad 0,95) y es-US-Chirp3-HD-Vindemiatrix es el guía (velocidad 1,0). generar.py necesita la clave en la variable GOOGLE_TTS_API_KEY; antes se usaba Piper.
- scripts/revisar.py y scripts/citas.py: verificadores del comentario. scripts/tandas.py reparte los archivos para publicar.
- pagina/genesis-exodo-levitico.html: la página, sin el esqueleto que agrega la publicación.

Los .py y la página llevan .txt al final solo para poder guardarlos aquí.

Pruebas de la página (Playwright, con el servidor local de scripts/servidor.py en el puerto 8801):
- pruebas/biblia-3.mjs: avance entre capítulos y libros, toques, índice, Continuar, velocidad, capturas en 360, 390, 768 y 1440.
- pruebas/biblia-volver.mjs: el botón "Volver a lo que suena".

Website fuera de Claude (Vercel, proyecto biblia-gel del equipo judomarketing):
- scripts/sitio.py arma el website (página completa, manifiesto para instalarla en el teléfono, íconos, vercel.json con encabezados de seguridad) y copia sitio-api/progreso.js como api/progreso.js.
- sitio-api/progreso.js guarda el avance de cada persona con su número de teléfono de Estados Unidos en Upstash Redis. El número no se guarda: la clave es un HMAC con PROGRESO_SECRETO. Límite de 20 números distintos cada 10 minutos por conexión.
- scripts/publicar.sh crea el secreto si falta, publica y revisa el sitio.
- La página precarga el capítulo siguiente en los últimos cinco minutos. Con la página a la vista, el siguiente sale de esa copia y empieza de inmediato; con la pantalla bloqueada se pide por su dirección, que la precarga ya dejó en la caché. Si una carga falla, reintenta sola desde el mismo punto y sigue cuando vuelve la señal (prueba: pruebas/corte.mjs).
- Pruebas nuevas: pruebas/avance.mjs (avance entre dos aparatos) y pruebas/salto.mjs (salto entre capítulos con conexión lenta), con un servidor de prueba en el puerto 8802.
- Diseño de libro: al entrar se abre una Biblia de cuero (unos 4 segundos, se salta tocando la pantalla), el texto está en una hoja de papel, los libros son separadores de papel en el canto derecho y cambiar de libro o de capítulo pasa hojas. En pantallas anchas el libro se ve abierto, con los capítulos en la página izquierda. Con "reducir movimiento" no hay animaciones. Prueba: pruebas/libro.mjs.
