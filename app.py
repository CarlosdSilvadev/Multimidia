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

    if not link or not path:
        return jsonify({"status": "error", "message": "Link ou diretório não fornecidos!"}), 400

    ydl_opts = {
        'format': 'best', 
        'ffmpeg_location': 'C:\\ffmpeg\\bin\\ffmpeg.exe', 
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
     
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
