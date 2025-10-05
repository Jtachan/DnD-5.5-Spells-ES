# Contributing Guidelines

¡Gracias por interesarte en este proyecto!
Toda contribución siempre es agradecida, ya sea para solventar errores o para mejorar la interfaz.

La extracción de datos para esta base de datos ha sido posible gracias a la IA.
Por eso mismo, es posible que haya errores o que ciertos aspectos puedan mejorarse.

## 📌 Cómo Contribuir

### 1. Identifica el problema

- Asegúrate de que tu problema no se encuentra documentado en ningún ticket ya abierto. En este caso, crea un ticket nuevo.
- Elige un título representativo y describe el cambio a introducir lo mejor posible.

> Ten en cuenta de que algunos tickets pueden ser separados en sub-tickets para facilitar la creación de pull requests.

### 2. Crea un nuevo PR

- Si quieres activamente introducir un cambio definido en un ticket ya creado, crea una PR referenciada al ticket.
- El PR ha de ser integrado en '**develop**'.
- Si el cambio afecta a un solo hechizo, nombra la PR como `Nombre del conjuro - N{x}`, siendo `x` el nivel del conjuro y usando `N0` para los trucos.
- Asocia tu PR con el ticket correct.

### 3. Trabaja en los cambios

- Aplica los cambios necesarios sobre los archivos de la carpeta [`spells/`](spells) o en el archivo ['index.html'](index.html).
- Asegúrate de tener los cambios del último commit en 'master'.
- Usa el script [`normalize_spell_files.py`](spells/normalize_spell_files.py) antes de poner los cambios para revisar.

### 4. Merging & releasing

Una vez la PR se encuentre con los cambios necesarios, los revisaré y los integraré.
Es posible que algunos cambios requieran de una discusión antes de que sean integrados.

Todo cambio nuevo introducido en 'main' será publicado automáticamente en la página, aunque es posible que sea necesario esperar un tiempo para ver los nuevos cambios.