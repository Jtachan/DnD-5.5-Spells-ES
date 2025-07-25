"""Script to unify all spells.

All unified spells have a new keyword 'nivel' showing the level of itself.
"""

import re
import json
import os


T_LANZ_TEXT = "Acción adicional, que realizas de inmediato tras acertar a una criatura con un arma cuerpo a cuerpo o un ataque sin armas"
ACC_NEW_DESC = "El conjuro se realiza de inmediato tras acertar a una criatura con un arma cuerpo a cuerpo o un ataque sin armas.<br><br>"


def unify_spells():
    """Preparing the file 'spells.json' to be loaded by the HTML table."""
    all_spells = []
    for idx in range(10):
        with open(f"level_{idx}.json", "r", encoding="utf-8") as fh:
            file_spells = json.load(fh)
        for spell in file_spells:
            if spell["tiempo_de_lanzamiento"] == T_LANZ_TEXT:
                spell["tiempo_de_lanzamiento"] = "Acción adicional"
                spell["descripcion"] = ACC_NEW_DESC + spell["descripcion"]
            spell["nivel"] = idx
            all_spells.append(spell)
    all_spells.sort(key=lambda sp: sp["nombre"])

    out_path = os.path.join(os.path.dirname(__file__), "..", "spells.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(all_spells, fh, indent=2)


def check_double_line_jump():
    """Checking if each description has a double line jump `<br><br>`"""
    pattern = r"(?<!<br>)<br>(?!<br>)"
    for idx in range(10)
        with open(f"level_{idx}.json", "r", encoding="utf-8") as fh:
            spells = json.load(fh)
        for spell in spells:
            spell["description"] = re.sub(pattern, "<br><br>", spell["description"])
        with open(f"level_{idx}.json", "w", encoding="utf-8") as fh:
            json.dump(spells, fh, indent=2)


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    unify_spells()