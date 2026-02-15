import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import classification_report

from app.utils.text_normalize import normalize_text

def main():
    df = pd.read_csv("data/text_train.csv")
    df["text"] = df["text"].astype(str).map(normalize_text)

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"]
    )

    base = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), analyzer="word", max_features=120000)),
        ("clf", LogisticRegression(max_iter=2000, class_weight="balanced"))
    ])

    cal = CalibratedClassifierCV(base, method="isotonic", cv=3)
    cal.fit(X_train, y_train)

    pred = cal.predict(X_test)
    print(classification_report(y_test, pred))

    joblib.dump(cal, "ml/artifacts/text_model.joblib")
    print("Saved: ml/artifacts/text_model.joblib")

if __name__ == "__main__":
    main()
