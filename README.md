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



## 🚨 Important Notes

- **Personal Use Only:** This application is for personal use only
- **Terms of Service:** Please respect YouTube's terms of service
- **Copyright:** Respect copyright laws when downloading content
- **Rate Limiting:** Be mindful of YouTube's rate limits

## 🐛 Troubleshooting

### Common Issues

1. **"Sign in to confirm you're not a bot"**
   - Solution: Upload cookies.txt file via `/upload-cookies`

2. **Download fails with no error**
   - Check if FFmpeg is properly installed
   - Verify internet connection
   - Try a different video URL

3. **App won't start**
   - Ensure Python 3.7+ is installed
   - Check if port 5001 is available
   - Verify all dependencies are installed

4. **Audio quality issues**
   - The app automatically selects the best available format
   - Some videos may have limited audio quality
  


#### How to Get cookies.txt File

**Method 1: Browser Extension (Recommended)**
1. **Chrome/Edge:** Install the "Get cookies.txt" extension from the Chrome Web Store
   - Search for "Get cookies.txt" in Chrome Web Store
   - Click "Add to Chrome"
2. **Go to YouTube:** Navigate to [youtube.com](https://youtube.com) and make sure you're logged in
3. **Export cookies:** Click the extension icon in your browser toolbar
4. **Select YouTube:** Choose youtube.com from the domain list
5. **Download:** Click "Export" to download your cookies.txt file

**Method 2: Manual Export (Advanced Users)**
1. **Open Developer Tools:** Press F12 or right-click → "Inspect"
2. **Go to Application/Storage tab:** Look for Cookies section
3. **Select youtube.com:** Find the YouTube domain
4. **Copy cookies:** Manually copy the cookie values (not recommended for beginners)

**Method 3: Alternative Extensions**
- **Chrome:** "EditThisCookie" extension
- **Firefox:** "Cookie Quick Manager" add-on
- **Edge:** "Get cookies.txt" (same as Chrome)


