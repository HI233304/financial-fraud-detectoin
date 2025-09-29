import requests, json
sample = {
    "amount": 12000,
    "time_delta": 40000,
    "typing_speed_ms": 120,
    "device_trust": 0.12,
    "is_night": 1,
    "merchant_cat": "luxury",
    "country": "US"
}
try:
    resp = requests.post("http://127.0.0.1:5000/predict", json=sample, timeout=10)
    print(resp.json())
    if resp.ok and resp.json().get("fraud"):
        print("BLOCK TRANSACTION")
    else:
        print("ALLOW TRANSACTION")
except Exception as e:
    print("Error calling API:", e)
