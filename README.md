# Audio & Video Downloader (TikTok / YouTube)

A simple CLI tool to download **audio (MP3)** or **video (MP4)** from **TikTok** and **YouTube** using `yt-dlp`.

Downloaded files are saved automatically to your `~/Downloads` folder.

---

## Features

- Download audio → `~/Downloads/audio`
- Download video → `~/Downloads/video`
- Supports:
  - TikTok videos
  - YouTube videos
  - YouTube Shorts
- Optional custom filename
- Auto-detects browser cookies when available
- Works even if no supported browser is found

---

## Requirements

- Python 3.9+
- ffmpeg

Install ffmpeg:

### Fedora
```bash
sudo dnf install ffmpeg
```

### Ubuntu / Debian
```bash
sudo apt install ffmpeg
```

### Windows
Using winget:
```bat
winget install Gyan.FFmpeg
```

Using Chocolatey:
```bat
choco install ffmpeg
```

Manual install: download a build from https://www.gyan.dev/ffmpeg/builds/ and add `ffmpeg` to your PATH.

---

## Install (Python deps)

Use pip (recommended inside a venv):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip yt-dlp
```

---

## Usage

### Option 1: Run the helper script (auto-venv)
```bash
./downloader.sh
```

### Option 2: Run the Python script directly
```bash
python downloader.py
```

### Windows: Run the Python script directly
```bat
py downloader.py
```

If `py` is not available, use:
```bat
python downloader.py
```

You will be prompted for:
- URL (TikTok / YouTube / Shorts)
- Audio or Video
- Optional filename (press Enter to use the video title)

---

## Output

- Audio files: `~/Downloads/audio`
- Video files: `~/Downloads/video`

If you set a filename, the extension is added automatically.

---

## Cookie Support

The script auto-detects cookies from supported browsers:
`firefox`, `chrome`, `chromium`, `brave`, `edge`, `opera`, `vivaldi`.

If none are found, it continues without cookies.

---

## TikTok Photo Mode Note

TikTok Photo Mode (`/photo/`) is not reliably supported by yt-dlp.
The script tries a `/photo/` -> `/video/` workaround for audio, but it may fail.

---

## Troubleshooting

- Ensure `ffmpeg` is installed and on your PATH.
- Update yt-dlp if downloads fail:
  ```bash
  python -m pip install -U yt-dlp
  ```
