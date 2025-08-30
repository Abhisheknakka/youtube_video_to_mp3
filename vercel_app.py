from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import os
import tempfile
from urllib.parse import urlparse
import json

app = Flask(__name__)

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL"""
    parsed = urlparse(url)
    return 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc

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
    """Note: File downloads may not work in Vercel's serverless environment"""
    return jsonify({
        'error': 'File downloads are not supported in this serverless environment. Please use the local version for downloads.',
        'message': 'This is a demo deployment. File downloads require the full Flask app running locally.'
    }), 400

# Vercel requires this for serverless deployment
app.debug = False

# For local development
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
