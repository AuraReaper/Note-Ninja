import streamlit as st
from transcribe import transcribe_audio, convert_mp4_to_mp3, download_youtube_audio
from generate_mom import generate_mom
import os

st.title("Meeting Minutes Generator")
st.write("NOTE: Max file size is 25 MB")
st.write("NOTE: Max video duration is 30 mins")
st.write("🥲Please wait patiently it will take max 2 mins")

input_type = st.radio("Select Input Type:", ("Audio File", "Markdown File", "MP4 Video File", "YouTube Link"))

default_prompt = """Generate professional meeting minutes including Date, Time, Participants, Agenda, Key Discussions, Decisions, and Action Items."""
prompt = st.text_area("Enter Prompt (Optional)", height=150, value=default_prompt)

gemini_api_key = st.secrets.get("GEMINI_API_KEY")
groq_api_key = st.secrets.get("GROQ_API_KEY")

if input_type == "Audio File":
    uploaded_audio = st.file_uploader("Upload Audio File", type=["mp3", "wav", "m4a"])
    if uploaded_audio and st.button("Generate Meeting Minutes"):
        with st.spinner("Processing..."):
            transcription = transcribe_audio(uploaded_audio , groq_api_key)
            mom_content = generate_mom(transcription, prompt, gemini_api_key)
            st.download_button("Download MoM", data=mom_content, file_name="mom.md", mime="text/markdown")
            st.write(mom_content)

elif input_type == "MP4 Video File":
    uploaded_mp4 = st.file_uploader("Upload MP4 File", type=["mp4"])
    if uploaded_mp4 and st.button("Generate Meeting Minutes"):
        with st.spinner("Processing..."):
            mp3_path = convert_mp4_to_mp3(uploaded_mp4)
            with open(mp3_path, "rb") as f:
                transcription = transcribe_audio(f , groq_api_key)
            os.remove(mp3_path)
            mom_content = generate_mom(transcription, prompt, gemini_api_key)
            st.download_button("Download MoM", data=mom_content, file_name="mom.md", mime="text/markdown")
            st.write(mom_content)

elif input_type == "YouTube Link":
    youtube_url = st.text_input("Enter YouTube URL")
    if youtube_url and st.button("Generate Meeting Minutes"):
        with st.spinner("Downloading and Processing..."):
            mp3_path = download_youtube_audio(youtube_url)
            with open(mp3_path, "rb") as f:
                transcription = transcribe_audio(f , groq_api_key)
            os.remove(mp3_path)
            mom_content = generate_mom(transcription, prompt, gemini_api_key)
            st.download_button("Download MoM", data=mom_content, file_name="mom.md", mime="text/markdown")
            st.write(mom_content)

elif input_type == "Markdown File":
    uploaded_md = st.file_uploader("Upload Markdown File", type=["md", "html", "txt"])
    if uploaded_md and st.button("Generate Meeting Minutes"):
        with st.spinner("Processing..."):
            md_content = uploaded_md.read().decode("utf-8")
            mom_content = generate_mom(md_content, prompt, gemini_api_key)
            st.download_button("Download MoM", data=mom_content, file_name="mom.md", mime="text/markdown")
            st.write(mom_content)
