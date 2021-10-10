"""Quick python script to turn the LED of a Google aiyproject-voicehat
on or off when snips is listening."""
from functools import partial
from datetime import datetime
import json

# If you didn't install the python module, uncomment the next two lines
#import sys
#sys.path.append('/home/pi/aiyprojects-raspbian/src/')
import aiy.voicehat
import RPi.GPIO
import paho.mqtt.client as mqtt

# Specify the host and port of mqtt for your snips server, if this is a
# satellite
HOST = 'localhost'
PORT = 1883

# Specify the username and password for the connection
USERNAME = ''
PASSWORD = ''

# Place your satellite's siteId here.  See bind setting in the
# [snips-audio-server] section of snips.toml.  Don't include the @mqtt part!
THIS_SITE = "default"

mqtt.Client.light_is_on = False
mqtt.Client.is_connected = False
mqtt.Client.press_time = datetime.now()

RPi.GPIO.setwarnings(False)
LED = aiy.voicehat.get_led()
BUTTON = aiy.voicehat.get_button()

def button_pressed(client):
    """Fakes hotword detection for snips"""
    if client.is_connected:
        last_press = client.press_time
        client.press_time = datetime.now()
        if (client.press_time - last_press).seconds >= 5:
            hotword = {"site_id": THIS_SITE, "model_id": "/usr/lib/rhasspy/usr/local/lib/python3.7/site-packages/pvporcupine/resources/keyword_files/raspberry-pi/hey google_raspberry-pi.ppn", "model_version": "", "model_type": "personal", "currentSensitivity": 0.5, "session_id": None, "send_audio_captured": None, "lang": None, "custom_entities": None}
            payload = json.dumps(hotword)
            client.publish("hermes/hotword/hey google_raspberry-pi/detected", payload)

def light_on(client):
    """Turns the LED on if it's not already on"""
    if client.light_is_on is False:
        LED.set_state(aiy.voicehat.LED.ON)
        client.light_is_on = True

def light_off(client):
    """Turns the LED off if it's on"""
    if client.light_is_on is True:
        LED.set_state(aiy.voicehat.LED.OFF)
        client.light_is_on = False

def start_listening(client, userdata, msg):
    """hermes/asr/startListening handler

    This is called when the hermes/asr/startListening intent is received.
    It first checks that the intent is for THIS_SITE, and if so, it
    turns the LED on.
    """
    del userdata

    payload = json.loads(msg.payload.decode('utf-8'))
    if payload is not None and \
       payload.get('siteId') is not None and \
       payload.get('siteId') == THIS_SITE:
        light_on(client)

def stop_listening(client, userdata, msg):
    """hermes/asr/stopListening handler

    This is called when the hermes/asr/stopListening intent is received.
    It first checks that the intent is for THIS_SITE, and if so, it
    turns the LED off.
    """
    del userdata
    payload = json.loads(msg.payload.decode('utf-8'))
    if payload is not None and \
       payload.get('siteId') is not None and \
       payload.get('siteId') == THIS_SITE:
        light_off(client)

def on_connect(client, userdata, flags, rc):
    """MQTT Client connect callback.

    This is invoked when the MQTT client connects to the server.  It
    then subscribes to the interesting intents
    """
    del userdata, flags
    if rc == 0:
        client.is_connected = True
        client.subscribe("hermes/asr/stopListening")
        client.subscribe("hermes/asr/startListening")

def main():
    """Main entry point"""
    LED.set_state(aiy.voicehat.LED.OFF)
    client = mqtt.Client()
    client.on_connect = on_connect
    button_pressed_partial = partial(button_pressed, client)
    BUTTON.on_press(button_pressed_partial)

    client.message_callback_add("hermes/asr/stopListening", stop_listening)
    client.message_callback_add("hermes/asr/startListening", start_listening)
    if USERNAME is not None and PASSWORD is not None:
        client.username_pw_set(username=USERNAME, password=PASSWORD)

    client.light_is_on = False
    client.connect(HOST, PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
