
# 🧠 Predicting Code Quality using Machine Learning

## 📌 Overview

This project predicts whether a code snippet is **buggy** or **safe** using machine learning and semantic code embeddings.

The system combines:

- Synthetic vulnerability generation
- Real-world vulnerable code from the Juliet Test Suite
- Traditional feature engineering
- Transformer-based embeddings (CodeBERT)
- Classical ML models and neural networks

The final system achieves approximately **86% test accuracy** on a large hybrid dataset of over **38,000 code samples**.

---

# ⚙️ Problem Statement

Manual code review is:

- Time-consuming
- Expensive
- Error-prone

The goal of this project is to automatically identify vulnerable or buggy code patterns using machine learning techniques.

---

# 📦 Dataset

## Hybrid Dataset (~38,000 samples)

The dataset combines:

| Source | Contribution |
|---|---|
| Synthetic Code Generation | ~60% |
| Juliet Vulnerability Dataset | ~40% |

---

## 🔹 Synthetic Data Generation

Custom templates were created to simulate vulnerable and safe C/C++ code snippets.

### Vulnerabilities Covered

- Buffer overflow
- NULL pointer dereference
- Divide-by-zero
- Use-after-free
- Double free
- Uninitialized variables
- Array index errors
- Unsafe string operations

### Data Augmentation Techniques

To improve generalization, multiple variations were introduced:

- Variable renaming
- Formatting noise
- Structural mutations
- Loop modifications
- Conditional mutations
- Controlled label noise

---

## 🔹 Juliet Test Suite

The project also uses the **Juliet Test Suite**, a widely used vulnerability benchmark dataset for C/C++ programs.

### Labels

| Label | Meaning |
|---|---|
| `0` | Safe Code |
| `1` | Vulnerable Code |

---

# 🤔 Why Juliet?

| Dataset | Reason Not Used |
|---|---|
| Defects4J | Complex preprocessing and commit-function mapping |
| CodeSearchNet | No vulnerability labels |
| Generic GitHub Data | Noisy and inconsistent labels |

Juliet provides:

- Clean labels
- Real vulnerability patterns
- Standardized structure
- Large vulnerability coverage

---

# 🧩 Feature Engineering

Multiple feature representations were explored.

---

## 1️⃣ TF-IDF Features

Captures token-level syntactic information.

### Examples

- `if`
- `return`
- `NULL`
- `malloc`
- `strcpy`

### Purpose

Detects local vulnerability-related token patterns.

---

## 2️⃣ Code Metrics

Simple structural indicators extracted from code.

### Examples

- Lines of code
- Number of loops
- Number of conditions
- Pointer count
- Function count

### Observation

Metrics alone were not strong predictors.

---

## 3️⃣ Structural Features

Additional structural signals explored:

- Brace counts
- Pointer operations
- Loop structure
- Conditional density

---

## 4️⃣ CodeBERT Embeddings ⭐

The most important feature representation.

### Details

- Pretrained transformer model
- 768-dimensional embeddings
- Semantic understanding of code

### Advantages

Captures:

- Code meaning
- Context
- Behavioral similarity
- Semantic vulnerability patterns

---

# 🤖 Models Explored

## Classical ML Models

| Model | Purpose |
|---|---|
| Logistic Regression | Strong linear baseline |
| Linear SVM | High-dimensional classifier |
| Random Forest | Non-linear ensemble model |

---

## Deep Learning Model

### Multi-Layer Perceptron (MLP)

Custom neural network trained on:

- PCA-reduced CodeBERT embeddings
- TF-IDF features
- Code metrics

### Architecture Features

- Batch normalization
- Dropout regularization
- Learning rate scheduling
- PCA dimensionality reduction

---

# 📊 Experimental Results

## Classical Models

| Feature Set | Logistic Regression | Linear SVM | Random Forest |
|---|---|---|---|
| TF-IDF | ~0.71 | ~0.71 | ~0.71 |
| Metrics | ~0.58 | ~0.58 | ~0.64 |
| Combined | ~0.71 | ~0.71 | ~0.69 |
| Full (with embeddings) | ~0.76 | ~0.76 | ~0.62 |

---

## Neural Network Results ⭐

| Model | Accuracy |
|---|---|
| MLP + Embeddings + TF-IDF + Metrics | **~0.86** |

---

# 📈 Key Insights

## ✅ Semantic embeddings significantly improve performance

CodeBERT embeddings improved accuracy substantially compared to traditional features alone.

---

## ✅ Metrics alone are weak predictors

Simple structural metrics achieved only ~58–64% accuracy.

---

## ✅ Hybrid feature engineering works best

Combining:

- semantic embeddings
- TF-IDF
- structural features

produced the strongest results.

---

## ✅ Larger datasets reduced overfitting

Earlier experiments on small datasets achieved unrealistically high test accuracy (~100%), indicating overfitting.

Increasing dataset size improved:

- generalization
- robustness
- reliability of evaluation

---

## ✅ Neural networks outperformed classical models

The final MLP achieved approximately:

```math
86\% \text{ accuracy}
```

on the large-scale hybrid dataset.

---

# 🔍 Explainability

The project also includes an explainability pipeline.

The explainability module:

- predicts whether code is vulnerable
- outputs confidence scores
- identifies influential features/tokens

### Example Important Features

- `malloc`
- `strcpy`
- `NULL`
- `return`
- `char`

This improves interpretability of model decisions.

---

# 🏗️ Project Structure

```text
code_quality_ml/
│
├── data/
│   ├── generate_dataset.py
│   ├── juliet_loader.py
│
├── features/
│   ├── feature_extractor.py
│   ├── embedding_extractor.py
│   ├── save_embeddings.py
│
├── models/
│   ├── train.py
│   ├── train_neural.py
│   ├── train_xgboost.py
│   ├── explain.py
│   ├── neural_net.py
│   ├── plot_results.py
│
├── predict.py
├── main.py
├── requirements.txt
├── README.md
│
├── dataset.csv                (generated locally)
├── embeddings.npy             (generated locally)
├── model.pkl                  (generated locally)
├── best_neural_model.pth      (generated locally)
```

---

# 🚀 Setup Instructions

## 1️⃣ Clone Repository

```bash
git clone https://github.com/sauravcodes-dotcom/ML-project.git

cd ML-project
```

---

## 2️⃣ Create Virtual Environment

### Mac/Linux

```bash
python -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📊 Generate Dataset

```bash
python -m data.generate_dataset
```

This step:

- Generates synthetic vulnerable code
- Loads Juliet dataset
- Creates hybrid dataset

Output:

```text
dataset.csv
```

---

# 🧠 Generate CodeBERT Embeddings

```bash
python -m features.save_embeddings
```

Outputs:

```text
embeddings.npy
labels.npy
```

---

# 🤖 Train Classical Models

```bash
python -m models.train
```

This step:

- Extracts features
- Trains ML models
- Evaluates performance
- Saves explainable model

Output:

```text
model.pkl
```

---

# 🧠 Train Neural Network

```bash
python -m models.train_neural
```

Outputs:

```text
best_neural_model.pth
```

---

# 📈 Generate Evaluation Plots

```bash
python -m models.plot_results
```

Generates:

- Accuracy comparison plots
- Feature engineering plots
- Learning curves
- Dataset scaling analysis

---

# 🔍 Run Explainability

```bash
python -m models.explain
```

Example output:

```text
Prediction: Vulnerable Code
Confidence: 0.92

Important Features:
malloc
strcpy
NULL
char
```

---

# ⚠️ Important Notes

The following files are generated locally and are NOT included in the repository:

- `dataset.csv`
- `embeddings.npy`
- `labels.npy`
- `model.pkl`
- `*.pth`

---

# 📥 Juliet Dataset Download

Download Juliet dataset from:

https://samate.nist.gov/SARD/test-suites/112

---

# 🔮 Future Improvements

- AST-based feature extraction
- Graph Neural Networks (GNNs)
- Fine-tuning CodeBERT
- Multi-language support
- CI/CD integration
- Real-world GitHub vulnerability mining
- Transformer-based end-to-end classifiers

---

# 🧠 Final Takeaway

This project demonstrates that combining:

- semantic embeddings
- traditional feature engineering
- deep learning

can effectively detect vulnerable code patterns at scale.

The final hybrid neural system achieved approximately:

# ⭐ ~86% Test Accuracy

while maintaining improved generalization on a large and diverse vulnerability dataset.
