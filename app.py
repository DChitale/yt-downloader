from flask import Flask, render_template, request, send_file
import os
import yt_dlp
import uuid

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        action = request.form.get("action")

        if action == "fetch":  # User clicked "Get Details"
            ydl_opts = {"quiet": True, "skip_download": True}
            formats = []

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)

                    thumbnail = info.get("thumbnail")
                    title = info.get("title")

                    # Collect video-only formats (video codec not none, audio codec none)
                    for f in info['formats']:
                        if f.get('vcodec') != 'none' and f.get('acodec') == 'none':
                            resolution = f.get("format_note") or f.get("height", "?")
                            formats.append({
                                "format_id": f["format_id"],
                                "resolution": f"{resolution}p",
                                "ext": f["ext"],
                                "filesize_mb": round(f.get("filesize", 0) / 1_048_576, 2) if f.get("filesize") else "?"
                            })

                    # Remove duplicates by (resolution, ext)
                    seen = set()
                    unique_formats = []
                    for f in formats:
                        key = (f['resolution'], f['ext'])
                        if key not in seen:
                            unique_formats.append(f)
                            seen.add(key)
                    formats = unique_formats

                    # Sort by resolution ascending
                    formats = sorted(
                        formats,
                        key=lambda x: int(x['resolution'].replace('p', '')) if x['resolution'].replace('p', '').isdigit() else 0
                    )

                return render_template("index.html", formats=formats, url=url, thumbnail=thumbnail, title=title)

            except Exception as e:
                return f"Error fetching formats: {str(e)}"

        elif action == "download":  # User clicked "Download"
            format_id = request.form["format"]
            url = request.form["url"]
            video_id = str(uuid.uuid4())
            output_path = os.path.join(DOWNLOAD_FOLDER, f"{video_id}.%(ext)s")

            ydl_opts = {
                "format": f"{format_id}+bestaudio",
                "outtmpl": output_path,
                "merge_output_format": "mp4",
                "quiet": True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)
                    filename = os.path.splitext(filename)[0] + ".mp4"

                return send_file(filename, as_attachment=True)

            except Exception as e:
                return f"Error downloading: {str(e)}"

    # GET or default
    return render_template("index.html", formats=None)

if __name__ == "__main__":
    app.run(debug=True)
