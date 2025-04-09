import streamlit as st
from PIL import Image
import io
import base64
import tempfile
from stegocrypto import aes_crypto, image_stego, audio_stego, pdf_stego, video_stego

st.set_page_config(page_title="🗭️ Multi-Format StegoCrypto App", layout="wide")
st.title("🗭️ Multi-Format StegoCrypto App")

st.sidebar.header("Select File Format")
format_type = st.sidebar.selectbox("Choose the format to hide your message in:", ("Image", "Audio", "PDF", "Video"))

operation = st.sidebar.radio("Operation", ("Encode", "Decode"))
password = st.sidebar.text_input("Enter password for AES encryption", type="password")

if not password:
    st.warning("Password is required for secure encryption.")
    st.stop()

def handle_result(success, message):
    if success:
        st.success(message)
    else:
        st.error(message)

if format_type == "Image":
    if operation == "Encode":
        uploaded_file = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
        secret_message = st.text_area("Enter the secret message")

        if st.button("Encode") and uploaded_file and secret_message:
            try:
                image = Image.open(uploaded_file)
                encrypted_message = aes_crypto.encrypt_message(secret_message, password)
                encoded_image = image_stego.encode_message_into_image(image, encrypted_message)
                buf = io.BytesIO()
                encoded_image.save(buf, format='PNG')
                byte_im = buf.getvalue()
                b64 = base64.b64encode(byte_im).decode()
                href = f'<a href="data:image/png;base64,{b64}" download="encoded_image.png">Download Encoded Image</a>'
                st.markdown(href, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error during encoding: {e}")

    else:  # Decode
        uploaded_file = st.file_uploader("Upload Encoded Image", type=["png", "jpg", "jpeg"])
        if st.button("Decode") and uploaded_file:
            try:
                image = Image.open(uploaded_file)
                encrypted_message = image_stego.decode_message_from_image(image)
                decrypted_message = aes_crypto.decrypt_message(encrypted_message, password)
                st.success("Hidden Message:")
                st.code(decrypted_message)
            except Exception as e:
                st.error(f"Error during decoding: {e}")

elif format_type == "Audio":
    if operation == "Encode":
        uploaded_file = st.file_uploader("Upload Audio", type=["wav"])
        secret_message = st.text_area("Enter the secret message")

        if st.button("Encode") and uploaded_file and secret_message:
            try:
                encrypted_message = aes_crypto.encrypt_message(secret_message, password)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_in:
                    tmp_in.write(uploaded_file.read())
                    tmp_in_path = tmp_in.name
                output_path = tmp_in_path.replace(".wav", "_encoded.wav")
                audio_stego.encode_audio(tmp_in_path, encrypted_message, output_path)
                with open(output_path, "rb") as file:
                    btn = st.download_button("Download Encoded Audio", file, file_name="encoded_audio.wav")
            except Exception as e:
                st.error(f"Error during audio encoding: {e}")

    else:  # Decode
        uploaded_file = st.file_uploader("Upload Encoded Audio", type=["wav"])
        if st.button("Decode") and uploaded_file:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                hidden_message = audio_stego.decode_audio(tmp_path)
                decrypted_message = aes_crypto.decrypt_message(hidden_message, password)
                st.success("Hidden Message:")
                st.code(decrypted_message)
            except Exception as e:
                st.error(f"Error during audio decoding: {e}")

elif format_type == "PDF":
    if operation == "Encode":
        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
        secret_message = st.text_area("Enter the secret message")

        if st.button("Encode") and uploaded_file and secret_message:
            try:
                encrypted_message = aes_crypto.encrypt_message(secret_message, password)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_in:
                    tmp_in.write(uploaded_file.read())
                    tmp_in_path = tmp_in.name
                output_path = tmp_in_path.replace(".pdf", "_encoded.pdf")
                pdf_stego.encode_pdf(tmp_in_path, encrypted_message, output_path)
                with open(output_path, "rb") as file:
                    st.download_button("Download Encoded PDF", file, file_name="encoded_pdf.pdf")
            except Exception as e:
                st.error(f"Error during PDF encoding: {e}")

    else:  # Decode
        uploaded_file = st.file_uploader("Upload Encoded PDF", type=["pdf"])
        if st.button("Decode") and uploaded_file:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                hidden_message = pdf_stego.decode_pdf(tmp_path)
                decrypted_message = aes_crypto.decrypt_message(hidden_message, password)
                st.success("Hidden Message:")
                st.code(decrypted_message)
            except Exception as e:
                st.error(f"Error during PDF decoding: {e}")

elif format_type == "Video":
    if operation == "Encode":
        uploaded_file = st.file_uploader("Upload Video", type=["mp4"])
        secret_message = st.text_area("Enter the secret message")

        if st.button("Encode") and uploaded_file and secret_message:
            try:
                encrypted_message = aes_crypto.encrypt_message(secret_message, password)
                message_bits = video_stego.text_to_bits(encrypted_message)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_in:
                    tmp_in.write(uploaded_file.read())
                    tmp_in_path = tmp_in.name
                output_path = tmp_in_path.replace(".mp4", "_encoded.mp4")
                video_stego.embed_message_in_video(tmp_in_path, message_bits, output_path)
                with open(output_path, "rb") as file:
                    st.download_button("Download Encoded Video", file, file_name="encoded_video.mp4")
            except Exception as e:
                st.error(f"Error during video encoding: {e}")

    else:  # Decode
        uploaded_file = st.file_uploader("Upload Encoded Video", type=["mp4"])
        bit_count = st.number_input("Enter number of bits to extract", min_value=1)
        if st.button("Decode") and uploaded_file and bit_count:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                bits = video_stego.extract_message_from_video(tmp_path, int(bit_count))
                encrypted_message = video_stego.bits_to_text(bits)
                decrypted_message = aes_crypto.decrypt_message(encrypted_message, password)
                st.success("Hidden Message:")
                st.code(decrypted_message)
            except Exception as e:
                st.error(f"Error during video decoding: {e}")
