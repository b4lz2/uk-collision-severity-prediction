import os
import time
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")

# ── Folder setup ──────────────────────────────
os.makedirs("data/processed", exist_ok=True)
os.makedirs("outputs/figures", exist_ok=True)

# ── DBRepo configuration ──────────────────────
DBREPO_BASE_URL = "https://test.dbrepo.tuwien.ac.at"
DATABASE_ID     = "82c19b39-246c-4409-b25c-8baf3a158a70"
VIEW_ID         = "9fe5373a-0942-4b87-8794-0951506317cb"   # collision_ml_features
PAGE_SIZE       = 5000

# Auth: read from environment variables
DBREPO_USER     = os.getenv("DBREPO_USERNAME")
DBREPO_PASSWORD = os.getenv("DBREPO_PASSWORD")

# ── Constants ─────────────────────────────────
LABEL        = "collision_severity"
FEATURES     = [
    "speed_limit",
    "light_conditions",
    "weather_conditions",
    "road_surface_conditions",
    "road_type",
    "urban_or_rural_id",
    "number_of_vehicles",
    "number_of_casualties",
    "day_of_week",
    "junction_detail",
    "junction_control",
    "pedestrian_crossing",
    "first_road_class",
    "special_conditions_at_site",
    "carriageway_hazards",
]
FEATURES      = list(dict.fromkeys(FEATURES))
SEV_COLORS    = {"Fatal": "#e74c3c", "Serious": "#e67e22", "Slight": "#2ecc71"}
ORDER         = ["Fatal", "Serious", "Slight"]
SEVERITY_MAP  = {1: "Fatal", 2: "Serious", 3: "Slight"}

RETRY_DELAY   = 10  



def _fetch_page(session: requests.Session, page: int):
    url     = (f"{DBREPO_BASE_URL}/api/v1/database/{DATABASE_ID}"
               f"/view/{VIEW_ID}/data")
    params  = {"page": page, "size": PAGE_SIZE}
    headers = {"Accept": "application/json"}

    for attempt in range(1, 3):   
        try:
            r = session.get(url, params=params, headers=headers, timeout=120)
        except (requests.exceptions.ConnectionError,
                requests.exceptions.Timeout) as exc:
            if attempt == 2:
                print(f"\n  Network error on page {page} after 2 attempts — "
                      f"treating as failed page. ({exc})")
                return None
            print(f"\n  Network error on page {page}, retrying in {RETRY_DELAY}s …")
            time.sleep(RETRY_DELAY)
            continue

        if r.status_code == 401:
            raise PermissionError(
                "DBRepo 401 — set DBREPO_USERNAME / DBREPO_PASSWORD.")
        if r.status_code == 403:
            raise PermissionError(
                "DBRepo 403 — account lacks READ access to this view.")
        if r.status_code == 404:
            raise LookupError(
                f"DBRepo 404 — view/database not found. "
                f"DB={DATABASE_ID} VIEW={VIEW_ID}")
        if r.status_code == 409:
            raise RuntimeError("DBRepo 409 — view schema could not be mapped.")
        if r.status_code == 400:
            raise ValueError(
                f"DBRepo 400 on page {page}: {r.text[:300]}")

        if r.status_code in (500, 502, 503, 504):
            if attempt == 2:
                print(f"\n  Server error HTTP {r.status_code} on page {page} "
                      f"after 2 attempts — treating as failed page.")
                return None
            print(f"\n  Server error HTTP {r.status_code} on page {page} "
                  f"(attempt {attempt}/2), retrying in {RETRY_DELAY}s …")
            time.sleep(RETRY_DELAY)
            continue

        if not r.ok:
            raise requests.HTTPError(
                f"Unexpected HTTP {r.status_code} on page {page}: {r.text[:200]}")

        return r.json()

    return None


def _extract_rows(page_data) -> list:
    if isinstance(page_data, list):
        return page_data
    if isinstance(page_data, dict):
        return (page_data.get("content")
                or page_data.get("data")
                or page_data.get("results")
                or [])
    return []


def get_total_count(session) -> int:
    url = (f"{DBREPO_BASE_URL}/api/v1/database/{DATABASE_ID}"
           f"/view/{VIEW_ID}/data")
    r = session.head(url, timeout=30)
    if r.status_code == 200:
        try:
            return int(r.headers["X-Count"])
        except (KeyError, ValueError):
            raise RuntimeError(f"HEAD missing X-Count. Headers: {dict(r.headers)}")
    raise RuntimeError(f"HEAD failed with status {r.status_code}.")


# ─────────────────────────────────────────────
# 1. LOAD DATA FROM DBREPO API
# ─────────────────────────────────────────────
print("Connecting to DBRepo REST API …")
print(f"  Base URL   : {DBREPO_BASE_URL}")
print(f"  Database ID: {DATABASE_ID}")
print(f"  View       : collision_ml_features ({VIEW_ID})")

if not DBREPO_USER:
    print("\n  DBREPO_USERNAME not set.")
    print('   PowerShell: $env:DBREPO_USERNAME="u"; $env:DBREPO_PASSWORD="p"')

session = requests.Session()
if DBREPO_USER:
    session.auth = (DBREPO_USER, DBREPO_PASSWORD)

try:
    expected_total = get_total_count(session)
    print(f"  Total rows expected (HEAD): {expected_total:,}")
except Exception as exc:
    print(f"    HEAD failed: {exc}")
    expected_total = None

all_rows = []
page     = 0
print()

while True:
    if expected_total and len(all_rows) >= expected_total:
        print(f"\n  Reached expected total ({expected_total:,}). Stopping.")
        break

    print(f"  Fetching page {page} … (rows so far: {len(all_rows):,})    ",
          end="\r")

    page_data = _fetch_page(session, page=page)

    if page_data is None:
        print(f"  Page {page} failed. Checking page {page + 1} …")
        next_data = _fetch_page(session, page=page + 1)

        if next_data is None:
            print(f"  Page {page + 1} also failed. "
                  f"Stopping with {len(all_rows):,} rows collected.")
            break

        print(f"  Page {page} skipped. Resuming from page {page + 1}.")
        rows = _extract_rows(next_data)
        if rows:
            all_rows.extend(rows)
        page += 2  
        time.sleep(0.2)
        continue

    rows = _extract_rows(page_data)

    if not rows:
        print(f"\n  Page {page} returned 0 rows — pagination complete.")
        break

    all_rows.extend(rows)
    page += 1
    time.sleep(0.2)

print(f"\nRows collected (before dedup): {len(all_rows):,}")
df = pd.DataFrame(all_rows)
before = len(df)
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)
after = len(df)
if before != after:
    print(f"Dropped {before - after:,} duplicate rows.")

print(f"Unique rows: {after:,}")
if expected_total:
    diff = after - expected_total
    sign = "+" if diff > 0 else ""
    print(f"Coverage: {after:,} / {expected_total:,} "
          f"({after / expected_total * 100:.1f}%  {sign}{diff:,}).")

print(f"Raw shape from API: {df.shape}")
if df.empty:
    raise RuntimeError("The DBRepo API returned no data.")


# ─────────────────────────────────────────────
# 2. SELECT FEATURES & LABEL
# ─────────────────────────────────────────────
available_cols = df.columns.tolist()
missing = [c for c in FEATURES + [LABEL] if c not in available_cols]
if missing:
    raise KeyError(f"Missing columns: {missing}\nAvailable: {available_cols}")

df = df[FEATURES + [LABEL]].copy()
print(f"After column selection: {df.shape}")


# ─────────────────────────────────────────────
# 3. CLEAN DATA
# ─────────────────────────────────────────────
for col in FEATURES + [LABEL]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df.replace([-1, -1.0], np.nan, inplace=True)
df.dropna(inplace=True)
df[LABEL] = df[LABEL].map(SEVERITY_MAP)

print(f"After cleaning: {df.shape}")
print("\nClass distribution:")
print(df[LABEL].value_counts())
print("\nClass percentages:")
print((df[LABEL].value_counts(normalize=True) * 100).round(1))


# ─────────────────────────────────────────────
# 4. DATA UNDERSTANDING – HISTOGRAMS
# ─────────────────────────────────────────────
print("\nGenerating data exploration plots...")

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
fig.suptitle("Data Understanding – Feature Distributions", fontsize=16)

ax = axes[0, 0]
counts = df[LABEL].value_counts().reindex(ORDER)
bars = ax.bar(ORDER, counts.values,
              color=[SEV_COLORS[c] for c in ORDER],
              edgecolor="white", linewidth=0.8)
ax.set_title("Accident Severity Distribution (Label)")
ax.set_xlabel("Severity"); ax.set_ylabel("Count")
for bar, val in zip(bars, counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300,
            f"{val:,}", ha="center", va="bottom", fontsize=10)

ax = axes[0, 1]
df["speed_limit"].value_counts().sort_index().plot(
    kind="bar", ax=ax, color="#3498db", edgecolor="white")
ax.set_title("Speed Limit Distribution")
ax.set_xlabel("Speed Limit (mph)"); ax.set_ylabel("Count")
ax.tick_params(axis="x", rotation=0)

ax = axes[0, 2]
cross = pd.crosstab(df["urban_or_rural_id"], df[LABEL])
for col in ORDER:
    if col not in cross.columns: cross[col] = 0
cross = cross[ORDER]
cross.index = ["Urban" if i == 1 else "Rural" for i in cross.index]
cross.plot(kind="bar", ax=ax, color=[SEV_COLORS[c] for c in ORDER], edgecolor="white")
ax.set_title("Severity by Urban / Rural Area")
ax.set_xlabel("Area Type"); ax.set_ylabel("Count")
ax.tick_params(axis="x", rotation=0); ax.legend(title="Severity")

ax = axes[1, 0]
light_map = {1: "Daylight", 4: "Dark-lit", 5: "Dark-unlit",
             6: "Dark-no light", 7: "Dark-unknown"}
df["light_label"] = df["light_conditions"].map(light_map).fillna("Other")
cross2 = pd.crosstab(df["light_label"], df[LABEL])
for col in ORDER:
    if col not in cross2.columns: cross2[col] = 0
cross2[ORDER].plot(kind="bar", ax=ax, color=[SEV_COLORS[c] for c in ORDER], edgecolor="white")
ax.set_title("Severity by Light Conditions")
ax.set_xlabel("Light Condition"); ax.set_ylabel("Count")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right"); ax.legend(title="Severity")

ax = axes[1, 1]
df["number_of_casualties"].value_counts().sort_index().head(8).plot(
    kind="bar", ax=ax, color="#9b59b6", edgecolor="white")
ax.set_title("Number of Casualties per Accident")
ax.set_xlabel("Casualties"); ax.set_ylabel("Count")
ax.tick_params(axis="x", rotation=0)

ax = axes[1, 2]
road_map = {1: "Roundabout", 2: "One way", 3: "Dual c/way",
            6: "Single c/way", 7: "Slip road", 12: "One way/slip"}
df["road_label"] = df["road_type"].map(road_map).fillna("Other")
cross3 = pd.crosstab(df["road_label"], df[LABEL])
for col in ORDER:
    if col not in cross3.columns: cross3[col] = 0
cross3[ORDER].plot(kind="bar", ax=ax, color=[SEV_COLORS[c] for c in ORDER], edgecolor="white")
ax.set_title("Severity by Road Type")
ax.set_xlabel("Road Type"); ax.set_ylabel("Count")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right"); ax.legend(title="Severity")

plt.tight_layout()
plt.savefig("outputs/figures/01_data_understanding.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: outputs/figures/01_data_understanding.png")
df.drop(columns=["light_label", "road_label"], inplace=True)


# ─────────────────────────────────────────────
# 5. TRAIN / VALIDATION / TEST SPLIT
# ─────────────────────────────────────────────
X = df[FEATURES]
y = df[LABEL]

X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.50, random_state=42, stratify=y_temp
)

print(f"\nTrain size     : {len(X_train):,}")
print(f"Validation size: {len(X_val):,}")
print(f"Test size      : {len(X_test):,}")

train_df = X_train.copy(); train_df[LABEL] = y_train.values
val_df   = X_val.copy();   val_df[LABEL]   = y_val.values
test_df  = X_test.copy();  test_df[LABEL]  = y_test.values

train_df.to_csv("data/processed/train.csv", index=False)
val_df.to_csv("data/processed/validation.csv", index=False)
test_df.to_csv("data/processed/test.csv", index=False)

print("\nSaved splits:")
print(f"  data/processed/train.csv      — {len(train_df):,} rows")
print(f"  data/processed/validation.csv — {len(val_df):,} rows")
print(f"  data/processed/test.csv       — {len(test_df):,} rows")
print("\n 01_load_data.py (API version) complete — run 02_preprocess.py next.")
