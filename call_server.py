import asyncio
import json
from websockets.server import serve
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

HANDSHAKE_RESPONSE_HEADERS = {
    "X-Use-Inkbox-Text-To-Speech": "true",
    "X-Use-Inkbox-Speech-To-Text": "true",
}

async def handle_call(websocket):
    print("📞 Call connected!")
    conversation = []

    async for message in websocket:
        data = json.loads(message)
        event_type = data.get("event")
        print("Received event:", event_type)

        if event_type == "start":
            greeting = "Hello! This is your daily health check-in from your medical assistant. How are you feeling today? Please tell me your blood sugar level and blood pressure."
            print(f"🤖 Bot says: {greeting}")
            await websocket.send(json.dumps({"event": "text", "delta": greeting}))
            await websocket.send(json.dumps({"event": "text", "done": True}))

        elif event_type == "transcript":
            is_final = data.get("is_final", False)
            if not is_final:
                continue

            patient_text = data.get("text", "")
            print(f"🗣️ Patient said: {patient_text}")
            conversation.append({"role": "user", "content": patient_text})

            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a friendly medical assistant on a phone call with a diabetic patient for their daily health check-in. You have already greeted the patient and asked for their blood sugar, blood pressure, and symptoms. Now listen to their responses and follow up naturally. Keep responses short and conversational. Do NOT ask for blood sugar and blood pressure again if they haven't answered yet — just respond to what they said. If readings are dangerous, strongly advise them to call their doctor."
                    }
                ] + conversation
            )

            reply = response.choices[0].message.content
            conversation.append({"role": "assistant", "content": reply})
            print(f"🤖 Bot says: {reply}")
            await websocket.send(json.dumps({"event": "text", "delta": reply}))
            await websocket.send(json.dumps({"event": "text", "done": True}))

        elif event_type == "stop":
            print("📵 Call ended.")
            break

async def main():
    print("🚀 Call server running on ws://localhost:8765")
    async with serve(
        handle_call,
        "0.0.0.0",
        8765,
        extra_headers=HANDSHAKE_RESPONSE_HEADERS,
    ):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())