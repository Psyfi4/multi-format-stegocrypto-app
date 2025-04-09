import streamlit as st
from PIL import Image
from stegocrypto import aes_crypto, image_stego, audio_stego, pdf_stego

st.set_page_config(page_title="Multi-Format StegoCrypto App")
st.title("🔐 Multi-Format Steganography + Cryptography")

menu = st.sidebar.radio("Select Mode", ["Image", "Audio", "PDF"])

if menu == "Image":
    st.subheader("🖼️ Image Steganography")

    option = st.radio("Choose Action", ["Encode", "Decode"])

    if option == "Encode":
        uploaded_file = st.file_uploader("Upload Cover Image", type=["png", "jpg", "jpeg"])
        message = st.text_area("Enter Message to Encrypt")
        password = st.text_input("Enter 16-character AES Password", max_chars=16, type="password")

        if st.button("🔒 Encode"):
            if uploaded_file and message and len(password) == 16:
                img = Image.open(uploaded_file).convert("RGB")
                enc = aes_crypto.encrypt(message, password)
                out = image_stego.hide_in_image(img, enc)
                st.image(out, caption="Stego Image")
                out.save("stego_output.png")
                with open("stego_output.png", "rb") as f:
                    st.download_button("Download Stego Image", f, "stego_output.png")
            else:
                st.warning("Upload an image, enter message, and ensure password is 16 chars.")

    elif option == "Decode":
        uploaded_file = st.file_uploader("Upload Stego Image", type=["png", "jpg", "jpeg"])
        password = st.text_input("Enter 16-character AES Password", max_chars=16, type="password")

        if st.button("🔓 Decode"):
            if uploaded_file and len(password) == 16:
                img = Image.open(uploaded_file).convert("RGB")
                extracted = image_stego.extract_from_image(img)
                try:
                    decrypted = aes_crypto.decrypt(extracted, password)
                    st.success("Decrypted Message:")
                    st.code(decrypted)
                except Exception as e:
                    st.error("Failed to decrypt: " + str(e))
            else:
                st.warning("Upload stego image and ensure password is 16 characters.")

elif menu == "Audio":
    st.subheader("🎵 Audio Steganography (Coming Soon)")
    st.info("This module is under development.")

elif menu == "PDF":
    st.subheader("📄 PDF Steganography (Coming Soon)")
    st.info("This module is under development.")

