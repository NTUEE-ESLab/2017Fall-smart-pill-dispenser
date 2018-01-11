var url = 'http://140.112.18.204:3000'
var socket = require('socket.io-client')(url);
var gpio = require('rpi-gpio');
var fetch = require('node-fetch');
 
var register_pin = 7;
var recognize_pin = 11;
var port = 8080;

gpio.setup(register_pin, gpio.DIR_IN, gpio.EDGE_BOTH);
gpio.setup(recognize_pin, gpio.DIR_IN, gpio.EDGE_BOTH);

const deviceId = "pi1";

const onConnect = () => {
    console.log("connected");
}

const onDisconnect = () => {
    console.log("disconnected");
}

function debounce(func, wait, immediate) {
    var timeout;
    return function() {
        var context = this, args = arguments;
        var later = function() {
	    timeout = null;
            if (!immediate) func.apply(context, args);
        };
	var callNow = immediate && !timeout;
	clearTimeout(timeout);
	timeout = setTimeout(later, wait);
        if (callNow) func.apply(context, args);
    };
};

const onRegisterPress = (info) => {
    console.log("entering onRegisterPress");
    const _onRegisterPress = (channel, value) => {
        if (channel == register_pin && !value) {
            console.log("onRegisterPress");
            fetch(`http://localhost:${port}/register`, {
                method: 'POST',
                body:    JSON.stringify(info),
                headers: { 'Content-Type': 'application/json' },
            })
            .then(res => res.json())
            .then(body => console.log(body))
            .catch(err => console.log(err));
        }
    };
    return _onRegisterPress;
};

const onRecognizePress = (channel, value) => {
    if (channel == recognize_pin && !value) {
        console.log("onRecognizePress");
        fetch(`http://localhost:${port}`)
        .then(res => res.json())
        .then(body => console.log(body))
        .catch(err => console.log(err));
    };
};

const onPress = (channel, value) => {
    if (channel === register_pin) {
        
    }
}

const onRegister = (info) => {
    console.log("entering onRegister");
    console.log(`device id: ${deviceId}, info.deviceId: ${info.deviceId}`);
    if (deviceId === info.deviceId) {
        debounceOnRegisterPress = debounce(onRegisterPress(info), 500, true);
        gpio.on('change', debounceOnRegisterPress);
	//gpio.read(register_pin, debounceOnRegisterPress);
    }
}

debounceOnRecognizePress = debounce(onRecognizePress, 500, true);
gpio.on('change', debounceOnRecognizePress);

socket.on('connect', onConnect);
socket.on('register', onRegister);
socket.on('disconnect', onDisconnect);

