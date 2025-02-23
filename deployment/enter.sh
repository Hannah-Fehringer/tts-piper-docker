docker run -it --rm \
    -v /etc/localtime:/etc/localtime \
    -v /home/hannah/Documents/llm-seppl/tts:/tts \
    -v /run/user/1000/pulse:/run/user/1000/pulse \
    --device=/dev/snd:/dev/snd \
    --device=/dev/bus/usb:/dev/bus/usb \
    -v /run/dbus:/run/dbus \
    -e PULSE_SERVER=unix:/run/user/1000/pulse/native \
    -e PULSE_COOKIE=/run/user/1000/pulse/cookie \
    --net=host \
    --name=speaker-piper \
    --privileged \
    --entrypoint /bin/bash \
    tts:latest
