import matplotlib.pyplot as plt
import numpy as np


# =====================================================
# DATASET SIZE EXPERIMENTS
# =====================================================

dataset_sizes = [1000, 20000, 38412]

# Best classical ML model from each feature category
tfidf_scores = [0.71, 0.71, 0.714]

metrics_scores = [0.69, 0.66, 0.64]

combined_scores = [0.71, 0.73, 0.712]

full_scores = [0.69, 0.74, 0.763]

# Neural network
neural_scores = [0.72, 0.81, 0.8605]


# =====================================================
# PLOT 1 — DATASET SIZE VS ACCURACY
# =====================================================

plt.figure(figsize=(10, 6))

plt.plot(
    dataset_sizes,
    tfidf_scores,
    marker='o',
    linewidth=3,
    label="TF-IDF"
)

plt.plot(
    dataset_sizes,
    metrics_scores,
    marker='o',
    linewidth=3,
    label="Metrics"
)

plt.plot(
    dataset_sizes,
    combined_scores,
    marker='o',
    linewidth=3,
    label="Combined"
)

plt.plot(
    dataset_sizes,
    full_scores,
    marker='o',
    linewidth=3,
    label="Full + Embeddings"
)

plt.plot(
    dataset_sizes,
    neural_scores,
    marker='o',
    linewidth=3,
    linestyle='--',
    label="Neural Network"
)

plt.xlabel("Dataset Size")

plt.ylabel("Accuracy")

plt.title("Dataset Size vs Model Accuracy")

plt.ylim(0.55, 0.9)

plt.xticks(dataset_sizes)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig("dataset_size_vs_accuracy.png")

print("Saved: dataset_size_vs_accuracy.png")

plt.close()


# =====================================================
# PLOT 2 — CLASSICAL MODEL COMPARISON
# =====================================================

results = {

    "TF-IDF": {
        "LogisticRegression": 0.709,
        "LinearSVM": 0.708,
        "RandomForest": 0.714
    },

    "Metrics": {
        "LogisticRegression": 0.579,
        "LinearSVM": 0.579,
        "RandomForest": 0.640
    },

    "Combined": {
        "LogisticRegression": 0.711,
        "LinearSVM": 0.712,
        "RandomForest": 0.694
    },

    "Full + Embeddings": {
        "LogisticRegression": 0.762,
        "LinearSVM": 0.763,
        "RandomForest": 0.623
    }
}

feature_sets = list(results.keys())

lr_scores = [
    results[x]["LogisticRegression"]
    for x in feature_sets
]

svm_scores = [
    results[x]["LinearSVM"]
    for x in feature_sets
]

rf_scores = [
    results[x]["RandomForest"]
    for x in feature_sets
]

x = np.arange(len(feature_sets))
width = 0.25

plt.figure(figsize=(10, 6))

plt.bar(
    x - width,
    lr_scores,
    width,
    label="Logistic Regression"
)

plt.bar(
    x,
    svm_scores,
    width,
    label="Linear SVM"
)

plt.bar(
    x + width,
    rf_scores,
    width,
    label="Random Forest"
)

plt.xticks(x, feature_sets)

plt.ylabel("Accuracy")

plt.ylim(0.5, 0.9)

plt.title("Classical ML Model Comparison")

plt.legend()

plt.grid(axis='y')

plt.tight_layout()

plt.savefig("classical_models_comparison.png")

print("Saved: classical_models_comparison.png")

plt.close()


# =====================================================
# PLOT 3 — FEATURE ENGINEERING IMPACT
# =====================================================

best_scores = [
    max(results[x].values())
    for x in feature_sets
]

plt.figure(figsize=(8, 5))

plt.plot(
    feature_sets,
    best_scores,
    marker='o',
    linewidth=3
)

plt.ylabel("Best Accuracy")

plt.ylim(0.5, 0.9)

plt.title("Impact of Feature Engineering")

plt.grid(True)

plt.tight_layout()

plt.savefig("feature_engineering_impact.png")

print("Saved: feature_engineering_impact.png")

plt.close()


# =====================================================
# PLOT 4 — FINAL MODEL COMPARISON
# =====================================================

final_models = [
    "Best Classical ML",
    "Neural Network"
]

final_scores = [
    0.763,
    0.8605
]

plt.figure(figsize=(7, 5))

bars = plt.bar(
    final_models,
    final_scores
)

plt.ylabel("Accuracy")

plt.ylim(0.5, 0.95)

plt.title("Final Model Comparison")

for bar, score in zip(bars, final_scores):

    plt.text(
        bar.get_x() + bar.get_width()/2,
        score + 0.01,
        f"{score:.3f}",
        ha='center'
    )

plt.tight_layout()

plt.savefig("final_model_comparison.png")

print("Saved: final_model_comparison.png")

plt.close()


# =====================================================
# PLOT 5 — NEURAL NETWORK LEARNING CURVE
# =====================================================

epochs = list(range(1, 51))

accuracies = [
    0.7082, 0.7182, 0.7307, 0.7401, 0.7519,
    0.7639, 0.7698, 0.7842, 0.7994, 0.7895,
    0.8109, 0.8182, 0.8205, 0.8153, 0.8278,
    0.8279, 0.8288, 0.8153, 0.8337, 0.8260,
    0.8287, 0.8342, 0.8389, 0.8389, 0.8409,
    0.8424, 0.8425, 0.8452, 0.8381, 0.8391,
    0.8395, 0.8467, 0.8471, 0.8412, 0.8503,
    0.8527, 0.8449, 0.8450, 0.8482, 0.8394,
    0.8529, 0.8529, 0.8579, 0.8518, 0.8538,
    0.8471, 0.8546, 0.8550, 0.8584, 0.8605
]

plt.figure(figsize=(10, 5))

plt.plot(
    epochs,
    accuracies,
    linewidth=2
)

plt.xlabel("Epoch")

plt.ylabel("Validation Accuracy")

plt.title("Neural Network Learning Curve")

plt.ylim(0.65, 0.9)

plt.grid(True)

plt.tight_layout()

plt.savefig("neural_learning_curve.png")

print("Saved: neural_learning_curve.png")

plt.close()


# =====================================================
# PLOT 6 — CLASSIFICATION METRICS
# =====================================================

metrics = ["Precision", "Recall", "F1-Score"]

safe_scores = [0.84, 0.89, 0.87]

vuln_scores = [0.88, 0.83, 0.86]

x = np.arange(len(metrics))

plt.figure(figsize=(8, 5))

plt.bar(
    x - 0.2,
    safe_scores,
    width=0.4,
    label="Safe Code"
)

plt.bar(
    x + 0.2,
    vuln_scores,
    width=0.4,
    label="Vulnerable Code"
)

plt.xticks(x, metrics)

plt.ylim(0.7, 1.0)

plt.ylabel("Score")

plt.title("Neural Network Classification Metrics")

plt.legend()

plt.grid(axis='y')

plt.tight_layout()

plt.savefig("classification_metrics.png")

print("Saved: classification_metrics.png")

plt.close()


print("\nAll plots generated successfully.")