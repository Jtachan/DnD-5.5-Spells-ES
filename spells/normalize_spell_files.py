"""Script with functions to normalize all spells though all the files.

The functions shown here should be run only to normalize the data among
the 'level_X.json' files.
"""

import re
import json
import os

METRIC_DISTANCE_REGEX = r"((\d+,)?\d+) ([kmc]?m|kg|l)[\s.]"


# ------ Field: 'descripcion' ------ #
def _norm_new_lines(text: str) -> str:
    """Ensuring each new-line jump is actually double within the description."""
    pattern = r"(?<!<br>)<br>(?!<br>)"
    return re.sub(pattern, "<br><br>", text)


def _norm_higher_level(text: str) -> str:
    """Checking the emphasis is correct."""
    higher_level_texts = [
        "Mejora de truco",
        "En niveles superiores",
        "Con un espacio de conjuro de nivel superior",
    ]
    for hlt in higher_level_texts:
        pattern = rf"<br>((?=<(i|b)>)?<(i|b)>){hlt}.((?=<\/(i|b)>)?<\/(i|b)>)"
        final_text = f"<br><b><i>{hlt}.</i></b>"
        text = re.sub(pattern, final_text, text)
    return text


def normalizar_descripcion(text: str | list) -> str:
    """Main function to normalize the spell description."""
    if isinstance(text, str):
        text = _norm_new_lines(_norm_higher_level(text))
    else:
        text = [_norm_new_lines(_norm_higher_level(t)) for t in text]
    return text


def expand_units_to_imperial(text: str) -> list[str]:
    """Converting a description with the metric system into a list with imperial and metric.
    This conversion consider only 'meters' -> 'feet'. Thus, all those other SI values (centimeters, kilograms, etc)
    are not converted.
    """
    def meters_to_feet(re_match: re.Match) -> str:
        meters = float(re_match.group(1).replace(",", "."))
        feet = int(meters * 5 / 1.5)
        return f"{feet} pies"

    def cm_to_inches(re_match: re.Match) -> str:
        centimeters = float(re_match.group(1).replace(",", "."))
        inches = int(centimeters / 2.5)
        return f"{inches} pulgada" if inches == 1 else f"{inches} pulgadas"

    def km_to_miles(re_match: re.Match) -> str:
        kilometers = float(re_match.group(1).replace(",", "."))
        miles = int(kilometers / 1.5)
        return f"{miles} millas" if miles > 1 else f"{miles} milla"

    def kg_to_pounds(re_match: re.Match) -> str:
        kilograms = float(re_match.group(1).replace(",", "."))
        pounds = int(kilograms * 2)
        return f"{pounds} lb"

    def liters_to_gallons(re_match: re.Match) -> str:
        liters = float(re_match.group(1).replace(",", "."))
        gallons = int(liters / 4)
        return f"{gallons} galón" if gallons == 1 else f"{gallons} galones"

    imperial_text = re.sub(r"((\d+,)?\d+) m", meters_to_feet, text)
    imperial_text = re.sub(r"((\d+,)?\d+) cm", cm_to_inches, imperial_text)
    imperial_text = re.sub(r"((\d+,)?\d+) km", km_to_miles, imperial_text)
    imperial_text = re.sub(r"((\d+,)?\d+) kg", kg_to_pounds, imperial_text)
    imperial_text = re.sub(r"((\d+,)?\d+) l", liters_to_gallons, imperial_text)

    return [imperial_text, text]


# ------ Field: 'materiales' ------ #
def normalizar_materiales(text: str) -> str:
    """Normalizing the field 'materiales' (capitalizing + full stop)."""
    text = text.lstrip("(").rstrip(")").capitalize()
    if not text.endswith("."):
        text += "."
    return text


# ------ Field: 'duracion' ------ #
def fix_concentration_duration_text(text: str) -> str:
    """Removing 'Concentracion' at the beginning of those that require it."""
    return text.lstrip("Concentración, ").capitalize()


# ------ Field: 'tiempo_de_lanzamiento' ------ #
def normalizar_tiempo_de_lanzamiento(text: str) -> str:
    """Normalizing the specified action of the spell."""
    text = text.replace("1 acción", "Acción")
    if text.endswith(("o ritual", "o un ritual", "o 1 ritual")):
        text = text.split(" o ")[0]
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
            if isinstance(spell["descripcion"], str) and re.search(METRIC_DISTANCE_REGEX, spell["descripcion"]):
                spell["descripcion"] = expand_units_to_imperial(spell["descripcion"])
            spell["descripcion"] = normalizar_descripcion(spell["descripcion"])

            if spell["materiales"]:
                spell["materiales"] = normalizar_materiales(spell["materiales"])

            if spell["concentracion"]:
                spell["duracion"] = fix_concentration_duration_text(spell["duracion"])

            spell["tiempo_de_lanzamiento"] = normalizar_tiempo_de_lanzamiento(
                spell["tiempo_de_lanzamiento"]
            )

        # Overriding the data in the file:
        # Warning, this will update all spanish special characters to unicode.
        #  for example 'ó' -> '\u00f3'.
        with open(file_name, "w", encoding="utf-8") as fh:
            json.dump(spells, fh, indent=2)
