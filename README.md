# 1er Parcial — Análisis de Datos

Estudio del mercado inmobiliario de Moscú (2020–2026): exploración de los datos, relaciones con el precio de venta y **modelado OLS** del mercado secundario, con experimentos registrados en **MLflow**.

**Integrantes:** Tomás Wajnerman y Felipe Sarco.

**Dataset:** [Moscow Real Estate: Sales and Rentals (2020–2026)](https://www.kaggle.com/datasets/sergionefedov/moscow-real-estate-sales-and-rentals-20202026) (Kaggle). Los CSV deben estar en `MOSCOW-DATASET/`:

| Archivo | Contenido |
| --- | --- |
| `rentals.csv` | Alquileres |
| `secondary_market.csv` | Venta en mercado secundario |
| `new_builds.csv` | Venta de obra nueva |
| `district_prices_monthly.csv` | Precios oficiales mensuales por distrito |
| `metro_stations.csv` | Estaciones de metro |

---

## Estructura del repositorio

| Elemento | Rol |
| --- | --- |
| `PARCIAL-1.ipynb` | Notebook con el flujo completo de análisis y modelado |
| `mlflow.db` | Backend SQLite de MLflow (metadatos de experimentos y runs) |
| `mlflow_backup.db` | Copia de seguridad de la base (generada al ejecutar el notebook) |
| `mlruns/` | Artefactos locales (gráficos, `summary.txt`, métricas de CV, etc.) |

---

## Flujo del notebook (por secciones)

El notebook está organizado en bloques consecutivos. A continuación, qué se hace en cada uno (sin duplicar el código).

### 1. Imports y configuración

- Librerías (`pandas`, `statsmodels`, `scikit-learn`, `mlflow`, etc.).
- Carga de los cinco CSV desde `./MOSCOW-DATASET/`.
- **MLflow:** tracking en `sqlite:///mlflow.db`, experimento `SECONDARY-MARKET-MOSCOW`, artefactos en la carpeta `mlruns/`.
- **Routeo de rutas:** lectura de `mlflow.db` y normalización de URIs de artefactos hacia `./mlruns` (evita rutas rotas en Windows y espacios en el path del proyecto).

### 2. Funciones auxiliares

- Gráficos de exploración (univariados, categóricos, binarios, residuos).
- Funciones de registro en MLflow (`log_params`, métricas, figuras, resumen OLS, validación cruzada).

### 3. Descripción de columnas y EDA inicial

- Diccionario de variables por archivo.
- `describe`, `info` y cardinalidad por dataset: precios mensuales por distrito, **rentals**, **secondary market**, **new builds** y **metro stations**.

### 4. Análisis univariado

- **Secondary market:** variables continuas, categóricas y binarias (distribuciones y frecuencias).
- **District prices monthly:** variables continuas/discretas relevantes (p. ej. precio oficial secundario por m²).
- *Alquileres y obra nueva:* explorados en el EDA inicial; no incluyen el desglose univariado completo del mercado secundario.

### 5. Análisis bivariado

- **Alcance:** solo `secondary_market`, objetivo **`price_rub`** (precio de venta).
- Heatmap y ranking de pares, correlaciones numéricas (Pearson/Spearman), detalle feature vs objetivo, y relaciones numérica–categórica.

### 6. Limpieza de datos y modelado (secondary market)

- Reemplazo de `price_per_sqm` por el precio oficial del distrito (`secondary_price_per_sqm` vía `district_prices_monthly`).
- Validación y limpieza de filas (duplicados, reglas de negocio, outliers).
- Transformación log del objetivo, variables dummy y **OLS** con `statsmodels`.
- Varias **runs** en MLflow (métricas, gráficos de regresión/residuos, resumen del modelo; validación cruzada cuando corresponda).

---

## Cómo ejecutar el código

### Requisitos

- Python 3.10+ recomendado.
- Paquetes: `pandas`, `numpy`, `matplotlib`, `seaborn`, `scipy`, `statsmodels`, `scikit-learn`, `mlflow`.

```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels scikit-learn mlflow jupyter
```

### Pasos

1. **Clonar el repositorio** y situarse en la **raíz del proyecto** (donde están `PARCIAL-1.ipynb`, `mlflow.db` y `mlruns/`).
2. **Descargar el dataset** de Kaggle y colocar los CSV en `MOSCOW-DATASET/`.
3. **Abrir el notebook** (JupyterLab, Jupyter Notebook o VS Code/Cursor).
4. **Ejecutar la primera celda de imports** (MLflow + routeo de `mlflow.db`) antes de registrar nuevos experimentos.
5. Ejecutar el resto **en orden** o *Run All*.

```bash
cd /ruta/al/repo
jupyter lab
```

> Si movés el repo a otra carpeta o clonás en otra máquina, volvé a ejecutar la celda de routeo para alinear las URIs con `./mlruns`.

---

## MLflow: backend, artefactos e interfaz

| Componente | Ubicación | Contenido |
| --- | --- | --- |
| Metadatos | `mlflow.db` (SQLite) | Experimentos, runs, parámetros, métricas, tags |
| Artefactos | `mlruns/` | PNG, `summary.txt`, CSV de CV, etc. |

```text
tracking URI:  sqlite:///mlflow.db
experimento:   SECONDARY-MARKET-MOSCOW
artefactos:    mlruns/
```

### Comandos para levantar el servicio (MLflow UI)

No hace falta ejecutar el notebook solo para **revisar** runs: basta clonar el repo y levantar la UI desde la **raíz** (misma carpeta que `mlflow.db`).

```bash
cd /ruta/al/repo
pip install mlflow
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
```

Abrir `http://127.0.0.1:5000` → experimento **SECONDARY-MARKET-MOSCOW** → run → **Artifacts**. Detener con `Ctrl+C`.

Puerto alternativo:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns --host 127.0.0.1 --port 5001
```

**Windows (PowerShell):**

```powershell
cd "C:\Users\...\parcial-introduccion-datos"
pip install mlflow
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
```

Si la UI no encuentra artefactos en Windows: ejecutar el comando desde la raíz del repo, re-ejecutar la celda de routeo del notebook y comprobar que exista la carpeta del run en `mlruns/`.

### Consultar la base sin la UI (opcional)

Metadatos en `mlflow.db` (SQLite, tablas `experiments` y `runs`). Imágenes y archivos en `mlruns/`.
