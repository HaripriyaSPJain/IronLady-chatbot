import os
import requests
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Hugging Face API setup
API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
HF_API_KEY = os.getenv("HF_TOKEN")  # Reads from .env
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

def ask_huggingface(question):
    context = """
    Iron Lady offers multiple leadership programs including workshops, career 
    accelerators, and mentoring. The duration varies: short workshops last a few 
    weeks, while full programs run 3-6 months. Programs are online, with some 
    offline events. Certificates are awarded upon completion. Mentors are industry 
    leaders, certified coaches, and experienced professionals.
    """

    payload = {"inputs": {"question": question, "context": context}}
    response = requests.post(API_URL, headers=headers, json=payload)

    # Debug log for development
    print("🔍 Hugging Face raw response:", response.text)

    try:
        data = response.json()
        # ✅ Only trust answer if confidence score > 0.3
        if isinstance(data, dict) and "answer" in data and data.get("score", 0) > 0.3:
            return data["answer"]
        else:
            return "I'm not sure, but I can help with Iron Lady programs!"
    except Exception as e:
        print("⚠️ Hugging Face error:", e)
        return "Error: Could not connect to Hugging Face API."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_msg = request.json.get("message", "")

    msg = user_msg.lower()
    if "what programs" in msg or "which programs" in msg:
        reply = "Iron Lady offers leadership, confidence building, communication, and executive presence programs."
    elif "duration" in msg or "how long" in msg:
        reply = "Programs typically run for 8–12 weeks."
    elif "online" in msg or "offline" in msg or "mode" in msg:
        reply = "All Iron Lady programs are conducted online."
    elif "certificate" in msg:
        reply = "Yes, a certificate is awarded after completing the program."
    elif "mentor" in msg or "coach" in msg:
        reply = "Our mentors are experienced industry leaders, coaches, and professionals."
    else:
        # ✅ Call Hugging Face for other questions
        reply = ask_huggingface(user_msg)

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
