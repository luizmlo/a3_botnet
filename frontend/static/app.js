particlesJS.load('particles-js', './static/particles-config.json');

// metrics
var debug_mode = true;
var total_messages = 0;
var log_counter = 0;

// get element console-messages
var console_messages = document.getElementById('console-messages');

function log_message(message, type='log-default') {
    log_counter += 1;
    var log = document.createElement('p')
    log.className = 'message ' + type;
    log.innerText = '[' + log_counter + '] ' + message;
    console_messages.appendChild(log);
    console_messages.scrollTop = console_messages.scrollHeight;
}

connect_websocket();