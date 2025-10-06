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

### 🚀Demo : 
[Link](https://health-care-assistant.streamlit.app/])

## 📂 Project Structure
📦 healthcare-assistant\
┣ 📜 app.py # Main Streamlit app\
┣ 📜 eclat_association_rules.pkl # Pre-trained association rules model\
┣ 📜 medicine_prescription_records.csv # Prescription dataset\
┣ 📜 requirements.txt # Dependencies\
┗ 📜 README.md # Project description\

## ⚙️ Installation & Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/serghine/healthcare-assistant.git
   cd healthcare-assistant
