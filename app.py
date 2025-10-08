from flask import Flask, render_template, request, send_file
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

# Temporary download folder on EC2
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def download_video():
    if request.method == "POST":
        url = request.form.get("url")
        try:
            # yt-dlp options
            ydl_opts = {
                'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
                'cookiefile': 'cookies.txt',  # optional if login required
            }

            # Download video
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url)
                filename = ydl.prepare_filename(info)

            # Send file to user's browser
            return send_file(filename, as_attachment=True)

        except Exception as e:
            # Friendly error message for the user
            return f"⚠️ Cannot download video: {str(e)}"

    # Render home page with form
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
