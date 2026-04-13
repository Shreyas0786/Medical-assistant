from dotenv import load_dotenv
import os
from inkbox import Inkbox

load_dotenv()

api_key = os.getenv("INKBOX_API_KEY")

with Inkbox(api_key=api_key) as inkbox:
    identity = inkbox.get_identity("Medical-assistant")
    
    identity.send_email(
        to=["sonwaneshreyas@gmail.com"],
        subject="Daily Health Check-in 🩺",
        body_text="""Good morning! This is your daily health check-in.

Please reply with the following information:

1. Blood sugar level (mg/dL)
2. Blood pressure (e.g. 120/80)
3. How are you feeling today? Any symptoms?

Your health assistant is here to help. Reply to this email with your update.""",
    )
    
    print("Health check-in email sent!")

    call = identity.place_call(
        to_number="+16785757153",
        client_websocket_url="wss://plod-wise-stuck.ngrok-free.dev/"
    )
    print("📞 Call placed!", call)