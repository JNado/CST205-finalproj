# Music Downloader

## Description
```
This software allows you to search for any track, album, artist, or any combination of the three using
the iTunes API. Search results can then be downloaded with the Youtube-dl module, as mp3 files. 
Once the file is complete, the ID3 data of that mp3 file is set using mutagen. The aforementioned ID3
data is embedded in the header of a mp3 file and stores information such as artist name, album name, 
track name, genre, cover art, etc. The mp3 file is then stored on your local machine in a file path 
that corresponds to: Fixed/[artist]/[album]/[track].mp3

If no match is found on the iTunes API, you can download straight from Youtube. However, this method is
not recommended due to the fact that the downloaded mp3 file is not guaranteed to be the song you originally 
wanted to download. This method does not set the ID3 data for the resulting mp3 file due to the 
lack of necessary data that could otherwise be retrieved with the iTunes API.
```

## Required Modules
```
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
PyQt5 
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
* Please Note: Do not press the "Search" or "Download" button more than once, as this will cause the  
current search results to be displayed on top of the previous results, or two sets of downloads to occur.
5) Clear search results in between each download phase to avoid downloading duplicates. Each
time "Download" is pressed, anything that is checked will be download.
6) If no results are found, NO MATCHES will be displayed. From there, you have two options: to give up, 
or to use the "No Match Download" button. This button downloads straight from Youtube and requires a track name
and an artist in the search fields. Please note this method is not as reliable, nodoes it embed the ID3 data 
into the resulting MP3 file.
```
