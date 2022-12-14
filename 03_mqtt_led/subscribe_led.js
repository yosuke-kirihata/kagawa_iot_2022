import mqtt from "mqtt";

import led from "./lib/led.js";

const MY_TOPIC = "/kagawa/kosen/rpi";

const client = mqtt.connect("mqtt://localhost");

client.on("connect", function () {
  console.log("subscriber.connected.");
});

client.subscribe(MY_TOPIC + "/led", function (_err, _granted) {
  console.log("subscriber.subscribed.");
});

client.on("message", function (topic, message) {
  console.log("subscriber.on.message", "topic:", topic, "message:", message.toString());

  if (topic === MY_TOPIC + "/led") {
    if (message == "on") {
      console.log("led on");
      led.on();
    } else if (message === "off") {
      console.log("led off");
      led.off();
    } else {
    }
  }
});
