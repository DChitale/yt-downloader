# 📹 YouTube Video Downloader (Flask + yt-dlp)

This is a simple web app built using **Flask**, **yt-dlp**, and **ffmpeg** that allows users to:

- Paste a YouTube video URL
- View video details (title, thumbnail)
- Select the desired video quality and format
- Download the video with audio in `.mp4` format

---

## 🚀 Features

- Fetch available video formats from YouTube
- Auto-merges video and audio streams
- Clean UI with thumbnail and resolution selector
- Filters duplicate formats
- Works with most YouTube videos

---

## 🛠 Requirements

- Python 3.7+
- `ffmpeg` installed and in system PATH
- The following Python packages:

```bash
pip install flask yt-dlp 
```
## How to Run
```bash
git clone https://github.com/DChitale/yt-downloader.git
cd yt-downloader
```
Start the Flask server:

```bash
python app.py
```
Open your browser and go to:
```http://localhost:5000```
