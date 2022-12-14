import dayjs from "dayjs";
import mqtt from "mqtt";
import { SerialPort, ReadlineParser } from "serialport";

const topic = "/kagawa/kosen/rpi/sensor";

const client = mqtt.connect("mqtt://localhost");
client.on("connect", function () {
  console.log("subscriber.connected.");
});

const port = new SerialPort({
  path: "/dev/ttyUSB0",
  baudRate: 115200,
  dataBits: 8,
  stopBits: 1,
  parity: "none",
});

const parser = new ReadlineParser({ delimiter: "\r\n" });
port.pipe(parser);

parser.on("data", function (data) {
  const splited = data.split(",");

  if (splited.length !== 3) return;

  const message = JSON.stringify({
    time: dayjs().format("YYYY-MM-DD hh:mm:ss"),
    temp: splited[1],
    hum: splited[2],
    co2: splited[0],
  });

  console.log(message);
  client.publish(topic, message);
});

parser.on("error", function (err) {
  console.error("Error :", err);
});
