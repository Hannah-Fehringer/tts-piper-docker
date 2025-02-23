# TTS piper in a docker container
This is a docker container for piper tts on a raspberry pi. It can be used very easily. Have fun :)

## Requirements
- Raspberry Pi 5 with 8 GB RAM
- Charger for Raspberry Pi
- 64 GB SD Card
- Bluetooth Speaker
- Mouse 
- Keyboard

## Setup on Raspberry Pi
Install the newest image for Raspberry Pi 5.

## Install and Run
Get repository and build the docker image:
```
git clone https://github.com/Hannah-Fehringer/tts-piper-docker.git
cd tts
./deployment/build.sh
```

Start the application:
```
docker-compose up
```

Send a message, which shall be spoken:
```
curl -u guest:guest -H "Content-Type: application/json" \
    -X POST \
    -d'{"properties":{},"routing_key":"output_tts",
        "payload":"I think ducks are the most precious animals on the planet. I like them.",
        "payload_encoding":"string"}' http://localhost:15672/api/exchanges/%2f/amq.default/publish
```

If you want to change the voices, check the following section.

### Change voices
Get the link for the voice you want to use:
https://github.com/rhasspy/piper/blob/master/VOICES.md

Download your voice like:
```
cd tts
mkdir models
cd models
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json
```

and the line in tts.py need to be changed to selected voice file:
```
onnx_model_path = "/tts/models/de_DE-thorsten-medium.onnx"
```

## for Bluetooth Output
add the following lines to /etc/pulse/default.pa
load-module module-native-protocol-unix auth-anonymous=1
load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1
