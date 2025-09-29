import streamlit as st
import requests

API_URL = "http://127.0.0.1:5000/predict"

# ==============================
# Authentication (Dummy Users)
# ==============================
USERS = {
    "himanshu": "1234",
    "admin": "admin"
}

# ==============================
# Login Page
# ==============================
def login():
    st.title("🔐 Bank Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success("Login successful ✅")
            st.experimental_rerun()
        else:
            st.error("Invalid username or password ❌")


# ==============================
# Transaction Page
# ==============================
def transaction_page():
    st.title("🏦 Bank Transaction")

    st.write(f"Welcome, **{st.session_state['user']}** 👋")

    # Transaction inputs
    amount = st.number_input("Enter Amount (₹)", min_value=1.0, step=1.0)
    card = st.text_input("Card Number (####-####-####-####)")
    merchant = st.text_input("Merchant")
    location = st.text_input("Location")

    if st.button("Submit Transaction"):
        # Dummy features (replace with real feature extraction later)
        features = [amount, len(card), len(merchant), len(location)]

        try:
            response = requests.post(API_URL, json={"features": features})
            result = response.json()

            if "error" in result:
                st.error("API Error: " + result["error"])
            else:
                fraud = result.get("prediction")
                prob = result.get("fraud_probability", 0)

                if fraud == "Fraudulent":
                    st.error(f"❌ BLOCK TRANSACTION — Fraud Probability: {prob:.2f}")
                else:
                    st.success(f"✅ ALLOW TRANSACTION — Fraud Probability: {prob:.2f}")

        except Exception as e:
            st.error(f"API Connection Failed: {e}")


# ==============================
# Main App
# ==============================
def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        login()
    else:
        transaction_page()


if __name__ == "__main__":
    main()

