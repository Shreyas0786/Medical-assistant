from flask import Flask, request, jsonify
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_health_update(sender, message):
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a compassionate medical assistant helping diabetic patients. 
When a patient shares their health update, analyze their blood sugar, blood pressure, and symptoms.
Give friendly, clear advice. If readings are dangerous, strongly urge them to contact their doctor.
Keep responses concise and easy to understand."""
            },
            {
                "role": "user",
                "content": f"Patient update from {sender}:\n\n{message}"
            }
        ]
    )
    return response.choices[0].message.content

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    sender = data.get("from", "Unknown")
    body = data.get("body_text") or data.get("body", "No content")
    
    print(f"\n📬 Health update from {sender}:")
    print(f"{body}\n")
    
    advice = analyze_health_update(sender, body)
    print(f"🤖 AI Response:\n{advice}\n")
    
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(port=5000)