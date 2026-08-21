import pandas as pd
import re
import joblib

from nltk.corpus import stopwords

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

from sklearn.metrics import accuracy_score, classification_report


# ==================================================
# 1. LOAD DATASET
# ==================================================

data = pd.read_csv(
    "data/SMSSpamCollection",
    sep="\t",
    header=None,
    names=["label", "message"]
)

print("Dataset loaded successfully!")
print("Total messages:", len(data))


# ==================================================
# 2. CONVERT LABELS
# ==================================================

data["label_num"] = data["label"].map({
    "ham": 0,
    "spam": 1
})


# ==================================================
# 3. TEXT CLEANING
# ==================================================

stop_words = set(stopwords.words("english"))


def clean_text(text):
    text = text.lower()

    # Remove numbers and special characters
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Split into words
    words = text.split()

    # Remove stopwords
    words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(words)


data["clean_message"] = data["message"].apply(clean_text)


# ==================================================
# 4. FEATURES AND TARGET
# ==================================================

X = data["clean_message"]
y = data["label_num"]


# ==================================================
# 5. TRAIN / TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training messages:", len(X_train))
print("Testing messages:", len(X_test))


# ==================================================
# 6. TF-IDF
# ==================================================

vectorizer = TfidfVectorizer(
    max_features=5000
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)


# ==================================================
# 7. CREATE MODELS
# ==================================================

models = {

    "Logistic Regression":
        LogisticRegression(),

    "Naive Bayes":
        MultinomialNB(),

    "Linear SVM":
        LinearSVC()
}


# ==================================================
# 8. TRAIN AND COMPARE MODELS
# ==================================================

results = {}

best_model = None
best_accuracy = 0
best_model_name = ""


for name, model in models.items():

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    # Train model
    model.fit(X_train_tfidf, y_train)

    # Predict
    y_pred = model.predict(X_test_tfidf)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)

    results[name] = accuracy

    print(
        "Accuracy:",
        round(accuracy * 100, 2),
        "%"
    )

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=[
                "Legitimate",
                "Scam/Spam"
            ]
        )
    )

    # Find best model
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name


# ==================================================
# 9. MODEL COMPARISON
# ==================================================

print("\n")
print("=" * 50)
print("MODEL COMPARISON")
print("=" * 50)

for name, accuracy in results.items():

    print(
        f"{name}: {accuracy * 100:.2f}%"
    )


# ==================================================
# 10. SAVE BEST MODEL
# ==================================================

joblib.dump(
    best_model,
    "models/scamshield_model.pkl"
)

joblib.dump(
    vectorizer,
    "models/tfidf_vectorizer.pkl"
)

print("\n")
print("=" * 50)
print("BEST MODEL SAVED")
print("=" * 50)

print("Best model:", best_model_name)
print(
    "Accuracy:",
    round(best_accuracy * 100, 2),
    "%"
)

print("\nModel saved to:")
print("models/scamshield_model.pkl")

print("\nTF-IDF vectorizer saved to:")
print("models/tfidf_vectorizer.pkl")