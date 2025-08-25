import streamlit as st
import pandas as pd
import pickle
from fpdf import FPDF

# Load the model from the pickle file
@st.cache_resource
def load_model():
    with open('eclat_association_rules.pkl', 'rb') as file:
        model = pickle.load(file)
    return pd.DataFrame(model)

# Load and preprocess the dataset
@st.cache_resource
def load_drug_data():
    data = pd.read_csv('medicine_prescription_records.csv')
    # Extract unique drug names
    drug_lists = data['cms_prescription_counts'].apply(lambda x: [drug.strip() for drug in x.split(',')])
    all_drugs = [drug for sublist in drug_lists for drug in sublist]
    return data, list(set(all_drugs))

# Initialize Streamlit app
st.set_page_config(page_title="Doctor Prescription Assistant", page_icon="💊", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #f5faff; }
        .stTextInput > div > label { color: #0073e6; font-size: 18px; }
        h1, h2 { color: #0073e6; }
        div[data-testid="stSidebar"] { background-color: #cce7ff; }
        .medicine-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("💊 Doctor Prescription Assistant")

# Load data and model
model1 = load_model()
data, unique_drugs = load_drug_data()

# Initialize session state
if "medicines" not in st.session_state:
    st.session_state.medicines = []
if "recommendations" not in st.session_state:
    st.session_state.recommendations = {}

# Input Fields
st.write("### Patient Information")
full_name = st.text_input("Full Name", placeholder="Enter patient's full name")
email = st.text_input("Email", placeholder="Enter patient's email")
telephone = st.text_input("Telephone", placeholder="Enter patient's phone number")

# Add Medicine Section
st.write("### Add Medicines")
new_medicine = st.selectbox("Choose a medicine to add", [''] + unique_drugs)

if st.button("Add Medicine"):
    if new_medicine:
        st.session_state.medicines.append(new_medicine)
        st.success(f"{new_medicine} added to the prescription.")
    else:
        st.error("Please select a valid medicine.")

# Generate recommendations dynamically
for medicine in st.session_state.medicines:
    if medicine not in st.session_state.recommendations:
        # Generate recommendation for the medicine
        an_list = list(model1["antecedents"])
        co_list = list(model1["consequents"])
        su_list = list(model1["support"])

        recommendations = [
            {"Consequents": list(c), "Support": s}
            for m, c, s in zip(an_list, co_list, su_list)
            if medicine in m
        ]
        if recommendations:
            best_recommendation = max(recommendations, key=lambda x: x["Support"])
            st.session_state.recommendations[medicine] = best_recommendation
        else:
            st.session_state.recommendations[medicine] = None

# Display recommendations
st.write("### Recommendations")
for medicine, recommendation in st.session_state.recommendations.items():
    if recommendation:
        recommended_drug = recommendation["Consequents"][0]
        support = recommendation["Support"]

        col1, col2, col3 = st.columns([4, 2, 2])
        with col1:
            st.write(f"**{medicine} → {recommended_drug}** (Support: {support:.2f})")
        with col2:
            if st.button(f"Accept {recommended_drug}", key=f"accept_{medicine}"):
                st.session_state.medicines.append(recommended_drug)
                st.success(f"{recommended_drug} added to the prescription.")
        with col3:
            if st.button(f"Change {medicine}", key=f"change_{medicine}"):
                alternative_drug = st.selectbox(f"Choose an alternative for {medicine}", unique_drugs, key=f"alt_{medicine}")
                if alternative_drug:
                    st.session_state.medicines.append(alternative_drug)
                    st.success(f"{alternative_drug} added to the prescription.")
    else:
        st.warning(f"No recommendations found for {medicine}.")

# Display current medicines list
st.write("### Current Medicines List")
if st.session_state.medicines:
    for medicine in st.session_state.medicines:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.write(f"- {medicine}")
        with col2:
            if st.button(f"Remove", key=f"remove_{medicine}"):
                st.session_state.medicines.remove(medicine)
                st.success(f"{medicine} removed from the prescription.")
else:
    st.info("No medicines added yet.")

# Confirm Prescription
if st.button("Confirm Prescription"):
    if not full_name or not email or not telephone:
        st.error("Please fill in all patient information before confirming.")
    elif not st.session_state.medicines:
        st.error("Please add at least one medicine before confirming.")
    else:
        st.success("Prescription confirmed!")

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Prescription", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Patient Name: {full_name}", ln=True)
        pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
        pdf.cell(200, 10, txt=f"Telephone: {telephone}", ln=True)
        pdf.cell(200, 10, txt="Medicines:", ln=True)
        for med in st.session_state.medicines:
            pdf.cell(200, 10, txt=f"- {med}", ln=True)
        pdf_output = "prescription.pdf"
        pdf.output(pdf_output)

        # Download link
        with open(pdf_output, "rb") as file:
            st.download_button(
                label="Download Prescription as PDF",
                data=file,
                file_name=pdf_output,
                mime="application/pdf",
            )
