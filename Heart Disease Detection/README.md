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
   git clone https://github.com/serghine-abdelillah/MachineLearning-Projects.git
   cd Heart Disease Detection
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Run the app:
   ```bash
   python app.py
4. Open in browser:
   ```bash
   http://localhost:7860
---

## 📊 Example Inputs

Here are some sample patients you can try directly in the app:\ 

| Age | Sex | ChestPainType | RestingBP | Cholesterol | FastingBS | RestingECG | MaxHR | ExerciseAngina | Oldpeak | ST_Slope |
|-----|-----|---------------|-----------|-------------|-----------|------------|-------|----------------|---------|----------|
| 40  | M   | ATA           | 140       | 289         | 0         | Normal     | 172   | N              | 0.0     | Up       |
| 49  | F   | NAP           | 160       | 180         | 0         | Normal     | 156   | N              | 1.0     | Flat     |
| 37  | M   | ATA           | 130       | 283         | 0         | ST         | 98    | N              | 0.0     | Up       |
| 48  | F   | ASY           | 138       | 214         | 0         | Normal     | 108   | Y              | 1.5     | Flat     |
| 54  | M   | NAP           | 150       | 195         | 0         | Normal     | 122   | N              | 0.0     | Up       |


## 🤝 Contributing

Pull requests are welcome! please open an issue first to discuss what you’d like to improve.
