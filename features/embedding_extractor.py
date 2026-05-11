from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np


class CodeBERTEmbedder:
    def __init__(self, model_name="microsoft/codebert-base", device=None):
        self.device = device if device else ("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

    def embed(self, code_list, batch_size=16, max_length=256):
        embeddings = []

        print(len(code_list), "code snippets to embed...")

        for i in range(0, len(code_list), batch_size):
            batch = code_list[i:i + batch_size]

            inputs = self.tokenizer(
                batch,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**inputs)

            # CLS token embedding
            cls_embeddings = outputs.last_hidden_state[:, 0, :]
            embeddings.append(cls_embeddings.cpu().numpy())

        return np.vstack(embeddings)