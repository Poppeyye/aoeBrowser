import asyncio
import websockets
import json

async def listen_to_websocket(uri):
    # Increase the receive buffer size limit to accommodate larger messages
    async with websockets.connect(uri, max_size=None) as websocket:  # Increase the max_size value as needed
        async for message in websocket:
            try:
                parsed_message = json.loads(message)
                print(len(message))
                data = parsed_message.get("data", None)

                if isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            check_game(item.get("data", {}))
                if isinstance(data, dict):
                    check_game(data)
            except json.JSONDecodeError:
                print("Received a non-JSON message:", message)

def check_game(data_dict):
    if isinstance(data_dict, dict):
        game = data_dict.get("game", "")
        if game == "RoR" or game == "AoE2":
            print(json.dumps(data_dict, indent=4))

# Run the WebSocket listener
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(listen_to_websocket("wss://aoe2recs.com/dashboard/api/"))
