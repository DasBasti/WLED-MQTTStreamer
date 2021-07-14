#!/usr/bin/python3
# -*- coding:utf-8 -*-
import paho.mqtt.client as mqtt
import json
import logging
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

lut=[]
for i in range(8):
    for j in range(8):
        lut.append((14-j-i,7+j-i))

def load_from_file(filename):
    strip=bytearray()
    try:
        Himage = Image.open(filename)
        raw = Himage.convert("RGB")
        data = raw.load()
        for p in range(64):
            r,g,b = data[lut[p][0], lut[p][1]]
            strip.append(r)
            strip.append(g)
            strip.append(b)
            strip.append(0)
        
    except IOError as e:
        logging.info(e)
    return strip

def on_connect(client, userdata, flags, rc):
    print("connected")

# Demo string: "!pcb rgwbrgb"
def on_message(client, userdata, msg):
    j=json.loads(msg.payload.decode("utf-8"))
    if j.get("message")[0:4] == "!pcb":
        image = bytearray(64*4)
        b=0
        try:
            for p in j.get("message")[4:]:
                if p == ' ':
                    continue
                elif p == 'w':
                    image[b]=255
                    image[b+1]=255
                    image[b+2]=255
                    image[b+3]=0
                elif p == 'k':
                    image[b]=0
                    image[b+1]=0
                    image[b+2]=0
                    image[b+3]=0
                elif p == 'b':
                    image[b]=0
                    image[b+1]=0
                    image[b+2]=127
                    image[b+3]=0
                elif p == 'r':
                    image[b]=127
                    image[b+1]=0
                    image[b+2]=0
                    image[b+3]=0
                elif p == 'g':
                    image[b]=0
                    image[b+1]=127
                    image[b+2]=0
                    image[b+3]=0
                elif p == 'y':
                    image[b]=127
                    image[b+1]=127
                    image[b+2]=0
                    image[b+3]=0
                elif p == 'c':
                    image[b]=0
                    image[b+1]=127
                    image[b+2]=127
                    image[b+3]=0
                elif p == 'm':
                    image[b]=127
                    image[b+1]=0
                    image[b+2]=127
                    image[b+3]=0
                b+=4
                if b > 4*64:
                    break
        except:
            mqtt_client.publish("chat/out", "Fehler im !pcb String!")
        mqtt_client.publish("pcb/all/stream", payload=image)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("cloud.eieiei.lol", 1883, 60)
mqtt_client.subscribe("pcb/chat")

mqtt_client.loop_forever()