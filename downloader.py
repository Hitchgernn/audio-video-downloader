#!/usr/bin/env python3
import os
import re
import yt_dlp
from urllib.parse import urlsplit, urlunsplit

def clean_url(url: str) -> str:
    p = urlsplit(url.strip())
    return urlunsplit((p.scheme, p.netloc, p.path, "", ""))

def hook(d):
    if d.get("status") == "finished":
        print("\nDone downloading, starting post-processing...")

def get_downloads_subdir(kind: str) -> str:
    base = os.path.join(os.path.expanduser("~"), "Downloads")
    out = os.path.join(base, kind)
    os.makedirs(out, exist_ok=True)
    return out

def sanitize_filename(name: str) -> str:
    name = name.strip()
    if not name:
        return ""
    name = re.sub(r'[\\/:*?"<>|]+', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name

def detect_browser_for_cookies() -> str | None:
    candidates = ["firefox", "chrome", "chromium", "brave", "edge", "opera", "vivaldi"]
    for b in candidates:
        try:
            yt_dlp.cookies.extract_cookies_from_browser(b)
            return b
        except Exception:
            continue
    return None

def get_impersonate_target():
    try:
        from yt_dlp.networking.impersonate import ImpersonateTarget
        return ImpersonateTarget.from_str("chrome")
    except Exception:
        return None

def is_tiktok_photo_mode(url: str) -> bool:
    return "tiktok.com" in url and "/photo/" in url

def try_convert_photo_to_video_url(url: str) -> str:
    return url.replace("/photo/", "/video/")

def download_audio(url: str, output_name: str | None = None):
    original_url = url
    url = clean_url(url)
    outdir = get_downloads_subdir("audio")
    browser = detect_browser_for_cookies()
    impersonate_target = get_impersonate_target()

    if is_tiktok_photo_mode(url):
        print("[WARN] TikTok Photo Mode (/photo/) detected. yt-dlp often can't download these reliably.")
        print("[WARN] Trying workaround: converting /photo/ -> /video/ (may still fail).")
        url = try_convert_photo_to_video_url(url)

    outtmpl = (
        os.path.join(outdir, f"{output_name}.%(ext)s")
        if output_name
        else os.path.join(outdir, "%(title)s.%(ext)s")
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "progress_hooks": [hook],
        "quiet": False,
        **({"cookiesfrombrowser": (browser,)} if browser else {}),
        **({"impersonate": impersonate_target} if impersonate_target else {}),
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ],
    }

    if browser:
        print(f"Using cookies from browser: {browser}")
    else:
        print("No supported browser cookies found. Continuing without cookies.")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n[SUCCESS] Audio saved to ~/Downloads/audio")
    except Exception as e:
        if is_tiktok_photo_mode(clean_url(original_url)):
            print("\n[ERROR] TikTok Photo Mode posts are not reliably supported by yt-dlp right now.")
            print("        Best workaround: repost/export as a normal TikTok video, then download that.")
        raise

def download_video(url: str, output_name: str | None = None):
    original_url = url
    url = clean_url(url)
    outdir = get_downloads_subdir("video")
    browser = detect_browser_for_cookies()
    impersonate_target = get_impersonate_target()

    if is_tiktok_photo_mode(url):
        print("[ERROR] TikTok Photo Mode (/photo/) posts are not reliably downloadable as video via yt-dlp.")
        print("        Best workaround: repost/export as a normal TikTok video.")
        return

    outtmpl = (
        os.path.join(outdir, f"{output_name}.%(ext)s")
        if output_name
        else os.path.join(outdir, "%(title)s.%(ext)s")
    )

    ydl_opts = {
        "format": "bv*+ba/best",
        "merge_output_format": "mp4",
        "outtmpl": outtmpl,
        "noplaylist": True,
        "progress_hooks": [hook],
        "quiet": False,
        **({"cookiesfrombrowser": (browser,)} if browser else {}),
        **({"impersonate": impersonate_target} if impersonate_target else {}),
    }

    if browser:
        print(f"Using cookies from browser: {browser}")
    else:
        print("No supported browser cookies found. Continuing without cookies.")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print("\n[SUCCESS] Video saved to ~/Downloads/video")

def main():
    url = input("Enter TikTok / YouTube link: ").strip()
    if not url:
        print("[ERROR] Empty URL.")
        return

    mode = input("Download (a)udio or (v)ideo? [a/v]: ").strip().lower()
    raw_name = input("Optional filename (Enter to use title): ")
    name = sanitize_filename(raw_name)
    output_name = name if name else None

    try:
        if mode in ("v", "video"):
            download_video(url, output_name=output_name)
        else:
            download_audio(url, output_name=output_name)
    except Exception as e:
        print(f"\n[ERROR] {e}")

if __name__ == "__main__":
    main()
