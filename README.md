🧠 Predicting Code Quality using Machine Learning
📌 Overview

This project predicts whether a given code snippet is buggy or safe using machine learning.

We combine:

synthetic code generation (100+ templates)
real-world vulnerability data (Juliet Test Suite)
multiple feature representations
multiple ML models

to build a robust code quality classifier.

⚙️ Problem Statement

Manual code review is slow and error-prone.
This project aims to automatically detect buggy code patterns using ML.

📦 Dataset

We use a hybrid dataset (~10,000 samples):

🔹 Synthetic Data (60%)
Generated using 100+ templates
Covers multiple bug types:
NULL pointer dereference
buffer overflow
divide-by-zero
uninitialized variables
Includes:
variable renaming
formatting variation
label noise
🔹 Juliet Dataset (40%)
Real-world vulnerability dataset (C language)
Labeled:
good → safe (0)
bad → buggy (1)
🤔 Why Juliet (and not others)?
Dataset	Reason not used
Defects4J	Requires mapping commits → functions (complex preprocessing)
CodeSearchNet	No bug labels (not suitable for classification)

👉 Juliet provides clean, labeled vulnerability data, making it ideal for supervised learning.

🧩 Feature Engineering

We extract multiple feature types:

1️⃣ TF-IDF (Syntax)
Token-level representation
Captures patterns like:
if, return, *, NULL
2️⃣ Code Metrics
Simple structural indicators:
Lines of code (LOC)
number of loops
number of conditions
3️⃣ Structural Patterns (Explored)
Pointer usage
brace counts
basic structure signals
4️⃣ CodeBERT Embeddings ⭐ (Most Important)
768-dimensional semantic vectors
Captures:
meaning
context
code behavior
🤖 Models Used
Logistic Regression → strong linear baseline
Linear SVM → sensitive to high-dimensional data
Random Forest ⭐ → best performing (non-linear model)
📊 Results (Final)
Feature Set	Logistic Regression	SVM	Random Forest
TF-IDF	~0.75	~0.75	~0.83
Combined	~0.76	~0.54	~0.84
Full (with embeddings)	~0.88	~0.63	~0.89 (BEST)
💡 Key Insights
CodeBERT embeddings significantly improve performance (~+10%)
Random Forest performs best due to non-linear feature interactions
Metrics alone are weak (~0.58 accuracy)
Performance saturates around ~89% → more data alone won’t help
🏗️ Project Structure
code_quality_ml/
│
├── data/
│   ├── generate_dataset.py
│   ├── juliet_loader.py
│
├── features/
│   ├── feature_extractor.py
│   ├── embedding_extractor.py
│
├── models/
│   ├── train.py
│
├── dataset.csv (generated, NOT tracked)
├── model.pkl (generated, NOT tracked)
🚀 Setup Instructions
1️⃣ Clone the repo
git clone https://github.com/sauravcodes-dotcom/ML-project.git
cd ML-project
2️⃣ Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
3️⃣ Install dependencies
pip install -r requirements.txt
📊 Generate Dataset
python -m data.generate_dataset

👉 This will:

generate synthetic data
load Juliet dataset
create dataset.csv
🧠 Train Models
python -m models.train

👉 This will:

extract features
train models
print evaluation metrics
save best model (model.pkl)
🔍 Make Predictions
python predict.py

(or your custom inference script)

⚠️ Important Notes
dataset.csv and model.pkl are not included in repo
They are generated locally
Juliet dataset must be downloaded separately:
https://samate.nist.gov/SARD/test-suites/112
🔮 Future Work
AST-based feature extraction
Multi-language support (Python, Java)
Fine-tuning CodeBERT (deep learning)
CI/CD integration for automated code review
Larger and more diverse datasets
🧠 Key Takeaway
Combining semantic embeddings with traditional features enables accurate bug detection (~89% accuracy), with Random Forest performing best due to its ability to model non-linear interactions.
