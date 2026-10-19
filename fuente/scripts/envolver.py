"""Envuelve la página como lo hace el artifact al publicar (doctype, charset, viewport, reset), solo para probar localmente."""
import sys
cuerpo = open(sys.argv[1], encoding="utf8").read()
esqueleto = ('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
             '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top);padding-bottom:env(safe-area-inset-bottom)}body{margin:0;font:14px system-ui}img{max-width:100%}[hidden]{display:none!important}</style>'
             '</head><body>' + cuerpo + '</body></html>')
open(sys.argv[2], "w", encoding="utf8").write(esqueleto)
