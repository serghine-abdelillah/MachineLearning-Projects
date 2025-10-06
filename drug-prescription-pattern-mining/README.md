# ⚕️ Healthcare Assistant

A **Streamlit-based Healthcare Assistant** that helps optimize pharmacy inventory and assist doctors in generating prescriptions.  
The app leverages **association rule mining** (ECLAT) and real-world prescription data to recommend complementary medicines, improve drug stocking, and generate patient-ready PDF reports.  

---

## 🚀 Features

### 🏥 Pharmacy Inventory Optimizer
- Add drugs to your pharmacy’s current inventory.  
- Get **recommendations of complementary drugs** to stock, based on association rules.  
- Download a **Pharmacy Inventory Report (PDF)** for record-keeping.  

### 💊 Doctor Prescription Assistant
- Add medicines for a patient prescription.  
- Get **smart recommendations** of additional medicines commonly prescribed together.  
- Fill in patient details (**Name, Email, Telephone**).  
- Export a **Prescription PDF** ready to share or print.  

---

## 🛠️ Tech Stack
- **Python**  
- **Streamlit** (Web UI)  
- **Pandas** (Data processing)  
- **FPDF** (PDF generation)  
- **Pickle** (Model storage)  
- **ECLAT Association Rules** (Frequent itemset mining)  

---



## 📂 Project Structure
📦 healthcare-assistant\
┣ 📜 app.py # Main Streamlit app\
┣ 📜 eclat_association_rules.pkl # Pre-trained association rules model\
┣ 📜 medicine_prescription_records.csv # Prescription dataset\
┣ 📜 requirements.txt # Dependencies\
┗ 📜 README.md # Project description\

## ⚙️ Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/serghine-abdelillah/MachineLearning-Projects.git
   cd drug-prescription-pattern-mining
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the app:
   ```bash
   streamlit run app.py
4. Open in browser:
   ```bash
   http://localhost:8501
---
## 📊 Example Workflow
- **Pharmacy Inventory Optimizer**
1. Select a drug (e.g., Amoxicillin).
2. Get suggested complementary drugs to stock.
3. Add them to inventory with a single click.
4. Export inventory report as PDF.

- **Doctor Prescription Assistant**

1. Enter patient details.
2. Add prescribed medicines.
3. Accept or reject recommendations.
4. Confirm and download prescription as PDF.

## 🤝 Contributing
Pull requests are welcome! Please open an issue first to discuss what you’d like to improve.

---
### 🚀 Demo : [Link](https://health-care-assistant.streamlit.app/])
