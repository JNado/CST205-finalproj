# Music Downloader

## Description
```
This software allows you to search for any track, album, artist, or any combination of the three using
the iTunes API. Search results can then be downloaded with the Youtube-dl module, as mp3 files. 
Once the file is complete, the ID3 data of that mp3 file is set using mutagen. The aforementioned ID3
data is embedded in the header of a mp3 file and stores information such as artist name, album name, 
track name, genre, cover art, etc. The mp3 file is then stored on your local machine in a file path 
that corresponds to: Fixed/[artist]/[album]/[track].mp3

The user can also create, edit, and play playlists. m3u files are used to store mp3 file paths, these m3u 
files can then be played using your operating system's default music browser.
```

## Required Modules
```
Use: pip install [module]

youtube-dl
mutagen
itunespy
requests
future
beautifulsoup4
pillow
pyqt5

Below are in the python standard library.
os (standard)
re (standard)
urllib (standard)
io(standard) 
```

## Directory Structure
```
The following directories must be present in the same directory that you are running this software:

YDL
CoverArt
Fixed
Playlists
```

## How To Use The Downloader
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
3) Downloads are dependent on Youtube. Meaning if your song can not be found on Youtube, the download
   will not occur. 
4) Downloads can take some time, so please be patient.
5) For Windows users: Youtube-DL requires FFMPeg to work, so follow the instructions on the install page very closely, such as having the                   directory information be correct as well. Else FFMPeg will not work and the program itself will not function correctly.

Complete instructions can be found at this URL:
http://adaptivesamples.com/how-to-install-ffmpeg-on-windows/
```

## How to Create, Edit, and Play Playlists
```
1) Press the "edit playlists" in the main GUI.
2) In this secondary GUI press "view songs" to get a list
of all the music you have downloaded. 
3) Check all the boxes you want to add to a playlist.
4) Enter a name of a playlist (if playlist doesn't exist
one will be created. If one exists, it will be edited.)
5) If you want to delete songs from a playlist
   - first click view playlist with the playlist name entered
   - check boxes of tracks you wish to delete
   - click "delete songs"
6) To play a playlist
   - enter name of playlist
   - click "play playlist"
   - this will open your operating system's default music player
      - if you are on mac the playlists will automatically be added to iTunes 
```

## What's to Come
```
In the future we would like to incorporate better searchfunctions, inside the
Downloader_Functions module. We would,also like to incorporate a check in order
to make sure the user is downloading the correct song from youtube. Right now we 
are just returning the first url from a list, we are not checking their titles, or 
meta data to make sure it is the actual song we want to download.

We would also like to incorporate the ability to alphabetize your search results, or
playlist results, when you click on the data header. Meaning, if you click on track, all
results will be alphabetized according to track names. 

It would also be nice to include song previews in search results, so you know you are
trying to download the correct track.
```

## Give Credit Where Credit is Due
```
1) Our search functions rely heavily on the
itunespy module, full documentation here: https://github.com/spaceisstrange/itunespy
That module allows us to search the itunes API and returns us a list of track objects,
it was our job to search through that list and find the correct data.

2) Our downloading function is all the youtube-dl module.
Full documentation: https://rg3.github.io/youtube-dl/
This is the work horse of our program.

3) We also relied heavily on BeautifulSoup to scrape Youtube to get the
url to download. Without a url we can not use youtube-dl.
Full documentation here: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

4) The mutagen module allowed us to set MP3 metadata, so when you played the songs
in your default music browser, all info and cover art was present and everything was organized.
Full documentation here: https://mutagen.readthedocs.io/en/latest/
```

## Disclaimer
```
This software is for educational purposes only, and should not be used to infringe the copyrights
of artists, Youtube, or iTunes. We are not responsible for others using our software, nor have we distributed
our software to any individuals to be used to infringe copyrights. We have not stored copyrighted data on any server
nor distributed any copyrighted data for our own gain.

The sole purpose of our software is to allow us to learn how to incorporate many Python modules into one project.
And explore how to use Python modules.

Usage of this software and all provided products is subject to compliance of your countries legal permissions, 
if your local laws do not permit downloads and audio conversions of online videos you are not allowed to use this
service. You are also not permitted to use this utility to infringe any sort of copyright by downloading multimedia
content which you don't have rights to use or is not open-source. We expressly point out that copyrighted material, 
ie videos, sound files, photographs, etc. may only be reproduced, distributed and processed with the consent of the
copyright holder. Before downloading a file, please inquire whether this is legal. Otherwise, you may face consequences
regarding civil and criminal conviction.
```
