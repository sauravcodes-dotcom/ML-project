import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class FeatureExtractor:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=100)

    def code_metrics(self, code):
        return [
            len(code),
            code.count("if"),
            code.count("for"),
            code.count("while"),
        ]

    
    def ast_features(self, code):
        return [
            code.count("{"),
            code.count("}"),
            code.count("("),
            code.count(")"),
        ]

    def fit_transform(self, codes, mode="full"):
        tfidf = self.vectorizer.fit_transform(codes).toarray()
        metrics = np.array([self.code_metrics(c) for c in codes])
        ast = np.array([self.ast_features(c) for c in codes])

        if mode == "tfidf":
            return tfidf
        elif mode == "metrics":
            return metrics
        elif mode == "combined":
            return np.hstack((tfidf, metrics))
        else:  # full
            return np.hstack((tfidf, metrics, ast))

    def transform(self, codes, mode="full"):
        tfidf = self.vectorizer.transform(codes).toarray()
        metrics = np.array([self.code_metrics(c) for c in codes])
        ast = np.array([self.ast_features(c) for c in codes])

        if mode == "tfidf":
            return tfidf
        elif mode == "metrics":
            return metrics
        elif mode == "combined":
            return np.hstack((tfidf, metrics))
        else:
            return np.hstack((tfidf, metrics, ast))