from flask import Flask, render_template, request
import itertools
import string
import time
import os

app = Flask(__name__)

# -----------------------------
# Password Cracking Function (UPDATED)
# -----------------------------
def crack_password(password):
    chars = string.ascii_letters + string.digits + "!@#$%"
    attempts = 0
    start_time = time.time()
    max_attempts = 500000  # limit to avoid long waiting

    for length in range(1, len(password) + 1):
        for guess in itertools.product(chars, repeat=length):
            guess = ''.join(guess)
            attempts += 1

            if guess == password:
                end_time = time.time()
                return attempts, round(end_time - start_time, 4)

            # Stop if too complex
            if attempts > max_attempts:
                return "Too Complex", "Time Exceeded"

    return attempts, None

# -----------------------------
# Password Strength Checker
# -----------------------------
def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*" for c in password):
        score += 1

    if score <= 1:
        return "Weak"
    elif score == 2:
        return "Medium"
    else:
        return "Strong"

# -----------------------------
# Route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        password = request.form["password"]

        attempts, time_taken = crack_password(password)
        strength = check_strength(password)

        result = {
            "password": password,
            "attempts": attempts,
            "time": time_taken,
            "strength": strength
        }

    return render_template("index.html", result=result)

# -----------------------------
# Run App (Render Compatible)
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
