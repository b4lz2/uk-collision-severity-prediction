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
<img width="4512" height="3145" alt="ERD" src="https://github.com/user-attachments/assets/6481bb34-a3a5-408a-9286-3909f32f54ef" />

## SQL CREATE statements

```
CREATE TABLE "dft-road-casualty-statistics-collision-last-5-years" (
    collision_index                                      VARCHAR PRIMARY KEY,
    collision_year                                       VARCHAR,
    collision_ref_no                                     VARCHAR,
    location_easting_osgr                                VARCHAR,
    location_northing_osgr                               VARCHAR,
    longitude                                            VARCHAR,
    latitude                                             VARCHAR,
    police_force                                         VARCHAR,
    collision_severity                                   VARCHAR,
    number_of_vehicles                                   VARCHAR,
    number_of_casualties                                 VARCHAR,
    date                                                 VARCHAR,
    day_of_week                                          VARCHAR,
    time                                                 VARCHAR,
    local_authority_district                             VARCHAR,
    local_authority_ons_district                         VARCHAR,
    local_authority_highway                              VARCHAR,
    local_authority_highway_current                      VARCHAR,
    first_road_class                                     VARCHAR,
    first_road_number                                    VARCHAR,
    road_type                                            VARCHAR,
    speed_limit                                          VARCHAR,
    junction_detail_historic                             VARCHAR,
    junction_detail                                      VARCHAR,
    junction_control                                     VARCHAR,
    second_road_class                                    VARCHAR,
    second_road_number                                   VARCHAR,
    pedestrian_crossing_human_control_historic           VARCHAR,
    pedestrian_crossing_physical_facilities_historic     VARCHAR,
    pedestrian_crossing                                  VARCHAR,
    light_conditions                                     VARCHAR,
    weather_conditions                                   VARCHAR,
    road_surface_conditions                              VARCHAR,
    special_conditions_at_site                           VARCHAR,
    carriageway_hazards_historic                         VARCHAR,
    carriageway_hazards                                  VARCHAR,
    urban_or_rural_area                                  VARCHAR,
    did_police_officer_attend_scene_of_accident          VARCHAR,
    trunk_road_flag                                      VARCHAR,
    lsoa_of_accident_location                            VARCHAR,
    enhanced_severity_collision                          VARCHAR,
    collision_injury_based                               VARCHAR,
    collision_adjusted_severity_serious                  VARCHAR,
    collision_adjusted_severity_slight                   VARCHAR
);

CREATE TABLE "dft-road-casualty-statistics-road-safety-open-dataset-data-guide" (
    field_name                                           VARCHAR PRIMARY KEY,
    code_format                                          VARCHAR,
    label                                                VARCHAR,
    note                                                 VARCHAR
);

CREATE VIEW "Date_and_Location_View" AS
SELECT
    collision_index,
    collision_year,
    location_easting_osgr,
    location_northing_osgr,
    longitude,
    latitude,
    date,
    day_of_week,
    time,
    lsoa_of_accident_location
FROM "dft-road-casualty-statistics-collision-last-5-years";
 
CREATE VIEW "Environment_View" AS
SELECT
    collision_index,
    weather_conditions,
    carriageway_hazards_historic,
    road_surface_conditions,
    did_police_officer_attend_scene_of_accident,
    light_conditions,
    carriageway_hazards,
    special_conditions_at_site
FROM "dft-road-casualty-statistics-collision-last-5-years";
 
CREATE VIEW "Local_Authority_View" AS
SELECT
    collision_index,
    local_authority_district,
    local_authority_ons_district,
    local_authority_highway,
    local_authority_highway_current,
    police_force
FROM "dft-road-casualty-statistics-collision-last-5-years";
 
CREATE VIEW "Road_Context_View" AS
SELECT
    collision_index,
    speed_limit,
    first_road_number,
    trunk_road_flag,
    second_road_class,
    pedestrian_crossing_human_control_historic,
    junction_detail,
    road_surface_conditions,
    second_road_number,
    pedestrian_crossing_physical_facilities_historic,
    first_road_class,
    junction_control,
    road_type,
    junction_detail_historic,
    pedestrian_crossing
FROM "dft-road-casualty-statistics-collision-last-5-years";
```

## Contributors

- A — Logan Charles
- B — Hardt Julian
- C — Höfinger Balthasar
- D — El Dib Yehea
