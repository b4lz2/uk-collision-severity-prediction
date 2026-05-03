"""
04_evaluate.py
==============
Loads the best saved model artefact and the test split, then generates
the confusion matrix and feature importance plots.

Inputs:
  data/processed/test.csv
  outputs/models/<latest>.pkl   (most recently saved model)

Outputs:
  outputs/figures/03_confusion_matrix.png
  outputs/figures/05_feature_importance.png
"""

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import joblib
from sklearn.metrics import (
    confusion_matrix, ConfusionMatrixDisplay,
    accuracy_score, f1_score
)
import warnings
warnings.filterwarnings("ignore")

# ── Folder setup ──────────────────────────────
os.makedirs("outputs/figures", exist_ok=True)

# ── Constants ─────────────────────────────────
LABEL      = "collision_severity"
ORDER      = ["Fatal", "Serious", "Slight"]
SEV_COLORS = {"Fatal": "#e74c3c", "Serious": "#e67e22", "Slight": "#2ecc71"}


# ─────────────────────────────────────────────
# 1. LOAD TEST DATA
# ─────────────────────────────────────────────
print("Loading test split...")
test_df  = pd.read_csv("data/processed/test.csv")
FEATURES = [c for c in test_df.columns if c != LABEL]
X_test   = test_df[FEATURES]
y_test   = test_df[LABEL]
print(f"Test shape: {test_df.shape}")


# ─────────────────────────────────────────────
# 2. LOAD BEST MODEL
# ─────────────────────────────────────────────
model_files = sorted(glob.glob("outputs/models/*.pkl"))
if not model_files:
    raise FileNotFoundError(
        "No model artefact found in outputs/models/. "
        "Run 03_train_classifier.py first."
    )
model_path = model_files[-1]   # most recently saved
print(f"Loading model: {model_path}")
best_model      = joblib.load(model_path)
best_model_name = os.path.basename(model_path).split("_severity_")[0].replace("_", " ").title()


# ─────────────────────────────────────────────
# 3. PREDICT & SCORE
# ─────────────────────────────────────────────
y_pred        = best_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)
test_macro_f1 = f1_score(y_test, y_pred, average="macro")

print(f"\nTest Accuracy : {test_accuracy:.3f}")
print(f"Test Macro F1 : {test_macro_f1:.3f}")


# ─────────────────────────────────────────────
# 4. CONFUSION MATRIX
# ─────────────────────────────────────────────
print("\nGenerating confusion matrix...")

fig, ax = plt.subplots(figsize=(8, 7))
cm   = confusion_matrix(y_test, y_pred, labels=ORDER)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=ORDER)
disp.plot(ax=ax, colorbar=True, cmap="Blues")
ax.set_title(
    f"Confusion Matrix – {best_model_name}\n"
    f"Accuracy: {test_accuracy:.1%}  |  Macro F1: {test_macro_f1:.3f}",
    fontsize=12
)
plt.tight_layout()
plt.savefig("outputs/figures/03_confusion_matrix.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: outputs/figures/03_confusion_matrix.png")


# ─────────────────────────────────────────────
# 5. FEATURE IMPORTANCE
# ─────────────────────────────────────────────
print("Generating feature importance chart...")

if hasattr(best_model, "feature_importances_"):
    importances = best_model.feature_importances_
    feat_imp    = pd.Series(importances, index=FEATURES).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 7))
    colors  = ["#2ecc71" if v >= feat_imp.median() else "#3498db"
               for v in feat_imp.values]
    feat_imp.plot(kind="barh", ax=ax, color=colors, edgecolor="white")
    ax.set_title(f"Feature Importance – {best_model_name}", fontsize=13)
    ax.set_xlabel("Importance Score")
    ax.axvline(x=feat_imp.median(), color="gray", linestyle="--", linewidth=0.8)
    high_patch = mpatches.Patch(color="#2ecc71", label="Above median importance")
    low_patch  = mpatches.Patch(color="#3498db", label="Below median importance")
    ax.legend(handles=[high_patch, low_patch])
    plt.tight_layout()
    plt.savefig("outputs/figures/05_feature_importance.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("Saved: outputs/figures/05_feature_importance.png")
else:
    print(f"  Note: {best_model_name} does not expose feature_importances_ — skipping plot.")

print("\n✅ 04_evaluate.py complete.")
print("\nSummary:")
print(f"  Model        : {best_model_name}")
print(f"  Test Accuracy: {test_accuracy:.1%}")
print(f"  Test Macro F1: {test_macro_f1:.3f}")
