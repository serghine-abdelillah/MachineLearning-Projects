import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# Load dataset
df = pd.read_csv("heart.csv")

# Load everything from one pkl if you saved as dict
saved_objects = joblib.load("heart_disease_model.pkl")
model = saved_objects["model"]
scaler = saved_objects["scaler"]
training_columns = saved_objects["columns"]


# ---------- EDA ----------
def explore_data(option):
    if option == "Dataset Info":
        desc = df.describe().reset_index()
        return gr.update(value=desc, visible=True), gr.update(visible=False)
    elif option == "Class Distribution":
        plt.figure(figsize=(6,4))
        sns.countplot(x="HeartDisease", data=df)
        plt.title("Class Distribution")
        plt.savefig("class_dist.png")
        plt.close()
        return gr.update(visible=False), gr.update(value="class_dist.png", visible=True)
    elif option == "Correlation Heatmap":
        plt.figure(figsize=(8,6))
        sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
        plt.title("Correlation Heatmap")
        plt.savefig("heatmap.png")
        plt.close()
        return gr.update(visible=False), gr.update(value="heatmap.png", visible=True)

# ---------- Prediction ----------
def predict_heart_disease(age, sex, cp, trestbps, chol, fbs,
                          restecg, thalach, exang, oldpeak, slope):
    input_dict = {
        "Age": [age],
        "RestingBP": [trestbps],
        "Cholesterol": [chol],
        "FastingBS": [fbs],
        "MaxHR": [thalach],
        "Oldpeak": [oldpeak],
        "Sex": ["M" if sex == "Male" else "F"],
        "ChestPainType": [cp],
        "RestingECG": [restecg],
        "ExerciseAngina": ["Y" if exang == "Yes" else "N"],
        "ST_Slope": [slope],
    }

    input_df = pd.DataFrame(input_dict)
    input_encoded = pd.get_dummies(input_df)
    input_encoded = input_encoded.reindex(columns=training_columns, fill_value=0)

    input_scaled = scaler.transform(input_encoded)
    prediction = model.predict(input_scaled)[0]
    return "💔 Heart Disease Detected" if prediction == 1 else "✅ No Heart Disease"

# ---------- Gradio Interface ----------
with gr.Blocks() as demo:
    gr.Markdown("# ❤️ Heart Disease Detection")

    with gr.Tab("📊 Data Exploration"):
        option = gr.Radio(
            ["Dataset Info", "Class Distribution", "Correlation Heatmap"],
            label="Choose EDA Option"
        )
        eda_text = gr.Dataframe(label="Dataset Info", visible=False)
        eda_image = gr.Image(label="Plot", visible=False)
        option.change(explore_data, inputs=option, outputs=[eda_text, eda_image])

    # ---------- Add Sample Inputs ----------
    samples = [
        [40, "M", "ATA", 140, 289, 0, "Normal", 172, "N", 0.0, "Up"],
        [49, "F", "NAP", 160, 180, 0, "Normal", 156, "N", 1.0, "Flat"],
        [37, "M", "ATA", 130, 283, 0, "ST", 98, "N", 0.0, "Up"],
        [48, "F", "ASY", 138, 214, 0, "Normal", 108, "Y", 1.5, "Flat"],
        [54, "M", "NAP", 150, 195, 0, "Normal", 122, "N", 0.0, "Up"],
    ]

    # Inside your "🧠 Prediction" Tab
    with gr.Tab("🧠 Prediction"):
        with gr.Row():
            age = gr.Number(label="Age")
            sex = gr.Dropdown(["M","F"], label="Sex")
            cp = gr.Dropdown(["ATA","NAP","ASY","TA"], label="Chest Pain Type")
            trestbps = gr.Number(label="Resting BP")
            chol = gr.Number(label="Cholesterol")
            fbs = gr.Radio([0,1], label="Fasting Blood Sugar >120mg/dl")
            restecg = gr.Dropdown(["Normal","ST"], label="Rest ECG")
            thalach = gr.Number(label="Max Heart Rate")
            exang = gr.Dropdown(["Y","N"], label="Exercise Induced Angina")
            oldpeak = gr.Number(label="Oldpeak")
            slope = gr.Dropdown(["Up","Flat","Down"], label="Slope")

        predict_btn = gr.Button("Predict ❤️")
        result = gr.Textbox(label="Prediction Result")

        # Add Examples (auto-fills inputs when clicked)
        gr.Examples(
            examples=samples,
            inputs=[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope],
            label="🔍 Try Sample Inputs"
        )

        predict_btn.click(
            predict_heart_disease,
            inputs=[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope],
            outputs=result
        )


# Launch
demo.launch()
