echo "To address the elephant in the room: using text-to-speech technology isn’t just practical, it’s a lot of fun too!" \
    | /opt/piper/build/piper \
    --model /opt/piper/voices/aru/medium/en_GB-aru-medium.onnx \
    --output_file /opt/app/welcome.wav