import os
from pathlib import Path
import numpy as np
import joblib
from src.preprocess import load_data, build_preprocessor, prepare_xy
from src.cnn_model import build_mlp, get_earlystop
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report

# ============================
# Paths
# ============================
DATA = "data/sample_transactions.csv"
OUT_DIR = Path("models")
OUT_DIR.mkdir(exist_ok=True)

# ============================
# Load + Preprocess Data
# ============================
df = load_data(DATA)

# Prepare features (X) and labels (y)
X, y = prepare_xy(df)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Build preprocessing pipeline
pre, _, _ = build_preprocessor(df)
pre.fit(X_train)

# Transform features
Xtr = pre.transform(X_train)
Xte = pre.transform(X_test)

# ============================
# Build & Train Model
# ============================
model = build_mlp(Xtr.shape[1])
es = get_earlystop()

model.fit(
    Xtr,
    y_train,
    validation_split=0.1,
    epochs=50,
    batch_size=64,
    callbacks=[es],
    verbose=2
)

# ============================
# Save Model & Preprocessor
# ============================
model.save(OUT_DIR / "cnn_fraud_model.h5")
joblib.dump(pre, OUT_DIR / "preprocessor.joblib")

# ============================
# Evaluation
# ============================
y_score = model.predict(Xte).ravel()
auc = roc_auc_score(y_test, y_score)

print("\n=======================")
print("✅ Training complete")
print("Test ROC AUC:", auc)
print(classification_report(y_test, (y_score >= 0.5).astype(int)))
print("=======================\n")
