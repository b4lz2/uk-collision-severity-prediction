# UK Collision Severity Prediction

Predicting the severity of road traffic collisions in the United Kingdom
using the Department for Transport's STATS19 open data (2019–2023).

## Project context

Developed as part of the FAIR Data Science course (DaSt 2026) at TU Wien.

## Data source

Department for Transport, UK Government — Road Safety Data:
https://www.gov.uk/government/statistical-data-sets/road-safety-open-data

## File organisation

### Folder structure

- `data/raw/` — original input datasets as published by the source
- `data/processed/` — cleaned and feature-engineered data
- `src/` — Python source code (preprocessing, models, evaluation)
- `notebooks/` — Jupyter notebooks (incl. DBRepo REST API interactions)
- `outputs/figures/` — generated plots and visualisations
- `outputs/models/` — trained model artefacts
- `outputs/predictions/` — model output predictions
- `docs/` — additional documentation (validation, model cards)
- `config/` — configuration files

### Naming conventions

All file and folder names use lowercase `snake_case` with no spaces
or special characters. Dates follow ISO 8601 (`YYYY-MM-DD`).

| Category       | Pattern                             | Example                                |
| -------------- | ----------------------------------- | -------------------------------------- |
| Input data     | `<source>_<content>_<period>.<ext>` | `dft_collisions_2019-2023.csv`         |
| Processed data | `<content>_<step>_<version>.<ext>`  | `collisions_cleaned_v1.parquet`        |
| Scripts        | `<NN>_<action>_<object>.py`         | `01_load_data.py`                      |
| Notebooks      | `<NN>_<topic>.ipynb`                | `01_dbrepo_setup.ipynb`                |
| Models         | `<algorithm>_<target>_<date>.pkl`   | `randomforest_severity_2026-05-05.pkl` |
| Figures        | `<plot-type>_<description>.png`     | `confusion-matrix_randomforest.png`    |
| Config files   | `config_<purpose>.yaml`             | `config_training.yaml`                 |

## Entity Relationship Diagram 
<img width="12713" height="7607" alt="ERD" src="https://github.com/user-attachments/assets/a3111636-37fe-4863-b18f-3a7a3678f6bd" />

## Database Views

The following views are created in DBRepo via the REST API.
See `notebooks/02_dbrepo_views.ipynb` for the full implementation.

| View Name | Purpose |
| ----------------------- | ----------------------------------------------------------------------- |
| `collision_ml_features` | Selects the 15 input features and the target label `collision_severity` directly from the raw collision table. This is the primary data source for the ML pipeline, used by `01_load_data.py` to load training, validation, and test splits without reading any local files. |
| `collision_severity_summary` | Groups collisions by severity, road type, urban or rural area, and speed limit, and counts the total records per group. Used to verify the class imbalance between Fatal, Serious, and Slight accidents before applying SMOTE balancing in `02_preprocess.py`. |


## Contributors

- A — Logan Charles
- B — Hardt Julian
- C — Höfinger Balthasar
- D — El Dib Yehea
