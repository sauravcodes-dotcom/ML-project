import pickle
import numpy as np

def predict_code(code):
    with open("model.pkl", "rb") as f:
        model, extractor, embedder = pickle.load(f)

    X_basic = extractor.transform([code])
    X_embed = embedder.embed([code])

    X = np.hstack((X_basic, X_embed * 0.5))

    pred = model.predict(X)[0]
    return "BUGGY" if pred == 1 else "SAFE"


if __name__ == "__main__":
    code = input("Enter code snippet:\n")
    print("Prediction:", predict_code(code))