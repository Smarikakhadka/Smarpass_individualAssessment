import pandas as pd
import string
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# -------------------------------
# Feature extraction
# -------------------------------
def extract_features(password):
    return [
        len(password),
        sum(c.isdigit() for c in password),
        sum(c.isupper() for c in password),
        sum(c.islower() for c in password),
        sum(c in string.punctuation for c in password)
    ]

# -------------------------------
# Load dataset
# -------------------------------
df = pd.read_csv("random_password.csv")

X = df["password"].apply(lambda x: extract_features(x)).tolist()
y = df["strength"]

# -------------------------------
# Train model
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# -------------------------------
# Accuracy (important for report)
# -------------------------------
accuracy = model.score(X_test, y_test)
print("Model Accuracy:", accuracy)

# -------------------------------
# Prediction function
# -------------------------------
def predict_strength(password):
    features = [extract_features(password)]
    return model.predict(features)[0]

# -------------------------------
# Explain prediction (for UI + viva)
# -------------------------------
def explain_prediction(password):
    reasons = []

    if len(password) >= 12:
        reasons.append("long length")
    else:
        reasons.append("short length")

    if any(c.isdigit() for c in password):
        reasons.append("includes numbers")

    if any(c.isupper() for c in password):
        reasons.append("includes uppercase")

    if any(c.islower() for c in password):
        reasons.append("includes lowercase")

    if any(c in string.punctuation for c in password):
        reasons.append("includes symbols")

    return ", ".join(reasons)