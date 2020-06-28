import youtube_dl
from pathlib import Path
import os
from termcolor import colored

# commands = sys.argv
# """txt_file contains list of URLs to download"""
# txt_file = commands[1]
# """name of the folder you want to put downloaded songs"""
# new_folder = commands[2]
#
#




def create_path(new_folder):
    """Generates new folder where songs will be placed. If folder with specific name already exists, it will not
    create/overwrite new one """
    full_path = os.path.expanduser('~/Downloads')
    if not new_folder:
        os.makedirs(new_folder)
    absolute_path = f'{full_path}/{new_folder}'
    return absolute_path


a_path = create_path("yt_songs")

ydl_options = {
    'sleep_interval': 2,
    'format': 'bestaudio/best',
    'extract_info': True,
    'quiet': True,
    'outtmpl': f"{a_path}/%(title)s.%(ext)s",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}


# def get_file_size(a_path, title):
#     """Get information of the size of the mp3 file"""
#     byteSize = os.stat(f'{a_path}/{title}.mp3').st_size
#     return colored(f'The size of downloaded file is: {round(byteSize * 0.000001, 1)}MB', 'magenta')


def download_mp3(url_list):
    """Download mp3 songs listed in file"""
    for url in url_list:
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info['title']
            ydl.download([url])


if __name__ == '__main__':
    download_mp3(url_list)
