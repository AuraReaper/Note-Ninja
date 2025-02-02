import numpy as np
import soundfile as sf
import io
import yt_dlp
from pydub import AudioSegment
from groq import Groq


def transcribe_audio(uploaded_file, groq_api_key):
	client = Groq(api_key=groq_api_key)

	try:
		# Read and process audio file
		audio_bytes = uploaded_file.read()
		audio_data, sample_rate = sf.read(io.BytesIO(audio_bytes))

		# Convert stereo to mono if necessary
		if len(audio_data.shape) > 1:
			audio_data = audio_data.mean(axis=1)

		audio_data = audio_data.astype(np.float32)

		# Create the prompt for Groq's whisper model
		messages = [
			{
				"role": "system",
				"content": "You are a whisper-large-v3 model. Transcribe the following audio accurately."
			},
			{
				"role": "user",
				"content": f"<audio>{audio_data.tobytes()}</audio>"
			}
		]

		# Make the API call to Groq using whisper-large-v3
		chat_completion = client.chat.completions.create(
			messages=messages,
			model="whisper-large-v3-turbo"
		)

		transcription = chat_completion.choices[0].message.content

		# Reset file pointer
		uploaded_file.seek(0)
		return transcription
	except Exception as e:
		return f"Transcription error: {e}"


def convert_mp4_to_mp3(mp4_file):
	temp_mp3_path = "temp_audio.mp3"
	audio = AudioSegment.from_file(mp4_file, format="mp4")
	audio.export(temp_mp3_path, format="mp3")
	return temp_mp3_path


def download_youtube_audio(youtube_url):
	ydl_opts = {
		'format': 'bestaudio/best',
		'postprocessors': [{
			'key': 'FFmpegExtractAudio',
			'preferredcodec': 'mp3',
			'preferredquality': '192',
		}],
		'outtmpl': 'yt_audio.%(ext)s'
	}

	with yt_dlp.YoutubeDL(ydl_opts) as ydl:
		ydl.download([youtube_url])

	return "yt_audio.mp3"