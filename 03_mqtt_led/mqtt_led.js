var led = require("./lib/led");
var mqtt = require("mqtt");

var myTopic = "/kagawa/kosen/rpi";

var client = mqtt.connect("mqtt://localhost");

client.on("connect", function () {
  console.log("subscriber.connected.");
});

client.subscribe(myTopic + "/led", function (_err, _granted) {
  console.log("subscriber.subscribed.");
});

client.on("message", function (topic, message) {
  console.log("subscriber.on.message", "topic:", topic, "message:", message.toString());

  if (topic == myTopic + "/led") {
    if (message == "on") {
      console.log("led on");
      led.on();
    } else if (message == "off") {
      console.log("led off");
      led.off();
    } else {
    }
  }
});
