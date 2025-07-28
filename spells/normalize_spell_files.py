"""Script with functions to normalize all spells though all the files.

The functions shown here should be run only to normalize the data among
the 'level_X.json' files.

"""

import re
import json
import os


def norm_materiales(text: str) -> str:
    """Normalizing the field 'materiales' (capitalizing + full stop).

    Required field: 'materiales'.
    """
    text = text.capitalize()
    if not text.endswith("."):
        text += "."
    return text


def norm_new_lines(text: str) -> str:
    """Ensuring each new-line jump is actually double within the description.

    Required field: 'descripcion'.
    """
    pattern = r"(?<!<br>)<br>(?!<br>)"
    return re.sub(pattern, "<br><br>", text)


def fix_concentration_duration_text(text: str) -> str:
    """Removing 'Concentracion' at the beginning of those that require it.

    Required field: 'duracion'.
    """
    return text.lstrip("Concentración, ").capitalize()


def norm_action(text: str) -> str:
    """Normalizing the specified action of the spell.

    Required field: 'tiempo_de_lanzamiento'.
    """
    text = text.replace("1 acción", "Acción")
    if text.endswith(("o ritual", "o un ritual", "o 1 ritual")):
        text = text.split(" o ")[0]
    return text


def norm_higher_level(text: str) -> str:
    """Checking the enphasis is correct"""
    higher_level_texts = [
        "Mejora de truco",
        "En niveles superiores",
        "Con un espacio de conjuro de nivel superior",
    ]
    for hlt in higher_level_texts:
        pattern = fr"<br>((?=<(i|b)>)?<(i|b)>){hlt}.((?=<\/(i|b)>)?<\/(i|b)>)"
        final_text = f"<br><b><i>{hlt}</i></b>"
        text = re.sub(pattern, final_text, text)
    return text


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    for idx in range(10):
        file_name = f"level_{idx}.json"
        # Loading all spells:
        with open(file_name, "r", encoding="utf-8") as fh:
            spells = json.load(fh)

        # Performing all corrections (one per spell):
        for spell in spells:
            spell["descripcion"] = norm_new_lines(spell["descripcion"])
            spell["descripcion"] = norm_higher_level(spell["descripcion"])

            if spell["materiales"]:
                spell["materiales"] = norm_materiales(spell["materiales"])

            if spell["concentracion"]:
                spell["duracion"] = fix_concentration_duration_text(spell["duracion"])

            spell["tiempo_de_lanzamiento"] = norm_action(spell["tiempo_de_lanzamiento"])

        # Overriding the data in the file:
        # Warning, this will update all spanish special characters to unicode.
        #  for example 'ó' -> '\u00f3'.
        with open(file_name, "w", encoding="utf-8") as fh:
            json.dump(spells, fh, indent=2)
