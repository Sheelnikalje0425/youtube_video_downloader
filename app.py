from flask import Flask, render_template, request
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', success=False)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    file_format = request.form['format']  # Get the selected format
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")

    if file_format == "mp3":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return render_template('index.html', success=True)
    except Exception as e:
        print("Error:", e)
        return render_template('index.html', success=False)

if __name__ == '__main__':
    app.run(debug=True)
