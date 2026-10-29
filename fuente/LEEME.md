# Respaldo del proyecto «La Biblia en voz alta»

Fuentes para rehacer el audio o seguir con otros libros en otra sesión. Hoy tiene seis libros: Génesis, Éxodo, Levítico, Números, Deuteronomio y Josué.

- texto-final.json: Reina Valera 1909 de los seis libros. Se cotejó con varias fuentes digitales y, donde no coincidían, con un ejemplar impreso de 1909 (La Liga Bíblica, escaneado en archive.org como «santabibliaantig0000vari»). correcciones.json tiene los cambios hechos al texto digital.
- comentario/*.json: notas, pausas e introducciones, por tramos. Cada tramo lo escribió un agente y lo revisó otro distinto. GUIA.md es la guía de estilo con la tabla de cronología; su sección final cubre Números, Deuteronomio y Josué.
- intro-general.json: el texto de "Antes de empezar". Ya no se usa en la página.
- scripts/armar.py: une texto y comentario en contenido.json y trabajos.json (las partes que dice cada voz).
- voz/generar.py y voz/hablar.py: la voz con caché por texto, audio AAC en .mp4 (mono, 24000 Hz, 30 kbps, codificado con PyAV) y la hora de cada parte. Antes era MP3 de 24 kbps, que cortaba los agudos.
- Voces (octubre de 2026): Google Cloud Text-to-Speech, Chirp 3 HD en español de Estados Unidos: es-US-Chirp3-HD-Iapetus lee la Biblia (velocidad 0,95) y es-US-Chirp3-HD-Vindemiatrix es el guía (velocidad 1,0). generar.py necesita la clave en la variable GOOGLE_TTS_API_KEY, que va solo en el encabezado de cada pedido y nunca a un archivo.
- Para generar solo algunos audios: `python3 -I fuente/voz/generar.py fuente NUM-01 NUM-02 ...`. Sin ids genera lo que falta en salida/audio y en ../sitio/audio; si un capítulo ya publicado cambió, hay que pasar su id.
- La cuota gratis de Chirp 3 HD es de un millón de caracteres por mes calendario (Google la reinicia el día 1, hora del Pacífico); lo que pasa de ahí cuesta. voz/generar.py cuenta antes lo que no está en la caché y no genera si el mes pasaría de 950 mil (variable TOPE_MENSUAL); lo usado queda anotado en voz/consumo.json, que va al repositorio.
- scripts/pendientes.py dice qué generar este mes: primero los capítulos grabados cuyo texto cambió (voz/rehacer.txt, o la huella que generar.py guarda en salida/tiempos), después libros enteros sin voz, en orden, mientras quepan. Una tarea programada lo corre el día 2 de cada mes: genera, prueba y publica.
- scripts/revisar.py y scripts/citas.py: verificadores del comentario. scripts/ver.py muestra el texto de un tramo. scripts/tandas.py reparte los archivos para publicar.
- pagina/genesis-exodo-levitico.html: la página, sin el esqueleto que agrega la publicación. El nombre del archivo quedó de cuando eran tres libros.

Website (Vercel, proyecto biblia del equipo judomarketing, dominio godhome.app). Vercel publica solo con cada push a main:
- scripts/sitio.py arma el website (página completa, manifiesto para instalarla en el teléfono, íconos, vercel.json con encabezados de seguridad) y copia sitio-api/progreso.js como api/progreso.js.
- sitio-api/progreso.js guarda el avance de cada persona con su número de teléfono de Estados Unidos en Upstash Redis. El número no se guarda: la clave es un HMAC con PROGRESO_SECRETO. Límite de 20 números distintos cada 10 minutos por conexión.
- scripts/publicar.sh es el camino alternativo con el CLI de Vercel: crea el secreto si falta, publica y revisa el sitio.
- Carga adelantada, como en YouTube: el service worker (pagina/sw.js, publicado como sitio/sw.js) guarda completos el capítulo que suena y el siguiente (el siguiente se baja a los 10 segundos; con «ahorro de datos», en los últimos cinco minutos), y los entrega por rangos de bytes. Se puede adelantar sin esperar, el paso al capítulo siguiente es inmediato y un corte de internet no detiene lo guardado. Guarda como mucho 6 archivos. La barra muestra lo oído y lo cargado. No se usan copias blob: la política de seguridad (media-src 'self') las bloquea; esa era la causa del «error de conexión» al cambiar de capítulo. Si una carga falla, reintenta sola desde el mismo punto (pruebas: pruebas/carga.mjs con el service worker y pruebas/corte.mjs sin él).
- Libros sin voz todavía: se pueden leer; en lugar del botón de escuchar dicen que la voz llega pronto, y al terminar el último capítulo con voz el audio se detiene y lo avisa.
- Diseño de libro: al entrar se abre una Biblia de cuero (unos 4 segundos, se salta tocando la pantalla), el texto está en una hoja de papel, los libros son separadores de papel en el canto derecho y cambiar de libro o de capítulo pasa hojas. En pantallas anchas el libro se ve abierto, con los capítulos en la página izquierda. Con "reducir movimiento" no hay animaciones.
- Encabezados de seguridad y `noindex` en `sitio/vercel.json`, para que no aparezca en buscadores.

Pruebas (Playwright, en pruebas/; `npm install` ahí una vez):
- pruebas/preparar.py arma una copia de prueba del website con el audio en MP3, porque el Chromium de Playwright no reproduce AAC. Copia también sw.js y vercel.json: scripts/servidor.py manda los mismos encabezados que Vercel, con la política de seguridad, para que las pruebas vean lo mismo que el sitio publicado. Su encabezado explica cómo levantar los dos servidores de prueba (8801 estático, 8802 con la función de avance y un Redis falso de servidor-prueba.mjs).
- biblia-3.mjs: avance entre capítulos y libros hasta Josué 24, toques, índice, Continuar, velocidad, capturas en 360, 390, 768 y 1440.
- libro.mjs: apertura, separadores, hojas, página izquierda, portada limpia y crédito.
- avance.mjs (avance entre dos aparatos), salto.mjs (salto entre capítulos con conexión lenta) y biblia-volver.mjs (el botón "Volver a lo que suena").
