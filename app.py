import streamlit as st
from PIL import Image
from stegocrypto import aes_crypto, image_stego

st.set_page_config(page_title="Multi-Format StegoCrypto App")
st.title("🛡️ Multi-Format Steganography + Cryptography")

st.header("🖼️ Image Steganography")
mode = st.radio("Select Mode", ["Encrypt & Hide", "Extract & Decrypt"], horizontal=True)

if mode == "Encrypt & Hide":
    img_file = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"], key="img_upload")
    msg = st.text_area("Enter Message")
    key = st.text_input("Enter 16-char AES Key", max_chars=16, type="password")

    if st.button("Encrypt & Hide") and img_file and msg and len(key) == 16:
        image = Image.open(img_file).convert("RGB")
        enc = aes_crypto.encrypt_message(msg, key)
        out = image_stego.hide_in_image(image, enc)
        st.image(out, caption="Stego Image")
        out.save("stego_output.png")
        with open("stego_output.png", "rb") as f:
            st.download_button("Download Stego Image", f, file_name="stego_output.png")

elif mode == "Extract & Decrypt":
    img_file = st.file_uploader("Upload Stego Image", type=["png", "jpg", "jpeg"], key="img_extract")
    key = st.text_input("Enter AES Key", max_chars=16, type="password")

    if st.button("Extract & Decrypt"):
        if img_file and len(key) == 16:
            image = Image.open(img_file).convert("RGB")
            msg_length = 1024  # Estimate or standard length used during encoding
            enc = image_stego.extract_from_image(image, msg_length)
            msg = aes_crypto.decrypt_message(enc, key)
            st.success("Decrypted Message:")
            st.write(msg)
        else:
            st.error("Upload an image and ensure your key is 16 characters long.")
