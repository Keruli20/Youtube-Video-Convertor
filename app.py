from flask import Flask, render_template, request, send_file, after_this_request
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():

    url = request.form.get("url")
    if not url:
        return render_template("index.html", error="Please enter a URL")
    # TODO Add checks to ensure that the URL is valid using regex
        

    # Gets the format of the button (Mp3 or Mp4)
    file_format = request.form.get("file_format")

    remove_sponsors = request.form.get("sponsorblock")

    sponsorblock_postprocessors = []
    if remove_sponsors:
        sponsorblock_postprocessors = [
            # Uses SponsorBlock to remove segments
            {
                "key": "SponsorBlock",
                "categories": [
                    "sponsor",
                    "selfpromo",
                    "outro",
                    "interaction",
                ],
            },
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

    if file_format == "mp3":
        options = {
            "format": "bestaudio/best",
            # Saves the output to a temp folder
            "outtmpl": "temp/%(title)s.%(ext)s",
            "overwrites": True,
            "postprocessors": [
                {  # Extract audio using ffmpeg
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                },
                # Unpacks the sponsorblock postprocessors list of dictionaries into the postprocessors list
                *sponsorblock_postprocessors,
            ],
        }
    else:
        options = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": "temp/%(title)s.%(ext)s",
            "merge_output_format": "mp4",
            "overwrites": True,
            "postprocessors": sponsorblock_postprocessors,
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

app.run(host="0.0.0.0", port=5000)