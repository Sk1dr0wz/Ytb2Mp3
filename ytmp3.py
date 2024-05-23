import yt_dlp
from moviepy.editor import VideoFileClip
import os
import re
import logging
import coloredlogs

# Setting up logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
coloredlogs.install(level='DEBUG')

def sanitize_filename(filename):
    # Remove or replace characters that are invalid in Windows filenames
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_youtube_video(url, download_path='downloads'):
    logger = logging.getLogger('download_youtube_video')

    # Create the download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)
        logger.debug(f'Created download directory: {download_path}')

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

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.debug(f'Starting download for URL: {url}')
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            video_title = sanitize_filename(info_dict.get('title', ''))
            video_path = os.path.join(download_path, video_title + '.mp3')
            logger.debug(f'Downloaded video title: {video_title}')
        return video_path
    except Exception as e:
        logger.error(f'Error downloading video: {e}')
        raise

def main(url):
    logger = logging.getLogger('main')

    download_path = 'downloads'
    try:
        logger.info(f'Starting download and conversion for URL: {url}')
        mp3_path = download_youtube_video(url, download_path)
        logger.info(f'Video downloaded and converted to MP3: {mp3_path}')
    except Exception as e:
        logger.error(f'Failed to download and convert video: {e}')

if __name__ == "__main__":
    youtube_url = input("Enter the YouTube video URL: ")
    main(youtube_url)
