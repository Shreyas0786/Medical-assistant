"""
Minimal WebSocket client to verify ngrok forwards WSS to localhost.
Run call_server.py first, then: python3 test_websocket.py
"""

import asyncio
import json
import sys

import websockets

WSS_URL = "wss://plod-wise-stuck.ngrok-free.dev"


async def main() -> None:
    try:
        async with websockets.connect(WSS_URL) as ws:
            await ws.send(json.dumps({"type": "start"}))
            msg = await ws.recv()
            print(msg)
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
