from PIL import Image
import numpy as np
from io import BytesIO

def hide_in_image(image_file, message):
    img = Image.open(image_file).convert("RGB")
    data = np.array(img)
    binary = ''.join([format(ord(i), '08b') for i in message]) + '1111111111111110'
    idx = 0
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if idx < len(binary):
                data[i, j, 0] = (data[i, j, 0] & ~1) | int(binary[idx])
                idx += 1
    stego_img = Image.fromarray(data)
    buf = BytesIO()
    stego_img.save(buf, format='PNG')
    return buf.getvalue()

def extract_from_image(stego_file):
    img = Image.open(stego_file)
    data = np.array(img)
    bits = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            bits.append(str(data[i, j, 0] & 1))
    bits = ''.join(bits)
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    message = ''
    for c in chars:
        if c == '11111110': break
        message += chr(int(c, 2))
    return message
