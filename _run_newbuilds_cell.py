import json
import os
from pathlib import Path

ROOT = Path(r"c:\Users\Tomas Wajnerman\Documents\Facultad\Intro datos\parcial-introducci-n-datos")
os.chdir(ROOT)
nb = json.loads((ROOT / "PARCIAL-1.ipynb").read_text(encoding="utf-8"))

def cell_src(idx):
    return "".join(nb["cells"][idx]["source"])

g = {"__name__": "__main__", "display": print}
for idx in (2, 6, 8):
    exec(cell_src(idx), g)

import pandas as pd

g["df_newbuilds"] = pd.read_csv(ROOT / "MOSCOW-DATASET/new_builds.csv")
exec(cell_src(194).split("df_secondary_limpio")[0], g)
exec(cell_src(199), g)
exec(cell_src(201), g)
