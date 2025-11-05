# DnD Conjuros (5° edición)

Base de datos NoSQL de los conjuros de _Dungeons and Dragons_ (reglas básicas).

Todos los hechizos contenidos en este proyecto pertenecen a _Wizards of the Coast_ bajo licencia **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
Aquellos conjuros que no se encuentran en el archivo [SRD v5.2](https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.pdf) han sido adaptados.

> Nota:
> La extracción de los datos se ha hecho con IA, aunque se han revisado manualmente.
> Puesto que hay errores que se me pueden escapar, por favor cread tickets si encontráis algún error.

## Estructura

Los conjuros están registrados en archivos `spells/ed/level_N.json`, donde `ed` corresponde a la edición (5.0 ó 5.5) y `N` es el nivel del propio conjuro.
En la carpeta también hay un archivo `all.json` (generado automáticamente) conteniendo todos conjuros de la edición.
Los conjuros están organizados en un diccionario organizado por el nombre.

En todas las entradas se han utilizado las siguientes reglas evitando caracteres españoles especiales:
 - Las tildes se han omitido. Ej.: duración -> duracion.
 - Los espacios han sido reemplazados por `_`.

Cada conjuro contiene las siguientes entradas:

- **nombre** `str`:<br>Nombre del conjuro.
- **clases** `list[str]`:<br>Todas las clases (organizadas alfabéticamente) que pueden aprender el conjuro. Ej.: ["Clérigo", "Bardo", "Brujo"]
- **escuela** `str`:<br>Escuela del conjuro. Ej.: "Transmutación", "Evocación", "Conjuración".
- **tiempo_de_lanzamiento** `str`:<br>El tiempo requerido para lanzar el conjuro.
- **ritual** `bool`:<br>Flag indicando si el conjuro puede ser lanzado como un ritual.
- **alcance** `str | list[str]`:<br>Información sobre a qué objetivos puede afectar el conjuro. Las distancias se almacenan en pies y metros. Ej.: ["60 pies", "18 m"]
- **visible** `bool`:<br>Flag indicando si el objetivo ha de estar a la vista del lanzador.
- **componentes** `list[str]`:<br>Los componentes necesarios para lanzar el conjuro. "V" = verbal, "S" = somático, "M" = material.
- **concentracion** `bool`:<br>Flag indicando si el conjuro requiere que el lanzador mantenga su concentración durante la duración del mismo.
- **duracion** `str`:<br>El tiempo que el efecto del conjuro se mantiene activo.
- **tirada_de_salvacion** `str | None`:<br>Atributo requerido para la tirada de salvación contra el conjuro. Toma el valor de `null` si no requiere ninguna tirada.
- **requiere_ataque** `bool`:<br>Flag indicando si el personaje que lanza el conjuro requiere una tirada de ataque.
- **descripcion** `str | list[str]`:<br> Descripción completa del conjuro en texto enriquecido. En caso de haber unidades en la descripción, esta se encuentra duplicada mostrando en la primera descripción todas las unidades en el sistema imperial y en la segunda, todas en el sistema métrico.
- **materiales** `str | None`:<br>Descripción de los materiales necesarios, en caso de que el conjuro requiera de componentes materiales.

### Ejemplos

- **Abrir**: Conjuro de nivel 2 sin daño ni materiales.
- **Agarre electrizante**: Conjuro de nivel 0 (Truco).
- **Alarma**: Conjuro de nivel 1 que requiere componentes.

```json
[
  {
    "nombre": "Abrir",
    "clases": [
      "Bardo",
      "Hechicero",
      "Mago"
    ],
    "escuela": "Transmutación",
    "tiempo_de_lanzamiento": "Acción",
    "ritual": false,
    "alcance": [
      "60 pies",
      "18 m"
    ],
    "visible": true,
    "componentes": [
      "V"
    ],
    "concentracion": false,
    "duracion": "Instantáneo",
    "tirada_de_salvacion": null,
    "requiere_ataque": false,
    "descripcion": [
      "Elige un objeto que puedas ver dentro del alcance. Este puede ser una puerta, una caja, un cofre, unas esposas, un candado o cualquier otro objeto que posea alguna manera, mágica o mundana, de impedir el acceso.<br>Un objetivo que esté cerrado mediante una cerradura normal o que esté atascado o atrancado se abre, desatasca o desatranca. Si el objeto tiene varios cerrojos, solo se desbloquea uno de ellos.<br>Si el objetivo está cerrado mediante <i>cerradura arcana</i>, ese conjuro quedará anulado durante 33 minutos y, durante ese tiempo, el objeto se podrá abrir y cerrar.<br>Cuando lanzas el conjuro, se escucha un fuerte golpe surgir del objetivo, que es audible a una distance de 300 pies .",
      "Elige un objeto que puedas ver dentro del alcance. Este puede ser una puerta, una caja, un cofre, unas esposas, un candado o cualquier otro objeto que posea alguna manera, mágica o mundana, de impedir el acceso.<br>Un objetivo que esté cerrado mediante una cerradura normal o que esté atascado o atrancado se abre, desatasca o desatranca. Si el objeto tiene varios cerrojos, solo se desbloquea uno de ellos.<br>Si el objetivo está cerrado mediante <i>cerradura arcana</i>, ese conjuro quedará anulado durante 10 minutos y, durante ese tiempo, el objeto se podrá abrir y cerrar.<br>Cuando lanzas el conjuro, se escucha un fuerte golpe surgir del objetivo, que es audible a una distance de 90 m ."
    ],
    "materiales": null,
    "nivel": 2
  },
  {
    "nombre": "Agarre electrizante",
    "clases": [
      "Hechicero",
      "Mago"
    ],
    "escuela": "Evocación",
    "tiempo_de_lanzamiento": "Acción",
    "ritual": false,
    "alcance": "Toque",
    "visible": false,
    "componentes": [
      "V",
      "S"
    ],
    "concentracion": false,
    "duracion": "Instantáneo",
    "tirada_de_salvacion": null,
    "requiere_ataque": true,
    "descripcion": "Una descarga eléctrica surge de tu mano hacia una criatura que intentas tocar. Haz un ataque de conjuro cuerpo a cuerpo contra el objetivo. Si acierta, el objetivo recibirá 1d8 de daño de relámpago y no podrá realizar ataques de oportunidad hasta el principio de su siguiente turno.<br><i><b>Mejora de truco.</b></i> El daño aumenta en 1d8 cuando alcanzas los niveles 5 (2d8), 11 (3d8) y 17 (4d8).",
    "materiales": null,
    "nivel": 0
  },
  {
    "nombre": "Alarma",
    "clases": [
      "Explorador",
      "Mago"
    ],
    "escuela": "Abjuración",
    "tiempo_de_lanzamiento": "1 minuto",
    "ritual": true,
    "alcance": [
      "30 pies",
      "9 m"
    ],
    "visible": false,
    "componentes": [
      "V",
      "S",
      "M"
    ],
    "concentracion": false,
    "duracion": "8 horas",
    "tirada_de_salvacion": null,
    "requiere_ataque": false,
    "descripcion": [
      "Preparas una alarma contra los intrusos. Elige una puerta, una ventana o una zona dentro del alcance que no sea mayor que un cubo de 20 pies  de lado. Hasta que el conjuro termine, una alarma te alertará siempre que una criatura toque la zona vigilada o entre en ella. Al lanzar el conjuro, puedes designar qué criaturas no activarán la alarma, que puede ser mental o sonora.<br><b>Alarma mental.</b> La alarma te avisará con un sonido dentro de tu mente si estás a 1 milla o menos de la zona vigilada. Si estás dormido, te despertará.<br><b>Alarma sonora.</b> La alarma producirá el sonido de una campanilla durante 10 segundos, que será audible a 60 pies  o menos de la zona vigilada.",
      "Preparas una alarma contra los intrusos. Elige una puerta, una ventana o una zona dentro del alcance que no sea mayor que un cubo de 6 m  de lado. Hasta que el conjuro termine, una alarma te alertará siempre que una criatura toque la zona vigilada o entre en ella. Al lanzar el conjuro, puedes designar qué criaturas no activarán la alarma, que puede ser mental o sonora.<br><b>Alarma mental.</b> La alarma te avisará con un sonido dentro de tu mente si estás a 1.5 km o menos de la zona vigilada. Si estás dormido, te despertará.<br><b>Alarma sonora.</b> La alarma producirá el sonido de una campanilla durante 10 segundos, que será audible a 18 m  o menos de la zona vigilada."
    ],
    "materiales": "Una campana de hilo de plata.",
    "nivel": 1
  }
]
```

> Nota:
> Este ejemplo ha sido preparado para una lectura fácil.
> No obstante, el texto original dentro de cada archivo JSON contiene la secuencia codificada en utf-8 para todos los caracteres especiales.
> Por ejemplo, el conjuro `"Adivinación"` está representado como `"Adivinaci\u00f3n"`
