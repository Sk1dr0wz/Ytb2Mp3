import yt_dlp
import os
import re
import logging
import coloredlogs
from colorama import Fore, Style, init

init(autoreset=True)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
coloredlogs.install(level='DEBUG')

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

def download_youtube_video(url, download_path='downloads'):
    logger = logging.getLogger('download_youtube_video')

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
        'ffmpeg_location': 'C:/ffmpeg/bin'  
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

def download_youtube_video_as_video(url, download_path='downloads'):
    logger = logging.getLogger('download_youtube_video_as_video')

    if not os.path.exists(download_path):
        os.makedirs(download_path)
        logger.debug(f'Created download directory: {download_path}')

    ydl_opts = {
        'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best[height<=1080]',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'merge_output_format': 'mp4',
        'ffmpeg_location': 'C:/ffmpeg/bin'  
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.debug(f'Starting download for URL: {url}')
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            video_title = sanitize_filename(info_dict.get('title', ''))
            video_path = os.path.join(download_path, video_title + '.mp4')
            logger.debug(f'Downloaded video title: {video_title}')
        return video_path
    except Exception as e:
        logger.error(f'Error downloading video: {e}')
        raise

def main(url, option):
    logger = logging.getLogger('main')

    download_path = 'downloads'
    try:
        if option == '1':
            logger.info(f'Starting download and conversion to MP3 for URL: {url}')
            mp3_path = download_youtube_video(url, download_path)
            logger.info(f'Video downloaded and converted to MP3: {mp3_path}')
        elif option == '2':
            logger.info(f'Starting video download for URL: {url}')
            video_path = download_youtube_video_as_video(url, download_path)
            logger.info(f'Video downloaded: {video_path}')
        else:
            logger.error(f'Invalid option: {option}')
    except Exception as e:
        logger.error(f'Failed to download: {e}')

if __name__ == "__main__":
    print(f"""{Style.BRIGHT + Fore.RED}

███████╗██╗  ██╗ ██╗██████╗ ██████╗  ██████╗ ██╗    ██╗███████╗
██╔════╝██║ ██╔╝███║██╔══██╗██╔══██╗██╔═████╗██║    ██║╚══███╔╝
███████╗█████╔╝ ╚██║██║  ██║██████╔╝██║██╔██║██║ █╗ ██║  ███╔╝
╚════██║██╔═██╗  ██║██║  ██║██╔══██╗████╔╝██║██║███╗██║ ███╔╝
███████║██║  ██╗ ██║██████╔╝██║  ██║╚██████╔╝╚███╔███╔╝███████╗
╚══════╝╚═╝  ╚═╝ ╚═╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚══╝╚══╝ ╚══════╝

{Fore.RED}════════════════════════════════════════════════════════════════════════════════════════
{Style.BRIGHT + Fore.YELLOW}{"Coded by sk1dr0wz".center(80)}
{"Youtube 2 Mp3".center(80)}
{"Copyright By: Hamba Abdi".center(80)}
{"pip install -r requirements.txt".center(80)}
{Fore.RED}════════════════════════════════════════════════════════════════════════════════════════""")

    youtube_url = input("Enter the YouTube video URL: ")
    print("Choose an option:")
    print("1. Download as MP3")
    print("2. Download as Video (720p to 1080p)")
    option = input("Enter the option (1 or 2): ")
    main(youtube_url, option)
