import streamlit as st
import os
import yt_dlp
import whisper
import pandas as pd
from googleapiclient.discovery import build
from datetime import datetime  # Importing datetime for timestamps
import csv

# Function to get current timestamp
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Function to map selected language to Whisper's supported language codes
def get_language_code(selected_language):
    language_map = {
        "Kannada": "kn",
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te",
        "Malayalam": "ml",
    }
    return language_map.get(selected_language, None)

# Function to get video IDs from a YouTube channel
def get_video_ids(channel_id, api_key, max_videos):
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_ids = []
    next_page_token = None

    while len(video_ids) < max_videos:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=min(50, max_videos - len(video_ids)),
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get('items', []):
            if item['id']['kind'] == 'youtube#video':
                video_ids.append(item['id']['videoId'])

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return video_ids[:max_videos]

# Function to download audio from a YouTube video ID
def download_youtube_audio(video_id, output_path='.'):
    try:
        os.makedirs(output_path, exist_ok=True)
        url = f"https://www.youtube.com/watch?v={video_id}"
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, f'{video_id}.%(ext)s'),
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return os.path.join(output_path, f"{video_id}.mp3")
    except Exception as e:
        st.error(f"[{get_timestamp()}] Error while downloading audio for video ID {video_id}: {e}")
        return None

# Function to transcribe audio in the selected language
def transcribe_audio(audio_file, language_code):
    try:
        model = whisper.load_model("large")
        result = model.transcribe(audio_file, language=language_code)
        return result
    except Exception as e:
        st.error(f"[{get_timestamp()}] Error while transcribing audio: {e}")
        return None

# Streamlit App
st.title("YouTube Channel Audio Downloader and Multi-Language Transcriber")

# Input YouTube Channel ID and API Key
channel_id = st.text_input("Enter YouTube Channel ID", "")
api_key = st.text_input("Enter YouTube Data API Key", type="password")

# Select the number of videos to process
max_videos = st.slider("Select number of videos to process", min_value=1, max_value=100, value=10)

# Select the language for transcription
selected_language = st.selectbox(
    "Select transcription language",
    ["Kannada", "Hindi", "Tamil", "Telugu", "Malayalam"]
)
language_code = get_language_code(selected_language)

# Output directory for audio files
output_path = "audio_files"

# Process channel and transcribe videos
if st.button("Process Channel"):
    if channel_id and api_key:
        with st.spinner(f"[{get_timestamp()}] Fetching video IDs..."):
            video_ids = get_video_ids(channel_id, api_key, max_videos)

        if video_ids:
            st.success(f"[{get_timestamp()}] Found {len(video_ids)} videos in the channel. Processing {len(video_ids)} videos.")

            for video_id in video_ids:
                with st.spinner(f"[{get_timestamp()}] Processing video ID: {video_id}"):
                    audio_file = download_youtube_audio(video_id, output_path)
                    if audio_file:
                        st.success(f"[{get_timestamp()}] Audio downloaded for video ID: {video_id}")
                        try:
                            result = transcribe_audio(audio_file, language_code)

                            if result:
                                # Save transcription and timestamps to CSV
                                csv_filename = os.path.join(output_path, f"{video_id}_transcription.csv")
                                with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
                                    writer = csv.writer(file)
                                    writer.writerow(["Video ID", "Start Time (s)", "End Time (s)", "Transcript"])
                                    for segment in result["segments"]:
                                        writer.writerow([
                                            video_id,
                                            round(segment["start"], 2),
                                            round(segment["end"], 2),
                                            segment["text"]
                                        ])

                                st.success(f"[{get_timestamp()}] Transcription saved to {csv_filename}")
                                st.download_button(
                                    label="📥 Download Transcription CSV",
                                    data=open(csv_filename, "r"),
                                    file_name=f"{video_id}_transcription.csv",
                                    mime="text/csv",
                                )
                        except Exception as e:
                            st.error(f"[{get_timestamp()}] Error during transcription: {e}")
                    else:
                        st.error(f"[{get_timestamp()}] Audio download failed for video ID: {video_id}")
        else:
            st.error(f"[{get_timestamp()}] No videos found in the channel.")
    else:
        st.error(f"[{get_timestamp()}] Please enter a valid Channel ID and API Key.")
