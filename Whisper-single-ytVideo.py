import streamlit as st
import whisper
import os
import yt_dlp
import csv  # Import the csv module

# Function to download audio from YouTube
def download_youtube_audio(url, output_path="audio_files"):
    try:
        os.makedirs(output_path, exist_ok=True)
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, '%(id)s.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_id = info_dict["id"]
            filename = os.path.join(output_path, f"{video_id}.mp3")
            return video_id, filename
    except Exception as e:
        st.error(f"An error occurred while downloading audio: {e}")
        return None, None

# Function to transcribe audio using Whisper
def transcribe_audio(audio_file, language_code="en"):
    try:
        model = whisper.load_model("turbo")  # Load Whisper model
        result = model.transcribe(audio_file, language=language_code)
        return result  # Returns transcription result including segments
    except Exception as e:
        st.error(f"An error occurred while transcribing audio: {e}")
        return None

# Function to save transcription to a CSV file
def save_transcription_to_csv(video_id, transcription_result, output_path="transcription.csv"):
    try:
        with open(output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Video ID", "Start Time (s)", "End Time (s)", "Transcript"])  # CSV headers
            
            # Iterate over segments from Whisper's result
            for segment in transcription_result.get('segments', []):
                writer.writerow([
                    f"https://youtu.be/{video_id}",
                    round(segment["start"], 2),  # Start time in seconds
                    round(segment["end"], 2),    # End time in seconds
                    segment["text"]              # Transcript
                ])
        return output_path
    except Exception as e:
        st.error(f"An error occurred while saving to CSV: {e}")
        return None

# Streamlit App
st.title("YouTube Audio Transcription with Whisper")

# Input YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL", "")

# Language selection
languages = {
    "en": "English",
    "hi": "Hindi",
    "kn": "Kannada",
    "ta": "Tamil",
    "te": "Telugu",
    "ml": "Malayalam"
}
selected_language = st.selectbox("Select Language for Transcription", list(languages.keys()), format_func=lambda x: languages[x])

# Process button
if st.button("Transcribe and Save"):
    if youtube_url and selected_language:
        # Step 1: Download the audio from YouTube
        st.info("Downloading audio from YouTube...")
        video_id, audio_file_path = download_youtube_audio(youtube_url)

        if audio_file_path:
            st.success(f"Audio downloaded successfully: {audio_file_path}")

            # Step 2: Transcribe the audio using Whisper
            st.info("Transcribing audio, please wait...")
            transcription_result = transcribe_audio(audio_file_path, selected_language)

            if transcription_result:
                st.success("Transcription completed successfully!")

                # Debugging: Display the JSON response
                st.json(transcription_result)

                # Step 3: Save transcription to CSV
                st.info("Saving transcription to CSV...")
                csv_file_path = save_transcription_to_csv(video_id, transcription_result)
                if csv_file_path:
                    st.success(f"Transcription saved to CSV: {csv_file_path}")

                    # Step 4: Provide download button for CSV
                    with open(csv_file_path, "rb") as csv_file:
                        st.download_button(
                            label="📥 Download Transcription CSV",
                            data=csv_file,
                            file_name=f"{video_id}_transcription.csv",
                            mime="text/csv"
                        )
                else:
                    st.error("Failed to save transcription to CSV.")
            else:
                st.error("Failed to transcribe the audio.")
        else:
            st.error("Failed to download audio.")
    else:
        st.error("Please provide both a YouTube URL and select a language.")
