# YouTube Audio Downloader

A simple web application to download audio from YouTube videos and shorts as MP3 files.

## Features

- 🎵 Download audio from YouTube videos and shorts
- 🎬 Support for both regular videos and YouTube Shorts

## Setup to run this locally

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg (required for audio conversion):**
   
   **On macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **On Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **On Windows:**
   Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)

3. **Run the application:**
   ```bash
   python3 app.py
   ```

4. **Open your browser and go to:**
   ```
   http://localhost:5000
   ```

## Usage

1. Choose between "YouTube Video" or "YouTube Shorts"
2. Paste a YouTube URL in the input field
3. Click "Download MP3"
4. Wait for the download to complete
5. The MP3 file will automatically download to your computer

## Requirements

- Python 3.7+
- Flask
- yt-dlp
- FFmpeg
- Internet connection

## Note

This application is for personal use only. Please respect YouTube's terms of service and copyright laws when downloading content.

application is deployed in render
```

https://youtube-video-to-mp3.onrender.com/upload-cookies

```
