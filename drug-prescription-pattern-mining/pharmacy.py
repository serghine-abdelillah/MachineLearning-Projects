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
st.set_page_config(page_title="Pharmacy Inventory Optimizer", page_icon="🏥", layout="wide")
st.markdown("""
    <style>
        .main { background-color: #f5faff; }
        .stTextInput > div > label { color: #0073e6; font-size: 18px; }
        h1, h2 { color: #0073e6; }
        div[data-testid="stSidebar"] { background-color: #cce7ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏥 Pharmacy Inventory Optimizer")

# Load data and model
model1 = load_model()
data, unique_drugs = load_drug_data()

# Initialize session state
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "recommendations" not in st.session_state:
    st.session_state.recommendations = {}

# Add Drug to Inventory
st.write("### Add a Drug to Inventory")
new_drug = st.selectbox("Choose a drug to add", [''] + unique_drugs)

if st.button("Add Drug to Inventory"):
    if new_drug:
        # Add new drug to inventory
        st.session_state.inventory.append(new_drug)

        # Extract recommendations based on the new drug
        an_list = list(model1["antecedents"])
        co_list = list(model1["consequents"])
        su_list = list(model1["support"])

        recommendations = [
            {"Consequents": list(c), "Support": s}
            for m, c, s in zip(an_list, co_list, su_list)
            if new_drug in m
        ]

        if recommendations:
            # Sort recommendations by support
            recommendations = sorted(recommendations, key=lambda x: x["Support"], reverse=True)
            st.session_state.recommendations[new_drug] = recommendations
        else:
            st.session_state.recommendations[new_drug] = []
        st.success(f"{new_drug} added to the inventory.")
    else:
        st.error("Please select a valid drug.")

# Display Current Inventory
st.write("### Current Inventory")
if st.session_state.inventory:
    st.table(pd.DataFrame({"Inventory": st.session_state.inventory}))
else:
    st.info("No drugs in the inventory yet.")

# Display Recommendations
if new_drug and new_drug in st.session_state.recommendations:
    st.write(f"### Recommended Drugs to Stock Along with {new_drug}")
    recommendations = st.session_state.recommendations[new_drug]

    if recommendations:
        for idx, rec in enumerate(recommendations):
            consequent_drugs = ', '.join(rec["Consequents"])
            support = rec["Support"]
            st.write(f"**{consequent_drugs}** (Support: {support:.2f})")
    else:
        st.warning(f"No recommendations found for {new_drug}.")

# Generate Inventory Report
if st.button("Download Inventory Report"):
    if not st.session_state.inventory:
        st.error("Inventory is empty. Add drugs to generate a report.")
    else:
        # Generate PDF report
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Pharmacy Inventory Report", ln=True, align="C")
        pdf.cell(200, 10, txt="Current Inventory:", ln=True)
        for drug in st.session_state.inventory:
            pdf.cell(200, 10, txt=f"- {drug}", ln=True)
        pdf_output = "pharmacy_inventory.pdf"
        pdf.output(pdf_output)

        # Download button
        with open(pdf_output, "rb") as file:
            st.download_button(
                label="Download Inventory Report as PDF",
                data=file,
                file_name=pdf_output,
                mime="application/pdf",
            )
