# stegocrypto/image_stego.py
import numpy as np
from PIL import Image

def _to_bin(data):
    return ''.join(f"{ord(i):08b}" for i in data)

def _from_bin(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join([chr(int(b, 2)) for b in chars])

def hide_in_image(img, secret_msg):
    data = np.array(img)
    h, w, _ = data.shape
    flat = data[:, :, 0].flatten()

    # Convert message to binary
    bin_msg = _to_bin(secret_msg)
    msg_len = len(bin_msg) // 8  # Length in bytes

    # Convert msg_len to 32-bit binary
    bin_len = f"{msg_len:032b}"

    full_binary = bin_len + bin_msg
    if len(full_binary) > len(flat):
        raise ValueError("Message too large to hide in image")

    for i in range(len(full_binary)):
        flat[i] = (flat[i] & ~1) | int(full_binary[i])

    # Reconstruct image
    data[:, :, 0] = flat.reshape((h, w))
    return Image.fromarray(data)

def extract_from_image(img):
    data = np.array(img)
    flat = data[:, :, 0].flatten()

    # First 32 bits = length
    bin_len = ''.join(str(flat[i] & 1) for i in range(32))
    msg_len = int(bin_len, 2)

    total_bits = msg_len * 8
    bin_msg = ''.join(str(flat[i + 32] & 1) for i in range(total_bits))

    return _from_bin(bin_msg)
