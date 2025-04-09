import streamlit as st
from PIL import Image
from stegocrypto import aes_crypto, image_stego

st.set_page_config(page_title="🕵️‍♂️ StegoCrypto App", layout="centered")
st.title("🕵️‍♂️ Multi-Format StegoCrypto App")
st.markdown("🔒 Embed encrypted text inside images using LSB + AES.")

st.header("🔐 Encode Message into Image")
img_file = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"], key="encode_image")
msg = st.text_area("Enter Secret Message")
key = st.text_input("Enter 16-char AES Key", max_chars=16, type="password")

if st.button("Encrypt & Hide") and img_file and msg and len(key) == 16:
    try:
        image = Image.open(img_file).convert("RGB")
        enc = aes_crypto.encrypt_message(msg, key)
        out = image_stego.hide_in_image(image, enc)

        st.image(out, caption="Stego Image")
        out.save("stego_output.png")
        with open("stego_output.png", "rb") as f:
            st.download_button("Download Stego Image", f, "stego_image.png", mime="image/png")
    except Exception as e:
        st.error(f"Error during encoding: {e}")

st.divider()

st.header("🧪 Decode Message from Image")
img_file2 = st.file_uploader("Upload Stego Image", type=["png", "jpg", "jpeg"], key="decode_image")
key2 = st.text_input("Enter AES Key", max_chars=16, type="password", key="decode_key")

if st.button("Extract & Decrypt") and img_file2 and len(key2) == 16:
    try:
        image = Image.open(img_file2).convert("RGB")
        enc = image_stego.extract_from_image(image)
        msg = aes_crypto.decrypt_message(enc, key2)
        st.success("Decrypted Message:")
        st.code(msg)
    except Exception as e:
        st.error(f"Error during extraction/decryption: {e}")
