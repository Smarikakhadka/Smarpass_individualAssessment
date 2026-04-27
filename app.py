from flask import Flask, render_template, request, jsonify
import re
import random
import string
from model import predict_strength, explain_prediction

app = Flask(__name__)

common_passwords = ["123456", "password", "qwerty", "abc123", "111111", "letmein"]

def detect_patterns(password):
    patterns = []

    if re.search(r"(.)\1{2,}", password):
        patterns.append("repeated characters")

    if re.search(r"\d{4}", password):
        patterns.append("possible date pattern")

    if password.lower() in ["sachin", "ram", "admin"]:
        patterns.append("common name usage")

    return patterns


def generate_password():
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(12))


def check_password_strength(password):
    score = 0
    feedback = []
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short")
        suggestions.append("Use at least 12 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Missing uppercase")
        suggestions.append("Add uppercase letters")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Missing lowercase")
        suggestions.append("Add lowercase letters")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Missing number")
        suggestions.append("Add numbers")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Missing special character")
        suggestions.append("Add symbols like @, #, $")

    if password.lower() in common_passwords:
        feedback.append("Common password detected")
        suggestions.append("Avoid common passwords")
        score = 0

    # Pattern detection
    patterns = detect_patterns(password)
    for p in patterns:
        feedback.append(f"Pattern detected: {p}")

    # Strength
    if score <= 2:
        strength = "Weak"
        crack_time = "Seconds"
    elif score <= 4:
        strength = "Medium"
        crack_time = "Hours to days"
    else:
        strength = "Strong"
        crack_time = "Years"

    score_percentage = int((score / 5) * 100)

    # ML
    ml_prediction = predict_strength(password)
    ml_reason = explain_prediction(password)

    return {
        "score_percentage": score_percentage,
        "strength": strength,
        "feedback": feedback,
        "suggestions": suggestions,
        "crack_time": crack_time,
        "ml_prediction": ml_prediction,
        "ml_reason": ml_reason
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    password = request.json.get("password")
    return jsonify(check_password_strength(password))


@app.route("/generate", methods=["GET"])
def generate():
    pwd = generate_password()
    result = check_password_strength(pwd)

    return jsonify({
        "generated_password": pwd,
        "generated_strength": result["strength"],
        "generated_score": result["score_percentage"]
    })


if __name__ == "__main__":
    app.run(debug=True)