// lê mensagens do servidor e executa funções de acordo com o tipo de mensagem
function parse_message(ws, message) {
    if (message['type'] == 'handshake_ping'){
        console.log('received ping: ' + message['server_key']);
        handshake_pong(ws, message['server_key']);
        return
    }
    if (message['type'] == 'heartbeat_ping'){
        console.log('received heartbeat_ping: ' + message['seed']);
        heartbeat_pong(ws, message['seed']);
    }
}

function hash(string) {
    const utf8 = new TextEncoder().encode(string);
    return crypto.subtle.digest('SHA-256', utf8).then((hashBuffer) => {
        const hashArray = Array.from(new Uint8Array(hashBuffer));
        const hashHex = hashArray
        .map((bytes) => bytes.toString(16).padStart(2, '0'))
        .join('');
        return hashHex;});
}


function connect_websocket(){
    // inicializa websocket e define o evento de recebimento de mensagens
    var ws = new WebSocket("ws://localhost:8765");

    ws.onmessage = function (event) {
        message = JSON.parse(event.data);
        console.log("message received: ", message);
        parse_message(ws, message);
    }
}


// function that sends a handshake_pong message to the server
async function handshake_pong(ws, server_key) {
    // generate random string of length 6
    var client_name = Math.random().toString(36).substring(2, 7);
    var client_key = Math.random().toString(36).substring(2, 5);

    var client_full_name = client_name + '_' + client_key + server_key;
    
    // first 16 chars of sha256 hash of the client_full_name
    hash(client_full_name).then(function(hash){
        var checksum = hash.substring(0, 16);
        var message = {
            'type': 'handshake_pong',
            'client_name': client_full_name,
            'checksum': checksum
        };
        ws.send(JSON.stringify(message));
    });

}

// reverse string js


function heartbeat_pong(ws, seed) {
    var message = {
        'type': 'heartbeat_pong',
        'pow': seed.toString().split('').reverse().join('')
    };
    ws.send(JSON.stringify(message));
}

// generate random string of 4 hexadecimal characters
// print string in console
function generateClientKey() {
    let chars = '0123456789abcdef';
    let result = '';
    for (let i = 0; i < 4; i++) {
        result += chars[Math.floor(Math.random() * chars.length)];
    }
    return result;
}


connect_websocket();