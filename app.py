import streamlit as st
from stegocrypto import aes_crypto, image_stego, audio_stego, pdf_stego
from PIL import Image
import io

st.set_page_config(page_title="Multi-format StegoCrypto App", layout="centered")
st.title("🛡️ Multi-format Steganography + Cryptography")

option = st.sidebar.selectbox("Select Format", ["Image", "Audio (Coming Soon)", "PDF (Coming Soon)"])

if option == "Image":
    mode = st.radio("Choose Mode", ["🔐 Encode", "🔓 Decode"])

    if mode == "🔐 Encode":
        img_file = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"])
        msg = st.text_area("Enter Message")
        key = st.text_input("Enter 16-char AES Key", max_chars=16, type="password")

        if st.button("Encrypt & Hide") and img_file and msg and len(key) == 16:
            image = Image.open(img_file).convert("RGB")
            enc = aes_crypto.encrypt_message(msg, key)
            out = image_stego.hide_in_image(image, enc)
            st.download_button("Download Stego Image", out, "stego.png", mime="image/png")

    else:
        img_file = st.file_uploader("Upload Stego Image", type=["png"])
        key = st.text_input("Enter AES Key", max_chars=16, type="password")

        if st.button("Extract & Decrypt") and img_file and len(key) == 16:
            image = Image.open(img_file).convert("RGB")
            enc = image_stego.extract_from_image(image)
            msg = aes_crypto.decrypt_message(enc, key)
            st.success("Decrypted Message:")
            st.code(msg)

elif option == "Audio (Coming Soon)":
    st.info("🔊 Audio steganography module coming soon!")

elif option == "PDF (Coming Soon)":
    st.info("📄 PDF steganography module coming soon!")
