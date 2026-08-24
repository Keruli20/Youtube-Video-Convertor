# Youtube To MP4 Converter

<!-- Put GIF Here -->

## What is my project?

YouTube to MP4 is a free, locally hosted tool that converts online YouTube videos into video files. It integrates SponsorBlock and allows for sponsored segments to be automatically removed from videos. Everything runs locally on your computer and is completely free to use.

## Features

- **Download Vidoes:** Converts online YouTube videos into video files.
- **SponsorBlock Integration:** Automatically detects and removes sponsored segments from videos.
- **Local Processing:** Runs entirely on your computer.
- **Free to Use:** No subscriptions, paid services, or ads.


## Tech Stack

- **Languages:** Python, HTML, CSS, JavaScript
- **Framework:** Flask
- **Libraries:** yt-dlp
- **API:** SponsorBlock API
- **Media Processing:** FFmpeg


## Usage

Run the application and open the web interface in your browser. Paste a YouTube video link,and choose whether to enable SponsorBlock. Click **Download MP4** to download an MP4 file or **Download MP3** for an MP3 file


## Getting Started

### Prerequisites

Before installing the project, make sure **FFmpeg** is installed on your system and available in your system PATH.

You can verify that FFmpeg is installed by running:

```bash
ffmpeg -version
```

If the command is not recognised, install FFmpeg and ensure it has been added to your system PATH before continuing.

### Installation

Clone the repository and navigate to the project folder:

```bash
git clone <repository>
cd <project>
```

Create a virtual environment:

```bash
python -m venv .venv
```

**Windows**

```bash
.venv\Scripts\activate
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Run

Start the application:

```bash
python main.py
```

Once the application is running, open your browser and go to:

```text
http://localhost:5000
```

> **Note:** FFmpeg must be installed and available in your system PATH for video processing to work correctly.

## Future Improvements

* Users can toggle between which sponsorblock options they want

* Only valid URLs should be accepted

* Add loading icon to tell users it's still loading (maybe also add a progress bar if possible?)

