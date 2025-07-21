"""Script to unify all spells.

All unified spells have a new keyword 'nivel' showing the level of itself.
"""

import json
import os


def unify_spells():
    all_spells = {}
    for idx in range(10):
        with open(f"level_{idx}.json", "r", encoding="utf-8") as fh:
            spells = json.load(fh)

        for spell_data in spells.values():
            spell_data.update(nivel=idx)
        all_spells |= spells

    out_path = os.path.join(os.path.dirname(__file__), "..", "spells.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(all_spells, fh, indent=2)


if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    unify_spells()