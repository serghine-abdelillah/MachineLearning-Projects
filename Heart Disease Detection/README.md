# ❤️ Heart Disease Detection

A **Gradio-based web application** for detecting heart disease risk using machine learning.  
The app provides **data exploration (EDA)** tools and a **prediction interface**, allowing users to explore the dataset and test the model with real or sample inputs.  

---

## 🚀 Features

### 📊 Data Exploration
- View **dataset statistics**.  
- Visualize **class distribution** of patients with/without heart disease.  
- Explore a **correlation heatmap** between features.  

### 🧠 Heart Disease Prediction
- Input patient details such as **Age, Sex, Chest Pain Type, Cholesterol, Max Heart Rate**, etc.  
- Get an instant **prediction result**:  
  - ✅ No Heart Disease  
  - 💔 Heart Disease Detected  
- Try with **sample patient cases** provided in the app.  

---

## 🛠️ Tech Stack
- **Python**  
- **Gradio** (Web UI)  
- **Pandas** & **Seaborn** (Data analysis & visualization)  
- **Matplotlib** (Plotting)  
- **Scikit-learn** (ML model)  
- **Joblib** (Model persistence)  

---

## 📂 Project Structure
📦 heart-disease-detection\
┣ 📜 app.py # Main Gradio app\
┣ 📜 heart.csv # Heart disease dataset\
┣ 📜 heart_disease_model.pkl # Trained model + scaler + columns\
┣ 📜 requirements.txt # Dependencies\
┗ 📜 README.md # Project description\


---

## ⚙️ Installation & Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/heart-disease-detection.git
   cd heart-disease-detection
