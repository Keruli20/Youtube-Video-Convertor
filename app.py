from flask import Flask, render_template, request, send_file, after_this_request
from yt_dlp import YoutubeDL
import os
import tempfile

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    # TODO Add checks to ensure that the URL is valid, using regex
    url = request.form.get("url")

    # Gets the format of the button (Mp3 or Mp4)
    file_format = request.form.get("file_format")
    print(file_format)
    if file_format == "mp3":
        options = {
            "format": "bestaudio/best",
            # Makes the downloaded file only display the title and extension
            "outtmpl": "temp/%(title)s.%(ext)s",
            "postprocessors": [
                {  # Extract audio using ffmpeg
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }
            ],
        }
    else:
        options = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": "temp/%(title)s.%(ext)s",
            "merge_output_format": "mp4",
        }

    with YoutubeDL(options) as ydl:
        # Gets the metadata of the URL
        info = ydl.extract_info(url, download=True)
        # Gets filename of the video
        filename = ydl.prepare_filename(info)
        if file_format == "mp3":
            filename = os.path.splitext(filename)[0] + ".mp3"

    return send_file(filename, as_attachment=True)
