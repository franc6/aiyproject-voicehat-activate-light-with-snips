# aiyproject-voicehat-activate-light-with-snips
Turns on the google aiyproject voicehat LED when snips ASR is active

First, be sure you have Google aiyprojects-raspbian repository available.
See https://github.com/google/aiyprojects-raspbian.git Be sure to checkout
"voicekit", too.

Install pip for python3 and paho-mqtt

```
sudo apt-get install -y python3-pip
sudo pip3 install paho-mqtt
```

Next, modify snips.lights.py to specify the HOST and PORT for your snip's MQTT.
If this is running on a snips satellite, these should match the "mqtt" entry in
the "[snips-common]" section of your snips.toml file.

Modify snips.lights.py to specify THIS_SITE if you have changed the name of the
site (this is mandatory for a satellite!).  You'll find this in the "bind"
setting of the "[snips-audio-server]" section of your snips.toml file.  Just
don't include the @mqtt part.

Update snips.lights.service to point to your copy of snips.lights.py

Copy snips.lights.service to /lib/systemd/system/

Run the following commands to enable and start snips.lights.py:

```
sudo systemctl daemon-reload
sudo systemctl enable snips.lights.service
sudo systemctl start snips.lights.service
```

Now, when you activate snips, the LED on your voicekit will light.  It will go
out after snips has recorded your command.  The light is triggered from
hermes/intent/asr/startListening and hermes/intent/asr/stopListening.

[![Buy me some pizza](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/qpunYPZx5)
