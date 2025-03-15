import websockets
import asyncio

async def handle_connection(websocket, path):
    async for message in websocket:
        await websocket.send(f"Received: {message}")

start_server = websockets.serve(handle_connection, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
