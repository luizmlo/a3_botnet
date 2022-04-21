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
                    client_checksum = message['checksum']
                    if len(client_name) >= 4 and len(client_checksum) == 16:
                        await finish_handshake(websocket, client_name, message['checksum'])

                    else:
                        print('EASTER EGG') # todo  

                else:
                    raise Exception(f'[C] unknown message type: {message}')

        except Exception as e:
            if 'no close frame received or sent' in str(e) or 'received 1000 (OK); then sent 1000 (OK)' in str(e):
                print(f'[C] {client_name} connection closed')
                break
            else:
                print(f'[S] server error on parse_message: {str(e)}')
                break

# heatbeat function that sends a message from the server to the client every second
async def heartbeat(websocket, client_name):
    print(f'[S] starting heartbeat to {client_name}')
    while True:
        try:
            await asyncio.sleep(1)
            if websocket in alive_bots:
                heartbeat_seed = random.randint(10000, 99999)
                heartbeat_message = {"type":"heartbeat_ping", "seed": heartbeat_seed}
                heartbeat_message = json.dumps(heartbeat_message)
                await websocket.send(heartbeat_message)
                print(f'[S] heartbeat to {client_name} - {heartbeat_seed}')

                response = await websocket.recv()
                response = json.loads(response)
                if response['type'] == 'heartbeat_pong':
                    if response['pow'] == str(heartbeat_seed)[::-1]:
                        print(f'[C] {client_name} alive')

                    else:
                        print(f'[S] {client_name} dead')
                        alive_bots.remove(websocket)
                        break


        except Exception as e:
            if 'received 1000' in str(e):
                print(f'[C] {client_name} disconnected')
                alive_bots.remove(websocket)
            else:
                print(f'[S] server error on heartbeat: {str(e)}')
            break

async def finish_handshake(websocket, client_name, client_checksum) -> bool:
    print(f'[C] received handshake_pong - {client_name}')
    server_checksum = hashlib.sha256(client_name.encode()).hexdigest()[:16]

    if client_checksum == server_checksum:
        handshake_success = {"type":"handshake_success", "checksum": server_checksum}
        print(f'[S] sending handshake_success - {server_checksum}')

    else:
        handshake_success = {"type":"handshake_fail", "server_checksum": server_checksum, "client_checksum": client_checksum}
        print(f'[S] sending handshake_fail - {server_checksum}/{client_checksum}')


    handshake_success = json.dumps(handshake_success)
    await websocket.send(handshake_success)
    print(f'[S] {client_name} alive - starting heartbeat')
    alive_bots.append(websocket)
    await heartbeat(websocket, client_name)


async def start_handshake(websocket):
    server_key = "".join([random.choice('abcdef0123456789') for _ in range(4)])     

    handshake_ping = {"type":"handshake_ping", "server_key": server_key}
    handshake_ping = json.dumps(handshake_ping)

    print(f'[S] sending handshake_ping - {server_key}')
    await websocket.send(handshake_ping)
    print(f'[S] waiting for handshake_pong with client_name')

    await parse_message(websocket)


async def handler(websocket):
    print(f'[C] new websocket connection')
    await start_handshake(websocket)

async def main():
    async with websockets.serve(handler, server_ip, server_port):
        await asyncio.Future()  # run forever

asyncio.run(main())