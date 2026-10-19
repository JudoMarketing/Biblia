# Guía del comentario · Génesis, Éxodo y Levítico (Reina-Valera 1909)

## Para quién y para qué

Una persona quiere **aprender la Biblia escuchándola completa**, empezando por
Génesis, Éxodo y Levítico. El texto bíblico va **íntegro y sin cambios**
(Reina-Valera 1909, dominio público, en `texto-final.json`). Tu trabajo es el
comentario, que se muestra y se escucha aparte, con otra voz:

1. **Notas**: cortas, después de un versículo, donde falte contexto para entender.
2. **Pausas**: después de un momento fuerte, un alto para dar el contexto
   histórico: qué pasaba en ese momento en el mundo, cómo vivía la gente, qué
   acontecimientos llevaron a ese hecho, cómo era el lugar.

Pidió expresamente: "quiero que las conclusiones las tome yo, pero que tú seas
quien pone los detalles y el contexto histórico y de acontecimientos que
llevaron a ese hecho". Y que la historia se vaya armando en su mente mientras
escucha.

## Reglas que no se negocian

1. **La Biblia no se toca.** Nunca resumas ni parafrasees como si fuera el
   texto. Si citas, cita palabras exactas de la RV1909 (de `texto-final.json`)
   entre comillas. No cites ni copies otras traducciones (ni RVR1960, ni NVI,
   ni otras) ni comentarios publicados: todo lo que escribas es tuyo.
2. **Sin conclusiones impuestas.** Nada de "esto nos enseña que…", "el mensaje
   es…", "debemos…". Describe: qué pasaba, quiénes eran, qué significaba en su
   cultura, qué dice el texto en otras partes, qué discuten los estudiosos.
   Para que él piense, cada pausa puede cerrar con una o dos preguntas
   abiertas (campo `preguntas`), que no insinúen la respuesta.
3. **Historia con honestidad y respeto por la fe.** Cuando una fecha o un dato
   se discute, dilo y da las posturas principales (la tradición judía y
   cristiana, y lo que piensan muchos historiadores), sin burla y sin presentar
   hipótesis como hechos. El oyente es creyente o se está acercando a la fe:
   trata el texto con respeto.
4. **Precisión.** Solo datos que conozcas con seguridad. Nada inventado: ni
   nombres de reyes, ni fechas exactas, ni hallazgos que no estén bien
   establecidos. Los textos y hallazgos antiguos, con su nombre y fecha
   aproximada (por ejemplo: Código de Hammurabi, hacia 1750 antes de Cristo;
   Epopeya de Gilgamesh; Enuma Elish; tablillas de Mari y de Nuzi; estela de
   Merneptah, hacia 1208 antes de Cristo). Si dudas de un dato, déjalo fuera.
5. **Escrito para escucharse.** Oraciones claras, de largo normal. Sin
   abreviaturas: "antes de Cristo" (nunca "a. C."), "aproximadamente",
   "kilómetros", "metros". Las citas bíblicas, en palabras: "Génesis 12,
   versículo 3" o "el capítulo 15" (nunca "12:3"). Números con cifras está
   bien ("1800"). Sin paréntesis largos, sin símbolos (%, /, &), sin viñetas
   ni listas dentro del texto, sin emojis.
6. **Sin rayas ni guiones para marcar pausas** (ni —, ni –, ni " - "). Usa
   comas, puntos o dos puntos.
7. **Español neutro latinoamericano**, tratando al oyente de "tú". Cálido y
   claro, como un buen guía de museo que sabe mucho y no presume.
8. **Nombres y palabras de 1909.** La RV1909 usa grafías y palabras antiguas.
   La primera vez que aparezcan en tu tramo, da la forma actual o el sentido:
   Rachêl es Raquel, Ephraim es Efraín, Beth-lehem es Belén, Hetheo es hitita,
   Amorrheo es amorreo; "crió" es "creó"; "la haz" es la superficie;
   "expansión" es el firmamento; "conocer a su mujer" es tener relaciones;
   "simiente" es descendencia; "horro" es libre; "el Mediodía" es el Néguev, el
   sur de Canaán. En 1909 la preposición "a" se escribía "á" y la conjunción
   "o", "ó": no hace falta explicarlo cada vez (la introducción general lo dice).
9. Las palabras entre corchetes en el texto, como "tráeme[lo]", son palabras
   que los traductores añadieron para que se entienda (se muestran en
   cursiva). No hace falta comentarlas.

## Notas (`notas`)

- Van **después** del versículo indicado (`cap`, `v`).
- 1 a 3 oraciones, de 15 a 70 palabras.
- Solo donde hagan falta: una palabra antigua, un nombre y lo que significa, un
  lugar y dónde queda, una costumbre, una medida (codo, unos 45 centímetros;
  siclo, unos 11 gramos; efa, unos 22 litros; usa valores aproximados
  aceptados y dilo así), o un lazo con algo anterior que ayuda a seguir la
  historia.
- No una por versículo. En promedio, una cada 8 a 15 versículos: más en los
  capítulos difíciles (genealogías, leyes, tabernáculo, sacrificios, pureza),
  menos en las narraciones que se entienden solas.

## Pausas (`pausas`)

- Van después de un momento fuerte (una escena decisiva, una promesa, una
  caída, un encuentro, una ley central), nunca en medio de una escena.
- `titulo`: 3 a 8 palabras. `epoca`: una sola oración corta (se dice en voz
  alta como "Época: …"), con el momento y de dónde sale la fecha (por ejemplo,
  "Abram tiene 75 años; hacia 2091 antes de Cristo, según la cronología
  bíblica tradicional"). Nada de rangos de siglos que mezclen cuentas
  distintas. `lugar`: una línea. `texto`: 350 a 700
  palabras, en 3 a 6 párrafos separados por una línea en blanco ("\n\n").
  `preguntas`: 0 a 2 preguntas abiertas y cortas.
- Contenido: qué pasaba en el mundo (Mesopotamia, Egipto, Canaán), cómo vivía
  la gente (pastores, ciudades, pactos, la familia, la tierra), qué
  acontecimientos llevaron a esta escena, cómo era el lugar (paisaje, clima,
  distancias), costumbres que ayudan a entender, cómo lo pudieron entender sus
  primeros lectores, y cómo se conecta con lo que ya pasó. No adelantes el
  final de las historias que vienen.

## Introducciones (`introduccion`)

Solo donde la tarea lo pida: `titulo` y `texto` de 600 a 900 palabras, en
párrafos separados por "\n\n": de qué trata el libro, cómo está organizado,
quién lo escribió según la tradición y qué dicen los estudiosos, en qué época
y lugar ocurre, y qué conviene tener presente al escucharlo.

## Formato del archivo

```json
{
  "tramo": "GEN-01",
  "libro": "GEN",
  "desde": {"cap": 1, "v": 1},
  "hasta": {"cap": 11, "v": 32},
  "introduccion": {"titulo": "...", "texto": "..."},
  "notas": [{"cap": 1, "v": 1, "texto": "..."}],
  "pausas": [{"cap": 1, "v": 31, "titulo": "...", "epoca": "...", "lugar": "...", "texto": "...", "preguntas": ["..."]}]
}
```

`introduccion` solo si te la piden (si no, no la pongas). Escribe el archivo
con Python (`json.dump(..., ensure_ascii=False, indent=1)`) para no romper
comillas, y compruébalo con:
`python3 -I scripts/revisar.py <archivo>` (desde la carpeta `biblia`).

## Cronología: una sola para toda la guía

Las fechas de las pausas salen de la **cronología bíblica tradicional**, que
se calcula con el propio texto hebreo: Primero de Reyes 6 pone la salida de
Egipto 480 años antes del cuarto año de Salomón (hacia 966), o sea hacia
**1446 antes de Cristo**; Éxodo 12 da 430 años en Egipto, y las edades de los
patriarcas hacen el resto:

| Hecho | Edad o dato | Antes de Cristo |
|---|---|---|
| Nace Abram | | 2166 |
| Sale de Harán | Abram, 75 | 2091 |
| Nace Ismael | Abram, 86 | 2080 |
| Pacto de la circuncisión, Sodoma | Abraham, 99 | 2067 |
| Nace Isaac | Abraham, 100 | 2066 |
| Muere Sara | 127; Abraham, 137 | 2029 |
| Isaac se casa con Rebeca | Isaac, 40 | 2026 |
| Nacen Esaú y Jacob | Isaac, 60 | 2006 |
| Muere Abraham | 175 | 1991 |
| Muere Ismael | 137 | 1943 |
| Jacob huye a Harán | Jacob, 77 | 1929 |
| Bodas de Jacob con Lea y Raquel | Jacob, 84 | 1922 |
| Nace José | Jacob, 91 | 1915 |
| Jacob vuelve a Canaán (Peniel) | Jacob, 97 | 1909 |
| José es vendido | José, 17 | 1898 |
| Muere Isaac | 180 | 1886 |
| José ante Faraón | José, 30 | 1885 |
| Israel baja a Egipto | Jacob, 130 | 1876 |
| Muere Jacob | 147 | 1859 |
| Muere José | 110 | 1805 |
| Nace Moisés | 80 años antes de la salida | 1526 |
| Salida de Egipto | | 1446 |

Esta cuenta es aproximada (depende de leer las edades al pie de la letra), y
hay otras dos posturas que se mencionan sin decidir:

- **La cuenta corta.** La antigua traducción griega y el Pentateuco samaritano
  leen en Éxodo 12 que los 430 años incluyen la estancia en Canaán; Egipto
  serían 215 años y todas las fechas de los patriarcas bajan unos 215 años
  (Israel llegaría a Egipto hacia 1661, en tiempos de los hicsos).
- **Los historiadores.** No hay rastros arqueológicos directos de los
  patriarcas; muchos ubican el mundo que describen las historias en la Edad
  del Bronce Medio (hacia 2000 a 1550 antes de Cristo), y muchos piensan que
  se pusieron por escrito siglos después. Para la salida de Egipto, muchos
  prefieren el siglo trece antes de Cristo (en tiempos de Ramsés II) en lugar
  de 1446.

En cada pausa: la fecha tradicional, dicha así ("según la cronología bíblica
tradicional"). Las otras posturas se explican con calma una vez (en la
primera pausa de Abraham y en la introducción de Éxodo) y después basta un
recordatorio breve cuando importe.
