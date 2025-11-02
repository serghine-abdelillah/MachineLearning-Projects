# 🧠 CIFAR-10 Image Clustering and Classification
This notebook demonstrates a complete pipeline for **image preprocessing**, **dimensionality reduction**, and **unsupervised learning** using the **CIFAR-10 dataset**.
The main goal is to explore how machine learning models (especially clustering methods like **K-Means**) can separate visual classes without supervision and analyze their performance using visualization and evaluation metrics.
## 📂 Project Structure
`Assignment-Solution.ipynb`\
The notebook is divided into several key parts, each building toward understanding and improving clustering performance.
## 🚀 Tasks Overview

**1. Dataset Preparation**
- Import the **CIFAR-10** dataset.
- Retain only 4 classes: `airplane`, `automobile`, `bird`, and `cat`.

**2. Visualization & Normalization**
- Display random samples with labels.
- Normalize pixel values to `[0, 1]`.

**3. Dimensionality Reduction**
- Apply **PCA** with 2 components for 2D visualization.
- Explore **PCA (95% variance)** and **LDA (3 components)** for feature compression.

**4. Clustering Models**
- Apply **K-Means**, **K-Means + PCA**, and **K-Means + LDA**.
- Visualize cluster results in 2D space.

**5. Evaluation**
- Compute **Davies-Bouldin score** for model comparison.
- Display **confusion matrices** and **classification reports**.

**6. Error Analysis**
- Visualize **misclassified samples** for the best model.
- Suggest improvements to enhance model accuracy.

## 🧩 Technologies Used
- **Python**
- **NumPy**, **Matplotlib**
- **Scikit-learn** (PCA, K-Means, LDA, metrics)
- **TensorFlow** / **Keras** (for dataset loading)

## 📊 Key Concepts Covered
- Unsupervised learning on image data
- Dimensionality reduction (PCA, LDA)
- Cluster evaluation metrics
- Visualization of high-dimensional data

## 🧪 How to Run
