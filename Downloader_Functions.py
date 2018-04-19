from __future__ import unicode_literals
import youtube_dl
import urllib, ssl, os, glob
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from SongScrub import *

"""
Group 7

This file contains functions to search the itunes API, for a single
track, or an album. This file also contains functions to download
those search results.
"""
def get_track(track, artist):
    """
    Returns a JSON object representation of our found song.
    """
    data = {}
    songs = itunespy.search_track(track)
    for song in songs:
        if song.artist_name.lower() == artist.lower():
        #may need additional checks here, I need help with this
            #print(song)
            return song

def get_album(album, artist):
    """
    returns all the songs off of given album
    """
    songs = []
    albums = itunespy.search_album(album)
    for album in albums:
        if album.artist_name.lower() == artist.lower():
            return album.get_tracks()

def download(songs):
    """
    Songs is a list, so if you want to download one
    song you must use: [song]

    Uses youtube-dl to donwload a song
    """
    ydl = get_ydl_obj()
    #scrubber = SongScrub()
    for song in songs:
        url = get_url(song.track_name, song.artist_name)
        #id = url.split("watch?v=")[-1]
        ydl.download([url])
        path = glob.glob("YDL/*.mp3")[0]

        #scrubber.set_data(path, album_tracks[track])
        #scrubber.set_cover_art(path, album_tracks[track])
        #scrubber.set_file_path(path, album_tracks[track])

def get_ydl_obj():
    """
    Returns a youtube_dl object with the specified
    parameters
    """
    #can we save as a custom string
    #is there anymore options
    ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'YDL/%(id)s.%(ext)s',
                'nocheckcertificate': True,
                'noplaylist' : True,
                'postprocessors':
                    [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }]
                }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    return ydl

def get_url(track, artist):
    """
    Searches youtube for a song that best matches
    text. Right now there is no good way to make
    sure search_results[1] is the song we want.
    Returns a youtube url for youtube-dl to take advantage of.
    """
    query = urllib.parse.quote(track + " " + artist)
    url = "https://www.youtube.com/results?search_query=" + query
    soup = get_soup(url)

    search_results = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        search_results.append('https://www.youtube.com' + vid['href'])

    return check_url(search_results, track, artist)

def get_soup(url):
    context = ssl._create_unverified_context()
    req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    resp = urlopen(req, context=context)
    soup = BeautifulSoup(resp.read(), 'lxml')
    return soup

def check_url(url_list, track, artist):
    artist = re.sub('[^0-9a-zA-Z ]+', '', artist.lower())
    track = re.sub('[^0-9a-zA-Z ]+', '', track.lower())
    for url in url_list:
        soup = get_soup(url)
        for title in soup.findAll(attrs={'class' : 'watch-title'}):
            cur_title = re.sub('[^0-9a-zA-Z ]+', '', title["title"].lower())
            if ((track == cur_title or track in cur_title)
            and artist in cur_title):
                #need to check if not music video
                return url
