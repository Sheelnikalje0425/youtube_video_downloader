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
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    ydl_opts = {'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s')}

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return render_template('index.html', success=True)

if __name__ == '__main__':
    app.run(debug=True)
