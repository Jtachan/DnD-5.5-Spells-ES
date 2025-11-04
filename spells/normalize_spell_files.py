"""Script with functions to normalize all spells though all the files.

The functions shown here should be run only to normalize the data among
the 'level_X.json' files.
"""

import re
import json
import os

METRIC_SYSTEM_REGEX = r"((\d+,)?\d+) ([kmc]?m|kg|l)[\s.,]"
IMPERIAL_SYSTEM_REGEX = r"((\d+,)?\d+) (pies?|pulgadas?|millas?|galón|galones|libras?)[\s.,]"

# Condiciones adicionales que aparecen en el campo de 'tiempo de lanzamiento'.
# Estas descripciones se mueven directamente al campo de 'descripcion'.
CONDITIONAL_ACTION_TEXT = {
    "que realizas de inmediato tras acertar a un objetivo con un arma cuerpo a cuerpo o un ataque sin armas": "El conjuro se realiza de inmediato tras acertar al objetivo con un arma cuerpo a cuerpo o un ataque sin armas.",
    "que realizas de inmediato tras acertar a una criatura con un arma cuerpo a cuerpo o un ataque sin armas": "El conjuro se realiza de inmediato tras acertar a una criatura con un arma cuerpo a cuerpo o un ataque sin armas.",
    "que realizas de inmediato tras acertar a una criatura con un arma a distancia": "El conjuro se realiza de inmediato tras acertar a una criatura con un arma a distancia.",
    "que llevas a cabo cuando tú o una criatura que puedes ver a 18 m o menos de ti caigáis": "El conjuro se lleva a cabo cuando tú o una criatura que puedes ver a 18 m o menos de ti caigáis.",
    "que llevas a cabo cuando una criatura que puedas ver a 18 m o menos de ti lance un conjuro usando componentes verbales, somáticos o materiales": "El conjuro se lleva a cabo cuando una criatura que puedas ver a 18 m o menos de ti lance un conjuro usando componentes verbales, somáticos o materiales.",
    "que llevas a cabo en respuesta a recibir daño de una criatura que puedas ver a 18 m o menos de ti": "El conjuro se lleva a cabo en respuesta a recibir daño de una criatura que puedas ver a 18 m o menos de ti.",
    "que llevas a cabo cuando te acierta una tirada de ataque o eres el objetivo del conjuro proyectil mágico": "El conjuro se lleva a cabo en respuesta al ser acertado por una tirada de ataque o ser objetivo del conjuro <i>proyectil mágico</i>.",
}


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


def _norm_unit_systems(text: str | list[str]) -> str | list[str]:
    """Normalizing the description for both metric and imperial systems."""
    if isinstance(text, str):
        if re.search(METRIC_SYSTEM_REGEX, text):
            text = expand_units_to_imperial(text)
        elif re.search(IMPERIAL_SYSTEM_REGEX, text):
            text = expand_units_to_metric(text)
    return text


def normalizar_descripcion(text: str | list) -> str:
    """Main function to normalize the spell description."""
    if isinstance(text, str):
        text = _norm_new_lines(_norm_higher_level(text))
    else:
        text = [_norm_new_lines(_norm_higher_level(t)) for t in text]
    text = _norm_unit_systems(text)
    return text


def expand_units_to_imperial(text: str) -> list[str]:
    """Converting a description with the metric system into a list with imperial and metric."""

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
        return f"{miles} milla" if miles == 1 else f"{miles} millas"

    def kg_to_pounds(re_match: re.Match) -> str:
        kilograms = float(re_match.group(1).replace(",", "."))
        pounds = int(kilograms * 2)
        return f"{pounds} libra" if pounds == 1 else f"{pounds} libras"

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

def expand_units_to_metric(text: str) -> list[str]:
    """Converting a description with the imperial system into a list with imperial and metric."""

    def feet_to_meters(re_match: re.Match) -> str:
        feet = float(re_match.group(1).replace(",", "."))
        meters = int(feet / 5 * 1.5)
        meters = int(meters) if int(meters) == meters else str(round(meters, 2)).replace(".", ",")
        return f"{meters} m"

    def inches_to_cm(re_match: re.Match) -> str:
        inches = float(re_match.group(1).replace(",", "."))
        centimeters = inches * 2.5
        centimeters = int(centimeters) if int(centimeters) == centimeters else str(round(centimeters, 2)).replace(".", ",")
        return f"{centimeters} cm"

    def miles_to_km(re_match: re.Match) -> str:
        miles = float(re_match.group(1).replace(",", "."))
        kilometers = miles * 1.5
        kilometers = int(kilometers) if int(kilometers) == kilometers else str(round(kilometers, 2)).replace(".", ",")
        return f"{kilometers} km"

    def pounds_to_kg(re_match: re.Match) -> str:
        pounds = float(re_match.group(1).replace(",", "."))
        kilograms = pounds / 2
        kilograms = int(kilograms) if int(kilograms) == kilograms else str(round(kilograms, 2)).replace(".", ",")
        return f"{kilograms} kg"

    def liters_to_gallons(re_match: re.Match) -> str:
        gallons = float(re_match.group(1).replace(",", "."))
        liters = gallons * 4
        liters = int(liters) if int(liters) == liters else str(round(liters, 2)).replace(".", ",")
        return f"{liters} l"

    metric_text = re.sub(r"((\d+,)?\d+) pies?", feet_to_meters, text)
    metric_text = re.sub(r"((\d+,)?\d+) pulgadas?", inches_to_cm, metric_text)
    metric_text = re.sub(r"((\d+,)?\d+) millas?", miles_to_km, metric_text)
    metric_text = re.sub(r"((\d+,)?\d+) libras?", pounds_to_kg, metric_text)
    metric_text = re.sub(r"((\d+,)?\d+) (galón|galones)", liters_to_gallons, metric_text)

    return [text, metric_text]


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
    text = text.replace("1 acción", "Acción").replace("1 reacción", "Reacción")
    if text.endswith(("o ritual", "o un ritual", "o 1 ritual")):
        text = text.split(" o ")[0]
    return text


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    for edition in ("ed5_5", "ed5_0"):
        for idx in range(10):
            file_name = os.path.join(edition, f"level_{idx}.json")
            # Loading all spells:
            with open(file_name, "r", encoding="utf-8") as fh:
                spells = json.load(fh)

            # Performing all corrections (one per spell):
            for spell in spells:
                for ending, cond_desc in CONDITIONAL_ACTION_TEXT.items():
                    if spell["tiempo_de_lanzamiento"].endswith(ending):
                        spell["tiempo_de_lanzamiento"] = spell[
                            "tiempo_de_lanzamiento"
                        ].split(",")[0]
                        if isinstance(spell["descripcion"], str):
                            spell["descripcion"] = (
                                f"{cond_desc}<br><br>{spell['descripcion']}"
                            )
                        else:
                            spell["descripcion"] = [
                                f"{cond_desc}<br><br>{d}" for d in spell["descripcion"]
                            ]

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
