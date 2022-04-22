particlesJS.load('particles-js', './static/particles-config.json');

// metrics
var debug_mode = true;
var log_counter = 0;
var sent_counter = 0;
var received_counter = 0;

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

// update footer labels
function update_footer_labels() {
    document.getElementById('sent-label').innerText = "sent:" + sent_counter;
    document.getElementById('received-label').innerText = "received:" + received_counter;
}

// run update_footer_labels every second
setInterval(update_footer_labels, 500);

connect_websocket();