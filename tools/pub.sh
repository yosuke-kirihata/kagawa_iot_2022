#!/bin/sh

cafile=#Your CA file
certfile=#Your Cert file
keyfile=#Your Key file

host=#Your host

port=8883
device="co2_sensor"
topic="co2_sensor/data/100"
qos=1

if [ -p /dev/stdin ]; then
    if [  `echo $@` == "" ]; then 
        message=`cat -`
    else
        message=$@
    fi
else
    message=$@
fi
message=$message
mosquitto_pub \
    --cafile $cafile \
    --cert $certfile \
    --key $keyfile \
    -q $qos \
    -h $host \
    -p $port \
    -t $topic \
    -q $qos \
    -i $device \
    -d -m $message
