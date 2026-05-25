"""
03_train_classifier.py
======================
Trains three classifiers (Decision Tree, Random Forest, Gradient Boosting)
on the SMOTE-resampled training set, selects the best model by Macro F1
on the validation set, evaluates it on the test set, saves the model
artefact, and plots the model comparison chart.

Inputs:
  data/processed/train_resampled.csv
  data/processed/validation.csv
  data/processed/test.csv

Outputs:
  outputs/models/<algorithm>_severity_<date>.pkl
  outputs/figures/04_performance_comparison.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
from datetime import date
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score, f1_score
import warnings
warnings.filterwarnings("ignore")

# ── Folder setup ──────────────────────────────
os.makedirs("outputs/models", exist_ok=True)
os.makedirs("outputs/figures", exist_ok=True)

# ── Constants ─────────────────────────────────
LABEL  = "collision_severity"
ORDER  = ["Fatal", "Serious", "Slight"]


# ─────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────
print("Loading processed splits...")
train_res_df = pd.read_csv("data/processed/train_resampled.csv")
val_df       = pd.read_csv("data/processed/validation.csv")
test_df      = pd.read_csv("data/processed/test.csv")

FEATURES = [c for c in train_res_df.columns if c != LABEL]

X_train_res = train_res_df[FEATURES]
y_train_res = train_res_df[LABEL]
X_val       = val_df[FEATURES]
y_val       = val_df[LABEL]
X_test      = test_df[FEATURES]
y_test      = test_df[LABEL]

print(f"  Resampled train : {len(X_train_res):,} rows")
print(f"  Validation      : {len(X_val):,} rows")
print(f"  Test            : {len(X_test):,} rows")


# ─────────────────────────────────────────────
# 2. TRAIN THREE MODELS
# ─────────────────────────────────────────────
print("\nTraining models (this may take a minute)...")

models = {
    "Decision Tree": DecisionTreeClassifier(
        max_depth=15,
        class_weight="balanced",
        random_state=42
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1
    ),
    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=150,
        max_depth=6,
        learning_rate=0.1,
        random_state=42
    ),
}

val_f1_scores  = {}
val_acc_scores = {}
for name, model in models.items():
    print(f"  Training {name}...")
    model.fit(X_train_res, y_train_res)
    y_val_pred = model.predict(X_val)
    macro_f1   = f1_score(y_val, y_val_pred, average="macro")
    acc        = accuracy_score(y_val, y_val_pred)
    val_f1_scores[name]  = macro_f1
    val_acc_scores[name] = acc
    print(f"  → Macro F1: {macro_f1:.3f} | Accuracy: {acc:.3f}")

best_model_name = max(val_f1_scores, key=val_f1_scores.get)
best_model      = models[best_model_name]
print(f"\nBest model (Macro F1): {best_model_name}")


# ─────────────────────────────────────────────
# 3. EVALUATE BEST MODEL ON TEST SET
# ─────────────────────────────────────────────
y_pred        = best_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)
test_macro_f1 = f1_score(y_test, y_pred, average="macro")

print(f"\nTest Accuracy : {test_accuracy:.3f}")
print(f"Test Macro F1 : {test_macro_f1:.3f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# ─────────────────────────────────────────────
# 4. SAVE MODEL ARTEFACT
# ─────────────────────────────────────────────
model_filename = (
    f"outputs/models/"
    f"{best_model_name.lower().replace(' ', '_')}"
    f"_severity_{date.today()}.pkl"
)
joblib.dump(best_model, model_filename)
print(f"\nSaved model artefact: {model_filename}")

# --- EXTRACT AND SAVE PREDICTIONS HERE ---
print("Saving model predictions...")

predictions_df = X_test.copy()

predictions_df["actual_severity"] = y_test
predictions_df["predicted_severity"] = y_pred

pred_filename = f"outputs/predictions/test_predictions_{date.today()}.csv"
predictions_df.to_csv(pred_filename, index=False)

print(f"Saved predictions to: {pred_filename}")


# ─────────────────────────────────────────────
# 5. PERFORMANCE COMPARISON CHART (validation)
# ─────────────────────────────────────────────
print("Generating performance comparison chart...")

report    = classification_report(y_test, y_pred, output_dict=True)
precision = [report[c]["precision"] for c in ORDER]
recall    = [report[c]["recall"]    for c in ORDER]
f1_vals   = [report[c]["f1-score"]  for c in ORDER]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle(f"Model Performance – {best_model_name}", fontsize=15)

# Left: per-class metrics on test set
x     = np.arange(len(ORDER))
width = 0.25
ax    = axes[0]
ax.bar(x - width, precision, width, label="Precision", color="#3498db", edgecolor="white")
ax.bar(x,         recall,    width, label="Recall",    color="#e67e22", edgecolor="white")
ax.bar(x + width, f1_vals,   width, label="F1-Score",  color="#2ecc71", edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels(ORDER)
ax.set_ylim(0, 1.15)
ax.set_title("Precision / Recall / F1 per Severity Class")
ax.set_ylabel("Score")
ax.legend()
for i, (p, r, f) in enumerate(zip(precision, recall, f1_vals)):
    ax.text(i - width, p + 0.02, f"{p:.2f}", ha="center", fontsize=9)
    ax.text(i,         r + 0.02, f"{r:.2f}", ha="center", fontsize=9)
    ax.text(i + width, f + 0.02, f"{f:.2f}", ha="center", fontsize=9)

# Right: model comparison on validation set
ax2          = axes[1]
model_names  = list(val_f1_scores.keys())
f1_vals_val  = list(val_f1_scores.values())
acc_vals_val = list(val_acc_scores.values())
x2 = np.arange(len(model_names))
w2 = 0.35
bar_colors_f1  = ["#2ecc71" if n == best_model_name else "#3498db" for n in model_names]
bar_colors_acc = ["#27ae60" if n == best_model_name else "#2980b9" for n in model_names]
b1 = ax2.bar(x2 - w2/2, f1_vals_val,  w2, label="Macro F1",
             color=bar_colors_f1, edgecolor="white")
b2 = ax2.bar(x2 + w2/2, acc_vals_val, w2, label="Accuracy",
             color=bar_colors_acc, edgecolor="white")
ax2.set_xticks(x2)
ax2.set_xticklabels(model_names, fontsize=9)
ax2.set_ylim(0, 1.05)
ax2.set_title("Model Comparison (Validation Set)")
ax2.set_ylabel("Score")
ax2.legend()
for bar, val in zip(list(b1) + list(b2), f1_vals_val + acc_vals_val):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
             f"{val:.2f}", ha="center", fontsize=9, fontweight="bold")

plt.tight_layout()
plt.savefig("outputs/figures/04_performance_comparison.png", dpi=150, bbox_inches="tight")
plt.close()
print("Saved: outputs/figures/04_performance_comparison.png")

print("\n 03_train_classifier.py complete — run 04_evaluate.py next.")
