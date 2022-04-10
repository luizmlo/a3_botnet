import asyncio
import websockets

server_ip = 'localhost'
server_port = 8765

async def hello():
    async with websockets.connect(f"ws://{server_ip}:{server_port}") as websocket:
        await websocket.send("Hello world!")
        response = await websocket.recv()
        print(f"[S] {response}")

asyncio.run(hello())