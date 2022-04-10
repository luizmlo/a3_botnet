import asyncio
import websockets

server_ip = 'localhost'
server_port = 8765

async def echo(websocket):
    async for message in websocket:
        print(f'[C] {message}')
        await websocket.send(message)

async def main():
    async with websockets.serve(echo, server_ip, server_port):
        await asyncio.Future()  # run forever

asyncio.run(main())