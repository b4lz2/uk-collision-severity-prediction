"""
01_load_data.py
===============
Loads the raw UK collision dataset, selects relevant features, cleans the
data, generates data-understanding plots, and saves train/validation/test
splits to data/processed/.

Inputs:
  data/raw/dft-road-casualty-statistics-collision-last-5-years.csv

Outputs:
  data/processed/train.csv
  data/processed/validation.csv
  data/processed/test.csv
  outputs/figures/01_data_understanding.png
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")

# ── Folder setup ──────────────────────────────
os.makedirs("data/processed", exist_ok=True)
os.makedirs("outputs/figures", exist_ok=True)

# ── Constants ─────────────────────────────────
FILE_PATH = "data/raw/dft-road-casualty-statistics-collision-last-5-years.csv"
LABEL     = "collision_severity"
FEATURES  = [
    "speed_limit",
    "light_conditions",
    "weather_conditions",
    "road_surface_conditions",
    "road_type",
    "urban_or_rural_area",
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


# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
print("Loading dataset...")
df = pd.read_csv(FILE_PATH, low_memory=False)
print(f"Raw shape: {df.shape}")


# ─────────────────────────────────────────────
# 2. SELECT FEATURES & LABEL
# ─────────────────────────────────────────────
df = df[FEATURES + [LABEL]].copy()
print(f"After column selection: {df.shape}")


# ─────────────────────────────────────────────
# 3. CLEAN DATA
# ─────────────────────────────────────────────
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

# Plot 1: Label distribution
ax = axes[0, 0]
counts = df[LABEL].value_counts().reindex(ORDER)
bars = ax.bar(ORDER, counts.values,
              color=[SEV_COLORS[c] for c in ORDER],
              edgecolor="white", linewidth=0.8)
ax.set_title("Accident Severity Distribution (Label)")
ax.set_xlabel("Severity")
ax.set_ylabel("Count")
for bar, val in zip(bars, counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 300,
            f"{val:,}", ha="center", va="bottom", fontsize=10)

# Plot 2: Speed limit distribution
ax = axes[0, 1]
df["speed_limit"].value_counts().sort_index().plot(
    kind="bar", ax=ax, color="#3498db", edgecolor="white")
ax.set_title("Speed Limit Distribution")
ax.set_xlabel("Speed Limit (mph)")
ax.set_ylabel("Count")
ax.tick_params(axis="x", rotation=0)

# Plot 3: Severity by urban/rural
ax = axes[0, 2]
cross = pd.crosstab(df["urban_or_rural_area"], df[LABEL])
for col in ORDER:
    if col not in cross.columns:
        cross[col] = 0
cross = cross[ORDER]
cross.index = ["Urban" if i == 1 else "Rural" for i in cross.index]
cross.plot(kind="bar", ax=ax,
           color=[SEV_COLORS[c] for c in ORDER], edgecolor="white")
ax.set_title("Severity by Urban / Rural Area")
ax.set_xlabel("Area Type")
ax.set_ylabel("Count")
ax.tick_params(axis="x", rotation=0)
ax.legend(title="Severity")

# Plot 4: Severity by light conditions
ax = axes[1, 0]
light_map = {1: "Daylight", 4: "Dark-lit", 5: "Dark-unlit",
             6: "Dark-no light", 7: "Dark-unknown"}
df["light_label"] = df["light_conditions"].map(light_map).fillna("Other")
cross2 = pd.crosstab(df["light_label"], df[LABEL])
for col in ORDER:
    if col not in cross2.columns:
        cross2[col] = 0
cross2[ORDER].plot(kind="bar", ax=ax,
                   color=[SEV_COLORS[c] for c in ORDER], edgecolor="white")
ax.set_title("Severity by Light Conditions")
ax.set_xlabel("Light Condition")
ax.set_ylabel("Count")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
ax.legend(title="Severity")

# Plot 5: Number of casualties distribution
ax = axes[1, 1]
df["number_of_casualties"].value_counts().sort_index().head(8).plot(
    kind="bar", ax=ax, color="#9b59b6", edgecolor="white")
ax.set_title("Number of Casualties per Accident")
ax.set_xlabel("Casualties")
ax.set_ylabel("Count")
ax.tick_params(axis="x", rotation=0)

# Plot 6: Severity by road type
ax = axes[1, 2]
road_map = {1: "Roundabout", 2: "One way", 3: "Dual c/way",
            6: "Single c/way", 7: "Slip road", 12: "One way/slip"}
df["road_label"] = df["road_type"].map(road_map).fillna("Other")
cross3 = pd.crosstab(df["road_label"], df[LABEL])
for col in ORDER:
    if col not in cross3.columns:
        cross3[col] = 0
cross3[ORDER].plot(kind="bar", ax=ax,
                   color=[SEV_COLORS[c] for c in ORDER], edgecolor="white")
ax.set_title("Severity by Road Type")
ax.set_xlabel("Road Type")
ax.set_ylabel("Count")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
ax.legend(title="Severity")

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
print("\n✅ 01_load_data.py complete — run 02_preprocess.py next.")
