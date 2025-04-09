from pydub import AudioSegment
from io import BytesIO

def hide_in_audio(audio_file, message):
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_channels(1)
    samples = audio.get_array_of_samples()
    bits = ''.join(format(ord(c), '08b') for c in message) + '1111111111111110'
    new_samples = []
    idx = 0
    for s in samples:
        if idx < len(bits):
            new_s = (s & ~1) | int(bits[idx])
            idx += 1
        else:
            new_s = s
        new_samples.append(new_s)
    audio = audio._spawn(data=bytes(new_samples))
    buf = BytesIO()
    audio.export(buf, format="wav")
    return buf.getvalue()

def extract_from_audio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    samples = audio.get_array_of_samples()
    bits = ''
    for s in samples:
        bits += str(s & 1)
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ''
    for c in chars:
        if c == '11111110': break
        message += chr(int(c, 2))
    return message
