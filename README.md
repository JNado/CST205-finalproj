# Music Downloader

## Description
```
This software allows you to search for any track, album, artist, or any combonation of the three using the iTunes API. 
Search results can then be used, with the Youtube-dl module, to be downloaded as an MP3 file. Once the file is complete
the ID3 data of the mp3 file is set using Mutagen. ID3 data is embedded in the header of a MP3 file and stores information 
such as artist name, album name, track name, genre, cover art, etc. Then the mp3 file is stored on your local machine in a 
file path that corresponds to: Fixed/[artist]/[album]/[track].mp3

If no match is found on the iTunes API, you can download straight from youtube. However, this method is not recommended due
to the donwloaded mp3 file is not guaranteed to be the song you originally wanted to download. Also, this method does not 
set the ID3 data of the resulting mp3 file due to their not being any data from the iTunes API.
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
1) Enter any combonation of artist, track, or album names into the search fields and hit search button.
2) Select all the tracks you want to download by checking the box to the left of each track.
3) Make sure the directory YDL is empty before each download phase.
4) Once you are done selecting tracks hit donwload.
* Please Note: Do not hit the search or download button more than once, as this will cause two 
search results to be displayed or two sets of downloads to occur.
5) Clear search results in between each download phase to avoid downloading duplicates. Each
time you hit download all checked boxes will be downloaded.
6) If no results are found, NO MATCHES will be displayed. And you have to options: give up, or use the "No Match Download" button.
This button downloads straight from youtube and requires a track name and an artist. Please note this method is not as reliable, nor 
embeds ID3 data into the resulting MP3 file.
```
