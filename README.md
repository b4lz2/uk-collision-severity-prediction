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

## Licences

This project involves three categories of artefact, each with a separate licence.

### Input Data

The input dataset is the **STATS19 Road Safety Open Dataset** published by the
UK Department for Transport and available at
<https://www.gov.uk/government/statistical-data-sets/road-safety-open-data>.

It is licensed under the **Open Government Licence v3.0 (OGL v3.0)**:
<https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/>

**Obligations:** Attribution is required. Derived works must acknowledge the
source with the statement:
> Contains public sector information licensed under the Open Government Licence v3.0.

OGL v3.0 is compatible with Creative Commons Attribution 4.0 (CC BY 4.0) and
does not impose ShareAlike restrictions, so the output data licence (CC BY 4.0)
is compatible.

### Software / Code

All source code in this repository is licensed under the **MIT Licence**.
See [LICENSE](./LICENSE) for the full text.

MIT was chosen because it is a permissive open-source licence that is fully
compatible with OGL v3.0 and imposes no restrictions on reuse, modification,
or distribution. It is one of the most widely adopted licences for research
software.

### Output Data

All output artefacts produced by this experiment — including trained model
files, preprocessed datasets, evaluation figures (confusion matrices,
performance charts, feature importance plots), and predictions — are released
under the **Creative Commons Attribution 4.0 International (CC BY 4.0)**
licence: <https://creativecommons.org/licenses/by/4.0/>

This licence permits unrestricted reuse, redistribution, and adaptation for
any purpose, including commercially, provided appropriate credit is given.
CC BY 4.0 is compatible with OGL v3.0 and consistent with the FWF Open
Access policy.
