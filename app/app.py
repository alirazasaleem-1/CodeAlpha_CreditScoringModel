import streamlit as st 
import pandas as pd 
import joblib 

model = joblib.load("models/random_forest_model.pkl")

st.title("💳 Credit Scoring Model")
st.write(
    "Predict credit risk using a Machine Learning Model."
)

st.header("Applicant Information")

person_age = st.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=25
)

person_income = st.number_input(
    "Annual Income",
    min_value=1,
    value=50000
)

person_emp_length = st.number_input(
    "Employment Length (Years)",
    min_value=0,
    max_value=50,
    value=5
)

st.header("Loan Information")

person_home_ownership = st.selectbox(
    "Home Ownership",
    ["RENT", "MORTGAGE", "OWN", "OTHER"]
)

loan_intent = st.selectbox(
    "Loan Intent",
    [
        "EDUCATION",
        "MEDICAL",
        "VENTURE",
        "PERSONAL",
        "DEBTCONSOLIDATION",
        "HOMEIMPROVEMENT"
    ]
)

loan_grade = st.selectbox(
    "Loan Grade",
    ["A", "B", "C", "D", "E", "F", "G"]
)

loan_amnt = st.number_input(
    "Loan Amount",
    min_value=0,
    value=10000
)

loan_int_rate = st.number_input(
    "Loan Interest Rate (%)",
    min_value=0.0,
    max_value=50.0,
    value=10.0
)



st.header("Credit History")

cb_person_default_on_file = st.selectbox(
    "Previous Default on File",
    ["Y", "N"]
)

cb_person_cred_hist_length = st.number_input(
    "Credit History Length (Years)",
    min_value=0,
    max_value=100,
    value=5
)

input_data = pd.DataFrame({
    "person_age": [person_age],
    "person_income": [person_income],
    "person_emp_length": [person_emp_length],
    "loan_amnt": [loan_amnt],
    "loan_int_rate": [loan_int_rate],
    "loan_percent_income": [loan_amnt / person_income],
    "cb_person_default_on_file": [
        1 if cb_person_default_on_file == "Y" else 0
    ],
    "cb_person_cred_hist_length": [cb_person_cred_hist_length]
})

input_data["person_home_ownership_MORTGAGE"] = (
    1 if person_home_ownership == "MORTGAGE" else 0
)

input_data["person_home_ownership_OTHER"] = (
    1 if person_home_ownership == "OTHER" else 0
)

input_data["person_home_ownership_OWN"] = (
    1 if person_home_ownership == "OWN" else 0
)

input_data["person_home_ownership_RENT"] = (
    1 if person_home_ownership == "RENT" else 0
)

loan_intents = [
    "DEBTCONSOLIDATION",
    "EDUCATION",
    "HOMEIMPROVEMENT",
    "MEDICAL",
    "PERSONAL",
    "VENTURE"
]

for intent in loan_intents:
    input_data[f"loan_intent_{intent}"] = (
        1 if loan_intent == intent else 0
    )

loan_grades = ["A", "B", "C", "D", "E", "F", "G"]

for grade in loan_grades:
    input_data[f"loan_grade_{grade}"] = (
        1 if loan_grade == grade else 0
    )


if st.button("Predict Credit Risk"):

    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)

    if prediction[0] == 1:
        st.error("⚠️ High Credit Risk")
        st.write(
            f"Probability of High Credit Risk: "
            f"{probability[0][1] * 100:.2f}%"
        )

    else:
        st.success("✅ Low Credit Risk")
        st.write(
            f"Probability of Low Credit Risk: "
            f"{probability[0][0] * 100:.2f}%"
        )

st.info(
    "This prediction is based on the financial and credit information "
    "provided above. It is intended for educational purposes only."
)