import streamlit as st
from stegocrypto import aes_crypto, image_stego, audio_stego, pdf_stego

st.set_page_config(page_title="Multi-format StegoCrypto", layout="centered")
st.title("🛡️ Multi-format Steganography + Cryptography")

option = st.sidebar.selectbox("Choose Format", ["Image", "Audio", "PDF"])
mode = st.sidebar.radio("Mode", ["Encode", "Decode"])
key = st.text_input("🔑 Enter 16-char AES Key", type="password")

if len(key) != 16:
    st.warning("AES key must be exactly 16 characters.")
    st.stop()

if option == "Image":
    if mode == "Encode":
        msg = st.text_area("Secret Message")
        img = st.file_uploader("Upload Cover Image", type=["png", "jpg"])
        if st.button("Encrypt & Hide") and img and msg:
            enc = aes_crypto.encrypt_message(msg, key)
            out = image_stego.hide_in_image(img, enc)
            st.download_button("Download Stego Image", out, "stego.png")
    else:
        img = st.file_uploader("Upload Stego Image", type=["png"])
        if st.button("Extract & Decrypt") and img:
            enc = image_stego.extract_from_image(img)
            try:
                dec = aes_crypto.decrypt_message(enc, key)
                st.success("Decrypted Message:")
                st.code(dec)
            except: st.error("Decryption failed.")

elif option == "Audio":
    if mode == "Encode":
        msg = st.text_area("Secret Message")
        audio = st.file_uploader("Upload WAV Audio", type=["wav"])
        if st.button("Encrypt & Hide") and audio and msg:
            enc = aes_crypto.encrypt_message(msg, key)
            out = audio_stego.hide_in_audio(audio, enc)
            st.download_button("Download Stego Audio", out, "stego.wav")
    else:
        audio = st.file_uploader("Upload Stego Audio", type=["wav"])
        if st.button("Extract & Decrypt") and audio:
            enc = audio_stego.extract_from_audio(audio)
            try:
                dec = aes_crypto.decrypt_message(enc, key)
                st.success("Decrypted Message:")
                st.code(dec)
            except: st.error("Decryption failed.")

elif option == "PDF":
    if mode == "Encode":
        msg = st.text_area("Secret Message")
        pdf = st.file_uploader("Upload PDF", type=["pdf"])
        if st.button("Encrypt & Hide") and pdf and msg:
            enc = aes_crypto.encrypt_message(msg, key)
            out = pdf_stego.hide_in_pdf(pdf, enc)
            st.download_button("Download Stego PDF", out, "stego.pdf")
    else:
        pdf = st.file_uploader("Upload Stego PDF", type=["pdf"])
        if st.button("Extract & Decrypt") and pdf:
            enc = pdf_stego.extract_from_pdf(pdf)
            try:
                dec = aes_crypto.decrypt_message(enc, key)
                st.success("Decrypted Message:")
                st.code(dec)
            except: st.error("Decryption failed.")
