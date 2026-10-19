import json
from pathlib import Path

p = Path(r"c:\Users\Tomas Wajnerman\Documents\Facultad\Intro datos\parcial-introducci-n-datos\PARCIAL-1.ipynb")
nb = json.loads(p.read_text(encoding="utf-8"))

replacements = [
    ("TUKEY_MIN_N_DISTRICT = 20\n", "TUKEY_MIN_N_OKRUG = 20\n"),
    (
        'run_name_newbuilds = "15-newbuilds-log-tukey-district-log-metro-distance"\n',
        'run_name_newbuilds = "16-newbuilds-log-tukey-okrug-log-metro-district-dummies"\n',
    ),
    (
        '    "Run 15 \u2014 Misma base que la run 14 (log_price_rub, Tukey de precio/m\u00b2 por district, "\n'
        '    "one-hot de district, sin deal_type). Sustituimos metro_distance_min en minutos por "\n'
        '    "log_metro_distance_min = log1p(metro_distance_min), para modelar efecto decreciente "\n'
        '    "de la distancia al metro y evitar problemas con ceros. La variable original queda "\n'
        '    "excluida del OLS."\n',
        '    "Run 16 \u2014 Igual especificaci\u00f3n de modelo que la run 15 (log_price_rub, one-hot de "\n'
        '    "district, log1p(metro_distance_min), sin deal_type). Cambiamos solo la detecci\u00f3n de "\n'
        '    "outliers: Tukey (Q1 \u2212 1,5\u00d7IQR y Q3 + 1,5\u00d7IQR) sobre precio/m\u00b2 calculado dentro "\n'
        '    "de cada okrug administrativo (~11 zonas), en lugar de por district. Grupos con "\n'
        '    "menos de 20 avisos no se filtran por IQR. Objetivo: comparar limpieza zonal m\u00e1s "\n'
        '    "agregada (okrugs) vs la run 15 (Tukey por distrito)."\n',
    ),
    (
        '    outlier = d.groupby("district", group_keys=False)["_price_m2"].transform(\n'
        "        lambda s: _tukey_outlier_mask(s, k=TUKEY_K, min_n=TUKEY_MIN_N_DISTRICT)\n"
        "    )\n"
        "    n_out = int(outlier.sum())\n"
        '    n_distritos_afectados = d.loc[outlier, "district"].nunique()\n',
        '    outlier = d.groupby("okrug", group_keys=False)["_price_m2"].transform(\n'
        "        lambda s: _tukey_outlier_mask(s, k=TUKEY_K, min_n=TUKEY_MIN_N_OKRUG)\n"
        "    )\n"
        "    n_out = int(outlier.sum())\n"
        '    n_okrugs_afectados = d.loc[outlier, "okrug"].nunique()\n',
    ),
    (
        '        "outliers Tukey precio/m\u00b2 por district (Q1/Q3 \u00b1 1.5\u00d7IQR)",\n',
        '        "outliers Tukey precio/m\u00b2 por okrug (Q1/Q3 \u00b1 1.5\u00d7IQR)",\n',
    ),
    (
        '        f"Outliers Tukey por district: {n_out} filas eliminadas "\n'
        '        f"({n_distritos_afectados} distritos con al menos un outlier; "\n'
        '        f"min_n={TUKEY_MIN_N_DISTRICT}, k={TUKEY_K})"\n',
        '        f"Outliers Tukey por okrug: {n_out} filas eliminadas "\n'
        '        f"({n_okrugs_afectados} okrugs con al menos un outlier; "\n'
        '        f"min_n={TUKEY_MIN_N_OKRUG}, k={TUKEY_K})"\n',
    ),
]

for cell in nb["cells"]:
    if cell.get("cell_type") != "code":
        continue
    src = "".join(cell["source"])
    if "validar_y_limpiar_newbuilds" not in src or "run_name_newbuilds" not in src:
        continue
    for old, new in replacements:
        if old not in src:
            raise SystemExit("Missing snippet: " + repr(old[:80]))
        src = src.replace(old, new)
    cell["source"] = src.splitlines(keepends=True)
    p.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
    print("PATCH OK")
    break
else:
    raise SystemExit("cell not found")
