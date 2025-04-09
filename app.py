import streamlit as st
from PIL import Image
import io
import base64
import numpy as np
import tempfile
import os
import cv2
from stegocrypto import aes_crypto, image_stego, audio_stego, pdf_stego, video_stego

st.set_page_config(page_title="🛡️ Multi-Format StegoCrypto App", layout="wide")
st.title("🛡️ Multi-Format StegoCrypto App")

# Tabs instead of selectbox
tab1, tab2, tab3, tab4 = st.tabs(["Image", "Audio", "PDF", "Video"])

with tab1:
    st.header("🔳 Image Steganography")
    mode = st.radio("Choose mode:", ("Encode", "Decode"), key="image_mode")
    password = st.text_input("Enter password:", type="password", key="image_pass")

    if mode == "Encode":
        uploaded_file = st.file_uploader("Choose an image to encode", type=["png", "jpg", "jpeg"], key="image_enc")
        message = st.text_area("Enter your secret message:")
        if st.button("Encode", key="image_enc_btn"):
            if uploaded_file and message and password:
                try:
                    encrypted = aes_crypto.encrypt_message(message, password)
                    result_img = image_stego.encode_image(uploaded_file, encrypted)
                    st.image(result_img, caption="Encoded Image")
                except Exception as e:
                    st.error(f"Error during encoding: {e}")
            else:
                st.warning("Please upload an image, enter a message, and a password.")

    elif mode == "Decode":
        uploaded_file = st.file_uploader("Choose an image to decode", type=["png", "jpg", "jpeg"], key="image_dec")
        if st.button("Decode", key="image_dec_btn"):
            if uploaded_file and password:
                try:
                    encrypted = image_stego.decode_image(uploaded_file)
                    decrypted = aes_crypto.decrypt_message(encrypted, password)
                    st.success(f"Secret Message: {decrypted}")
                except Exception as e:
                    st.error(f"Error during decoding: {e}")
            else:
                st.warning("Please upload an image and enter a password.")

with tab2:
    st.header("🔊 Audio Steganography")
    mode = st.radio("Choose mode:", ("Encode", "Decode"), key="audio_mode")
    password = st.text_input("Enter password:", type="password", key="audio_pass")

    if mode == "Encode":
        uploaded_file = st.file_uploader("Choose an audio file (wav)", type=["wav"], key="audio_enc")
        message = st.text_area("Enter your secret message:")
        if st.button("Encode", key="audio_enc_btn"):
            if uploaded_file and message and password:
                try:
                    encrypted = aes_crypto.encrypt_message(message, password)
                    result_audio = audio_stego.encode_audio(uploaded_file, encrypted)
                    st.audio(result_audio, format="audio/wav")
                except Exception as e:
                    st.error(f"Error during encoding: {e}")
            else:
                st.warning("Please upload audio, enter a message and password.")

    elif mode == "Decode":
        uploaded_file = st.file_uploader("Choose an audio file to decode (wav)", type=["wav"], key="audio_dec")
        if st.button("Decode", key="audio_dec_btn"):
            if uploaded_file and password:
                try:
                    encrypted = audio_stego.decode_audio(uploaded_file)
                    decrypted = aes_crypto.decrypt_message(encrypted, password)
                    st.success(f"Secret Message: {decrypted}")
                except Exception as e:
                    st.error(f"Error during decoding: {e}")
            else:
                st.warning("Please upload audio and enter a password.")

with tab3:
    st.header("📄 PDF Steganography")
    mode = st.radio("Choose mode:", ("Encode", "Decode"), key="pdf_mode")
    password = st.text_input("Enter password:", type="password", key="pdf_pass")

    if mode == "Encode":
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], key="pdf_enc")
        message = st.text_area("Enter your secret message:")
        if st.button("Encode", key="pdf_enc_btn"):
            if uploaded_file and message and password:
                try:
                    encrypted = aes_crypto.encrypt_message(message, password)
                    result_pdf = pdf_stego.encode_pdf(uploaded_file, encrypted)
                    st.download_button("Download encoded PDF", data=result_pdf, file_name="encoded.pdf")
                except Exception as e:
                    st.error(f"Error during encoding: {e}")
            else:
                st.warning("Please upload PDF, enter a message and password.")

    elif mode == "Decode":
        uploaded_file = st.file_uploader("Choose a PDF to decode", type=["pdf"], key="pdf_dec")
        if st.button("Decode", key="pdf_dec_btn"):
            if uploaded_file and password:
                try:
                    encrypted = pdf_stego.decode_pdf(uploaded_file)
                    decrypted = aes_crypto.decrypt_message(encrypted, password)
                    st.success(f"Secret Message: {decrypted}")
                except Exception as e:
                    st.error(f"Error during decoding: {e}")
            else:
                st.warning("Please upload PDF and enter a password.")

with tab4:
    st.header("🎥 Video Steganography")
    mode = st.radio("Choose mode:", ("Encode", "Decode"), key="video_mode")
    password = st.text_input("Enter password:", type="password", key="video_pass")

    if mode == "Encode":
        uploaded_file = st.file_uploader("Upload MP4 video", type=["mp4"], key="video_enc")
        message = st.text_area("Enter your secret message:")
        if st.button("Encode", key="video_enc_btn"):
            if uploaded_file and message and password:
                try:
                    encrypted = aes_crypto.encrypt_message(message, password)
                    result_video = video_stego.encode_video(uploaded_file, encrypted)
                    st.video(result_video)
                except Exception as e:
                    st.error(f"Error during encoding: {e}")
            else:
                st.warning("Please upload video, enter a message and password.")

    elif mode == "Decode":
        uploaded_file = st.file_uploader("Upload MP4 video to decode", type=["mp4"], key="video_dec")
        if st.button("Decode", key="video_dec_btn"):
            if uploaded_file and password:
                try:
                    encrypted = video_stego.decode_video(uploaded_file)
                    decrypted = aes_crypto.decrypt_message(encrypted, password)
                    st.success(f"Secret Message: {decrypted}")
                except Exception as e:
                    st.error(f"Error during decoding: {e}")
            else:
                st.warning("Please upload video and enter a password.")
