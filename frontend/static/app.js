particlesJS.load('particles-js', './static/particles-config.json');

// get element console-messages
var console_messages = document.getElementById('console-messages');

for (var i=0; i<=10; i++) {
    var message = document.createElement('p')
    message.className = 'message default';
    message.innerText = 'message: ' + i;
    console_messages.appendChild(message);
}