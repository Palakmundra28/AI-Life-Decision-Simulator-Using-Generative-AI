from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# 🔑 Paste your Gemini API key here
API_KEY = "AIzaSyB-T6sWl8Nxi88tivXvPklQide2_qQuaiA"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["message"]

        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"


        
        prompt = f"""
You are an AI Life Decision Advisor. Be concise and smart.

User question: {user_input}

Rules:
- If the question is simple (yes/no, short query) → give a SHORT answer in 2-4 lines. No bullet points.
- If the question is complex or detailed → give a structured answer with choices, consequences, and recommendation.
- Never give unnecessary long responses.
- Always end with a confident 1-line recommendation.
- Talk like a smart friend, not a robot.

"""

        data = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(url, json=data)
        result = response.json()

        print(result)  # Debug (optional)

        # ✅ Safe response handling
        if "candidates" in result:
            reply = result["candidates"][0]["content"]["parts"][0].get("text", "No response")

        
        elif "error" in result:
             reply = "⚠️ Server is busy right now. Please wait a few seconds and try again."
        else:
            reply = "Unexpected response from API"

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
    