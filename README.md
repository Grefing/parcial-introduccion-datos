# 1er Parcial — Análisis de Datos

Primer parcial de la materia **Análisis de Datos**. El trabajo explora el mercado inmobiliario de Moscú a partir de anuncios de alquiler y venta, y termina modelando el **precio de venta** con regresión lineal (OLS), comparando **mercado secundario** y **obra nueva**.

## Dataset

[Moscow Real Estate: Sales and Rentals (2020–2026)](https://www.kaggle.com/datasets/sergionefedov/moscow-real-estate-sales-and-rentals-20202026) (Kaggle).

Los CSV están en `MOSCOW-DATASET/`:

| Archivo | Contenido |
| --- | --- |
| `rentals.csv` | Alquileres |
| `secondary_market.csv` | Venta en mercado secundario |
| `new_builds.csv` | Venta de obra nueva |
| `district_prices_monthly.csv` | Precios oficiales mensuales por distrito |
| `metro_stations.csv` | Estaciones de metro |

## Contenido del repositorio

- **`PARCIAL-1.ipynb`**: notebook principal con todo el flujo de análisis.
- **`mlruns/`**: artefactos y métricas de experimentos registrados con [MLflow](https://mlflow.org/) (modelos, gráficos de residuos/regresión, validación cruzada).

## Qué hace el análisis (resumen)

1. **Exploración**: descripción de columnas, `describe`/`info`, análisis **univariado** (continuas, categóricas y binarias) y **bivariado** (asociaciones, correlaciones, gráficos vs precio).
2. **Modelado de ventas** (dos pipelines separados):
   - **Secondary market**: variable objetivo `price_rub` (log), enriquecimiento con precio oficial del distrito (`secondary_price_per_sqm`), limpieza de filas, variables dummy y OLS.
   - **New builds**: mismo enfoque con `newbuild_price_per_sqm`, reglas de limpieza propias de obra nueva (p. ej. año de entrega, outliers de precio/m² por distrito) y OLS con `log_price_rub`.
3. **Seguimiento de experimentos**: distintas especificaciones de modelo y, en obra nueva, **validación cruzada k-fold** registrada en MLflow.

## Cómo ejecutarlo

1. Entorno Python con `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `statsmodels` y `mlflow`.
2. Abrir y ejecutar `PARCIAL-1.ipynb` desde la raíz del repo (las rutas asumen `./MOSCOW-DATASET/`).
3. Para ver runs locales: `mlflow ui` (apunta al directorio `mlruns` del proyecto).
