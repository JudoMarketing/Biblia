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
   Amorrheo es amorreo; "la haz" es la superficie;
   "expansión" es el firmamento; "conocer a su mujer" es tener relaciones;
   "simiente" es descendencia; "horro" es libre; "el Mediodía" es el Néguev, el
   sur de Canaán. En 1909 la preposición "a" se escribía "á" y la conjunción
   "o", "ó": no hace falta explicarlo cada vez (la introducción general lo dice).
   Donde la de 1909 decía "crió", "criado" o "criador" con el sentido de crear,
   el texto ya dice "creó", "creado" y "creador" (está en correcciones.json):
   no hace falta explicarlo. Donde quiere decir criar, quedó igual.
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

## Números, Deuteronomio y Josué

Lo mismo de arriba vale para estos tres libros. Además:

### La cronología sigue

La misma cronología bíblica tradicional, contando la salida de Egipto como el año 1 (1446 antes de Cristo):

| Hecho | Dato del texto | Antes de Cristo |
|---|---|---|
| Se levanta el tabernáculo | día 1 del mes 1, año 2 (Éxodo 40:17) | 1445 |
| Censo en el desierto de Sinaí | día 1 del mes 2, año 2 (Números 1:1) | 1445 |
| Israel sale del Sinaí | día 20 del mes 2, año 2 (Números 10:11) | 1445 |
| Los doce espías en Cades | en el segundo año; Caleb tiene 40 (Josué 14:7) | hacia 1445 |
| Treinta y ocho años de desierto | de Cades al arroyo Zered (Deuteronomio 2:14) | 1445 a 1407 |
| Muere Aarón en el monte Hor | 123 años; mes 5 del año 40 (Números 33:38 y 39) | 1407 |
| Discursos de Moisés en Moab | mes 11 del año 40 (Deuteronomio 1:3) | hacia 1406 |
| Muere Moisés | 120 años (Deuteronomio 34:7) | hacia 1406 |
| Israel cruza el Jordán | día 10 del mes 1 (Josué 4:19) | 1406 |
| Caleb pide Hebrón | 85 años, 45 después de Cades (Josué 14:10) | hacia 1400 |
| Muere Josué | 110 años (Josué 24:29); el texto no da el año | |

Las otras posturas se explican con calma en la introducción de Números y en la de Josué; después basta un recordatorio breve cuando importe. Para muchos historiadores, si la salida fue en el siglo trece antes de Cristo, la entrada en Canaán sería hacia fines de ese siglo; la estela de Merneptah (hacia 1208 antes de Cristo) es la primera mención de Israel fuera de la Biblia y lo nombra como un pueblo ya presente en Canaán.

### Datos externos que se pueden usar (con su fecha aproximada)

Solo si vienen al caso, y nunca más de lo que se sabe:
- Amuletos de plata de Ketef Hinnom, en Jerusalén (hacia 600 antes de Cristo): llevan una forma de la bendición de Números 6:24 a 26, el texto bíblico más antiguo que se conoce escrito.
- Inscripción de Deir Alla, en Jordania (hacia 800 antes de Cristo): habla de un vidente llamado Balaam hijo de Beor.
- Estela de Mesa, rey de Moab (hacia 840 antes de Cristo): cuenta que Mesa consagró una ciudad a su dios Quemos destruyéndola por completo; es el paralelo más claro, fuera de la Biblia, de la práctica que la RV1909 llama dar al anatema.
- Cartas de Amarna (hacia 1360 a 1330 antes de Cristo): cartas de reyes de Canaán al faraón que se quejan de grupos llamados habiru.
- Tratados hititas (siglos catorce y trece antes de Cristo) y tratados de sucesión de Asarhadón, rey de Asiria (672 antes de Cristo): muchos estudiosos comparan su forma (historia, cláusulas, testigos, bendiciones y maldiciones) con la de Deuteronomio. Unos ven más cerca los hititas y otros los asirios; dilo así.
- Segundo de Reyes 22: en tiempos del rey Josías (hacia 622 antes de Cristo) se encuentra en el templo un libro de la ley; muchos estudiosos piensan que era Deuteronomio o una parte de él, y la tradición lo atribuye a Moisés.
- Jericó (Tell es Sultan): John Garstang, en los años treinta, fechó la destrucción de la ciudad hacia 1400 antes de Cristo; Kathleen Kenyon, en los años cincuenta, la fechó hacia 1550 y no encontró una ciudad amurallada hacia 1400; Bryant Wood, en 1990, volvió a defender una fecha cercana a 1400. Sigue discutido: da las posturas sin decidir.
- Hai: se suele identificar con et Tell, que no parece habitado en la época de Josué; algunos proponen otro lugar, como Khirbet el Maqatir. Discutido.

### Los pasajes difíciles

Estos libros tienen guerras, ciudades destruidas por completo, castigos a muerte y leyes que hoy chocan (sobre esclavos, mujeres, extranjeros). Trátalos con la misma regla de siempre: describe qué dice el texto, qué significaban esas palabras y prácticas en su mundo (con paralelos reales, como la estela de Mesa), y cómo los han leído la tradición judía, la cristiana y los estudiosos (por ejemplo, quienes subrayan que Josué mismo dice que muchos cananeos siguieron viviendo en la tierra, o quienes leen esos relatos sobre todo como lenguaje de guerra de la época). No los suavices ni los condenes, no los justifiques ni los acuses: deja que el oyente piense. Una o dos preguntas abiertas al final de la pausa ayudan.

### Nombres y lugares

Mismas reglas de la grafía de 1909 (mira el texto con scripts/ver.py). Ubica los lugares con palabras sencillas y distancias aproximadas: el desierto de Parán y Cades Barnea, al sur de Canaán; el Arabá; los campos de Moab, al este del Jordán frente a Jericó; el monte Nebo; Gilgal; los montes Ebal y Gerizim junto a Siquem; Silo.

## Jueces y Rut

Lo mismo de arriba vale para estos dos libros. Además:

### La cronología sigue

La misma cronología bíblica tradicional: la salida de Egipto hacia 1446 antes de Cristo, 480 años antes del cuarto año de Salomón (1 Reyes 6:1), y la entrada en Canaán hacia 1406. Jueces no da una fecha seguida: da los años de cada opresión, de cada juez y de cada descanso, y sumados dan unos 410 años, más de los que caben entre la entrada en Canaán y el rey Saúl. Por eso la cuenta tradicional supone que varios jueces gobernaron al mismo tiempo en regiones distintas (Jueces 10:7 pone juntos a los Filisteos en el oeste y a los Ammonitas en el este). El dato que sirve de ancla es el de Jefté, que le dice al rey de Ammón que Israel lleva trescientos años en Hesbón (Jueces 11:26).

| Hecho | Dato del texto | Antes de Cristo |
|---|---|---|
| Israel cruza el Jordán | día 10 del mes 1 (Josué 4:19) | 1406 |
| Muere Josué | 110 años (Jueces 2:8); el texto no da el año | |
| Jefté y el rey de Ammón | Israel lleva 300 años en Hesbón, tomada antes de cruzar el Jordán (Jueces 11:26; Números 21:25) | hacia 1100 |
| Comienza a reinar Saúl | 40 años antes de David (Hechos 13:21) | hacia 1050 |
| David, rey en Hebrón | a los 30 años; reina 40 (2 Samuel 5:4) | 1010 |
| Rut, Booz y Obed | «en los días que gobernaban los jueces» (Rut 1:1); Booz es bisabuelo de David (Rut 4:21 y 22) | el texto no da el año |

En las pausas no pongas un año exacto para cada juez: basta "hacia" y de dónde sale (por ejemplo, "hacia 1100 antes de Cristo, según la cronología bíblica tradicional, por el dato de Jueces 11:26"). Para Rut: si David nació hacia 1040 (reinó desde los 30 años) y Booz es su bisabuelo, la historia cabría hacia el siglo 12 antes de Cristo; es una estimación y conviene decirlo. La genealogía de Rut 4:18 a 22 tiene pocas generaciones para tantos años (Nahasón vivió en tiempos de Moisés, Números 1:7, donde la de 1909 lo escribe Naasón), y muchos piensan que es selectiva, como otras genealogías bíblicas. La tradición judía atribuye Jueces y Rut a Samuel (Talmud, Bava Batra 14b) y el mismo Talmud identifica a Booz con Ibzan de Beth-lehem (Jueces 12:8; Bava Batra 91a).

Para muchos historiadores, el mundo de Jueces es la Edad del Hierro I (hacia 1200 a 1000 antes de Cristo): las ciudades cananeas de la Edad del Bronce Tardío han caído o decaído, Egipto se retira de Canaán hacia mediados del siglo 12, los filisteos se asientan en la costa y aparecen cientos de aldeas pequeñas en la serranía. Muchos piensan también que el libro se ordenó y se escribió siglos después, con un marco que se repite (el pueblo hace lo malo, llega un opresor, el pueblo clama, Dios levanta un libertador y la tierra reposa). Sobre Rut se discute más: unos lo fechan en tiempos de los reyes y otros después del exilio. En la Biblia hebrea, Rut está entre los Escritos y se lee en la fiesta de Shavuot (Pentecostés); en las Biblias cristianas, siguiendo la antigua traducción griega, va después de Jueces. Explica estas posturas con calma en la introducción de Jueces y en la de Rut; después basta un recordatorio breve.

### Datos externos que se pueden usar (con su fecha aproximada)

Solo si vienen al caso, y nunca más de lo que se sabe:
- Estela de Merneptah (hacia 1208 antes de Cristo): el faraón presume de victorias en Canaán (nombra Ascalón, Gezer y Yenoam) y dice que Israel fue arrasado; el signo que acompaña el nombre indica un pueblo, no una ciudad ni un país. Es la primera mención de Israel fuera de la Biblia y, para muchos historiadores, cae en la época de los jueces.
- Los Pueblos del Mar y la llegada de los filisteos: los relieves y las inscripciones del templo funerario de Ramsés tercero en Medinet Habu, en Tebas, cuentan batallas por tierra y por mar contra pueblos venidos del Mediterráneo, en el año 8 de su reinado (hacia 1177 antes de Cristo; la fecha cambia unos pocos años según la cronología egipcia). Entre ellos están los Peleset, que casi todos identifican con los filisteos. La Biblia los hace venir de Caphtor (Amós 9:7), que muchos identifican con Creta.
- Las ciudades filisteas: Gaza, Ascalón, Asdod, Ecrón y Gat (Josué 13:3, donde la de 1909 dice Accarón por Ecrón). Las excavaciones de Ascalón, Asdod, Ecrón (Tel Miqne) y Gat (Tell es Safi) muestran una cultura distinta de la de sus vecinos: cerámica de estilo egeo hecha en el lugar, hogares de tipo egeo y consumo de cerdo. Un estudio de ADN de restos humanos de Ascalón (publicado en 2019) encontró en los primeros filisteos, de comienzos de la Edad del Hierro, una parte de ascendencia del sur de Europa que se diluyó en pocas generaciones. En Tell Qasile, hoy dentro de Tel Aviv, hay un templo filisteo cuyo techo descansaba sobre dos columnas centrales de madera; se suele comparar con Jueces 16:29, sin que pruebe nada sobre Samsón.
- Las aldeas de la serranía (Hierro I, hacia 1200 a 1000 antes de Cristo): en la serranía central, donde ocurren casi todos los relatos de Jueces, aparecen en poco tiempo cientos de poblados pequeños sin murallas, con casas de pilares de varias habitaciones, silos, cisternas, terrazas de cultivo, tinajas grandes de borde con collar y casi sin huesos de cerdo. Muchos los relacionan con el Israel primitivo; de dónde venían sus habitantes se discute (de fuera, de las ciudades cananeas o de pastores que se asentaron). Ayuda a imaginar Jueces 5:7, aunque el sentido de la palabra hebrea que la de 1909 traduce "aldeas" se discute.
- Hazor (la de 1909 escribe Asor en Jueces 4:2 y 17, y Asor o Hasor en Josué 11): excavada por Yigael Yadin (1955 a 1958 y 1968 a 1969) y por Amnon Ben-Tor (desde 1990). La gran ciudad cananea de la Edad del Bronce Tardío fue destruida por un incendio en el siglo 13 antes de Cristo; quién la destruyó se discute (israelitas, egipcios, Pueblos del Mar o una revuelta interna). Josué 11 cuenta que Josué quemó Hazor y mató a su rey Jabín, y Jueces 4 presenta a otro Jabín que reina allí: unos piensan que Jabín era un nombre de la dinastía (los archivos de Mari, del siglo 18 antes de Cristo, nombran a un rey de Hazor llamado Ibni Adad, que algunos relacionan con Jabín), y algunos de quienes siguen la cronología tradicional relacionan el incendio del siglo 13 con Débora y Barac (Jueces 4:24) y no con Josué. Discutido.
- Silo (Khirbet Seilun), unos 30 kilómetros al norte de Jerusalén, donde estaba el tabernáculo (Josué 18:1; Jueces 18:31 y 21:19): excavaciones danesas (1926 a 1932), de Israel Finkelstein (1981 a 1984) y, desde 2017, de Scott Stripling. Finkelstein halló un poblado del Hierro I con edificios de pilares y muchas tinajas de almacén, destruido por un incendio en el siglo 11; muchos lo relacionan con la derrota de 1 Samuel 4 y con Jeremías 7:12, aunque la Biblia no cuenta cómo fue destruida Silo. Discutido.
- Dan, antes Lais (Jueces 18): Tel Dan, al pie del monte Hermón, junto a una de las fuentes del Jordán. Avraham Biran la excavó de 1966 a 1999: una ciudad del Bronce Medio con una puerta de ladrillo con arco (hacia el siglo 18 antes de Cristo) y encima el poblado del Hierro I. Allí apareció la estela de Tel Dan (hacia 840 antes de Cristo), en arameo, que nombra la "casa de David": la mención más antigua de David fuera de la Biblia; casi todos aceptan esa lectura y unos pocos la discuten. Sirve también para el final de Rut.
- Bet Semes de Judá (no la de Nephtalí de Jueces 1:33) y el valle de Sorec, la tierra de Samsón: Sora, Esthaol y Timnah, que se identifica con Tel Batash. En Bet Semes (excavaciones de Shlomo Bunimovitz y Zvi Lederman, desde 1990) la gente del Hierro I casi no comía cerdo, a diferencia de las ciudades filisteas cercanas: una frontera cultural justo donde Jueces pone a Samsón. Un sello de piedra del siglo 11 con una figura humana junto a un animal grande se presentó en 2012 como "sello de Samsón"; los propios excavadores dijeron que no prueba nada sobre él.
- El cántico de Débora (Jueces 5): muchos estudiosos lo cuentan entre las poesías hebreas más antiguas, junto con el cántico de Éxodo 15, por su hebreo arcaico, y varios lo fechan en el siglo 12 o 11 antes de Cristo, cerca de los hechos; otros lo creen más tardío. Nombra a diez grupos de Israel (alaba a unos y reprocha a otros) y no menciona a Judá ni a Simeón. Discutido.
- El levirato y el goel: Deuteronomio 25:5 a 10 manda que, si un hombre muere sin hijo, su hermano tome a la viuda para que el primogénito lleve el nombre del muerto, y si no quiere, ella le quita el zapato delante de los ancianos. Levítico 25:25 y 47 a 49 manda al pariente cercano (la de 1909 dice "el rescatador, su cercano") rescatar la tierra o la persona de su pariente empobrecido. Rut junta las dos cosas: Booz es "pariente cercano" y uno de "nuestros redentores" (Rut 2:20; 3:9 y 12; 4:1 a 10), aunque no es cuñado de Rut, y Rut 4:7 explica la costumbre del zapato como algo antiguo que se hace de otra manera que en Deuteronomio. Cómo se relacionan exactamente estas costumbres se discute. Ayuda Génesis 38 (Thamar y Judá), que Rut 4:12 recuerda.
- Rut moabita: Deuteronomio 23:3 prohíbe que el Moabita entre en la congregación de Jehová; la Mishná (Yevamot 8:3) entiende que la prohibición es para los varones y no para las mujeres, y así explica la tradición judía el caso de Rut. Mateo 1:5 pone a Booz y a Rut en la genealogía de Jesús.

### Los pasajes difíciles

Jueces tiene algunas de las escenas más duras de la Biblia. La regla es la de siempre: describe lo que dice el texto sin suavizarlo, explica el mundo en que ocurre, da las lecturas de la tradición judía, la cristiana y los estudiosos, y no impongas una conclusión. Ayuda notar que el mismo libro juzga su época con el estribillo "En estos días no había rey en Israel: cada uno hacía lo recto delante de sus ojos" (21:25; ver 17:6), pero no lo uses para cerrar la discusión.

La hija de Jefté (11:29 a 40). Jefté promete: "Cualquiera que me saliere á recibir de las puertas de mi casa, cuando volviere de los Ammonitas en paz, será de Jehová, y le ofreceré en holocausto", y sale su única hija. El texto dice que "hizo de ella conforme á su voto" y que "ella nunca conoció varón" (11:39). Hay dos lecturas principales. Una entiende que la sacrificó: así lo leen Josefo (siglo 1 después de Cristo), muchos rabinos, que condenan el voto (algunos midrashim dicen que pudo anularse y que el orgullo de Jefté y del sacerdote Phinees lo impidió), y muchos padres de la Iglesia. La otra entiende que la consagró a Dios y vivió sin casarse: la proponen comentaristas judíos medievales como David Kimhi, que leen "será de Jehová, ó le ofreceré en holocausto", y la siguen muchos lectores cristianos, que señalan que ella llora "su virginidad" y no su muerte. Los estudiosos recuerdan que la ley prohíbe sacrificar hijos (Levítico 18:21; Deuteronomio 12:31 y 18:10) y comparan con 2 Reyes 3:27; notan que Dios no habla en la escena, y algunos (Phyllis Trible, en 1984) la leen entre los "textos de terror" sobre mujeres. Hebreos 11:32 nombra a Jefté entre los que obraron por la fe.

Los capítulos 19 a 21. Un Levita va a buscar a su concubina; en Gabaa, los hombres de la ciudad rodean la casa como en Sodoma (Génesis 19), el dueño ofrece a su hija y a la concubina, el Levita entrega a la mujer, abusan de ella toda la noche y al amanecer está caída en la puerta; él la corta en doce pedazos y los envía por todo Israel. Sigue una guerra civil en la que Benjamín casi desaparece (quedan seiscientos hombres), la destrucción de Jabes-galaad, de donde toman cuatrocientas doncellas, y el rapto de las hijas de Silo. El texto lo llama maldad ("Jamás se ha hecho ni visto tal cosa", 19:30; "¿Qué maldad es ésta...?", 20:12), y Oseas 9:9 y 10:9 recuerdan "los días de Gabaa". Lecturas: muchos judíos y cristianos ven aquí lo que pasa cuando no hay ley ni guía, no algo aprobado; los estudiosos notan el paralelo con Sodoma, que Gabaa y Jabes-galaad vuelven a aparecer con Saúl (1 Samuel 10:26 y 11), por lo que muchos leen también estos capítulos como favorables a la monarquía de David frente a la de Saúl, y las lecturas feministas ponen en el centro a la mujer sin nombre. Que todavía sea sacerdote Phinees, nieto de Aarón (20:28), hace pensar a la tradición judía y a muchos estudiosos que estos hechos ocurrieron al principio del período, aunque se cuentan al final.

La violencia de Samsón (capítulos 13 a 16). Es Nazareo desde el vientre (13:5; Números 6), pero toca el cadáver del león, hace banquete, mata a treinta hombres de Ascalón para pagar una apuesta (14:19), quema los sembrados con zorras (15:4 y 5), mata a mil con una quijada (15:15), va con una ramera en Gaza (16:1) y muere derribando el templo de Dagón sobre unos tres mil (16:27 a 30) después de pedir venganza "por mis dos ojos" (16:28). A la vez, el texto dice que "esto venía de Jehová" (14:4) y que el espíritu de Jehová venía sobre él (14:6 y 19; 15:14). La Mishná (Sotá 1:8) dice que Samsón fue tras sus ojos y por eso los Filisteos le sacaron los ojos; Hebreos 11:32 lo nombra entre los que obraron por la fe, y Agustín (La ciudad de Dios, libro 1) sostiene que su muerte no fue un suicidio culpable porque se lo mandó el Espíritu; muchos padres vieron en él una figura de Cristo. Los estudiosos notan rasgos de relato de héroe popular (adivinanzas, fuerza, la mujer que traiciona), la cadena de venganzas y el nombre Samsón, parecido a la palabra hebrea para "sol", con Bet Semes muy cerca. No lo excuses ni lo condenes: deja que el oyente piense.

### Nombres y lugares

Mismas reglas de la grafía de 1909 (mira el texto con scripts/ver.py). El libro se llama Rut, pero en el texto de 1909 la persona es Ruth. Las formas que más aparecen y su forma actual: Othoniel es Otoniel; Aod es Aod (en otras lenguas, Ehud); Débora, Barac, Jael, Sísara y Jabín quedan igual; Gedeón también se llama Jerobaal; Abimelech es Abimelec; Jephté es Jefté; Samsón es Sansón; Manoa queda igual; Dalila queda igual; Michâs es Micaías; Phinees es Finees; Chêmos es Quemos, el dios de Moab; Dagón, el dios de los filisteos; los Baales y Astaroth son Baal y Astarté. En Rut: Noemi es Noemí (la de 1909 la escribe sin tilde), Orpha es Orfa, Elimelech es Elimelec, Mahalón y Chelión son Mahlón y Quelión, Booz queda igual, Obed queda igual, Isaí es Isaí (en otras lenguas, Jesé) y Phares es Fares. La de 1909 escribe Ibzan sin tilde (12:8 y 10), Samgar "hijo de Anat" en 3:31 y "hijo de Anath" en 5:6, Taanach en 1:27 y Taanac en 5:19 (la misma ciudad), y "Shiboleth" y "Siboleth" en 12:6.

Lugares, con palabras sencillas y distancias aproximadas: Chîriath-arba es Quiriat-arba, el nombre antiguo de Hebrón; Chîriath-sepher es Quiriat-séfer, o Debir; Chîriath-jearim es Quiriat-jearim; Bochîm es Boquim, "los que lloran"; Sichêm es Siquem, entre los montes Ebal y Gerizim; Gabaa es Guibeá, que se suele identificar con Tell el Ful, unos 5 kilómetros al norte de Jerusalén; Jebus es Jerusalén; Lais es la ciudad que después se llamó Dan, en el extremo norte; Silo, unos 30 kilómetros al norte de Jerusalén; Mizpa (hay una en Galaad y otra en Benjamín); Jabes-galaad, al este del Jordán; Beth-lehem de Judá es Belén, unos 8 kilómetros al sur de Jerusalén, y Ephrata es otro nombre de su región; Sora, Esthaol y Timnah son Zora, Estaol y Timna, en el valle de Sorec, que baja de la serranía hacia la costa filistea; Samsón lleva las puertas de Gaza hasta "la cumbre del monte que está delante de Hebrón" (16:3), unos 60 kilómetros cuesta arriba; el arroyo de Cisón es el Quisón, que corre por el valle de Jezreel; Haroseth de las Gentes, el monte Tabor, Megiddo (Meguido) y Asor, que es Hazor, al norte del mar de Galilea.

Palabras: "el bosque" de Jueces 6:25 a 30 es la Asera, un poste o árbol sagrado de la diosa Asera junto al altar de Baal; "ephod" y "teraphim" son una vestidura sagrada y figurillas de dioses de la casa (Jueces 8:27 y 17 y 18); "Nazareo" es el consagrado a Dios de Números 6; "adufes" son panderos; "aquilón" es el norte y "mediodía" el sur; "los orientales" son los hijos del oriente, nómadas del desierto; "Cineo" es ceneo, el clan del suegro de Moisés; en Rut, "pariente cercano", "redentores" y "redimir" traducen la palabra hebrea goel y su verbo; "extender el borde de la capa" (Rut 3:9) es pedir matrimonio y protección; Noemi quiere decir "placentera" y Mara "amarga" (Rut 1:20). En Jueces 18:30 la de 1909 dice "Jonathán, hijo de Gersón, hijo de Manasés": en el texto hebreo la letra que convierte Moisés en Manasés está escrita en alto, y el Talmud (Bava Batra 109b) explica que se puso para no avergonzar a Moisés; muchos estudiosos piensan que el texto original decía Moisés.
