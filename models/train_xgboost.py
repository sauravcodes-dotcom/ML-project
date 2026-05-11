import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

from xgboost import XGBClassifier


def train():

    print("Loading embeddings...")

    X = np.load("embeddings.npy")
    y = np.load("labels.npy")

    X = X.astype(np.float32)

    print("Normalizing embeddings...")

    scaler = StandardScaler()

    X = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print("Training XGBoost model...\n")

    model = XGBClassifier(

        n_estimators=500,
        max_depth=8,
        learning_rate=0.05,

        subsample=0.8,
        colsample_bytree=0.8,

        objective="binary:logistic",

        eval_metric="logloss",

        tree_method="hist",

        random_state=42
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print(classification_report(y_test, predictions))

    accuracy = accuracy_score(y_test, predictions)

    print(f"\nAccuracy: {accuracy:.4f}")


if __name__ == "__main__":
    train()