import os
import sys
import subprocess
import re
from pytube import YouTube
from pytube import Playlist

DOWNLOADS = './downloads'
CWD = '.'

def extract_from_list(link):
    try:
        yt = YouTube(link, use_oauth=True, allow_oauth_cache=True)
        yt._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
    except:
        print("Invalid link")
        return -1

    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path=CWD)

    if not out_file:
        print("Download failed for: ", yt.title)
        return -1
   
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    final = yt.title + ".mp3" 

    convert_final(os.path.join(CWD, new_file), os.path.join(DOWNLOADS, final))
    
    os.remove(new_file)

    print(yt.title + " has been successfully downloaded!")

    return 0

def extract_playlist(link):
    try:
        playlist = Playlist(link)
    except:
        print("Invalid link")
        return -1
    
    playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")

    lines = []
    for video in playlist.videos:
        lines.append(video.watch_url + "\n")
    
    update_list(lines)


def convert_final(input_file, output_file):
    subprocess.run([
        'ffmpeg',
        '-i', input_file,
        output_file
    ])

def empty_downloads():
    for file in os.listdir("./downloads"):
        os.remove(os.path.join("./downloads", file))
    print("Downloads folder has been emptied")

def update_list(lines):
    with open('list.txt', 'w') as f:
        for line in lines:
            if "$delete$" not in line:
                f.write(line)
    print("Download list has been updated")

def clear_list():
    with open('list.txt', 'w') as f:
        f.write("")
        print("Download list has been cleared")

def program():
    with open('list.txt') as f:
        lines = f.readlines()
        for line in lines:
            res = extract_from_list(line)
            if res == 0:
                lines.remove(line)
            else: 
                break
    update_list(lines)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        program()
    elif len(sys.argv) == 2 and sys.argv[1] == "clear":
        clear_list()
    elif len(sys.argv) == 2 and sys.argv[1] == "empty":
        empty_downloads()
    elif len(sys.argv) == 2 and sys.argv[1] == "playlist":
        playlist = input("Enter playlist link: ")
        extract_playlist(playlist)
        program()
    else:
        print("Invalid arguments")
        exit()






