"""Script to unify all spells.

All unified spells have a new keyword 'nivel' showing the level of itself.
"""

import json
import os

from _utils import *


def unify_spells():
    """Preparing the file 'spells.json' to be loaded by the HTML table."""

    for edition in FOLDER_EDITIONS:
        all_spells = []
        for idx in range(10):
            file_name = os.path.join(edition, f"level_{idx}.json")
            with open(file_name, "r", encoding="utf-8") as fh:
                file_spells = json.load(fh)
            for spell in file_spells:
                spell["nivel"] = idx
                all_spells.append(spell)
        all_spells.sort(key=lambda sp: sp["nombre"])

        out_path = os.path.join(os.path.dirname(__file__), edition, "all.json")
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(all_spells, fh, indent=2)


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    unify_spells()
