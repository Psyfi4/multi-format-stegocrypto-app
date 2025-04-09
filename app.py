import streamlit as st
from PIL import Image
from io import BytesIO
from stegocrypto import aes_crypto, image_stego

st.set_page_config(page_title="Multi-Format StegoCrypto App", layout="centered")
st.title("🛡️ Multi-Format Steganography + Cryptography")

option = st.sidebar.selectbox("Select Format", ["Image"], key="format_select")

# Image Steganography
if option == "Image":
    st.subheader("🖼️ Image Steganography")
    img_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="img_upload")
    msg = st.text_area("Enter Message")
    key = st.text_input("Enter 16-char AES Key", max_chars=16, type="password", key="img_key")

    if st.button("Encrypt & Hide") and img_file and msg and len(key) == 16:
        image = Image.open(img_file).convert("RGB")
        enc = aes_crypto.encrypt_message(msg, key)
        out = image_stego.hide_in_image(image, enc)
        st.image(out, caption="Stego Image")
        buf = BytesIO()
        out.save(buf, format="PNG")
        st.download_button("Download Stego Image", buf.getvalue(), "stego.png", mime="image/png")

    st.markdown("---")

    img_file2 = st.file_uploader("Upload Stego Image", type=["png"], key="stego_upload")
    key2 = st.text_input("Enter AES Key for Decryption", max_chars=16, type="password", key="decrypt_key")

    if st.button("Extract & Decrypt") and img_file2 and len(key2) == 16:
        image = Image.open(img_file2).convert("RGB")
        enc = image_stego.extract_from_image(image)
        msg = aes_crypto.decrypt_message(enc, key2)
        st.success("Decrypted Message:")
        st.code(msg)
