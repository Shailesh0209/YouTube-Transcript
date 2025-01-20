# **YouTube Channel Audio Downloader and Multi-Language Transcriber**

## **Overview**
This Streamlit-based application allows users to:
1. Download audio from videos of a specified YouTube channel.
2. Transcribe the audio into text in multiple languages.
3. Save the transcription with timestamps in a CSV file for easy access and download.

Supported transcription languages include **Kannada, Hindi, Tamil, Telugu, and Malayalam**.

---

## **Features**
- **Fetch YouTube Video IDs**: Retrieves video IDs from a given YouTube channel using the YouTube Data API.
- **Audio Download**: Downloads audio from YouTube videos in MP3 format using `yt_dlp`.
- **Language-Specific Transcription**: Supports transcription in selected languages using the Whisper AI model.
- **Timestamped Transcription**: Includes start and end timestamps for each segment of the transcription.
- **CSV Export**: Allows users to download the transcription with timestamps as a CSV file.

---

## **Prerequisites**
### **Required Tools and Libraries**
1. Python 3.7+
2. Streamlit
3. yt_dlp
4. Whisper
5. Pandas
6. Google API Client
7. ffmpeg (for audio processing)

### **API Key**
- A valid YouTube Data API Key is required to fetch video information. You can generate an API key from the [Google Cloud Console](https://console.cloud.google.com/).

---

## **Installation**
1. Clone the repository or copy the script file.
2. Install the required dependencies:
   ```bash
   pip install streamlit yt-dlp whisper google-api-python-client pandas
   ```
3. Ensure `ffmpeg` is installed on your system. You can install it via:
   - For Linux: `sudo apt install ffmpeg`
   - For macOS: `brew install ffmpeg`
   - For Windows: Download and install from the [FFmpeg website](https://ffmpeg.org/download.html).

---

## **How to Run**
1. Save the script as `app.py`.
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open the application in your web browser using the URL displayed in the terminal.

---

## **Usage**
### **Step 1: Enter Inputs**
- **YouTube Channel ID**: Provide the Channel ID (e.g., `UC_x5XG1OV2P6uZZ5FSM9Ttw`).
- **YouTube Data API Key**: Enter your API key securely.
- **Number of Videos**: Select how many videos you want to process using the slider.
- **Transcription Language**: Choose one of the supported languages (Kannada, Hindi, Tamil, Telugu, Malayalam).

### **Step 2: Process Channel**
- Click on the **"Process Channel"** button to:
  1. Fetch video IDs from the specified channel.
  2. Download audio from the videos.
  3. Transcribe the audio in the selected language.

### **Step 3: Download Transcription**
- Once processing is complete, the application generates a CSV file containing:
  - **Video ID**
  - **Start Time (s)**
  - **End Time (s)**
  - **Transcript**
- Use the **"Download Transcription CSV"** button to save the file locally.

---

## **Code Documentation**
### **1. Function Descriptions**
#### **`get_timestamp()`**
- Returns the current timestamp in the format `YYYY-MM-DD HH:MM:SS`.
- Used for logging and debugging.

#### **`get_language_code(selected_language)`**
- Maps the user's selected language to the corresponding Whisper-supported language code.
- Supported mappings:
  - Kannada → `kn`
  - Hindi → `hi`
  - Tamil → `ta`
  - Telugu → `te`
  - Malayalam → `ml`

#### **`get_video_ids(channel_id, api_key, max_videos)`**
- Fetches video IDs from the given YouTube channel using the YouTube Data API.
- Parameters:
  - `channel_id`: The Channel ID.
  - `api_key`: YouTube Data API Key.
  - `max_videos`: Maximum number of videos to fetch.
- Returns:
  - A list of video IDs.

#### **`download_youtube_audio(video_id, output_path)`**
- Downloads the audio of a video from YouTube in MP3 format using `yt_dlp`.
- Parameters:
  - `video_id`: The ID of the YouTube video.
  - `output_path`: Directory where the audio file will be saved.
- Returns:
  - Path to the downloaded MP3 file.

#### **`transcribe_audio(audio_file, language_code)`**
- Transcribes audio using Whisper's "large" model.
- Parameters:
  - `audio_file`: Path to the MP3 file.
  - `language_code`: Language code for transcription.
- Returns:
  - Transcription results including text and timestamps for each segment.

---

### **2. Key Variables**
- **`channel_id`**: Stores the Channel ID entered by the user.
- **`api_key`**: Stores the YouTube Data API Key securely.
- **`selected_language`**: The language selected by the user for transcription.
- **`output_path`**: Directory to save audio and CSV files (`audio_files` by default).

---

## **CSV Output**
The generated CSV file contains the following columns:
1. **Video ID**: The ID of the YouTube video.
2. **Start Time (s)**: The start time of the transcript segment.
3. **End Time (s)**: The end time of the transcript segment.
4. **Transcript**: The text transcription of the audio segment.

Example:
| Video ID      | Start Time (s) | End Time (s) | Transcript             |
|---------------|----------------|--------------|------------------------|
| `KrOV0Andk3E` | 4.88           | 6.64         | पांच खंबो वाला गांव      |
| `KrOV0Andk3E` | 7.68           | 9.84         | लेखक मुकेश माविया       |

---

## **Error Handling**
1. **Invalid Channel ID or API Key**:
   - Displays an error message if the Channel ID or API Key is invalid.
2. **Audio Download Failure**:
   - Catches issues during audio download and logs the error.
3. **Transcription Issues**:
   - Handles exceptions during transcription and provides detailed error logs.

---

## **Future Enhancements**
- Add support for more languages.
- Allow batch processing for multiple channels.
- Include additional audio formats for downloading.

---

## **Credits**
This application leverages the following:
- **[Streamlit](https://streamlit.io/)**: For building an interactive web interface.
- **[yt_dlp](https://github.com/yt-dlp/yt-dlp)**: For downloading YouTube audio.
- **[Whisper AI](https://github.com/openai/whisper)**: For state-of-the-art transcription.
- **[YouTube Data API](https://developers.google.com/youtube/v3)**: For fetching video details.

---

## **License**
This project is licensed under the MIT License. Feel free to use, modify, and distribute as needed.

---

This documentation is designed to make onboarding and usage straightforward for developers and non-technical users alike. Let me know if you'd like any refinements! 🚀
