from flask import Flask, render_template, request, send_file, after_this_request
from yt_dlp import YoutubeDL
import os
import time
import tempfile
import shutil
import re

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    pattern = "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$"
    url = request.form.get("url")
    if not url:
        return render_template("index.html", error="Please enter a URL")
    # TODO Add checks to ensure that a youtube URL is valid using regex
    elif not (re.search(pattern, url)):
         return render_template("index.html", error="Invalid URL")

    # Gets the requested download format for the file (Mp3 or Mp4)
    file_format = request.form.get("file_format")

    # Create a directory to store the downloads
    os.makedirs("downloads", exist_ok=True)

    # Runs cleanup function to remove old downloads in temp directory
    cleanup_old_downloads()

    remove_sponsors = request.form.get("sponsorblock")
    
    sponsorblock_postprocessors = []
    if remove_sponsors:
        sponsorblock_postprocessors = [
            # Retrieves segments timestamps from SponsorBlock
            {
                "key": "SponsorBlock",
                "categories": [
                    "sponsor",
                    "selfpromo",
                    "intro",
                    "outro",
                    "interaction",
                ],
            },
            # Uses FFmpeg to remove the selected segments
            {
                "key": "ModifyChapters",
                "remove_sponsor_segments": [
                    "sponsor",
                    "selfpromo",
                    "intro",
                    "outro",
                    "interaction",
                ],
            },
        ]

    # Create a unique temporary directory to store the downloaded file
    temp_dir = tempfile.mkdtemp(dir="downloads")

    if file_format == "mp3":
        options = {
            # Selects the best audio stream
            "format": "bestaudio/best",
            # Uses FFmpeg to convert the downloaded audio into mp3
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3" ,
                },
                # Unpacks the sponsorblock postprocessors list of dictionaries into the postprocessors list
                *sponsorblock_postprocessors,
            ],
            # Saves the output to the temporary directory
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
        }
    else:
        options = {
            # Selects the best video + audio stream
            "format": "bestvideo+bestaudio/best",
            # Uses an MP4 container when merging the video + audio stream
            "merge_output_format": "mp4",
            "postprocessors": sponsorblock_postprocessors,
            "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
        }

    with YoutubeDL(options) as ydl:
        # Gets the metadata of the URL
        info = ydl.extract_info(url, download=True)
        # Gets filename of the video
        filename = ydl.prepare_filename(info)
        if file_format == "mp3":
            filename = os.path.splitext(filename)[0] + ".mp3"
        else:
            filename = os.path.splitext(filename)[0] + ".mp4"

    return send_file(filename, as_attachment=True)


# Function that cleans up old downloads in the downloads directory
def cleanup_old_downloads():
    path = "downloads"
    # Maximum age before the directory is deleted (1 hour)
    max_age = 1 * 60 * 60
    current_time = time.time()

    # Scans each directory and gets their age
    for directory in os.scandir(path):
        if directory.is_dir():
            age = current_time - directory.stat().st_mtime

        # If their age is greater than the maximum age, the directory is removed
        if age > max_age:
            shutil.rmtree(directory.path)
            

app.run(host="0.0.0.0", port=5000)