FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt -y install \
    alsa-utils \
    bluez \
    curl \
    build-essential \
    ffmpeg \
    git \
    libasound2-dev \
    libportaudio2 \
    libcairo2-dev \  
    libffi-dev \
    libpango1.0-dev \            
    libgdk-pixbuf2.0-dev \       
    pkg-config \ 
    software-properties-common \
    pulseaudio \
    pulseaudio-utils \
    python3-pip \
    python3-dev \
    wget

# Install Python 3.11
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update && apt-get install -y python3.11 python3.11-venv python3.11-dev
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.11 get-pip.py && rm get-pip.py

RUN pip install --upgrade pip setuptools wheel #needed to avoid PEP517 error
RUN pip install pycairo

RUN pip install git+https://github.com/huggingface/parler-tts.git

WORKDIR /tts
COPY ./ /tts

RUN pip install -r ./requirements.txt

# get model files from https://github.com/rhasspy/piper/blob/master/VOICES.md
RUN mkdir -p /tts/models && \
    cd /tts/models && \
    wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/medium/en_US-ryan-medium.onnx && \
    wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/en/en_US/ryan/medium/en_US-ryan-medium.onnx.json && \
    wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx && \
    wget https://huggingface.co/rhasspy/piper-voices/resolve/v1.0.0/de/de_DE/thorsten/medium/de_DE-thorsten-medium.onnx.json

# Run the application
ENTRYPOINT ["python3", "/tts/tts.py"]