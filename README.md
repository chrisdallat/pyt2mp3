# pyt2mp3 - Simple YouTube Downloader

### Description

Single file Python3 script for downloading singular youtube video audio tracks, or exctracting a full playlist in 128kbps mp3 format.

If any age restrictions prevent download, authentication tools have been built in so authentication only needs to take place once in the session on the API to allow downloads to continue unhindered.

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

## Errors

When errors with download occur for whatever reason the undownloaded urls will remain in the list.txt so users can reattempt to download without confusion on what has been downloaded or not. if urls were manually entered then they can be reinspected for errors. Errors will print to the terminal for the most common issues so refer to the CLI for 'DOWNLOADER: ------'  

NOTE: on MacOS when songs are imported to Apple Music/Itunes the duration has doubled, but can be rectified by selecting the files, and doing 
```
    File > Convert > Create MP3 Version
```

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this software, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.

In jurisdictions that do not allow for the waiver of certain rights, you may need to consult with legal counsel before using this license.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND. THE AUTHOR(S) SHALL NOT BE HELD LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE.





