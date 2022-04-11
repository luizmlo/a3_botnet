import asyncio
import hashlib
import websockets
import random
import json

server_ip = 'localhost'
server_port = 8765

alive_bots = [] # list of bots that are still alive, responding to heartbeat

async def parse_message(websocket):
    while True:
        try:
            message = await websocket.recv()
            message = json.loads(message) # convert to json
            if message:
                if message['type'] == 'handshake_pong':
                    client_name = message['client_name']
                    if len(client_name) >= 4 and len(client_name) <= 16:
                        await finish_handshake(websocket, client_name)

                    else:
                        print('EASTER EGG') # todo

                else:
                    raise Exception(f'[C] unknown message type: {message}')

        except Exception as e:
            print(f'[S] server error on parse_message: {str(e)}')

        response = json.dumps(message)  
        await websocket.send(response)

async def finish_handshake(websocket, client_name):
    print(f'[C] received handshake_pong - {client_name}')

    server_checksum = hashlib.sha256(client_name.encode()).hexdigest()[:16]
    handshake_success = {"type":"handshake_success", "checksum": server_checksum}
    handshake_success = json.dumps(handshake_success)
    await websocket.send(handshake_success)
    print(f'[S] sending handshake_success - {server_checksum}')


async def start_handshake(websocket):
    server_key = "".join([random.choice('abcdef0123456789') for _ in range(4)])     
    print(f'[S] sending handshake_ping - {server_key}')

    handshake_ping = {"type":"handshake_ping", "server_key": server_key}
    handshake_ping = json.dumps(handshake_ping)

    await websocket.send(handshake_ping)
    await parse_message(websocket)


async def handler(websocket):
    print(f'[C] new websocket connection')
    await start_handshake(websocket)

async def main():
    async with websockets.serve(handler, server_ip, server_port):
        await asyncio.Future()  # run forever

asyncio.run(main())