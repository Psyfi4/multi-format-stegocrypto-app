from PIL import Image
import numpy as np

def text_to_binary(text):
    return ''.join(f"{ord(c):08b}" for c in text)

def binary_to_text(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(c, 2)) for c in chars)

def hide_in_image(img: Image.Image, message: str) -> Image.Image:
    binary_msg = text_to_binary(message)
    msg_len = len(binary_msg)
    
    # Store message length as 32-bit binary
    len_bin = f"{msg_len:032b}"
    full_binary = len_bin + binary_msg

    data = np.array(img)
    flat = data.flatten()

    if len(full_binary) > len(flat):
        raise ValueError("Message too large to hide in this image.")

    for i in range(len(full_binary)):
        flat[i] = (flat[i] & ~1) | int(full_binary[i])  # Set LSB

    # Reshape and return new image
    new_data = flat.reshape(data.shape)
    return Image.fromarray(new_data.astype(np.uint8))

def extract_from_image(img: Image.Image) -> str:
    data = np.array(img)
    flat = data.flatten()

    # Read the first 32 bits to get message length
    len_bin = ''.join(str(flat[i] & 1) for i in range(32))
    msg_len = int(len_bin, 2)

    # Then extract the actual message
    msg_bits = ''.join(str(flat[i] & 1) for i in range(32, 32 + msg_len))
    return binary_to_text(msg_bits)
