from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"

# OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ API Key is missing! Check your .env file.")
else:
    print("✅ API Key Loaded Successfully!")

client = OpenAI()

chat_history = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session["username"] = username
            return redirect(url_for("chat"))
    return render_template("login.html")

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("home"))
    return render_template("frontend.html", username=session['username'])

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.json.get("message")
    chat_history.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                *chat_history
            ]
        )
        reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": reply})
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Error: {e}"})


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
