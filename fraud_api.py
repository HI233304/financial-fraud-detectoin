from flask import Flask, request, jsonify
import joblib
import tensorflow as tf
import numpy as np
from pathlib import Path

app = Flask(__name__)

MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "cnn_fraud_model.h5"
PRE_PATH = Path(__file__).resolve().parent.parent / "models" / "preprocessor.joblib"

_model = None
_pre = None

def load_artifacts():
    global _model, _pre
    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH)
    if _pre is None:
        _pre = joblib.load(PRE_PATH)
    return _model, _pre

def preprocess_input(data: dict):
    order = ["amount","time_delta","typing_speed_ms","device_trust","is_night","merchant_cat","country"]
    arr = [data.get(k, 0) for k in order]
    import pandas as pd
    df = pd.DataFrame([arr], columns=order)
    return df

@app.route("/predict", methods=["POST"])
def predict():
    model, pre = load_artifacts()
    data = request.json
    if not data:
        return jsonify({"error":"No JSON payload provided"}), 400
    df = preprocess_input(data)
    Xp = pre.transform(df)
    prob = float(model.predict(Xp).ravel()[0])
    return jsonify({"fraud_probability": prob, "fraud": prob>0.5})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
