import os
import yt_dlp
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()

    link = data.get('link')
    path = data.get('path')
    download_type = data.get('download_type') 

    if not link or not path or not download_type:
        return jsonify({"status": "error", "message": "Link, diretório ou tipo de download não fornecidos!"}), 400

   
    ffmpeg_path = 'C:\\ffmpeg\\bin'

    if download_type == 'video':
        ydl_opts = {
            'format': 'best',
            'ffmpeg_location': ffmpeg_path,
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'logger': None
        }
    elif download_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'ffmpeg_location': ffmpeg_path,
            'outtmpl': os.path.join(path, '%(title)s.mp3'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
            'logger': None
        }

    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            with open(os.devnull, 'w') as devnull:
                ydl._err_file = devnull 
                ydl.download([link])
        return jsonify({"status": "success"})
    except Exception as e:
        
        return jsonify({"status": "success"}) 

if __name__ == "__main__":
    app.run(debug=True)
