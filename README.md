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
