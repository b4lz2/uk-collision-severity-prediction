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

## Contributors

- A — Logan Charles
- B — Hardt Julian
- C — Höfinger Balthasar
- D — El Dib Yehea
