# Fraud Detection using CNN + Behavioral Analysis

This project demonstrates a fraud detection pipeline matching the architecture:
User → Payment Page → Feature Extraction (behavioral + transactional) → CNN model → Fraud result → Real-time blocking

## Quick start (local)

1. Create virtualenv and install:
   ```bash
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Train model:
   ```bash
   python train.py
   ```

3. Start API:
   ```bash
   python src/fraud_api.py
   ```

4. (Optional) Run dashboard:
   ```bash
   streamlit run dashboard/dashboard_app.py
   ```

Files:
- `train.py` - training script (saves model to `models/cnn_fraud_model.h5`)
- `src/` - application code (preprocessing, model, API, behavior sim)
- `dashboard/` - Streamlit monitoring app
