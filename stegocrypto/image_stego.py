from PIL import Image
import numpy as np

def hide_in_image(img: Image.Image, message: str) -> Image.Image:
    """Hide encrypted message into image using LSB."""
    binary = ''.join([format(b, '08b') for b in message.encode('utf-8')])
    img = img.convert('RGB')
    data = np.array(img).astype(np.uint8)
    h, w, _ = data.shape
    idx = 0

    for i in range(h):
        for j in range(w):
            if idx < len(binary):
                pixel_val = int(data[i, j, 0])
                bit = int(binary[idx])
                data[i, j, 0] = (pixel_val & 0xFE) | bit
                idx += 1
            else:
                break
        if idx >= len(binary):
            break

    return Image.fromarray(data)

def extract_from_image(img: Image.Image, msg_length: int) -> str:
    """Extract encrypted message from image."""
    img = img.convert('RGB')
    data = np.array(img).astype(np.uint8)
    h, w, _ = data.shape
    bits = []
    idx = 0
    total_bits = msg_length * 8

    for i in range(h):
        for j in range(w):
            if idx < total_bits:
                bits.append(str(data[i, j, 0] & 1))
                idx += 1
            else:
                break
        if idx >= total_bits:
            break

    byte_data = [bits[i:i+8] for i in range(0, total_bits, 8)]
    message = ''.join([chr(int(''.join(b), 2)) for b in byte_data])
    return message
