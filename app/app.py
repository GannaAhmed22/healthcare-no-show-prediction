import json
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

BASE = Path(__file__).parent
MODEL_PATH = BASE.parent / "models" / "No_show_prediction_model.joblib"
if not MODEL_PATH.exists():
    MODEL_PATH = BASE / "No_show_prediction_model.joblib"

AVERAGE_RATE = 0.136
HIGH_RISK = 0.5

LABELS = {
    "lead_days": "Days between booking and visit",
    "transportation_barrier_flag": "Transportation barrier",
    "sdoh_risk_score": "Social risk score",
    "interpreter_needed_flag": "Needs an interpreter",
    "distance_to_clinic_miles": "Distance to clinic",
    "weather_severity_group": "Weather",
    "prior_no_show_count_12m": "No-shows in the last 12 months",
    "reminder_sent_flag": "Reminder sent",
    "telehealth_flag": "Telehealth visit",
}


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_defaults():
    return json.loads((BASE / "defaults.json").read_text())


def build_row(inputs, defaults):
    row = dict(defaults)
    row["lead_days"] = inputs["lead_days"]
    row["same_day_flag"] = int(inputs["lead_days"] == 0)
    row["transportation_barrier_flag"] = int(inputs["transportation_barrier_flag"])
    row["sdoh_risk_score_x"] = inputs["sdoh_risk_score"]
    row["sdoh_risk_score_y"] = inputs["sdoh_risk_score"]
    row["interpreter_needed_flag_x"] = int(inputs["interpreter_needed_flag"])
    row["interpreter_needed_flag_y"] = int(inputs["interpreter_needed_flag"])
    row["distance_to_clinic_miles"] = inputs["distance_to_clinic_miles"]
    row["weather_severity_group"] = inputs["weather_severity_group"]
    row["prior_no_show_count_12m"] = inputs["prior_no_show_count_12m"]
    row["reminder_sent_flag"] = int(inputs["reminder_sent_flag"])
    row["reminder_days_before"] = defaults["reminder_days_before"] if inputs["reminder_sent_flag"] else 0
    row["telehealth_flag"] = int(inputs["telehealth_flag"])
    return pd.DataFrame([row])


def predict(model, inputs, defaults):
    return float(model.predict_proba(build_row(inputs, defaults))[0, 1])


def drivers(model, inputs, defaults, base_prob):
    typical = {
        "lead_days": defaults["lead_days"],
        "transportation_barrier_flag": False,
        "sdoh_risk_score": defaults["sdoh_risk_score_y"],
        "interpreter_needed_flag": False,
        "distance_to_clinic_miles": defaults["distance_to_clinic_miles"],
        "weather_severity_group": "Normal",
        "prior_no_show_count_12m": 0,
        "reminder_sent_flag": True,
        "telehealth_flag": False,
    }
    rows = []
    for key, value in typical.items():
        changed = dict(inputs)
        changed[key] = value
        effect = base_prob - predict(model, changed, defaults)
        rows.append((LABELS[key], effect))
    rows.sort(key=lambda r: abs(r[1]), reverse=True)
    return [r for r in rows if abs(r[1]) >= 0.01][:4]


st.set_page_config(page_title="No-Show Risk Predictor", page_icon="🏥", layout="wide")
st.title("🏥 Appointment No-Show Risk")
st.caption("DEPI Graduation Project · Healthcare No-Show Prediction")

model = load_model()
defaults = load_defaults()

left, right = st.columns([3, 2], gap="large")

with left:
    st.subheader("Appointment details")
    c1, c2 = st.columns(2)
    with c1:
        lead_days = st.slider(LABELS["lead_days"], 0, 120, 14)
        distance = st.slider(LABELS["distance_to_clinic_miles"] + " (miles)", 0.0, 60.0, 10.0, 0.5)
        weather = st.selectbox(LABELS["weather_severity_group"], ["Normal", "Rain", "Snow", "Severe weather"])
        reminder = st.toggle(LABELS["reminder_sent_flag"], value=True)
        telehealth = st.toggle(LABELS["telehealth_flag"], value=False)
    with c2:
        sdoh = st.slider(LABELS["sdoh_risk_score"] + " (0-100)", 0.0, 100.0, 49.0, 1.0)
        prior = st.number_input(LABELS["prior_no_show_count_12m"], 0, 10, 0)
        transport = st.toggle(LABELS["transportation_barrier_flag"], value=False)
        interpreter = st.toggle(LABELS["interpreter_needed_flag"], value=False)

inputs = {
    "lead_days": lead_days,
    "transportation_barrier_flag": transport,
    "sdoh_risk_score": sdoh,
    "interpreter_needed_flag": interpreter,
    "distance_to_clinic_miles": distance,
    "weather_severity_group": weather,
    "prior_no_show_count_12m": prior,
    "reminder_sent_flag": reminder,
    "telehealth_flag": telehealth,
}

prob = predict(model, inputs, defaults)

with right:
    st.subheader("Prediction")
    if prob >= HIGH_RISK:
        st.error("High risk of no-show")
    elif prob >= 0.3:
        st.warning("Medium risk of no-show")
    else:
        st.success("Low risk of no-show")
    st.metric("Risk score", f"{prob:.0%}")
    st.progress(min(prob, 1.0))
    st.caption(
        "The model uses balanced class weights, so the score ranks patients by risk. "
        f"It is not the real chance of missing the visit (the real average is about {AVERAGE_RATE:.0%})."
    )

    top = drivers(model, inputs, defaults, prob)
    if top:
        st.markdown("**What changed the score**")
        for label, effect in top:
            arrow = "🔺" if effect > 0 else "🔻"
            st.write(f"{arrow} {label}: {effect:+.0%}")

    if prob >= HIGH_RISK:
        st.info("Suggested action: call the patient or send an extra reminder before the visit.")

with st.expander("About the model"):
    st.write(
        "Logistic Regression with balanced class weights, trained on 36,000 synthetic appointments. "
        "The inputs above are the features with the biggest effect on the prediction "
        "(permutation importance). All other features are set to their most common value."
    )
