import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report

from features.feature_extractor import FeatureExtractor
from features.embedding_extractor import CodeBERTEmbedder


def run_experiment(X, y, name):
    print(f"\n===== {name} =====")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    models = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "LinearSVM": LinearSVC()
    }

    results = {}

    for mname, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        print(f"\nModel: {mname}")
        print(classification_report(y_test, preds))

        acc = model.score(X_test, y_test)
        results[mname] = acc

        # 🔥 Error analysis
        for i in range(len(preds)):
            if preds[i] != y_test[i]:
                print("\nExample misclassified sample:")
                print("Pred:", preds[i], "Actual:", y_test[i])
                break

    return results


def train():
    print("Loading dataset...")
    df = pd.read_csv("dataset.csv")

    # 🔥 Dataset size experiment (optional)
    sizes = [1000, 5000, len(df)]

    extractor = FeatureExtractor()
    embedder = CodeBERTEmbedder()

    final_results = {}

    for size in sizes:
        print(f"\n\n========== DATASET SIZE: {size} ==========")
        sub_df = df.sample(size, random_state=42)

        codes = sub_df["code"].tolist()
        y = sub_df["label"].values

        # ---- Feature sets ----
        X_tfidf = extractor.fit_transform(codes, mode="tfidf")
        X_metrics = extractor.fit_transform(codes, mode="metrics")
        X_combined = extractor.fit_transform(codes, mode="combined")

        print("\nExtracting embeddings...")
        X_embed = embedder.embed(codes)

        X_full = np.hstack((X_combined, X_embed * 0.2))

        # ---- Experiments ----
        res = {}
        res["TF-IDF"] = run_experiment(X_tfidf, y, "TF-IDF")
        res["Metrics"] = run_experiment(X_metrics, y, "Metrics")
        res["Combined"] = run_experiment(X_combined, y, "Combined")
        res["Full"] = run_experiment(X_full, y, "Full (with embeddings)")

        final_results[size] = res

    # 🔥 Print summary table
    print("\n\n====== FINAL SUMMARY ======")
    for size, res in final_results.items():
        print(f"\nDataset size: {size}")
        for feature_type, models in res.items():
            for model, acc in models.items():
                print(f"{feature_type} | {model} → {acc:.3f}")

    # Save final model (full features)
    print("\nSaving final model...")
    X = X_full
    y = y

    model = LinearSVC()
    model.fit(X, y)

    with open("model.pkl", "wb") as f:
        pickle.dump((model, extractor, embedder), f)

    print("Done.")


if __name__ == "__main__":
    train()