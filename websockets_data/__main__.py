import asyncio
import websockets
import json

async def listen_to_websocket():
    uri = "wss://aoe2recs.com/dashboard/api/"

    async with websockets.connect(uri) as websocket:
        while True:
            raw_data = await websocket.recv()
            if raw_data:
                print("Raw data" + raw_data)
                try:
                    json_data = json.loads(raw_data)
                    data = process_json_data(json_data)
                    if data:
                        print(data)
                except json.JSONDecodeError as e:
                    print("Error decoding JSON:", e)

def process_json_data(json_data):
    if isinstance(json_data, dict):
        process_data(json_data.get("data"))
    elif isinstance(json_data, list):
        for item in json_data:
            process_data(item)

def process_data(data):
    if (
            isinstance(data, dict) and data.get("ror") == True
    ):
        print("RoR Lobby:", data)

asyncio.get_event_loop().run_until_complete(listen_to_websocket())
