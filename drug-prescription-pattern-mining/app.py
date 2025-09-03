import streamlit as st
import pandas as pd
import pickle
from fpdf import FPDF

# ---------------------------
# Shared Functions
# ---------------------------
@st.cache_resource
def load_model():
    with open('eclat_association_rules.pkl', 'rb') as file:
        model = pickle.load(file)
    return pd.DataFrame(model)

@st.cache_resource
def load_drug_data():
    data = pd.read_csv('medicine_prescription_records.csv')
    # Extract unique drug names
    drug_lists = data['cms_prescription_counts'].apply(lambda x: [drug.strip() for drug in x.split(',')])
    all_drugs = [drug for sublist in drug_lists for drug in sublist]
    return data, list(set(all_drugs))

# ---------------------------
# Streamlit Setup
# ---------------------------
st.set_page_config(page_title="Healthcare Assistant", page_icon="⚕️", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f5faff; }
        .stTextInput > div > label { color: #0073e6; font-size: 18px; }
        h1, h2 { color: #0073e6; }
        div[data-testid="stSidebar"] { background-color: #cce7ff; }
        .medicine-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("⚕️ Healthcare Assistant")

# Load data and model
model1 = load_model()
data, unique_drugs = load_drug_data()

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2 = st.tabs(["🏥 Pharmacy Inventory Optimizer", "💊 Doctor Prescription Assistant"])

# ---------------------------
# Tab 1: Pharmacy Inventory Optimizer
# ---------------------------
with tab1:
    st.header("🏥 Pharmacy Inventory Optimizer")

    if "inventory" not in st.session_state:
        st.session_state.inventory = []
    if "inventory_recs" not in st.session_state:
        st.session_state.inventory_recs = {}

    # new_drug = st.selectbox("Choose a drug to add", [''] + unique_drugs, key="inv_select", placeholder="Select contact method...",)
    new_drug = st.selectbox(
    "Choose a drug to add",
    [''] + unique_drugs,
    key="inv_select",
    index=None,
    placeholder="Try AMOXICILLIN...",
)

    if st.button("Add Drug to Inventory"):
        if new_drug:
            if new_drug not in st.session_state.inventory:
                st.session_state.inventory.append(new_drug)

                # --- generate recommendations ---
                an_list = list(model1["antecedents"])
                co_list = list(model1["consequents"])
                su_list = list(model1["support"])

                recommendations = [
                    {"Consequents": list(c), "Support": s}
                    for m, c, s in zip(an_list, co_list, su_list)
                    if new_drug in m and s > 0.03 and not any(drug in st.session_state.inventory for drug in c)
                ]

                seen = set()
                unique_recs = []
                for rec in recommendations:
                    conseq_tuple = tuple(rec["Consequents"])
                    if conseq_tuple not in seen:
                        unique_recs.append(rec)
                        seen.add(conseq_tuple)

                if unique_recs:
                    unique_recs = sorted(unique_recs, key=lambda x: x["Support"], reverse=True)
                    st.session_state.inventory_recs[new_drug] = unique_recs
                else:
                    st.session_state.inventory_recs[new_drug] = []

                st.success(f"{new_drug} added to the inventory.")
                st.rerun()
            else:
                st.warning(f"{new_drug} is already in inventory.")
        else:
            st.error("Please select a valid drug.")

    # --- show recommendations ---
    st.write("### Inventory Recommendations")
    for med, recs in st.session_state.inventory_recs.items():
        st.write(f"#### Recommended Drugs to Stock Along with :blue[{med}]")
        if recs:
            for idx, rec in enumerate(recs):
                recommended = rec["Consequents"][0]
                support = rec["Support"]
                col1, col2 = st.columns([4, 2])
                with col1:
                    st.write(f"**{med} → {recommended}** (Support: {support:.2f})")
                with col2:
                    if st.button(f"Add {recommended}", key=f"inv_add_{med}_{idx}"):
                        if recommended not in st.session_state.inventory:
                            st.session_state.inventory.append(recommended)
                            st.success(f"{recommended} added to inventory.")
                            
                            # 🔑 generate new recs for this new drug
                            an_list = list(model1["antecedents"])
                            co_list = list(model1["consequents"])
                            su_list = list(model1["support"])

                            recommendations = [
                                {"Consequents": list(c), "Support": s}
                                for m, c, s in zip(an_list, co_list, su_list)
                                if recommended in m and s > 0.03 and not any(drug in st.session_state.inventory for drug in c)
                            ]

                            seen = set()
                            unique_recs = []
                            for r in recommendations:
                                conseq_tuple = tuple(r["Consequents"])
                                if conseq_tuple not in seen:
                                    unique_recs.append(r)
                                    seen.add(conseq_tuple)

                            if unique_recs:
                                unique_recs = sorted(unique_recs, key=lambda x: x["Support"], reverse=True)
                                st.session_state.inventory_recs[recommended] = unique_recs
                            else:
                                st.session_state.inventory_recs[recommended] = []

                            st.rerun()
                        else:
                            st.warning(f"{recommended} is already in inventory.")
        else:
            st.warning(f"No recommendations found for {med}.")


    # Current Inventory
    st.write("### Current Inventory")
    if st.session_state.inventory:
        st.table(pd.DataFrame({"Inventory": st.session_state.inventory}))
    else:
        st.info("No drugs in the inventory yet.")

    # # Recommendations
    # if new_drug and new_drug in st.session_state.inventory_recs:
    #     st.write(f"### Recommended Drugs to Stock Along with {new_drug}")
    #     recs = st.session_state.inventory_recs[new_drug]
    #     if recs:
    #         for rec in recs:
    #             st.write(f"**{', '.join(rec['Consequents'])}** (Support: {rec['Support']:.2f})")
    #     else:
    #         st.warning(f"No recommendations found for {new_drug}.")

    # PDF Report
    if st.button("Download Inventory Report"):
        if not st.session_state.inventory:
            st.error("Inventory is empty. Add drugs to generate a report.")
        else:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="Pharmacy Inventory Report", ln=True, align="C")
            pdf.cell(200, 10, txt="Current Inventory:", ln=True)
            for drug in st.session_state.inventory:
                pdf.cell(200, 10, txt=f"- {drug}", ln=True)
            pdf_output = "pharmacy_inventory.pdf"
            pdf.output(pdf_output)

            with open(pdf_output, "rb") as file:
                st.download_button("Download Inventory Report as PDF", data=file, file_name=pdf_output, mime="application/pdf")

# ---------------------------
# Tab 2: Doctor Prescription Assistant
# ---------------------------
with tab2:
    st.header("💊 Doctor Prescription Assistant")

    if "medicines" not in st.session_state:
        st.session_state.medicines = []
    if "presc_recs" not in st.session_state:
        st.session_state.presc_recs = {}

    full_name = st.text_input("Full Name", placeholder="Enter patient's full name")
    email = st.text_input("Email", placeholder="Enter patient's email")
    telephone = st.text_input("Telephone", placeholder="Enter patient's phone number")

    # new_medicine = st.selectbox("Choose a medicine to add", [''] + unique_drugs, key="med_select")
    new_medicine = st.selectbox(
    "Choose a medicine to add",
    [''] + unique_drugs,
    key="med_select",
    index=None,
    placeholder="Try AMOXICILLIN...",
    )
    # Recommendations
    def update_recommendations():
        for med in st.session_state.medicines:
            if med not in st.session_state.presc_recs:
                an_list = list(model1["antecedents"])
                co_list = list(model1["consequents"])
                su_list = list(model1["support"])
                recs = [
                    {"Consequents": list(c), "Support": s}
                    for m, c, s in zip(an_list, co_list, su_list)
                    if med in m and s > 0.03 and not any(d in st.session_state.medicines for d in c)
                ]

                # Remove duplicates
                seen = set()
                unique_recs = []
                for rec in recs:
                    conseq_tuple = tuple(rec["Consequents"])
                    if conseq_tuple not in seen:
                        unique_recs.append(rec)
                        seen.add(conseq_tuple)
                
                if unique_recs:
                    best = max(unique_recs, key=lambda x: x["Support"])
                    st.session_state.presc_recs[med] = best
                else:
                    st.session_state.presc_recs[med] = None
    if st.button("Add Medicine"):
        if new_medicine:
            st.session_state.medicines.append(new_medicine)
            st.success(f"{new_medicine} added to the prescription.")
            update_recommendations()
            st.rerun() 
        else:
            st.error("Please select a valid medicine.")


    st.write("### Recommendations")
    for med, rec in list(st.session_state.presc_recs.items()):
        if rec:
            recommended = rec["Consequents"][0]
            support = rec["Support"]
            col1, col2, col3 = st.columns([4, 2, 2])
            with col1:
                st.write(f"**{med} → {recommended}** (Support: {support:.2f})")
            with col2:
                if st.button(f"Accept {recommended}", key=f"accept_{med}"):
                    if recommended not in st.session_state.medicines :
                        st.session_state.medicines.append(recommended)
                        update_recommendations()
                        st.success(f"{recommended} added to the prescription.")
                        st.rerun() 
                    else:
                        st.warning(f"{recommended} is already in the prescription.")
                    st.success(f"{recommended} added to the prescription.")
            # with col3:
            #     if st.button(f"Change {med}", key=f"change_{med}"):
            #         alternative = st.selectbox(f"Choose alternative for {med}", unique_drugs, key=f"alt_{med}")
            #         if alternative:
            #             st.session_state.medicines.append(alternative)
            #             update_recommendations() 
            #             st.success(f"{alternative} added to the prescription.")
            #             st.rerun()
        else:
            st.warning(f"No recommendations found for {med}.")

    st.write("### Current Medicines List")
    if st.session_state.medicines:
        for med in st.session_state.medicines:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.write(f"- {med}")
            with col2:
                if st.button("Remove", key=f"remove_{med}"):
                    st.session_state.medicines.remove(med)
                    st.success(f"{med} removed from the prescription.")
    else:
        st.info("No medicines added yet.")

    if st.button("Confirm Prescription"):
        if not full_name or not email or not telephone:
            st.error("Please fill in all patient information before confirming.")
        elif not st.session_state.medicines:
            st.error("Please add at least one medicine before confirming.")
        else:
            st.success("Prescription confirmed!")

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
            pdf_output = f"prescription-{full_name}.pdf"
            pdf.output(pdf_output)

            with open(pdf_output, "rb") as file:
                st.download_button("Download Prescription as PDF", data=file, file_name=pdf_output, mime="application/pdf")
