import cv2
import numpy as np

def embed_message_in_video(video_path, message_bits, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    bit_idx = 0
    success, frame = cap.read()
    while success:
        if bit_idx < len(message_bits):
            for i in range(frame.shape[0]):
                for j in range(frame.shape[1]):
                    if bit_idx >= len(message_bits):
                        break
                    frame[i, j, 0] = (frame[i, j, 0] & ~1) | message_bits[bit_idx]
                    bit_idx += 1
        out.write(frame)
        success, frame = cap.read()

    cap.release()
    out.release()

def extract_message_from_video(video_path, bit_count):
    cap = cv2.VideoCapture(video_path)
    bits = []
    success, frame = cap.read()
    while success and len(bits) < bit_count:
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if len(bits) >= bit_count:
                    break
                bits.append(frame[i, j, 0] & 1)
        success, frame = cap.read()
    cap.release()
    return bits

def text_to_bits(text):
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

def bits_to_text(bits):
    chars = [chr(int(''.join(str(b) for b in bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

