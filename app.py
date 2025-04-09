import streamlit as st
from PIL import Image
from stegocrypto import aes_crypto, image_stego

st.set_page_config(page_title="🔐 Multi-Format StegoCrypto", layout="centered")
st.title("🔐 Multi-Format Steganography + Cryptography")

menu = st.sidebar.radio("Choose Option", ["Image Encode", "Image Decode"])

if menu == "Image Encode":
    st.header("🖼️ Hide Message in Image")
    uploaded_file = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"], key="encode_img")
    message = st.text_area("Enter Message to Hide")
    password = st.text_input("Enter 16-char AES Key", max_chars=16, type="password")

    if st.button("🔒 Encode"):
        if uploaded_file and message and len(password) == 16:
            img = Image.open(uploaded_file).convert("RGB")
            enc = aes_crypto.encrypt(message, password)
            out = image_stego.hide_in_image(img, enc)

            st.image(out, caption="Stego Image")
            out.save("stego_output.png")
            with open("stego_output.png", "rb") as f:
                st.download_button("📥 Download Stego Image", f, file_name="stego_output.png")
        else:
            st.warning("Please upload an image, enter a message, and use a 16-character key.")

elif menu == "Image Decode":
    st.header("🕵️ Extract Message from Image")
    img_file = st.file_uploader("Upload Stego Image", type=["png", "jpg", "jpeg"], key="decode_img")
    key = st.text_input("Enter AES Key", max_chars=16, type="password")

    if st.button("Extract & Decrypt"):
        if img_file and len(key) == 16:
            image = Image.open(img_file).convert("RGB")
            enc = image_stego.extract_from_image(image)
            msg = aes_crypto.decrypt(enc, key)
            st.success("Decrypted Message:")
            st.code(msg)
        else:
            st.warning("Please upload a stego image and enter a 16-character key.")
