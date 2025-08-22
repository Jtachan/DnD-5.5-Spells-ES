"""Script to unify all spells.

All unified spells have a new keyword 'nivel' showing the level of itself.
"""

import json
import os


CONDITIONAL_ACTION_TEXT = {
    "que realizas de inmediato tras acertar a un objetivo con un arma cuerpo a cuerpo o un ataque sin armas": "El conjuro se realiza de inmediato tras acertar al objetivo con un arma cuerpo a cuerpo o un ataque sin armas.",
    "que realizas de inmediato tras acertar a una criatura con un arma cuerpo a cuerpo o un ataque sin armas": "El conjuro se realiza de inmediato tras acertar a una criatura con un arma cuerpo a cuerpo o un ataque sin armas.",
    "que llevas a cabo cuando tú o una criatura que puedes ver a 18 m o menos de ti caigáis": "El conjuro se lleva a cabo cuando tú o una criatura que puedes ver a 18 m o menos de ti caigáis.",
    "que llevas a cabo cuando una criatura que puedas ver a 18 m o menos de ti lance un conjuro usando componentes verbales, somáticos o materiales": "El conjuro se lleva a cabo cuando una criatura que puedas ver a 18 m o menos de ti lance un conjuro usando componentes verbales, somáticos o materiales.",
}


def unify_spells():
    """Preparing the file 'spells.json' to be loaded by the HTML table."""
    all_spells = []
    for idx in range(10):
        with open(f"level_{idx}.json", "r", encoding="utf-8") as fh:
            file_spells = json.load(fh)
        for spell in file_spells:
            for ending, cond_desc in CONDITIONAL_ACTION_TEXT.items():
                if spell["tiempo_de_lanzamiento"].endswith(ending):
                    spell["tiempo_de_lanzamiento"] = spell[
                        "tiempo_de_lanzamiento"
                    ].split(",")[0]
                    if isinstance(spell["descripcion"], str):
                        spell["descripcion"] = f"{cond_desc}<br><br>{spell['descripcion']}"
                    else:
                        spell["descripcion"] = [f"{cond_desc}<br><br>{d}" for d in spell["descripcion"]]
                    break
            spell["nivel"] = idx
            all_spells.append(spell)
    all_spells.sort(key=lambda sp: sp["nombre"])

    out_path = os.path.join(os.path.dirname(__file__), "..", "spells.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(all_spells, fh, indent=2)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    unify_spells()
