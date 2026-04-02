import asyncio
import websockets
import os

connected = set()

async def handler(ws):
    connected.add(ws)
    print(f"Client connected. Total: {len(connected)}")
    try:
        async for msg in ws:
            # broadcast to all other clients
            others = [c for c in connected if c != ws]
            if others:
                await asyncio.gather(*[c.send(msg) for c in others])
    finally:
        connected.discard(ws)
        print(f"Client disconnected. Total: {len(connected)}")

async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"WebSocket server running on port {port}")
        await asyncio.Future()

asyncio.run(main())
