import streamlit as st
from PIL import Image
import io
from stegocrypto import aes_crypto, image_stego, audio_stego, pdf_stego, video_stego

st.set_page_config(page_title="🛡️ Multi-Format StegoCrypto App", layout="centered")
st.title("🛡️ Multi-Format StegoCrypto App")
st.markdown("Securely encrypt and embed messages into **Images**, **Audio**, **PDFs**, or **Video**.")

# Sidebar Navigation
option = st.sidebar.selectbox("Select Format", ["Image", "Audio", "PDF", "Video"])

# IMAGE TAB
if option == "Image":
    st.header("🖼️ Image Steganography")

    st.subheader("🔐 Encode Message")
    img_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"], key="img_upload")
    msg = st.text_area("Enter Message")
    key = st.text_input("Enter 16-char AES Key", max_chars=16, type="password")

    if st.button("Encrypt & Hide") and img_file and msg and len(key) == 16:
        try:
            image = Image.open(img_file).convert("RGB")
            enc = aes_crypto.encrypt_message(msg, key)
            out = image_stego.hide_in_image(image, enc)
            st.image(out, caption="Stego Image")
            buf = io.BytesIO()
            out.save(buf, format="PNG")
            st.download_button("Download Stego Image", buf.getvalue(), "stego.png")
        except Exception as e:
            st.error(f"Error during encoding: {e}")

    st.subheader("🔓 Decode Message")
    img_file2 = st.file_uploader("Upload Stego Image", type=["png", "jpg", "jpeg"], key="img_extract")
    key2 = st.text_input("Enter AES Key", max_chars=16, type="password")

    if st.button("Extract & Decrypt") and img_file2 and len(key2) == 16:
        try:
            image = Image.open(img_file2).convert("RGB")
            enc = image_stego.extract_from_image(image)
            msg = aes_crypto.decrypt_message(enc, key2)
            st.success("Decrypted Message:")
            st.code(msg)
        except Exception as e:
            st.error(f"Error during extraction/decryption: {e}")

# AUDIO TAB
elif option == "Audio":
    st.header("🔊 Audio Steganography")

    st.subheader("🔐 Encode Message")
    audio_file = st.file_uploader("Upload WAV Audio", type=["wav"], key="audio_upload")
    msg = st.text_area("Enter Message")
    key = st.text_input("Enter 16-char AES Key", max_chars=16, type="password")

    if st.button("Encrypt & Hide in Audio") and audio_file and msg and len(key) == 16:
        try:
            enc = aes_crypto.encrypt_message(msg, key)
            out = audio_stego.hide_in_audio(audio_file, enc)
            st.audio(out)
            st.download_button("Download Stego Audio", out, "stego_audio.wav")
        except Exception as e:
            st.error(f"Error during audio encoding: {e}")

    st.subheader("🔓 Decode Message")
    audio_file2 = st.file_uploader("Upload Stego Audio", type=["wav"], key="audio_extract")
    key2 = st.text_input("Enter AES Key", max_chars=16, type="password")

    if st.button("Extract & Decrypt Audio") and audio_file2 and len(key2) == 16:
        try:
            enc = audio_stego.extract_from_audio(audio_file2)
            msg = aes_crypto.decrypt_message(enc, key2)
            st.success("Decrypted Message:")
            st.code(msg)
        except Exception as e:
            st.error(f"Error during audio extraction/decryption: {e}")

# PDF TAB
elif option == "PDF":
    st.header("📄 PDF Steganography")

    st.subheader("🔐 Encode Message")
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"], key="pdf_upload")
    msg = st.text_area("Enter Message")
    key = st.text_input("Enter 16-char AES Key", max_chars=16, type="password")

    if st.button("Encrypt & Hide in PDF") and pdf_file and msg and len(key) == 16:
        try:
            enc = aes_crypto.encrypt_message(msg, key)
            out = pdf_stego.hide_in_pdf(pdf_file, enc)
            st.download_button("Download Stego PDF", out, "stego.pdf")
        except Exception as e:
            st.error(f"Error during PDF encoding: {e}")

    st.subheader("🔓 Decode Message")
    pdf_file2 = st.file_uploader("Upload Stego PDF", type=["pdf"], key="pdf_extract")
    key2 = st.text_input("Enter AES Key", max_chars=16, type="password")

    if st.button("Extract & Decrypt PDF") and pdf_file2 and len(key2) == 16:
        try:
            enc = pdf_stego.extract_from_pdf(pdf_file2)
            msg = aes_crypto.decrypt_message(enc, key2)
            st.success("Decrypted Message:")
            st.code(msg)
        except Exception as e:
            st.error(f"Error during PDF extraction/decryption: {e}")

# VIDEO TAB
st.sidebar.markdown("---")
mode = st.sidebar.radio("Mode", ["Encode", "Decode"])
password = st.sidebar.text_input("Password", type="password")

if option == "Video":
    if mode == "Encode":
        video_file = st.file_uploader("Upload a video file (mp4)", type=["mp4"])
        secret_message = st.text_area("Secret Message")

        if st.button("Encrypt & Hide") and video_file and secret_message:
            try:
                encrypted = aes_crypto.encrypt_message(secret_message, password)
                input_path = "input_video.mp4"
                output_path = "encoded_video.mp4"

                with open(input_path, "wb") as f:
                    f.write(video_file.read())

                video_stego.embed_message_in_video(input_path, encrypted, output_path)

                with open(output_path, "rb") as f:
                    st.download_button("Download Encoded Video", f, file_name="stego_video.mp4")
            except Exception as e:
                st.error(f"Error during video encoding: {e}")

    elif mode == "Decode":
        stego_video = st.file_uploader("Upload a stego video", type=["mp4"])

        if st.button("Extract & Decrypt") and stego_video:
            try:
                stego_path = "received_video.mp4"
                with open(stego_path, "wb") as f:
                    f.write(stego_video.read())

                extracted = video_stego.extract_message_from_video(stego_path)
                decrypted = aes_crypto.decrypt_message(extracted, password)
                st.success("Decrypted Message:")
                st.code(decrypted)
            except Exception as e:
                st.error(f"Error during video decoding: {e}")
