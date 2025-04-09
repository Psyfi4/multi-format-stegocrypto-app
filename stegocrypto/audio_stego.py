import wave
import base64
import os
from cryptography.fernet import Fernet
from pydub import AudioSegment
from pydub.utils import which

# Ensure ffmpeg tools are found
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

def embed_message_in_audio(audio_file, message, output_path):
    try:
        audio = AudioSegment.from_file(audio_file)
        samples = audio.get_array_of_samples()

        # Convert message to binary and store message length
        message_bytes = message.encode()
        message_b64 = base64.b64encode(message_bytes).decode()
        message_bits = ''.join(format(ord(i), '08b') for i in message_b64)
        msg_length = len(message_bits)

        if msg_length > len(samples):
            raise ValueError("Message too long to encode in audio")

        # Embed bits into LSB of samples
        modified_samples = samples[:]
        for i in range(msg_length):
            modified_samples[i] &= ~1
            modified_samples[i] |= int(message_bits[i])

        # Create new audio with modified samples
        stego_audio = audio._spawn(modified_samples.tobytes())
        stego_audio.export(output_path, format="wav")
        return True
    except Exception as e:
        print("Error during audio encoding:", e)
        return False

def extract_message_from_audio(audio_file):
    try:
        audio = AudioSegment.from_file(audio_file)
        samples = audio.get_array_of_samples()

        bits = [str(samples[i] & 1) for i in range(len(samples))]
        chars = []
        for i in range(0, len(bits), 8):
            byte = bits[i:i+8]
            if len(byte) < 8:
                break
            char = chr(int(''.join(byte), 2))
            chars.append(char)
            if ''.join(chars).endswith('=='):
                break

        message_b64 = ''.join(chars)
        message_bytes = base64.b64decode(message_b64)
        return message_bytes.decode()
    except Exception as e:
        print("Error during audio decoding:", e)
        return ""
