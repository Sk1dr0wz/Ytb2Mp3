import yt_dlp
from moviepy.editor import VideoFileClip
import os
import re

def sanitize_filename(filename):
    # Remove or replace characters that are invalid in Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_youtube_video(url, download_path='downloads'):
    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': 'C:/ffmpeg/bin'  # Specify the path to ffmpeg
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        video_title = sanitize_filename(info_dict.get('title', ''))
        video_path = os.path.join(download_path, video_title + '.mp3')
    return video_path

def main(url):
    download_path = 'downloads'
    mp3_path = download_youtube_video(url, download_path)
    print(f'Video downloaded and converted to MP3: {mp3_path}')

if __name__ == "__main__":
    youtube_url = input("Enter the YouTube video URL: ")
    main(youtube_url)
