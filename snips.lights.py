import sys
import os
import time

# If you don't bother to install the python module, uncomment the next line
#sys.path.append('/home/pi/aiyprojects-raspbian/src/')
import aiy.voicehat
import RPi.GPIO

import paho.mqtt.client as mqtt

mqtt.Client.light_is_on = False

RPi.GPIO.setwarnings(False)
led = aiy.voicehat.get_led()

host = 'localhost'
port = 1883

def light_on(client, userdata, msg):
    if client.light_is_on is False:
        led.set_state(aiy.voicehat.LED.ON)
        client.light_is_on = True

def light_off(client, userdata, msg):
    if client.light_is_on is True:
        led.set_state(aiy.voicehat.LED.OFF)
        client.light_is_on = False

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code" + str(rc))
    client.subscribe("hermes/asr/stopListening")
    client.subscribe("hermes/asr/startListening")

client = mqtt.Client()
client.on_connect = on_connect

client.message_callback_add("hermes/asr/stopListening", light_off)
client.message_callback_add("hermes/asr/startListening", light_on)

client.light_is_on = False
client.connect(host, port, 60)
client.loop_forever()
