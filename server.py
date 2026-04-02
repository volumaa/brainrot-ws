import asyncio
import websockets
import json
import urllib.request
import os

connected = set()
WEBHOOK = "https://discord.com/api/webhooks/1487174114929148125/5QgDcRzxztVqKkJOWDE5YGjWp9ldp5_QrqM-x9gHtmAgjZ3K7rIC3ITgnBFAU0Mkx7kw"

def send_discord(best, others, join_link):
    other_lines = "\n".join([f"• {p}" for p in others]) or "None"
    embed = {
        "username": "Brainrot Scanner",
        "embeds": [{
            "title": "🧠 Target Brainrot Found!",
            "description": f"🏷️ **Best in Server**\n**{best}**\n\n🐾 **Others**\n```\n{other_lines}\n```\n🔗 **Join:** {join_link}",
            "color": 16744448,
            "footer": {"text": "Steal a Brainrot Scanner"}
        }]
    }
    data = json.dumps(embed).encode()
    req = urllib.request.Request(WEBHOOK, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        urllib.request.urlopen(req)
    except Exception as e:
        print("Webhook error:", e)

async def handler(ws):
    connected.add(ws)
    print(f"Connected: {len(connected)} clients")
    try:
        async for msg in ws:
            try:
                data = json.loads(msg)
                best      = data.get("best", "Unknown")
                others    = data.get("others", [])
                join_link = data.get("join_link", "")
                print(f"Found: {best} | Server: {join_link}")
                send_discord(best, others, join_link)
            except Exception as e:
                print("Error:", e)
    finally:
        connected.discard(ws)

async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"Running on port {port}")
        await asyncio.Future()

asyncio.run(main())
