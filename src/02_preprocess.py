"""
02_preprocess.py
================
Reads the training split produced by 01_load_data.py, applies SMOTE to
balance the class distribution, saves the resampled training set, and
plots the class imbalance before vs. after SMOTE.

Inputs:
  data/processed/train.csv

Outputs:
  data/processed/train_resampled.csv
  outputs/figures/02_class_imbalance.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings("ignore")

# ── Folder setup ──────────────────────────────
os.makedirs("data/processed", exist_ok=True)
os.makedirs("outputs/figures", exist_ok=True)

# ── Constants ─────────────────────────────────
LABEL      = "collision_severity"
SEV_COLORS = {"Fatal": "#e74c3c", "Serious": "#e67e22", "Slight": "#2ecc71"}
ORDER      = ["Fatal", "Serious", "Slight"]


# ─────────────────────────────────────────────
# 1. LOAD TRAINING SPLIT
# ─────────────────────────────────────────────
print("Loading training split...")
train_df = pd.read_csv("data/processed/train.csv")
FEATURES = [c for c in train_df.columns if c != LABEL]

X_train = train_df[FEATURES]
y_train = train_df[LABEL]

print(f"Train shape: {train_df.shape}")
print("\nClass distribution before SMOTE:")
print(y_train.value_counts())


# ─────────────────────────────────────────────
# 2. SMOTE – OVERSAMPLE TRAINING SET ONLY
# ─────────────────────────────────────────────
print("\nApplying SMOTE to balance training classes...")
before_counts = y_train.value_counts().reindex(ORDER)

smote = SMOTE(random_state=42)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

after_counts = pd.Series(y_train_res).value_counts().reindex(ORDER)

print(f"Resampled train size: {len(X_train_res):,}")
print("New training distribution:")
print(pd.Series(y_train_res).value_counts())

train_res_df = pd.DataFrame(X_train_res, columns=FEATURES)
train_res_df[LABEL] = y_train_res.values
train_res_df.to_csv("data/processed/train_resampled.csv", index=False)
print(f"\nSaved: data/processed/train_resampled.csv — {len(train_res_df):,} rows")


# ─────────────────────────────────────────────
# 3. PLOT CLASS IMBALANCE BEFORE vs AFTER SMOTE
# ─────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Class Imbalance: Before vs After SMOTE", fontsize=15)

ax = axes[0]
bars = ax.bar(ORDER, before_counts.values,
              color=[SEV_COLORS[c] for c in ORDER], edgecolor="white")
ax.set_title("Before SMOTE (Original Training Set)")
ax.set_xlabel("Severity Class")
ax.set_ylabel("Number of Samples")
ax.set_ylim(0, before_counts.max() * 1.25)
for bar, val in zip(bars, before_counts.values):
    pct = val / before_counts.sum() * 100
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
            f"{val:,}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=10)

ax = axes[1]
bars = ax.bar(ORDER, after_counts.values,
              color=[SEV_COLORS[c] for c in ORDER], edgecolor="white")
ax.set_title("After SMOTE (Resampled Training Set)")
ax.set_xlabel("Severity Class")
ax.set_ylabel("Number of Samples")
ax.set_ylim(0, after_counts.max() * 1.25)
for bar, val in zip(bars, after_counts.values):
    pct = val / after_counts.sum() * 100
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
            f"{val:,}\n({pct:.1f}%)", ha="center", va="bottom", fontsize=10)

plt.tight_layout()
plt.savefig("outputs/figures/02_class_imbalance.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: outputs/figures/02_class_imbalance.png")
print("\n✅ 02_preprocess.py complete — run 03_train_classifier.py next.")
