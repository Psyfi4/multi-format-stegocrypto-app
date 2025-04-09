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
def embed_message_in_video(video_path, message_bits, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    bit_idx = 0
    success, frame = cap.read()
    while success:
        frame = frame.copy()
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if bit_idx >= len(message_bits):
                    break
                bit = message_bits[bit_idx]
                bit = 1 if bit else 0
                original_val = int(frame[i, j, 0])
                modified_val = (original_val & ~1) | bit
                frame[i, j, 0] = np.uint8(modified_val)
                bit_idx += 1
            if bit_idx >= len(message_bits):
                break
        out.write(frame)
        success, frame = cap.read()

    cap.release()
    out.release()

def extract_message_from_video(video_path, bit_count):
    cap = cv2.VideoCapture(video_path)
    bits = []
    success, frame = cap.read()
    while success and len(bits) < bit_count:
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                if len(bits) >= bit_count:
                    break
                bits.append(frame[i, j, 0] & 1)
        success, frame = cap.read()
    cap.release()
    return bits

def text_to_bits(text):
    return [int(bit) for char in text for bit in format(ord(char), '08b')]

def bits_to_text(bits):
    chars = [chr(int(''.join(str(b) for b in bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
    return ''.join(chars)

if format_option == "Video":
    uploaded_file = st.file_uploader("Upload Video File", type=["mp4"])
    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_vid:
            tmp_vid.write(uploaded_file.read())
            tmp_vid_path = tmp_vid.name

        if action == "Encode":
            secret_message = st.text_area("Enter message to encode")
            if st.button("Encode"):
                try:
                    if not password:
                        st.error("Password is required for encryption.")
                    else:
                        encrypted = aes_crypto.encrypt_message(secret_message, password)
                        message_bits = text_to_bits(encrypted)
                        output_path = tmp_vid_path.replace(".mp4", "_stego.mp4")
                        embed_message_in_video(tmp_vid_path, message_bits, output_path)
                        with open(output_path, "rb") as f:
                            st.download_button("Download Stego Video", f, file_name="stego_video.mp4")
                except Exception as e:
                    st.error(f"Error during video encoding: {e}")

        elif action == "Decode":
            bit_count = st.number_input("Enter number of bits to extract", min_value=1, value=1024)
            if st.button("Decode"):
                try:
                    bits = extract_message_from_video(tmp_vid_path, bit_count)
                    extracted_encrypted = bits_to_text(bits)
                    decrypted = aes_crypto.decrypt_message(extracted_encrypted, password)
                    st.success("Decrypted Message:")
                    st.code(decrypted)
                except Exception as e:
                    st.error(f"Error during video decoding: {e}")
