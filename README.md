# 🩺 Medical Assistant Bot

An AI-powered medical assistant that proactively calls diabetic patients every day to check in on their health. The bot asks about blood sugar levels, blood pressure, and symptoms — then uses Groq AI to provide personalized advice in real time over a live phone call.

## How It Works

1. `bot.py` sends a daily health check-in email and places a phone call to the patient
2. The patient answers and speaks with the AI assistant
3. Inkbox handles speech-to-text and text-to-speech
4. Groq AI analyzes responses and replies with personalized health advice
5. If readings are dangerous, the bot urges the patient to contact their doctor

## Tech Stack

- **[Inkbox](https://inkbox.ai)** — AI agent identity, email, and phone calls
- **[Groq](https://groq.com)** — Fast LLM inference (llama-3.3-70b-versatile)
- **Python** — Flask webhook server + WebSocket call server
- **ngrok** — Tunnels local server for Inkbox webhook and WebSocket

## Setup

### 1. Install dependencies

    pip install inkbox groq flask websockets python-dotenv

### 2. Create `.env` file

    INKBOX_API_KEY=your_inkbox_api_key
    GROQ_API_KEY=your_groq_api_key

### 3. Run the call server

    python3 call_server.py

### 4. Expose it with ngrok

    ngrok http 8765

### 5. Update the WebSocket URL in `bot.py`

Replace `client_websocket_url` with your ngrok URL.

### 6. Send the check-in and place the call

    python3 bot.py

## Files

| File | Description |
|------|-------------|
| `bot.py` | Sends daily health check-in email and places phone call |
| `call_server.py` | WebSocket server that handles live call with Groq AI |
| `server.py` | Flask webhook server for receiving email replies |

## Built At

HackPrinceton 2026