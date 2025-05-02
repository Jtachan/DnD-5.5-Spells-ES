# DnD Conjuros (5 edición)

Base de datos NoSQL de los conjuros de _Dungeons and Dragons_ (reglas básicas).

> ℹ️ Nota:
> En todas las entradas se han utilizado las siguientes reglas evitando caracteres españoles especiales:
> - Las tildes se han omitido. Ej.: duración -> duracion.
> - El caracter 'ñ' se ha subtituido por 'ny'. Ej.: daño -> danyo.

## Index

Para la búsqueda rápida de un conjuro, el archivo [`spells/index.md`](spells/index.md) contiene todos los conjuros registrados indicando su nivel correspondiente.

## Estructura

Los conjuros está registrados en archivos `spells/level_N.json`, donde N es el nivel del propio conjuro.
Dentro del archivo, los conjuros están organizados en un diccionario organizados por el nombre (en minúsculas).
Cada conjuro contiene las siguientes entradas:

- **clases** `list[str]`:<br>Todas las clases (organizadas alfa) que pueden aprender el conjuro. Ej.: ["Clérigo", "Bardo", "Brujo"]
- **escuela** `str`:<br>Escuela del conjuro. Ej.: "Transmutación", "Evocación", "Conjuración".
- **tiempo_de_lanzamiento** `str`:<br>El tiempo requerido para lanzar el conjuro.
- **ritual** `bool`:<br>Flag indicando si el conjuro puede ser lanzado como un ritual.
- **alcance** `str`:<br>Información sobre a qué objetivos puede afectar el conjuro.
- **visible** `bool`:<br>Flag indicando si el objetivo ha de estar a la vista del lanzador.
- **componentes** `list[str]`:<br>Los componentes necesarios para lanzar el conjuro. "V" = verbal, "S" = somático, "M" = material. Los componentes materiales viene explicados entre paréntesis.
- **concentracion** `bool`:<br>Flag indicando si el conjuro requiere que el lanzador mantenga su concentración durante la duración del mismo.
- **duracion** `str`:<br>El tiempo que el efecto del conjuro se mantiene activo.
- **tirada_de_salvacion** `str | None`:<br>Atributo requerido para la tirada de salvación contra el conjuro. Toma el valor de `null` si no requiere ninguna tirada.
- **requiere_ataque** `bool`:<br>Flag indicando si el personaje que lanza el conjuro requiere una tirada de ataque.
- **danyo** `dict | None`:<br>Información sobre el daño producido. Toma el valor de `null` si el conjuro no realiza ningún daño.
    - **tipo** `str`:<br>Tipo de daño producido. Ej.: "Fuego", "Radiante", etc.
    - **base** `str`:<br>Daño producido a nivel base del conjuro. El daño está definido con notación de dado. Por ejemplo, "1d8" corresponde a una tirada de un dado de ocho caras.
    - **escala** `dict[str, str]`:<br>Información sobre el daño producido en niveles superiores (solo si es aplicable).
- **descripcion** `str`:<br> Descripción completa del conjuro en texto enriquecido.

### Ejemplos

```json
{
  // Conjuro de nivel 2 sin daño ni materiales:
  "abrir": {
    "clases": [
      "Bardo",
      "Hechizero",
      "Mago"
    ],
    "escuela": "Transmutación",
    "tiempo_de_lanzamiento": "1 acción",
    "ritual": false,
    "alcance": "60 pies",
    "visible": true,
    "componentes": [
      "V"
    ],
    "concentracion": false,
    "duracion": "Instantáneo",
    "tirada_de_salvacion": null,
    "requiere_ataque": false,
    "danyo": null,
    "descripcion": "Elige un objeto que puedas ver dentro del alcance. Este puede ser una puerta, una caja, un cofre, unas esposas, un candado o cualquier otro objeto que posea alguna manera, mágica o mundana, de impedir el acceso.<br>Un objetivo que esté cerrado mediante una cerradura normal o que esté atascado o atrancado se abre, desatasca o desatranca. Si el objeto tenía varios cerrojos, solo se desbloquea uno de ellos.<br>Si eliges un objetivo que está cerrado mediante <i>cerradura arcana</i>, este conjuro queda anulado durante 10 minutos, y durante este tiempo el objeto se puede abrir y cerrar con normalidad.<br>Cuando lanzas este conjuro, un fuerte golpe suena desde el objeto, audible desde 300 pies de distancia."
  },
  // Conjuro de nivel 0 con daño escalable:
  "agarre_electrizante": {
    "clases": [
      "Hechizero",
      "Mago"
    ],
    "escuela": "Evocación",
    "tiempo_de_lanzamiento": "1 acción",
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
    "danyo": {
      "tipo": "Relámpago",
      "base": "1d8",
      "escala": {
        "nivel_5": "2d8",
        "nivel_11": "3d8",
        "nivel_17": "4d8"
      }
    },
    "descripcion": "Un relámpago salta de tu mano para dar una descarga eléctrica a la criatura que intentas tocar. Haz un ataque de conjuro cuerpo a cuerpo contra el objetivo. Tienes ventaja en la tirada de ataque si la criatura lleva armadura de metal. Si impactas, el objetivo sufre 1d8 de daño de relámpago y no podrá llevar a cabo reacciones hasta el comienzo de su próximo turno."
  },
  // Conjuro de nivel 1 con componentes:
  "alarma": {
    "clases": [
      "Explorador",
      "Mago"
    ],
    "escuela": "Abjuración",
    "tiempo_de_lanzamiento": "1 minuto",
    "ritual": true,
    "alcance": "30 pies",
    "visible": false,
    "componentes": [
      "V",
      "S",
      "M (una pequeña campana y un hilo de plata fina)"
    ],
    "concentracion": false,
    "duracion": "8 horas",
    "tirada_de_salvacion": null,
    "requiere_ataque": false,
    "danyo": null,
    "descripcion": "Preparas una alarma contra intrusos. Elige una puerta, ventana o cualquier otra área dentro del alcance cuyo volumen sea menor o igual que un cubo de 20 pies de lado. Una alarma te avisará siempre que una criatura, Diminuta o de tamaño superior, toque o entre en la zona vigilada antes del final del conjuro. Al lanzarlo puedes elegir que ciertas criaturas no activarán la alarma, que puede ser mental o sonora.<br>Una alarma mental te alerta con un sonido dentro de tu mente si estás a 1 milla de la zona vigilada. Si estás dormido, te despertará.<br>Una alarma sonora produce un sonido de campanilla durante 10 segundos audible a 60 pies de distancia."
  }
}
```

## Contribución

Cualquiera puede contribuir añadiendo nuevos conjuros, siempre que sean conjuros de las reglas básicas.
Para cotribuir, sigue las siguientes reglas:

1. Asegurate de que el conjuro que quieres añadir no se encuentra ya en [`spells/index.md`](spells/index.md) ni en ningún _pull request_ abierto.
2. Crea un nuevo _pull request_ con el nombre `{Conjuro} - N{nivel}`. Por ejemplo: `Abrir N2`. Aquí debería encontrarse únicamente el conjuro a añadir.
3. Asegurate de rellenar los campos correctamente, manteniendo la descripción con el texto exacto del manual.
4. Añade el nombre del conjuto en [`spells/index.md`](spells/index.md) en su posición alfabética correcta.

> Se cambiarán los permisos del repositorio únicamente a modo lectura cuando todos los conjuros se hayan añadido.
