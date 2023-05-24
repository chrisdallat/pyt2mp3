# pyt2mp3 - Simple YouTube Downloader

### Description

Single file Python3 script for downloading singular youtube video audio tracks, or exctracting a full playlist.

### Dependencies

```
    pip install pytube
    pip install ffmpeg
```

an error may occur in pytube on downloads which resembles this compiler message

```
    pytube.exceptions.RegexMatchError: __init__: could not find match for ^\w+\W
``` 
in this case find the pathway mentioned in the preceeding messages to get to the file
```
    pytube/cipher.py
```
and change line 30 to
```
    var_regex = re.compile(r"^\$*\w+\W")
```
as suggested in the comments here
https://github.com/pytube/pytube/issues/1199

## Usage

The usage of the script is a very simple CLI, running the script with no arguments will, on first use, initialise a 'list.txt' file and a './downloads' folder

Users can copy and paste urls to youtube videos into the list.txt file separated by newlines for download next time the downloader is executed. 

These downloaded audio files will, when converted successfully, be stored in the DOWNLOADS folder. 
```
    python3 downloader.py
```
The user can also chose to download full PUBLIC playlists by inputing 'playlist' as an argument and then inputing the url when prompted. 
```
    python3 downloader.py playlist
```
This will then extract the urls of all the videos in the playlist and write them to list.txt before the program moves to downloading them as before.

The list will auto clear each url as videos are successfully downloaded. if failure occurs that video url will remain in the list for next execution. Manually clearing the list can be done with the argument 'clear'
```
    python3 downloader.py clear
```

To manually delete all the audio files saved in downloads, leaving it empty, can be achieved using the argument 'empty'
```
    python3 downloader.py empty
```

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that do not allow for the waiver of certain rights, you may need to consult with legal counsel before using this license.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND. THE AUTHOR(S) SHALL NOT BE HELD LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE.





