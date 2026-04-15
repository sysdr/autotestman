#!/usr/bin/env python3.11
"""
Minimal Flask app — the Application Under Test (AUT).
Serves a login page and a protected dashboard.
"""
import os
from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
# Local-dev only; override in production with env (not an external API key).
app.secret_key = os.environ.get("LESSON64_FLASK_SECRET_KEY", "lesson-64-local-dev-only")

VALID_USERS = {"admin": "secret123"}

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
  <h1>Login</h1>
  {% if error %}<p id="error-msg" style="color:red">{{ error }}</p>{% endif %}
  <form method="POST" action="/login">
    <input id="username" name="username" placeholder="Username" />
    <input id="password" name="password" type="password" placeholder="Password" />
    <button id="login-btn" type="submit">Login</button>
  </form>
</body>
</html>
"""

DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head><title>Dashboard</title></head>
<body>
  <h1>Dashboard</h1>
  <p>Welcome, {{ username }}!</p>
  <a href="/logout">Logout</a>
</body>
</html>
"""

@app.route("/")
def root():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "GET":
        return render_template_string(LOGIN_HTML, error=None)
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not username or not password:
        return render_template_string(LOGIN_HTML, error="All fields are required."), 400
    if VALID_USERS.get(username) == password:
        session["user"] = username
        return redirect(url_for("dashboard"))
    return render_template_string(LOGIN_HTML, error="Invalid credentials."), 401

@app.route("/dashboard")
def dashboard():
    user = session.get("user")
    if not user:
        return redirect(url_for("login_page"))
    return render_template_string(DASHBOARD_HTML, username=user)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(port=5001, debug=False)
