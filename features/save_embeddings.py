import pandas as pd
import numpy as np

from features.embedding_extractor import CodeBERTEmbedder


def main():

    print("Loading dataset...")

    df = pd.read_csv("dataset.csv")

    codes = df["code"].tolist()
    labels = df["label"].values

    print("Generating embeddings...")

    embedder = CodeBERTEmbedder()

    embeddings = embedder.embed(codes)

    embeddings = np.array(embeddings)

    print("Saving embeddings...")

    np.save("embeddings.npy", embeddings)
    np.save("labels.npy", labels)

    print("Done.")


if __name__ == "__main__":
    main()