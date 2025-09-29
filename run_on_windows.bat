@echo off
title Fraud Detection CNN Project
echo ==============================
echo Fraud Detection CNN Project
echo ==============================

REM Step 1: Go to project folder
cd /d %~dp0

REM Step 2: Create venv if not exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Step 3: Activate venv
call venv\Scripts\activate.bat

REM Step 4: Install requirements
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

REM Step 5: Train the model
echo Training model...
python train.py

REM Step 6: Start the API in new terminal
echo Starting Flask Fraud Detection API...
start cmd /k "call venv\Scripts\activate.bat && python src\fraud_api.py"

REM Step 7: Start the dashboard in new terminal
echo Starting Streamlit dashboard...
start cmd /k "call venv\Scripts\activate.bat && streamlit run dashboard\dashboard_app.py"

REM Step 8: Auto-test a sample transaction after short delay
echo Waiting 10 seconds for API to start...
timeout /t 10 >nul
echo Running sample fraud test transaction...
start cmd /k "call venv\Scripts\activate.bat && python src\realtime_block.py"

echo ==============================
echo Project is running!
echo API:       http://127.0.0.1:5000/predict
echo Dashboard: http://localhost:8501
echo ==============================

pause
