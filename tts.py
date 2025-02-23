import json
import numpy as np
import sounddevice as sd
from rich.console import Console
from piper.voice import PiperVoice, PiperConfig
import wave
import onnxruntime
import pika

onnx_model_path = "/tts/models/en_US-ryan-medium.onnx"

print(f"Using model: {onnx_model_path}")

console = Console()

def load_onnx(model, sess_options, providers = ["CPUExecutionProvider"]):
    with open(f"{model}.json", 'r') as file:
        config_data = json.load(file)
    
    # Extract required values from the nested dictionaries
    num_speakers = config_data['num_speakers']
    sample_rate = config_data['audio']['sample_rate']
    espeak_voice = config_data['espeak']['voice']
    length_scale = config_data['inference']['length_scale']
    noise_scale = config_data['inference']['noise_scale']
    noise_w = config_data['inference']['noise_w']
    phoneme_id_map = config_data['phoneme_id_map']
    phoneme_type = config_data.get('phoneme_type', 'espeak')  # Use 'default' or another appropriate default value
    num_symbols = config_data['num_symbols']

    # Check for missing phonemes and log a warning
    required_phonemes = ['̧', '.', ',', '!', "'", '(', ')', '-', ':', ';']  # Add all required phonemes here
    for phoneme in required_phonemes:
        if phoneme not in phoneme_id_map:
            console.print(f"Warning: Missing phoneme from id map: {phoneme}")


    # Initialize PiperConfig with the extracted values
    config = PiperConfig(
        num_speakers=num_speakers,
        sample_rate=sample_rate,
        espeak_voice=espeak_voice,
        length_scale=length_scale,
        noise_scale=noise_scale,
        noise_w=noise_w,
        phoneme_id_map=phoneme_id_map,
        phoneme_type=phoneme_type,
        num_symbols=num_symbols
    )

    model = onnxruntime.InferenceSession(str(model), sess_options, providers)

    return model, config

def on_message_callback(ch, method, properties, body):
    global model, sess_options, voice, config
    # Convert body from bytes to str
    message = body.decode()
    console.print("\nReceived: ", message)
    
    # Call the LLM response function
    try:
        stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype=np.int16)
        stream.start()

        for audio_bytes in voice.synthesize_stream_raw(message): # processes one sentence in a step
            int_data = np.frombuffer(audio_bytes, dtype=np.int16)
            sd.play(int_data, samplerate=voice.config.sample_rate)
            sd.wait()
            #stream.write(int_data)

        stream.stop()
        stream.close()
    except Exception as e:
        console.print("No text to speak", e)

def load_voice():
    global onnx_model_path, config
    sess_options = onnxruntime.SessionOptions()
    model, config = load_onnx(onnx_model_path, sess_options)
    voice = PiperVoice(model, config)

    return voice

if __name__ == "__main__":
    # Establish a connection to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    global voice
    voice = load_voice()

    # Declare a queue
    channel.queue_declare(queue='output_tts')
    
    # Set up the consumer
    channel.basic_consume(queue='output_tts',
                      on_message_callback=on_message_callback,
                      auto_ack=True)

    console.print(' [*] Waiting for messages. To exit press CTRL+C')
    # Start consuming messages
    channel.start_consuming()
