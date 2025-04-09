import cv2
import numpy as np

HEADER_SIZE = 32  # Number of bits used to store message length

def text_to_bits(text):
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

def bits_to_text(bits):
    chars = [chr(int(''.join(str(b) for b in bits[i:i + 8]), 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

def embed_message_in_video(video_path, message, output_path):
    message_bits = text_to_bits(message)
    message_length = len(message_bits)
    header_bits = [int(bit) for bit in format(message_length, f'0{HEADER_SIZE}b')]
    full_bits = header_bits + message_bits

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    bit_idx = 0
    success, frame = cap.read()

    while success:
        if bit_idx < len(full_bits):
            for i in range(frame.shape[0]):
                for j in range(frame.shape[1]):
                    if bit_idx >= len(full_bits):
                        break
                    frame[i, j, 0] = (frame[i, j, 0] & ~1) | full_bits[bit_idx]
                    bit_idx += 1
        out.write(frame)
        success, frame = cap.read()

    cap.release()
    out.release()

def extract_message_from_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    bits = []
    success, frame = cap.read()

    # First, extract the header (message length)
    while success and len(bits) < HEADER_SIZE:
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if len(bits) >= HEADER_SIZE:
                    break
                bits.append(frame[i, j, 0] & 1)
        success, frame = cap.read()

    message_length = int(''.join(str(b) for b in bits), 2)
    message_bits = []

    while success and len(message_bits) < message_length:
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if len(message_bits) >= message_length:
                    break
                message_bits.append(frame[i, j, 0] & 1)
        success, frame = cap.read()

    cap.release()
    return bits_to_text(message_bits)
