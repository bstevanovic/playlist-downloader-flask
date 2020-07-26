import youtube_dl
import os
import sys


def create_path(new_folder):
    """Generates new folder where songs will be placed. If folder with specific name already exists, it will not
    create/overwrite new one """
    full_path = os.path.expanduser('~/Downloads')
    if not new_folder:
        os.makedirs(new_folder)
    absolute_path = f'{full_path}/{new_folder}'
    return absolute_path


a_path = create_path("yt_songs")


def os_platform():
    """Get information about platform and set path to the ffmpeg """
    platform = sys.platform
    if 'win' in platform:
        current_platform = 'win-platform/ffmpeg.exe'
    elif platform == 'darwin':
        current_platform = 'mac-platform/ffmpeg.exe'
    elif platform == 'linux':
        current_platform = '/usr/bin/ffmpeg'

    return current_platform


ffmpeg_path = os_platform()

ydl_options = {
    'sleep_interval': 2,
    'format': 'bestaudio/best',
    'extract_info': True,
    'quiet': True,
    'outtmpl': f"{a_path}/%(title)s.%(ext)s",
    'ffmpeg_location': ffmpeg_path,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


def get_file_size(a_path, title):
    """Get information of the size of the mp3 file"""
    byteSize = os.stat(f'{a_path}/{title}.mp3').st_size
    return f'Size: {round(byteSize * 0.000001, 1)}MB'


titles = []


def download_mp3(url_list):
    """Download mp3 songs listed in file; convert list to sets; edd title and file size to the tiles list"""
    url_list = set(url_list)
    for url in url_list:
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            ydl.download([url])
            size = get_file_size(a_path, title)
            titles.append(f'{title} - {size}')


if __name__ == '__main__':
    download_mp3(url_list)
