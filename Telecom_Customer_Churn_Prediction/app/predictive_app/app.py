"""
Streamlit app: Telecom Customer Analytics — 4 live prediction models.
Run with: streamlit run app.py
(All model files must sit in ./models next to this app.py)
"""
import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")


def model_path(filename):
    return os.path.join(MODEL_DIR, filename)


st.set_page_config(page_title="Telecom Customer Analytics", layout="wide", page_icon="📡")
st.title("📡 Telecom Customer Analytics")
st.caption(
    "Enter a customer's profile once below, then use any of the 4 tabs to get a live "
    "prediction from that customer's data."
)

INTERNET_OPTIONS = ["Cable", "DSL", "Fiber Optic", "No Internet Service"]
OFFER_OPTIONS = ["No Offer", "Offer A", "Offer B", "Offer C", "Offer D", "Offer E"]
CONTRACT_OPTIONS = ["Month-to-Month", "One Year", "Two Year"]
PAYMENT_OPTIONS = ["Bank Withdrawal", "Credit Card", "Mailed Check"]

# ------------------------------------------------------------------
# Shared customer-profile form
# ------------------------------------------------------------------
with st.form("customer_profile"):
    st.subheader("Customer profile")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Demographics**")
        gender = st.selectbox("Gender", ["Female", "Male"])
        age = st.number_input("Age", min_value=18, max_value=100, value=40)
        married = st.selectbox("Married", ["No", "Yes"])
        dependents = st.number_input("Number of Dependents", min_value=0, max_value=10, value=0)
        st.markdown("**Location**")
        latitude = st.number_input("Latitude", value=34.0, format="%.4f")
        longitude = st.number_input("Longitude", value=-118.0, format="%.4f")
        population = st.number_input("ZIP population", min_value=0, value=25000, step=1000)

    with c2:
        st.markdown("**Services**")
        phone_service = st.selectbox("Phone Service", ["No", "Yes"])
        multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes"])
        internet_type = st.selectbox("Internet Type", INTERNET_OPTIONS, index=2)
        avg_gb = st.number_input("Avg Monthly GB Download", min_value=0.0, value=20.0)
        online_security = st.selectbox("Online Security", ["No", "Yes"])
        online_backup = st.selectbox("Online Backup", ["No", "Yes"])
        device_protection = st.selectbox("Device Protection Plan", ["No", "Yes"])
        premium_support = st.selectbox("Premium Tech Support", ["No", "Yes"])
        streaming_tv = st.selectbox("Streaming TV", ["No", "Yes"])
        streaming_music = st.selectbox("Streaming Music", ["No", "Yes"])
        unlimited_data = st.selectbox("Unlimited Data", ["No", "Yes"])

    with c3:
        st.markdown("**Account & billing**")
        offer = st.selectbox("Current Offer", OFFER_OPTIONS)
        contract = st.selectbox("Contract", CONTRACT_OPTIONS)
        payment_method = st.selectbox("Payment Method", PAYMENT_OPTIONS)
        paperless = st.selectbox("Paperless Billing", ["No", "Yes"])
        referrals = st.number_input("Number of Referrals", min_value=0, max_value=20, value=1)
        long_distance = st.number_input("Avg Monthly Long Distance Charges", min_value=0.0, value=15.0)
        monthly_charge = st.number_input("Monthly Charge ($)", min_value=0.0, value=65.0)
        discount_amount = st.number_input("Monthly Discount Amount ($, 0 if none)", min_value=0.0, value=0.0)
        total_refunds = st.number_input("Total Refunds to date ($)", min_value=0.0, value=0.0)
        extra_data_charges = st.number_input("Total Extra Data Charges to date ($)", min_value=0.0, value=0.0)

    submitted = st.form_submit_button("Save profile", use_container_width=True)

if submitted or "profile" in st.session_state:
    profile = {
        "gender": gender if submitted else st.session_state["profile"]["gender"],
        "age": age if submitted else st.session_state["profile"]["age"],
        "married": married if submitted else st.session_state["profile"]["married"],
        "dependents": dependents if submitted else st.session_state["profile"]["dependents"],
        "latitude": latitude if submitted else st.session_state["profile"]["latitude"],
        "longitude": longitude if submitted else st.session_state["profile"]["longitude"],
        "population": population if submitted else st.session_state["profile"]["population"],
        "phone_service": phone_service if submitted else st.session_state["profile"]["phone_service"],
        "multiple_lines": multiple_lines if submitted else st.session_state["profile"]["multiple_lines"],
        "internet_type": internet_type if submitted else st.session_state["profile"]["internet_type"],
        "avg_gb": avg_gb if submitted else st.session_state["profile"]["avg_gb"],
        "online_security": online_security if submitted else st.session_state["profile"]["online_security"],
        "online_backup": online_backup if submitted else st.session_state["profile"]["online_backup"],
        "device_protection": device_protection if submitted else st.session_state["profile"]["device_protection"],
        "premium_support": premium_support if submitted else st.session_state["profile"]["premium_support"],
        "streaming_tv": streaming_tv if submitted else st.session_state["profile"]["streaming_tv"],
        "streaming_music": streaming_music if submitted else st.session_state["profile"]["streaming_music"],
        "unlimited_data": unlimited_data if submitted else st.session_state["profile"]["unlimited_data"],
        "offer": offer if submitted else st.session_state["profile"]["offer"],
        "contract": contract if submitted else st.session_state["profile"]["contract"],
        "payment_method": payment_method if submitted else st.session_state["profile"]["payment_method"],
        "paperless": paperless if submitted else st.session_state["profile"]["paperless"],
        "referrals": referrals if submitted else st.session_state["profile"]["referrals"],
        "long_distance": long_distance if submitted else st.session_state["profile"]["long_distance"],
        "monthly_charge": monthly_charge if submitted else st.session_state["profile"]["monthly_charge"],
        "discount_amount": discount_amount if submitted else st.session_state["profile"]["discount_amount"],
        "total_refunds": total_refunds if submitted else st.session_state["profile"]["total_refunds"],
        "extra_data_charges": extra_data_charges if submitted else st.session_state["profile"]["extra_data_charges"],
    }
    st.session_state["profile"] = profile
else:
    st.info("Fill in the customer profile above and click **Save profile** to unlock the prediction tabs.")
    st.stop()


def yn(v):
    return 1 if v == "Yes" else 0


# ------------------------------------------------------------------
# Feature-row builders — mirror each notebook's exact encoding
# ------------------------------------------------------------------
def build_common_encoded(p):
    return {
        "Gender": 1 if p["gender"] == "Male" else 0,
        "Age": p["age"],
        "Married": yn(p["married"]),
        "Number_of_Dependents": p["dependents"],
        "Phone_Service": yn(p["phone_service"]),
        "Avg_Monthly_Long_Distance_Charges": p["long_distance"],
        "Multiple_Lines": yn(p["multiple_lines"]),
        "Avg_Monthly_GB_Download": p["avg_gb"],
        "Online_Security": yn(p["online_security"]),
        "Online_Backup": yn(p["online_backup"]),
        "Device_Protection_Plan": yn(p["device_protection"]),
        "Premium_Tech_Support": yn(p["premium_support"]),
        "Streaming_TV": yn(p["streaming_tv"]),
        "Streaming_Music": yn(p["streaming_music"]),
        "Unlimited_Data": yn(p["unlimited_data"]),
        "Number_of_Referrals": p["referrals"],
        "Paperless_Billing": yn(p["paperless"]),
        "Population": p["population"],
        "Internet_Type_Clean_DSL": 1 if p["internet_type"] == "DSL" else 0,
        "Offer_Clean_Offer_A": 1 if p["offer"] == "Offer A" else 0,
        "Offer_Clean_Offer_B": 1 if p["offer"] == "Offer B" else 0,
        "Offer_Clean_Offer_C": 1 if p["offer"] == "Offer C" else 0,
        "Offer_Clean_Offer_D": 1 if p["offer"] == "Offer D" else 0,
        "Offer_Clean_Offer_E": 1 if p["offer"] == "Offer E" else 0,
        "Contract_One_Year": 1 if p["contract"] == "One Year" else 0,
        "Contract_Two_Year": 1 if p["contract"] == "Two Year" else 0,
        "Payment_Method_Credit_Card": 1 if p["payment_method"] == "Credit Card" else 0,
        "Payment_Method_Mailed_Check": 1 if p["payment_method"] == "Mailed Check" else 0,
    }


tab1, tab2, tab3, tab4 = st.tabs(
    ["🔻 Churn Prediction", "💰 Revenue Prediction", "🧩 Customer Segmentation", "🎁 Best Offer Prediction"]
)

# ------------------------------------------------------------------
# Tab 1: Churn Prediction
# ------------------------------------------------------------------
with tab1:
    st.write("Predicts the probability this customer churns, using the saved customer profile above.")
    if st.button("Predict churn probability", key="btn_churn"):
        model = joblib.load(model_path("churn_model.pkl"))
        train_columns = joblib.load(model_path("churn_model_columns.pkl"))
        row = build_common_encoded(st.session_state["profile"])
        row["Monthly_Discount_Amount"] = st.session_state["profile"]["discount_amount"]
        X = pd.DataFrame([row]).reindex(columns=train_columns, fill_value=0)
        prob = model.predict_proba(X)[0][1]
        st.metric("Churn probability", f"{prob:.1%}")
        if prob >= 0.5:
            st.warning("This customer is at **high risk** of churning.")
        else:
            st.success("This customer looks likely to **stay**.")

# ------------------------------------------------------------------
# Tab 2: Revenue Prediction
# ------------------------------------------------------------------
with tab2:
    st.write("Predicts this customer's total lifetime revenue so far, using the saved customer profile above.")
    if st.button("Predict total revenue", key="btn_revenue"):
        model = joblib.load(model_path("revenue_model.pkl"))
        train_columns = joblib.load(model_path("revenue_model_columns.pkl"))
        row = build_common_encoded(st.session_state["profile"])
        row["Total_Refunds"] = st.session_state["profile"]["total_refunds"]
        row["Total_Extra_Data_Charges"] = st.session_state["profile"]["extra_data_charges"]
        row["Monthly_Discount_Amount"] = st.session_state["profile"]["discount_amount"]
        X = pd.DataFrame([row]).reindex(columns=train_columns, fill_value=0)
        pred_revenue = model.predict(X)[0]
        st.metric("Predicted Total Revenue", f"${pred_revenue:,.2f}")

# ------------------------------------------------------------------
# Tab 3: Customer Segmentation
# ------------------------------------------------------------------
with tab3:
    st.write("Assigns this customer to one of 5 behavioral segments (K-Means, fit on the full customer base).")
    if st.button("Assign segment", key="btn_segment"):
        bundle = joblib.load(model_path("segmentation_model.pkl"))
        scaler, kmeans, feature_order = bundle["scaler"], bundle["kmeans"], bundle["feature_order"]
        p = st.session_state["profile"]
        row = {
            "Age": p["age"], "Number_of_Dependents": p["dependents"], "Latitude": p["latitude"],
            "Longitude": p["longitude"], "Avg_Monthly_GB_Download": p["avg_gb"],
            "Avg_Monthly_Long_Distance_Charges": p["long_distance"], "Number_of_Referrals": p["referrals"],
            "Monthly_Charge": p["monthly_charge"], "Monthly_Discount_Amount": p["discount_amount"],
        }
        X = pd.DataFrame([row])[feature_order]
        X_scaled = scaler.transform(X)
        cluster = int(kmeans.predict(X_scaled)[0])
        st.metric("Assigned segment", f"Cluster {cluster}")

        profile_df = pd.read_csv(model_path("cluster_profile.csv"))
        row_match = profile_df[profile_df["Cluster"] == cluster]
        if not row_match.empty:
            r = row_match.iloc[0]
            st.write("**Typical profile of this segment** (average across its members):")
            sc1, sc2, sc3, sc4 = st.columns(4)
            sc1.metric("Avg Age", f"{r['Age']:.0f}")
            sc2.metric("Avg Monthly GB Download", f"{r['Avg_Monthly_GB_Download']:.1f}")
            sc3.metric("Avg Monthly Charge ($)", f"{r['Monthly_Charge']:.2f}")
            sc4.metric("Avg Referrals", f"{r['Number_of_Referrals']:.1f}")
            st.caption(f"This segment has {int(r['Customer_Count'])} customers in the training data.")

        st.caption(
            "Segments were derived from Age, Dependents, Location, Avg GB Download, "
            "Long-Distance Charges, Referrals, Monthly Charge, and Discount Amount."
        )

# ------------------------------------------------------------------
# Tab 4: Best Offer Prediction
# ------------------------------------------------------------------
with tab4:
    st.write(
        "Simulates this customer's churn probability under each available offer, and "
        "recommends whichever offer minimizes it (uses this customer's segment from Tab 3's model)."
    )
    if st.button("Recommend best offer", key="btn_offer"):
        seg_bundle = joblib.load(model_path("segmentation_model.pkl"))
        scaler, kmeans, feature_order = seg_bundle["scaler"], seg_bundle["kmeans"], seg_bundle["feature_order"]
        p = st.session_state["profile"]
        seg_row = {
            "Age": p["age"], "Number_of_Dependents": p["dependents"], "Latitude": p["latitude"],
            "Longitude": p["longitude"], "Avg_Monthly_GB_Download": p["avg_gb"],
            "Avg_Monthly_Long_Distance_Charges": p["long_distance"], "Number_of_Referrals": p["referrals"],
            "Monthly_Charge": p["monthly_charge"], "Monthly_Discount_Amount": p["discount_amount"],
        }
        X_seg = pd.DataFrame([seg_row])[feature_order]
        cluster = int(kmeans.predict(scaler.transform(X_seg))[0])

        model = joblib.load(model_path("best_offer_churn_model.pkl"))
        train_columns = joblib.load(model_path("best_offer_model_columns.pkl"))
        base_row = build_common_encoded(p)
        base_row.pop("Offer_Clean_Offer_A", None)
        base_row.pop("Offer_Clean_Offer_B", None)
        base_row.pop("Offer_Clean_Offer_C", None)
        base_row.pop("Offer_Clean_Offer_D", None)
        base_row.pop("Offer_Clean_Offer_E", None)
        for c in ["Cluster_1", "Cluster_2", "Cluster_3", "Cluster_4"]:
            base_row[c] = 1 if c == f"Cluster_{cluster}" else 0

        offer_cols = ["Offer_Clean_Offer_A", "Offer_Clean_Offer_B", "Offer_Clean_Offer_C",
                      "Offer_Clean_Offer_D", "Offer_Clean_Offer_E"]
        scenario_names = ["No Offer", "Offer A", "Offer B", "Offer C", "Offer D", "Offer E"]
        results = {}
        for name in scenario_names:
            row = dict(base_row)
            for c in offer_cols:
                row[c] = 0
            if name != "No Offer":
                row[f"Offer_Clean_{name.replace(' ', '_')}"] = 1
            X = pd.DataFrame([row]).reindex(columns=train_columns, fill_value=0)
            results[name] = model.predict_proba(X)[0][1]

        results_df = pd.DataFrame({"Offer": list(results.keys()), "Predicted churn probability": list(results.values())})
        results_df = results_df.sort_values("Predicted churn probability").reset_index(drop=True)
        best = results_df.iloc[0]

        st.metric("Assigned segment", f"Cluster {cluster}")
        st.success(f"**Recommended offer: {best['Offer']}** (lowest predicted churn probability: {best['Predicted churn probability']:.1%})")
        st.dataframe(
            results_df.style.format({"Predicted churn probability": "{:.1%}"}),
            use_container_width=True, hide_index=True,
        )
