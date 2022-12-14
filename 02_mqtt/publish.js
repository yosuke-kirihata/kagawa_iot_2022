import mqtt from "mqtt";

const client = mqtt.connect("mqtt://localhost");

const topic = "/kagawa/kosen/rpi";
const message = "Hello MQTT!";

client.on("connect", function () {
  console.log("publisher.connected.");

  client.publish(topic, message);
  console.log("topic:", topic, ", message:", message);
});
