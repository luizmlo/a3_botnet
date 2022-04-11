import websockets
import hashlib
import asyncio
import random
import json

server_ip = 'localhost'
server_port = 8765

# sends a ping to the websocket server every second with a random string
async def parse_message(websocket, message):
    debug_mode = True # prints all messages
    
    try:
        message = json.loads(message) # convert to json
        if message:
            if message['type'] == 'handshake_ping':
                if debug_mode:
                    print(f"[S] received handshake_ping: server_key: {message['server_key']}")
                await handshake_pong(websocket, message['server_key'])
                return {'type': 'handshake_ping', 'server_key': message['server_key']}

            elif message['type'] == 'handshake_success' and len(message['checksum']) > 0:
                if debug_mode:
                    print(f"[S] received handshake_success - checksum: {message['checksum']}")
                return {"type":"handshake_success", "checksum": message['checksum']}

    except Exception as e: 
        print(f'[C] client error on parse_message: {str(e)}')
        return {"type":"error", "error": str(e)}


async def main():
    async with websockets.connect(f"ws://{server_ip}:{server_port}") as websocket:
        print(f'[C] created connection to server {server_ip}:{server_port}')

        while True:
            # generate random key for encryption
            try:
                message = await websocket.recv()
                if message:
                    #print(f'[S] Received raw message: {message}')
                    await parse_message(websocket, message)    

            except Exception as e:
                print(f'[C] client error on main: {str(e)}')

async def handshake_finish(client_checksum, server_checksum):
    try:
        if client_checksum == server_checksum:
            #print(f"[C] handshake_finish valid - checksum: {client_checksum}")
            print(f'[C] checksum valid  - ready to start heartbeat')

    except Exception as e:
        print(f'[C] client error on handshake_finish: {str(e)}')

async def handshake_pong(websocket, server_key):
    try:
        client_key = "".join([random.choice('abcdef0123456789') for _ in range(4)])
        client_name = None
        while not client_name:
            client_name = input('> Enter client name: ').strip()        
            if len(client_name) >= 4 and len(client_name) < 16:
                print(f'[C] Client name: {client_name} - starting connection')
            else:
                print('[C] Invalid client name, input between 4 and 16 characters')
                client_name = None

        client_full_name = client_name + "_" + client_key + server_key
        client_checksum = hashlib.sha256(client_full_name.encode()).hexdigest()[:16]
        print(f"[C] client_full_name: {client_full_name} - checksum: {client_checksum}")
        message = {"type": "handshake_pong", "client_name": f"{client_full_name}"}
        message = json.dumps(message)
        await websocket.send(message)

        print(f"[C] handshake_pong sent: {client_full_name}")

        handshake_success = await websocket.recv()
        success = await parse_message(websocket, handshake_success)
        await handshake_finish(client_checksum, success['checksum'])

    except Exception as e:
        print(f'[C] client error on handshake_pong: {str(e)}')

asyncio.run(main())