from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import tempfile
from urllib.parse import urlparse
import subprocess

app = Flask(__name__)

def get_browser_cookies():
    """Detect available browsers and return cookies"""
    browsers = ['chrome', 'firefox', 'safari', 'edge', 'brave']
    for browser in browsers:
        try:
            # Test if browser cookies are accessible
            ydl_opts = {'cookiesfrombrowser': (browser,)}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Just test cookie access, don't download
                pass
            return browser
        except:
            continue
    return None

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL"""
    parsed = urlparse(url)
    return 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc

def download_audio(url, output_path):
    """Download audio from YouTube URL"""
    ydl_opts = {
        'format': '249/bestaudio[ext=m4a]/bestaudio[ext=webm]/bestaudio/best',
        'outtmpl': output_path + '.%(ext)s',
        'noplaylist': True,
        'extractaudio': False,
        'prefer_ffmpeg': True,
        'keepvideo': False,
        'quiet': False,
        'no_warnings': False,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'extractor_retries': 3,
        'fragment_retries': 3,
    }
    
    # Try to use cookies.txt if it exists
    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'
        print("Using cookies.txt file")
    else:
        print("No cookies.txt found, trying without authentication")
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            if not info:
                raise Exception("Could not extract video information")
            
            # Check available formats
            formats = info.get('formats', [])
            audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
            
            if not audio_formats:
                raise Exception("No audio-only formats available")
            
            # Download the audio
            ydl.download([url])
            
            # Find the downloaded file - look for the actual downloaded file
            base_path = output_path.rsplit('.', 1)[0]
            downloaded_file = None
            
            # Check for the actual downloaded file with webm extension
            for ext in ['webm', 'm4a', 'mp3', 'mp4']:
                temp_file = f"{base_path}.{ext}"
                if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                    downloaded_file = temp_file
                    break
            
            # If no file found, look for any file in the temp directory
            if not downloaded_file:
                import glob
                temp_dir = os.path.dirname(base_path)
                pattern = f"{os.path.basename(base_path)}.*"
                files = glob.glob(os.path.join(temp_dir, pattern))
                print(f"Debug: Looking for files with pattern {pattern} in {temp_dir}")
                print(f"Debug: Found files: {files}")
                for file in files:
                    if os.path.getsize(file) > 0:
                        downloaded_file = file
                        print(f"Debug: Found downloaded file: {file} (size: {os.path.getsize(file)})")
                        break
            
            if not downloaded_file:
                print(f"Debug: Base path: {base_path}")
                print(f"Debug: Output path: {output_path}")
                raise Exception("No audio file was downloaded")
            
            # Convert to MP3 if needed
            if not downloaded_file.endswith('.mp3'):
                import subprocess
                result = subprocess.run([
                    'ffmpeg', '-i', downloaded_file, '-acodec', 'libmp3lame', 
                    '-ab', '192k', output_path, '-y'
                ], capture_output=True, text=True)
                if result.returncode != 0:
                    raise Exception(f"FFmpeg conversion failed: {result.stderr}")
                os.remove(downloaded_file)
            else:
                os.rename(downloaded_file, output_path)
                
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test_download():
    """Test route to debug yt-dlp functionality"""
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        # Test yt-dlp info extraction
        ydl_opts = {
            'quiet': True,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        if info:
            formats = info.get('formats', [])
            audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
            
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 'Unknown'),
                'total_formats': len(formats),
                'audio_formats': len(audio_formats),
                'best_audio_format': audio_formats[0] if audio_formats else None,
                'status': 'success'
            })
        else:
            return jsonify({'error': 'No info extracted'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-different-videos')
def test_different_videos():
    """Test different videos to see which ones work without cookies"""
    test_videos = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Rick Roll (very popular)
        "https://www.youtube.com/watch?v=9bZkp7q19f0",  # Gangnam Style (very popular)
        "https://www.youtube.com/watch?v=kJQP7kiw5Fk",  # Despacito (very popular)
    ]
    
    results = []
    for video_url in test_videos:
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                
            results.append({
                'url': video_url,
                'title': info.get('title', 'Unknown'),
                'status': 'success'
            })
        except Exception as e:
            results.append({
                'url': video_url,
                'error': str(e),
                'status': 'failed'
            })
    
    return jsonify({'results': results})

@app.route('/get-video-info', methods=['POST'])
def get_video_info():
    """Get video information for display"""
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url or not is_valid_youtube_url(url):
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        if info:
            return jsonify({
                'title': info.get('title', 'Unknown Title'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration', 0),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0),
                'status': 'success'
            })
        else:
            return jsonify({'error': 'Could not extract video information'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url')
        video_type = data.get('type')
        
        if not url or not is_valid_youtube_url(url):
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        
        # Get video info first to get the title
        ydl_opts = {
            'quiet': True,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if not info:
                return jsonify({'error': 'Could not extract video information'}), 500
            
            # Get video title and clean it for filename
            video_title = info.get('title', 'Unknown Title')
            print(f"Debug: Original video title: {video_title}")
            
            # Just take the first word for simple filename
            first_word = video_title.split()[0] if video_title else 'Video'
            filename = f"{first_word}.mp3"
            print(f"Debug: Simple filename: {filename}")
        
        # Create temporary file for download
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
            temp_path = tmp_file.name
        
        # Download the audio
        download_audio(url, temp_path)
        
        # Check if file was actually created and has content
        if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
            return jsonify({'error': 'Download failed - no audio content found'}), 500
        
        # Return the file for download with the video title as filename
        print(f"Debug: Sending file with download_name: {filename}")
        return send_file(temp_path, as_attachment=True, download_name=filename)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
