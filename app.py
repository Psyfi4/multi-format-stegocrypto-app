import streamlit as st
from PIL import Image
from stegocrypto import aes_crypto, image_stego

st.set_page_config(page_title="Multi-Format StegoCrypto App")
st.title("🔐 Multi-Format Steganography + Cryptography")
st.write("Encrypt and hide messages inside images using AES + LSB techniques.")

st.header("🖼️ Image Encoder")
img_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="img_uploader")
msg = st.text_area("Enter Message")
key = st.text_input("Enter 16-char AES Key", max_chars=16, type="password", key="key1")

if st.button("Encrypt & Hide"):
    if img_file and msg and len(key) == 16:
        image = Image.open(img_file).convert("RGB")
        try:
            enc = aes_crypto.encrypt_message(msg, key)
            out = image_stego.hide_in_image(image, enc)
            st.image(out, caption="Stego Image")
            out.save("stego_output.png")
            with open("stego_output.png", "rb") as file:
                btn = st.download_button(
                    label="📥 Download Stego Image",
                    data=file,
                    file_name="stego_image.png",
                    mime="image/png"
                )
        except Exception as e:
            st.error(f"Error during encoding: {e}")
    else:
        st.warning("Upload an image, type a message, and ensure AES key is 16 characters.")

st.header("🧪 Image Decoder")
img_file2 = st.file_uploader("Upload Stego Image", type=["png", "jpg", "jpeg"], key="stego_img")
key2 = st.text_input("Enter AES Key", max_chars=16, type="password", key="key2")

if st.button("Extract & Decrypt"):
    if img_file2 and len(key2) == 16:
        try:
            image = Image.open(img_file2).convert("RGB")
            enc = image_stego.extract_from_image(image, msg_length=1024)  # Fixed length or make dynamic
            msg = aes_crypto.decrypt_message(enc, key2)
            st.success("Decrypted Message:")
            st.code(msg)
        except Exception as e:
            st.error(f"Error during extraction/decryption: {e}")
    else:
        st.warning("Upload a stego image and ensure AES key is 16 characters.")
