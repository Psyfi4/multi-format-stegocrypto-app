import streamlit as st
from PIL import Image
import io
import base64
import numpy as np
import tempfile
import os
import cv2
from stegocrypto import aes_crypto, image_stego, audio_stego, pdf_stego, video_stego

st.set_page_config(page_title="🗭️ Multi-Format StegoCrypto App", layout="wide")
st.title("🗭️ Multi-Format StegoCrypto App")

# Helper functions
def show_success(message):
    st.success(message)

def show_error(message):
    st.error(message)

# AES encryption wrapper
def encrypt_message(key, message):
    return aes_crypto.encrypt_data(key.encode(), message)

def decrypt_message(key, ciphertext):
    return aes_crypto.decrypt_data(key.encode(), ciphertext)

# Tabs for modes
tabs = st.tabs(["Image", "Audio", "PDF", "Video"])

# ------------------------- IMAGE TAB -------------------------
with tabs[0]:
    st.header("🖼️ Image Steganography")
    operation = st.radio("Choose operation:", ["Encode", "Decode"], key="image_operation")

    if operation == "Encode":
        uploaded_image = st.file_uploader("Upload image:", type=["png"], key="image_upload")
        message = st.text_area("Enter your secret message:", key="message_image")
        password = st.text_input("Enter AES encryption key:", type="password", key="key_image")

        if st.button("Encode Message", key="btn_encode_image"):
            if uploaded_image and message and password:
                try:
                    encrypted = encrypt_message(password, message)
                    image = Image.open(uploaded_image)
                    output = image_stego.encode_message_into_image(image, encrypted)
                    st.image(output, caption="Image with hidden message")
                    buf = io.BytesIO()
                    output.save(buf, format="PNG")
                    b64 = base64.b64encode(buf.getvalue()).decode()
                    href = f'<a href="data:image/png;base64,{b64}" download="stego_image.png">Download Stego Image</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    show_success("Message encoded successfully.")
                except Exception as e:
                    show_error(f"Error: {e}")
            else:
                show_error("Please upload image, enter message and key.")

    else:
        uploaded_image = st.file_uploader("Upload stego image:", type=["png"], key="decode_image_upload")
        password = st.text_input("Enter AES decryption key:", type="password", key="key_image_decode")
        if st.button("Decode Message", key="btn_decode_image"):
            if uploaded_image and password:
                try:
                    image = Image.open(uploaded_image)
                    encrypted = image_stego.decode_message_from_image(image)
                    decrypted = decrypt_message(password, encrypted)
                    st.text_area("Decrypted Message:", decrypted, height=200, key="decoded_message_image")
                    show_success("Message decoded successfully.")
                except Exception as e:
                    show_error(f"Error: {e}")
            else:
                show_error("Please upload image and enter key.")

# ------------------------- AUDIO TAB -------------------------
with tabs[1]:
    st.header("🎧 Audio Steganography")
    operation = st.radio("Choose operation:", ["Encode", "Decode"], key="audio_operation")

    if operation == "Encode":
        uploaded_audio = st.file_uploader("Upload WAV audio file:", type=["wav"], key="audio_upload")
        message = st.text_area("Enter your secret message:", key="message_audio")
        password = st.text_input("Enter AES encryption key:", type="password", key="key_audio")

        if st.button("Encode Message", key="btn_encode_audio"):
            if uploaded_audio and message and password:
                try:
                    encrypted = encrypt_message(password, message)
                    audio_bytes = uploaded_audio.read()
                    stego_audio = audio_stego.hide_in_audio(audio_bytes, encrypted)
                    b64 = base64.b64encode(stego_audio).decode()
                    href = f'<a href="data:audio/wav;base64,{b64}" download="stego_audio.wav">Download Stego Audio</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    show_success("Message encoded in audio successfully.")
                except Exception as e:
                    show_error(f"Error during audio encoding: {e}")
            else:
                show_error("Please upload audio, enter message and key.")

    else:
        uploaded_audio = st.file_uploader("Upload stego audio file:", type=["wav"], key="decode_audio_upload")
        password = st.text_input("Enter AES decryption key:", type="password", key="key_audio_decode")
        if st.button("Decode Message", key="btn_decode_audio"):
            if uploaded_audio and password:
                try:
                    audio_bytes = uploaded_audio.read()
                    encrypted = audio_stego.reveal_from_audio(audio_bytes)
                    decrypted = decrypt_message(password, encrypted)
                    st.text_area("Decrypted Message:", decrypted, height=200, key="decoded_message_audio")
                    show_success("Message decoded from audio successfully.")
                except Exception as e:
                    show_error(f"Error during audio decoding: {e}")
            else:
                show_error("Please upload audio and enter key.")

# ------------------------- PDF TAB -------------------------
with tabs[2]:
    st.header("📄 PDF Steganography")
    operation = st.radio("Choose operation:", ["Encode", "Decode"], key="pdf_operation")

    if operation == "Encode":
        uploaded_pdf = st.file_uploader("Upload PDF file:", type=["pdf"], key="pdf_upload")
        message = st.text_area("Enter your secret message:", key="message_pdf")
        password = st.text_input("Enter AES encryption key:", type="password", key="key_pdf")

        if st.button("Encode Message", key="btn_encode_pdf"):
            if uploaded_pdf and message and password:
                try:
                    encrypted = encrypt_message(password, message)
                    output_pdf = pdf_stego.hide_message_in_pdf(uploaded_pdf, encrypted)
                    b64 = base64.b64encode(output_pdf).decode()
                    href = f'<a href="data:application/pdf;base64,{b64}" download="stego_pdf.pdf">Download Stego PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    show_success("Message encoded in PDF successfully.")
                except Exception as e:
                    show_error(f"Error: {e}")
            else:
                show_error("Please upload PDF, enter message and key.")

    else:
        uploaded_pdf = st.file_uploader("Upload stego PDF file:", type=["pdf"], key="decode_pdf_upload")
        password = st.text_input("Enter AES decryption key:", type="password", key="key_pdf_decode")
        if st.button("Decode Message", key="btn_decode_pdf"):
            if uploaded_pdf and password:
                try:
                    encrypted = pdf_stego.extract_message_from_pdf(uploaded_pdf)
                    decrypted = decrypt_message(password, encrypted)
                    st.text_area("Decrypted Message:", decrypted, height=200, key="decoded_message_pdf")
                    show_success("Message decoded from PDF successfully.")
                except Exception as e:
                    show_error(f"Error: {e}")
            else:
                show_error("Please upload PDF and enter key.")

# ------------------------- VIDEO TAB -------------------------
with tabs[3]:
    st.header("🎥 Video Steganography")
    operation = st.radio("Choose operation:", ["Encode", "Decode"], key="video_operation")

    if operation == "Encode":
        uploaded_video = st.file_uploader("Upload MP4 video file:", type=["mp4"], key="video_upload")
        message = st.text_area("Enter your secret message:", key="message_video")
        password = st.text_input("Enter AES encryption key:", type="password", key="key_video")

        if st.button("Encode Message", key="btn_encode_video"):
            if uploaded_video and message and password:
                try:
                    encrypted = encrypt_message(password, message)
                    video_bytes = uploaded_video.read()
                    temp_input = "input_temp.mp4"
                    temp_output = "output_stego.mp4"
                    with open(temp_input, "wb") as f:
                        f.write(video_bytes)
                    video_stego.hide_in_video(temp_input, encrypted, temp_output)
                    with open(temp_output, "rb") as f:
                        stego_video = f.read()
                    b64 = base64.b64encode(stego_video).decode()
                    href = f'<a href="data:video/mp4;base64,{b64}" download="stego_video.mp4">Download Stego Video</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    show_success("Message encoded in video successfully.")
                except Exception as e:
                    show_error(f"Error during video encoding: {e}")
            else:
                show_error("Please upload video, enter message and key.")

    else:
        uploaded_video = st.file_uploader("Upload stego video file:", type=["mp4"], key="decode_video_upload")
        password = st.text_input("Enter AES decryption key:", type="password", key="key_video_decode")
        bit_count = st.number_input("Enter expected bit count (8 x length of hidden text):", min_value=8, step=8, key="bitcount_video")
        if st.button("Decode Message", key="btn_decode_video"):
            if uploaded_video and password and bit_count:
                try:
                    temp_input = "input_temp_decode.mp4"
                    with open(temp_input, "wb") as f:
                        f.write(uploaded_video.read())
                    bits = video_stego.extract_message_from_video(temp_input, int(bit_count))
                    encrypted = video_stego.bits_to_text(bits)
                    decrypted = decrypt_message(password, encrypted)
                    st.text_area("Decrypted Message:", decrypted, height=200, key="decoded_message_video")
                    show_success("Message decoded from video successfully.")
                except Exception as e:
                    show_error(f"Error during video decoding: {e}")
            else:
                show_error("Please upload video, enter key and bit count.")
