# UK Collision Severity Prediction

[![DOI](https://zenodo.org/badge/DOI/TBD.svg)](TBD_ZENODO_DOI_LINK)

Predicting the severity of road traffic collisions in the United Kingdom
using the Department for Transport's STATS19 open data (2020–2024).

## Project context

Developed as part of the FAIR Data Science course (DaSt 2026) at TU Wien.

## Abstract

The UK government publishes road safety data — every accident reported by the
police since 1979. We load the last few years into a normalised database on
TU Wien's DBRepo and train a classifier that tries to predict how bad a
collision was (Fatal, Serious, or Slight) from things like the weather, road
type, and time of day.

The whole pipeline runs from one REST API source, no local CSVs. We compare
three classifiers on a validation set, pick the best (Gradient Boosting),
and evaluate it on a held-out test set. Everything — code, model, predictions,
figures, metadata — is open licensed and documented with the usual FAIR
metadata stuff (RO-Crate, CodeMeta, FAIR4ML, Croissant, Model Card).

## Data source

Department for Transport, UK Government — Road Safety Data:
https://www.gov.uk/government/statistical-data-sets/road-safety-open-data

Mirrored as a 3NF database on TU Wien DBRepo:
https://test.dbrepo.tuwien.ac.at/database/82c19b39-246c-4409-b25c-8baf3a158a70
(DOI: `10.82556/c8r3-bf26`)

## Requirements and installation

- **Python** 3.13.11
- All Python dependencies are pinned in [`requirements.txt`](./requirements.txt)

```powershell
git clone https://github.com/b4lz2/uk-collision-severity-prediction.git
cd uk-collision-severity-prediction
pip install -r requirements.txt
```

You also need a DBRepo account to fetch the data. See [Authentication](#authentication) below.

## Reproducing the experiment

The pipeline runs as four scripts in order, from the `src/` folder:

```powershell
cd src

# 1. Fetch the data from DBRepo (paginated, ~500k rows)
python 01_load_data.py

# 2. Apply SMOTE to balance the training set, produce splits
python 02_preprocess.py

# 3. Train three classifiers, pick the best by Macro F1, save the model
python 03_train_classifier.py

# 4. Evaluate the best model on the test set and produce figures
python 04_evaluate.py
```

Each script writes its outputs to `src/data/processed/` or `src/outputs/` —
see the table below.

## Inputs and outputs

### Inputs

| Source                                   | Format            | Description                                                                                                                                                                                           |
| ---------------------------------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DBRepo view `collision_ml_features`      | JSON via REST API | 16 columns (15 features + the `collision_severity` label), one row per collision — used by the ML pipeline                                                                                            |
| DBRepo view `collision_severity_summary` | JSON via REST API | 6 columns (speed_limit, road_type, number_of_vehicles, urban_or_rural_id, number_of_casualties, collision_severity), one row per collision — used for the class imbalance check in `02_preprocess.py` |

### Outputs

| Path                                                       | Format | Description                                      |
| ---------------------------------------------------------- | ------ | ------------------------------------------------ |
| `src/data/processed/train.csv`                             | CSV    | Training split (stratified)                      |
| `src/data/processed/train_resampled.csv`                   | CSV    | Training split after SMOTE oversampling          |
| `src/data/processed/validation.csv`                        | CSV    | Validation split for model selection             |
| `src/data/processed/test.csv`                              | CSV    | Held-out test split                              |
| `src/outputs/models/gradient_boosting_severity_<date>.pkl` | joblib | Best trained model                               |
| `src/outputs/predictions/test_predictions_<date>.csv`      | CSV    | Predictions on the test set                      |
| `src/outputs/figures/01_data_understanding.png`            | PNG    | Feature distributions and class balance overview |
| `src/outputs/figures/02_class_imbalance.png`               | PNG    | Class distribution before vs. after SMOTE        |
| `src/outputs/figures/03_confusion_matrix.png`              | PNG    | Test set confusion matrix                        |
| `src/outputs/figures/04_performance_comparison.png`        | PNG    | Per-class metrics + model comparison             |
| `src/outputs/figures/05_feature_importance.png`            | PNG    | Feature importances of the chosen model          |

## File organisation

### Folder structure

- `src/data/processed/` — cleaned and feature-engineered data
- `src/` — Python source code (preprocessing, models, evaluation)
- `notebooks/` — Jupyter notebooks (incl. DBRepo REST API interactions)
- `src/outputs/figures/` — generated plots and visualisations
- `src/outputs/models/` — trained model artefacts
- `src/outputs/predictions/` — model output predictions
- `docs/` — additional documentation (validation, model cards)
- `config/` — configuration files

### Naming conventions

All file and folder names use lowercase `snake_case` with no spaces
or special characters. Dates follow ISO 8601 (`YYYY-MM-DD`).

| Category       | Pattern                             | Example                                |
| -------------- | ----------------------------------- | -------------------------------------- |
| Input data     | `<source>_<content>_<period>.<ext>` | `dft_collisions_2020-2024.csv`         |
| Processed data | `<content>_<step>_<version>.<ext>`  | `collisions_cleaned_v1.parquet`        |
| Scripts        | `<NN>_<action>_<object>.py`         | `01_load_data.py`                      |
| Notebooks      | `<NN>_<topic>.ipynb`                | `01_dbrepo_setup.ipynb`                |
| Models         | `<algorithm>_<target>_<date>.pkl`   | `randomforest_severity_2026-05-05.pkl` |
| Figures        | `<plot-type>_<description>.png`     | `confusion-matrix_randomforest.png`    |
| Config files   | `config_<purpose>.yaml`             | `config_training.yaml`                 |

## Entity Relationship Diagram

<img alt="ERD" src="https://github.com/user-attachments/assets/a3111636-37fe-4863-b18f-3a7a3678f6bd" width="900" />

## Database Views

The following views are created in DBRepo via the REST API.
See `notebooks/02_dbrepo_views.ipynb` for the full implementation.

| View Name                    | Purpose                                                                                                                                                                                                                                                                      |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `collision_ml_features`      | Selects the 15 input features and the target label `collision_severity` directly from the raw collision table. This is the primary data source for the ML pipeline, used by `01_load_data.py` to load training, validation, and test splits without reading any local files. |
| `collision_severity_summary` | Groups collisions by severity, road type, urban or rural area, and speed limit, and counts the total records per group. Used to verify the class imbalance between Fatal, Serious, and Slight accidents before applying SMOTE balancing in `02_preprocess.py`.               |

# DBRepo API Integration

The experiment retrieves all input data exclusively from the TU Wien DBRepo REST API. No local CSV files are read in the final pipeline.

## API Base URL

```
https://test.dbrepo.tuwien.ac.at
```

## Authentication

The API requires HTTP Basic Authentication. Credentials are read from two environment variables at runtime — they are never hardcoded in the source code:

| Variable          | Description                  |
| ----------------- | ---------------------------- |
| `DBREPO_USERNAME` | Your DBRepo account username |
| `DBREPO_PASSWORD` | Your DBRepo account password |

Set them before running the script:

**PowerShell (Windows):**

```powershell
$env:DBREPO_USERNAME = "your_username"
$env:DBREPO_PASSWORD = "your_password"
python src/01_load_data.py
```

## Endpoints Used

### 1. HEAD — Get total row count

```
HEAD /api/v1/database/{databaseId}/view/{viewId}/data
```

| Parameter    | Value                                  |
| ------------ | -------------------------------------- |
| `databaseId` | `82c19b39-246c-4409-b25c-8baf3a158a70` |
| `viewId`     | `9fe5373a-0942-4b87-8794-0951506317cb` |

Used at startup to read the `X-Count` response header, which gives the total number of rows in the view. This is used for progress reporting and coverage validation.

---

### 2. GET — Fetch paginated view data

```
GET /api/v1/database/{databaseId}/view/{viewId}/data?page={page}&size={size}
```

| Parameter    | Value                                                                 |
| ------------ | --------------------------------------------------------------------- |
| `databaseId` | `82c19b39-246c-4409-b25c-8baf3a158a70`                                |
| `viewId`     | `9fe5373a-0942-4b87-8794-0951506317cb`                                |
| `page`       | 0-based integer, incremented each request                             |
| `size`       | `1000` (smaller page size avoids server-side timeout on high offsets) |

Used to download the full contents of the `collision_ml_features` view in sequential pages. The response format is `application/json`. Pagination stops when a page returns 0 rows, or when two consecutive pages both return HTTP 500.

---

## Views Used

| View Name               | View ID                                | Purpose                                                                                              |
| ----------------------- | -------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `collision_ml_features` | `9fe5373a-0942-4b87-8794-0951506317cb` | All 15 ML features + label, one row per collision. Used as the sole data source for the ML pipeline. |

---

## Error Handling

The data loading script handles all documented API error codes:

| HTTP Status             | Meaning                    | Handling                                                                                           |
| ----------------------- | -------------------------- | -------------------------------------------------------------------------------------------------- |
| `400`                   | Malformed request          | Raises `ValueError` with details                                                                   |
| `401`                   | Unauthorized               | Raises `PermissionError` — check credentials                                                       |
| `403`                   | Forbidden                  | Raises `PermissionError` — check account access                                                    |
| `404`                   | View / database not found  | Raises `LookupError`                                                                               |
| `409`                   | View schema mapping failed | Raises `RuntimeError`                                                                              |
| `500 / 502 / 503 / 504` | Transient server error     | Retries twice with 10s delay; if the following page also fails, stops gracefully with current data |

## RO-Crate

RO-Crate JSON file: https://github.com/b4lz2/uk-collision-severity-prediction/blob/main/ro-crate-metadata.json

RO-Crate Validation: https://github.com/b4lz2/uk-collision-severity-prediction/blob/main/docs/validation

## Contributors

- A — Logan, Charles ([0009-0002-3977-1286](https://orcid.org/0009-0002-3977-1286))
- B — Hardt, Julian ([0009-0003-0171-5796](https://orcid.org/0009-0003-0171-5796))
- C — Höfinger, Balthasar ([0009-0000-2002-4200](https://orcid.org/0009-0000-2002-4200))
- D — El Dib, Yehea ([0009-0003-8506-0271](https://orcid.org/0009-0003-8506-0271))

## Citation

This repository can be cited using the metadata in `CITATION.cff` (will be added in T3.8 together with the Zenodo DOI badge above).

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
