var host = 'http://140.112.18.204:3000'
var socket = require('socket.io-client')(host);
var gpio = require('rpi-gpio');
var fetch = require('node-fetch');

//to take a snapshot, start a timelapse or video recording
var register_pin = 7;
var recognize_pin = 37;
var port = 8000;
var debounceTime = 100;

gpio.setup(register_pin, gpio.DIR_IN, gpio.EDGE_BOTH);
gpio.setup(recognize_pin, gpio.DIR_IN, gpio.EDGE_BOTH);

var listeners = {}

const deviceId = "pi1";

const onConnect = () => {
    console.log("connected");
}
const onUnRegister = (username) => {
    console.log(username);
    console.log(listeners);
    if (listeners[username]) {
        gpio.removeListener('change', listeners[username]);
        delete listeners[username];
    }
    console.log(gpio.listeners('change'));
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
    const _onPress = (channel, value) => {
        if (channel == register_pin && !value && 
            Object.getOwnPropertyNames(info).length != 0) {
            console.log("register");
            console.log(info);
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
    return _onPress;
};

const onRecognizePress = (channel, value) => {
    if (channel == recognize_pin && !value) {
        console.log("recognize");
        fetch(`http://localhost:${port}/recognize`)
        .then(res => {
          console.log(`res: ${res}`);
          a = res.json();
          console.log(`a: ${a}`);
          return a;
        })
        .then(body => {
          console.log(`body: ${body}`);
          const person = body['person'];
          var emitted = '';
          if (person !== '') {
            emitted = 'success';
            var drugA = 0;
            var drugB = 0;
            fetch(`${host}/api/user/${person}`)
            .then(res => res.json())
            .then(user => {
              console.log("user");
              console.log(user);
              const prescription = user['prescription'];
              console.log("prescription");
              console.log(prescription);
              for (var idx in prescription) {
                const instruction = prescription[idx];
                if (instruction['drug'] === 'drugA') drugA = instruction['amount'];
                if (instruction['drug'] === 'drugB') drugB = instruction['amount'];
              }
              console.log(`drugA: ${drugA}`);
              console.log(`drugB: ${drugB}`);
              const drugs = {
                "drugA": drugA,
                "drugB": drugB,
              };
              fetch(`http://localhost:${port}/delivery`, {
                method: 'POST',
                body:    JSON.stringify(drugs),
                headers: { 'Content-Type': 'application/json' },
              })
              .then(res => res.json())
              .then(delivery => {
                socket.emit('delivery', delivery['status']);
              })
              .catch(err => console.log(err));
            })
            .catch(err => console.log(err));
          } else {
            emitted = 'fail';
          }
          socket.emit('recognization', emitted);
        })
        .catch(err => console.log(err));
    }
};

debounceOnPress = debounce(onRecognizePress, debounceTime, true);
gpio.on('change', debounceOnPress);

const onRegister = (info) => {
    console.log("entering onRegister");
    console.log(`device id: ${deviceId}, info.deviceId: ${info.deviceId}`);
    if (deviceId === info.deviceId) {
        debounceOnRegisterPress = debounce(onRegisterPress(info), debounceTime, true);
        listeners[info.username] = debounceOnRegisterPress;
        gpio.on('change', debounceOnRegisterPress);
    }
}


socket.on('connect', onConnect);
socket.on('register', onRegister);
socket.on('unregister', onUnRegister);
socket.on('disconnect', onDisconnect);
