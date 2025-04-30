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

- **classes** `list[str]`:<br>Todas las clases (organizadas alfa) que pueden aprender el conjuro. Ej.: ["Clérigo", "Bardo", "Brujo"]
- **componentes** `list[str]`:<br>Los componentes necesarios para lanzar el conjuro. "V" = verbal, "C" = componente, "S" = somático.
- **tiempo_de_lanzamiento** `str`:<br>El tiempo requerido para lanzar el conjuro.
- **alcance** `str`:<br>Información sobre a qué objetivos puede afectar el conjuro.
- **duracion** `str`:<br>El tiempo que el efecto del conjuro se mantiene activo.
- **tirada_de_salvacion** `str | None`:<br>Atributo requerido para la tirada de salvación contra el conjuro. Toma el valor de `null` si no requiere ninguna tirada.
- **requiere_ataque** `bool`:<br>Flag indicando si el personaje que lanza el conjuro requiere una tirada de ataque.
- **danyo** `dict | None`:<br>Información sobre el daño producido. Toma el valor de `null` si el conjuro no realiza ningún daño.
    - **tipo** `str`:<br>Tipo de daño producido. Ej.: "Fuego", "Radiante", etc.
    - **base** `str`:<br>Daño producido a nivel base del conjuro. El daño está definido con notación de dado. Por ejemplo, "1d8" corresponde a una tirada de un dado de ocho caras.
    - **tipo** `dict[str, str]`:<br>Información sobre el daño producido en niveles superiores (solo si es aplicable).
- **descripcion** `str`:<br> Descripción completa del conjuro.

## Contribución

Cualquiera puede contribuir añadiendo nuevos conjuros, siempre que sean conjuros de las reglas básicas.
Para cotribuir, sigue las siguientes reglas:

1. Asegurate de que el conjuro que quieres añadir no se encuentra ya en [`spells/index.md`](spells/index.md) ni en ningún _pull request_ abierto.
2. Crea un nuevo _pull request_ con el nombre `{Conjuro} - N{nivel}`. Por ejemplo: `Abrir N2`. Aquí debería encontrarse únicamente el conjuro a añadir.
3. Asegurate de rellenar los campos correctamente, manteniendo la descripción con el texto exacto del manual.
4. Añade el nombre del conjuto en [`spells/index.md`](spells/index.md) en su posición alfabética correcta.

> Se cambiarán los permisos del repositorio únicamente a modo lectura cuando todos los conjuros se hayan añadido.
