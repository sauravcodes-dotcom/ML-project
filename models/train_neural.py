# ONLY EMBEDDINGS
# 
# import numpy as np
# import torch
# import torch.nn as nn

# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report
# from sklearn.metrics import accuracy_score
# from sklearn.preprocessing import StandardScaler

# from models.neural_net import MLP


# def train():

#     print("Loading saved embeddings...")

#     X = np.load("embeddings.npy")
#     y = np.load("labels.npy")

#     X = X.astype(np.float32)
#     y = y.astype(np.float32)

#     print(f"Dataset shape: {X.shape}")

#     print("Normalizing embeddings...")

#     scaler = StandardScaler()

#     X = scaler.fit_transform(X)

#     X = X.astype(np.float32)

#     X_train, X_test, y_train, y_test = train_test_split(
#         X,
#         y,
#         test_size=0.2,
#         random_state=42,
#         stratify=y
#     )

#     X_train = torch.tensor(X_train)
#     X_test = torch.tensor(X_test)

#     y_train = torch.tensor(y_train).unsqueeze(1)
#     y_test = torch.tensor(y_test).unsqueeze(1)

#     device = torch.device(
#         "cuda" if torch.cuda.is_available() else "cpu"
#     )

#     print(f"Using device: {device}")

#     X_train = X_train.to(device)
#     X_test = X_test.to(device)

#     y_train = y_train.to(device)
#     y_test = y_test.to(device)

#     model = MLP(
#         input_dim=X.shape[1]
#     ).to(device)

#     criterion = nn.BCEWithLogitsLoss()

#     optimizer = torch.optim.AdamW(
#         model.parameters(),
#         lr=0.0005,
#         weight_decay=1e-4
#     )

#     scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
#         optimizer,
#         mode="max",
#         factor=0.5,
#         patience=3
#     )

#     epochs = 50
#     batch_size = 128

#     best_acc = 0

#     print("\nTraining neural network...\n")

#     for epoch in range(epochs):

#         model.train()

#         permutation = torch.randperm(
#             X_train.size()[0]
#         )

#         total_loss = 0

#         for i in range(
#             0,
#             X_train.size()[0],
#             batch_size
#         ):

#             indices = permutation[i:i + batch_size]

#             batch_x = X_train[indices]
#             batch_y = y_train[indices]

#             optimizer.zero_grad()

#             outputs = model(batch_x)

#             loss = criterion(
#                 outputs,
#                 batch_y
#             )

#             loss.backward()

#             torch.nn.utils.clip_grad_norm_(
#                 model.parameters(),
#                 max_norm=1.0
#             )

#             optimizer.step()

#             total_loss += loss.item()

#         print(f"\nEpoch {epoch + 1}/{epochs}")
#         print(f"Loss: {total_loss:.4f}")

#         model.eval()

#         with torch.no_grad():

#             outputs = model(X_test)

#             predictions = torch.sigmoid(outputs)

#             predictions = (
#                 predictions > 0.5
#             ).float()

#         y_pred = predictions.cpu().numpy()

#         accuracy = accuracy_score(
#             y_test.cpu().numpy(),
#             y_pred
#         )

#         print(
#             f"Validation Accuracy: "
#             f"{accuracy:.4f}"
#         )

#         scheduler.step(accuracy)

#         current_lr = optimizer.param_groups[0]["lr"]

#         print(f"Learning Rate: {current_lr}")

#         if accuracy > best_acc:

#             best_acc = accuracy

#             torch.save(
#                 model.state_dict(),
#                 "best_neural_model.pth"
#             )

#             print("Best model saved.")

#     print("\nFinal Evaluation\n")

#     print(
#         classification_report(
#             y_test.cpu().numpy(),
#             y_pred
#         )
#     )

#     print(
#         f"\nBest Accuracy: "
#         f"{best_acc:.4f}"
#     )


# if __name__ == "__main__":
#     train()


import numpy as np
import pandas as pd

import torch
import torch.nn as nn

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from features.feature_extractor import FeatureExtractor
from models.neural_net import MLP


def train():

    # ==================================================
    # LOAD DATASET
    # ==================================================

    print("Loading dataset...")

    df = pd.read_csv("dataset.csv")

    codes = df["code"].tolist()
    y = df["label"].values

    # ==================================================
    # LOAD EMBEDDINGS
    # ==================================================

    print("Loading saved embeddings...")

    X_embed = np.load("embeddings.npy")

    print(f"Embeddings shape: {X_embed.shape}")

    # ==================================================
    # FEATURE EXTRACTION
    # ==================================================

    extractor = FeatureExtractor()

    print("Extracting TF-IDF features...")

    X_tfidf = extractor.fit_transform(
        codes,
        mode="tfidf"
    )

    print("Extracting metric features...")

    X_metrics = extractor.fit_transform(
        codes,
        mode="metrics"
    )

    # ==================================================
    # PCA ON EMBEDDINGS
    # ==================================================

    print("Reducing embedding dimensions with PCA...")

    pca = PCA(n_components=100)

    X_embed = pca.fit_transform(X_embed)

    # ==================================================
    # COMBINE FEATURES
    # ==================================================

    print("Combining all features...")

    X_tfidf_dense = X_tfidf

    X_combined = np.hstack([
        X_tfidf_dense,
        X_metrics
    ])

    X_full = np.hstack([
        X_combined,
        X_embed
    ])

    print(f"Final feature shape: {X_full.shape}")

    # ==================================================
    # NORMALIZATION
    # ==================================================

    print("Normalizing features...")

    scaler = StandardScaler()

    X_full = scaler.fit_transform(X_full)

    X_full = X_full.astype(np.float32)
    y = y.astype(np.float32)

    # ==================================================
    # TRAIN TEST SPLIT
    # ==================================================

    print("Splitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X_full,
        y,
        test_size=0.2,
        random_state=42
    )

    # ==================================================
    # DEVICE
    # ==================================================

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print(f"Using device: {device}")

    # ==================================================
    # TENSORS
    # ==================================================

    X_train = torch.tensor(X_train).to(device)
    X_test = torch.tensor(X_test).to(device)

    y_train = torch.tensor(y_train).unsqueeze(1).to(device)
    y_test = torch.tensor(y_test).unsqueeze(1).to(device)

    # ==================================================
    # MODEL
    # ==================================================

    model = MLP(
        input_dim=X_full.shape[1]
    ).to(device)

    criterion = nn.BCEWithLogitsLoss()

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=0.0005,
        weight_decay=1e-4
    )

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="max",
        factor=0.5,
        patience=3
    )

    # ==================================================
    # TRAINING
    # ==================================================

    epochs = 50
    batch_size = 128

    best_acc = 0

    print("\nTraining neural network...\n")

    for epoch in range(epochs):

        model.train()

        permutation = torch.randperm(
            X_train.size()[0]
        )

        total_loss = 0

        for i in range(0, X_train.size()[0], batch_size):

            indices = permutation[i:i + batch_size]

            batch_x = X_train[indices]
            batch_y = y_train[indices]

            optimizer.zero_grad()

            outputs = model(batch_x)

            loss = criterion(outputs, batch_y)

            loss.backward()

            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                1.0
            )

            optimizer.step()

            total_loss += loss.item()

        # ==================================================
        # VALIDATION
        # ==================================================

        model.eval()

        with torch.no_grad():

            outputs = model(X_test)

            predictions = torch.sigmoid(outputs)

            predictions = (
                predictions > 0.5
            ).float()

        y_pred = predictions.cpu().numpy()

        accuracy = accuracy_score(
            y_test.cpu().numpy(),
            y_pred
        )

        scheduler.step(accuracy)

        print(f"\nEpoch {epoch+1}/{epochs}")
        print(f"Loss: {total_loss:.4f}")
        print(f"Validation Accuracy: {accuracy:.4f}")

        print(
            f"Learning Rate: "
            f"{optimizer.param_groups[0]['lr']}"
        )

        if accuracy > best_acc:

            best_acc = accuracy

            torch.save(
                model.state_dict(),
                "best_neural_model.pth"
            )

            print("Best model saved.")

    # ==================================================
    # FINAL REPORT
    # ==================================================

    print("\nFinal Evaluation\n")

    print(
        classification_report(
            y_test.cpu().numpy(),
            y_pred
        )
    )

    print(f"\nBest Accuracy: {best_acc:.4f}")


if __name__ == "__main__":
    train()