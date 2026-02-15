import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

from app.utils.url_features import url_to_features

def main():
    df = pd.read_csv("data/url_train.csv")
    X = df["url"].astype(str).map(url_to_features).tolist()
    y = df["label"].astype(int).tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = LogisticRegression(max_iter=5000, class_weight="balanced")
    model.fit(X_train, y_train)

    pred = model.predict(X_test)
    print(classification_report(y_test, pred))

    joblib.dump(model, "ml/artifacts/url_model.joblib")
    print("Saved: ml/artifacts/url_model.joblib")

if __name__ == "__main__":
    main()
