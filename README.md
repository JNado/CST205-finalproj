# Music Downloader

## Description
```
This software allows you to search for any track, album, artist, or any combination of the three using
the iTunes API. Search results can then be downloaded with the Youtube-dl module, as mp3 files. 
Once the file is complete, the ID3 data of that mp3 file is set using mutagen. The aforementioned ID3
data is embedded in the header of a mp3 file and stores information such as artist name, album name, 
track name, genre, cover art, etc. The mp3 file is then stored on your local machine in a file path 
that corresponds to: Fixed/[artist]/[album]/[track].mp3
```

## Required Modules
```
PyQt5 
youtube-dl 
mutagen 
itunespy 
requests 
BeautifulSoup 
os 
re
urllib 
ssl
glob 
pillow
io
sys
subprocess
```

## Directory Structure
```
The following directories must be present in the same directory that you are running this software:
YDL
CoverArt
Fixed
```

## How To Use
```
1) Enter any combination of artist, track, or album names into the search fields, then press "Search."
2) Select all the tracks you want to download by checking the box to the left of each track.
3) Make sure the "YDL" directory is empty before each download phase.
4) Once you are done selecting the tracks, press "Download."
```

## Side Notes
```
1) Do not press the search or download button more than once.
2) Search results are dependent on the iTunes API. Meaning if the song is not in the iTunes store, 
   there will be no search results.
3) Downloads are dependent youtube. Meaning if your song can not be found on Youtube, the download
   will not occur. 
4) Downloads can take some time, so please be patient. 
```
