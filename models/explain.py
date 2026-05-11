import pickle
import numpy as np


def load_model():

    with open("model.pkl", "rb") as f:

        data = pickle.load(f)

    model = data["model"]

    extractor = data["extractor"]

    feature_count = data["feature_count"]

    return model, extractor, feature_count


def explain_code(code):

    model, extractor, feature_count = load_model()

    # Extract TF-IDF features
    X = extractor.transform(
        [code],
        mode="tfidf"
    )

    # Predict
    prediction = model.predict(X)[0]

    # Confidence
    probabilities = model.predict_proba(X)[0]

    confidence = np.max(probabilities)

    # Feature importance
    feature_names = extractor.vectorizer.get_feature_names_out()

    coefs = model.coef_[0]

    x_dense = X[0]

    important_features = []

    for idx, value in enumerate(x_dense):

        if value > 0:

            important_features.append(
                (
                    feature_names[idx],
                    coefs[idx] * value
                )
            )

    # Sort by absolute importance
    important_features = sorted(
        important_features,
        key=lambda x: abs(x[1]),
        reverse=True
    )

    top_features = important_features[:10]

    return prediction, confidence, top_features


if __name__ == "__main__":

    sample_code = """
    #include <stdio.h>
    #include <string.h>

    int main() {

        char buffer[10];

        gets(buffer);

        printf("%s", buffer);

        return 0;
    }
    """

    pred, conf, features = explain_code(sample_code)

    print("\n===== PREDICTION =====")

    if pred == 1:

        print("Vulnerable Code")

    else:

        print("Safe Code")

    print(f"Confidence: {conf:.4f}")

    print("\n===== TOP IMPORTANT FEATURES =====")

    for feat, score in features:

        print(f"{feat:20} {score:.4f}")