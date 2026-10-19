# La Biblia en voz alta

Los seis primeros libros de la Biblia completos, de Génesis a Josué, en la Reina Valera 1909 (dominio público), para escuchar en voz alta. Una voz lee el texto bíblico y otra, la del guía, explica con notas y pausas de contexto histórico. Se publica en https://www.godhome.app.

## Qué hay aquí

- `sitio/`: el website tal como se publica en Vercel (proyecto `biblia` del equipo judomarketing, con los dominios godhome.app y www.godhome.app). Es estático, más una función en `sitio/api/progreso.js` que guarda el avance de cada persona con su número de teléfono.
- `fuente/`: todo lo necesario para rehacerlo: el texto (`texto-final.json`), el comentario (`comentario/`), la guía de estilo (`GUIA.md`), la página (`pagina/`), la voz (`voz/`), los scripts (`scripts/`) y las pruebas (`pruebas/`). `fuente/LEEME.md` tiene el detalle.

## Publicar

Vercel publica solo cada vez que hay un push a `main`, con `sitio` como carpeta raíz del proyecto. Para que el avance se guarde, el proyecto necesita en Vercel:

1. Upstash for Redis conectado (pestaña Storage). Crea `KV_REST_API_URL` y `KV_REST_API_TOKEN`.
2. La variable `PROGRESO_SECRETO` con un texto largo y al azar. Se crea una sola vez y no se cambia: si cambia, cada número apunta a un avance nuevo y el anterior queda perdido.

Sin esas dos cosas el sitio funciona igual, pero el avance solo se guarda en cada aparato.

## Cambiar la página

Edita `fuente/pagina/genesis-exodo-levitico.html` y vuelve a armar el sitio desde la raíz del repositorio:

```
python3 -I fuente/scripts/sitio.py fuente sitio
```

Conserva los audios y `contenido.json` que ya están en `sitio/`. Para rehacer el audio hace falta la clave de Google Cloud Text-to-Speech en `GOOGLE_TTS_API_KEY` (ver `fuente/LEEME.md`); la clave nunca va al repositorio.

## Seguridad

- El número de teléfono no se guarda: la base solo tiene un HMAC del número con `PROGRESO_SECRETO`.
- Cada conexión puede probar como máximo 20 números distintos cada 10 minutos.
- Sin PIN: quien escriba el número de otra persona puede ver y cambiar su avance. La página lo dice junto al formulario.
- Encabezados de seguridad y `noindex` en `sitio/vercel.json`, para que no aparezca en buscadores.
