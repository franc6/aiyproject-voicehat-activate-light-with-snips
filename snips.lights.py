import sys
import os
import time
import json

# If you don't bother to install the python module, uncomment the next line
#sys.path.append('/home/pi/aiyprojects-raspbian/src/')
import aiy.voicehat
import RPi.GPIO
import paho.mqtt.client as mqtt

# Specify the host and port of mqtt for your snips server, if this is a
# satellite
HOST = 'localhost'
PORT = 1883

# Place your satellite's siteId here.  See bind setting in the
# [snips-audio-server] section of snips.toml.  Don't include the @mqtt part!
THIS_SITE="default"

mqtt.Client.light_is_on = False

RPi.GPIO.setwarnings(False)
led = aiy.voicehat.get_led()

def light_on(client):
    if client.light_is_on is False:
        led.set_state(aiy.voicehat.LED.ON)
        client.light_is_on = True

def light_off(client):
    if client.light_is_on is True:
        led.set_state(aiy.voicehat.LED.OFF)
        client.light_is_on = False

def start_listening(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    if payload is not None and payload.get('siteId') is not None and payload.get('siteId') == THIS_SITE:
        light_on(client)

def stop_listening(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    if payload is not None and payload.get('siteId') is not None and payload.get('siteId') == THIS_SITE:
        light_off(client)

def on_connect(client, userdata, flags, rc):
    #print("Connected with result code" + str(rc))
    client.subscribe("hermes/asr/stopListening")
    client.subscribe("hermes/asr/startListening")

client = mqtt.Client()
client.on_connect = on_connect

client.message_callback_add("hermes/asr/stopListening", stop_listening)
client.message_callback_add("hermes/asr/startListening", start_listening)

client.light_is_on = False
client.connect(HOST, PORT, 60)
client.loop_forever()
