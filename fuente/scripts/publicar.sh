#!/usr/bin/env bash
# Publica el website en Vercel (proyecto biblia del equipo judomarketing, dominio godhome.app) y lo revisa.
#
#   VERCEL_TOKEN=... bash fuente/scripts/publicar.sh fuente <ruta al CLI de vercel>   (desde la raíz del repositorio)
#
# Es el camino alternativo: lo normal es que Vercel publique solo al hacer push a main.
#
# Antes: Upstash for Redis conectado al proyecto en Vercel (crea KV_REST_API_URL y KV_REST_API_TOKEN).
# El secreto PROGRESO_SECRETO se crea aquí la primera vez, sin mostrarlo ni guardarlo en ningún archivo.
set -euo pipefail
B="$(cd "$1" && pwd)"
VERCEL="$2"
EQUIPO=judomarketing
PROYECTO=biblia
SITIO="$(dirname "$B")/sitio"
: "${VERCEL_TOKEN:?falta VERCEL_TOKEN}"
export NODE_USE_ENV_PROXY=1 NODE_EXTRA_CA_CERTS=/root/.ccr/ca-bundle.crt VERCEL_TELEMETRY_DISABLED=1
v() { "$VERCEL" --token "$VERCEL_TOKEN" --scope "$EQUIPO" "$@"; }

echo "1. Armar el website"
python3 -I "$B/scripts/sitio.py" "$B" "$SITIO"
cd "$SITIO"
v link --yes --project "$PROYECTO" > /dev/null

echo "2. Revisar las variables del proyecto"
VARIABLES="$(v env ls production 2>/dev/null || true)"
if ! grep -q "KV_REST_API_URL" <<< "$VARIABLES"; then
  echo "   FALTA la base de datos: conecta Upstash for Redis a $PROYECTO en Vercel (Storage). Sin ella el sitio funciona, pero no guarda el avance."
fi
if grep -q "PROGRESO_SECRETO" <<< "$VARIABLES"; then
  echo "   PROGRESO_SECRETO ya existe"
else
  openssl rand -hex 32 | tr -d '\n' | v env add PROGRESO_SECRETO production > /dev/null
  echo "   PROGRESO_SECRETO creado (no se muestra)"
fi

echo "3. Publicar"
URL="$(v deploy --prod --yes --archive=tgz 2> "$B/../deploy.log")"
echo "   publicado: $URL"
DOMINIO="https://www.godhome.app"

echo "4. Revisar el sitio publicado"
for u in "$DOMINIO" "$URL"; do
  codigo="$(curl -s -o /dev/null -w '%{http_code}' "$u/")"
  echo "   $u -> $codigo"
done
curl -sI "$DOMINIO/audio/GEN-01.mp4" | grep -iE '^(HTTP|content-type|accept-ranges|cache-control)' | sed 's/^/   /'
curl -sI "$DOMINIO/" | grep -iE '^(content-security-policy|x-robots-tag)' | cut -c1-90 | sed 's/^/   /'
echo "   api/progreso (número de prueba 202-555-0100):"
curl -s -X POST "$DOMINIO/api/progreso" -H 'Content-Type: application/json' -d '{"accion":"leer","telefono":"2025550100"}' | sed 's/^/   /'
echo
