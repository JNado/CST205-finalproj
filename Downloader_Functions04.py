from __future__ import unicode_literals
import youtube_dl, mutagen, itunespy, os, re, requests
import urllib, ssl, glob
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON
from mutagen.mp3 import MP3
from PIL import Image
from io import BytesIO


"""
Torin Foss | tfoss@csumb.edu | 2018

Download:
Contains functions to download songs from youtube.
Songs must be present on youtube, as well as from
the iTunes store, as the song information is filled
with data from the iTunes API.
"""

def get_track(track, artist):
    """
    Returns a track object from the itunespy module
    """
    songs = itunespy.search_track(track)
    for song in songs:
        if song.artist_name.lower() == artist.lower():
            return song

def get_album(album, artist):
    """
    Returns a list of track objects from the
    album made by artist.
    """
    albums = itunespy.search_album(album)
    for album in albums:
        if album.artist_name.lower() == artist.lower():
            return album.get_tracks()

def get_album_no_artist(album):
    """
    Finds all albums with the name album. Returns
    a list of track objects of each album.
    """
    songs = []
    albums = itunespy.search_album(album)
    for album in albums:
        for track in album.get_tracks():
            songs.append(track)
    return songs

def get_track_on_album(track, album):
    """
    Returns a single track object off album.
    """
    for song in itunespy.search_track(track):
        if song.collection_name.lower() == album.lower():
            return song

def get_artist(artist):
    """
    Finds all songs affiliated with artist.
    """
    results = []
    artists = itunespy.search_artist(artist)
    albums = artists[0].get_albums()
    for album in albums:
        for song in album.get_tracks():
            results.append(song)
    return results

def download(songs):
    """
    Downloads songs from youtube.
    Songs must be a list of track objects.
    """
    ydl = get_ydl_obj()
    for song in songs:
        url = get_url(song.track_name, song.artist_name)
        ydl.download([url])
        path = glob.glob("YDL/*.mp3")[0]
        set_data(path, song)
        set_cover_art(path, song)
        set_file_path(path, song)

def download_no_itunes(track, artist):
    """
    Downloads straight from youtube without checking
    the iTunes API. This method does not add ID3 data
    to the MP3 file, nor ensures you are downloading
    the exact song you want.
    """
    ydl = get_ydl_obj()
    url = get_url(track, artist)
    ydl.download([url])
    path = glob.glob("YDL/*.mp3")[0]
    new_dir = '"' + 'Fixed/'+artist+ '/' + '"'
    os.system('mkdir -p %s' % (new_dir))
    os.system("mv " + path + " " + new_dir + track + ".mp3")

def get_ydl_obj():
    """
    Returns a youtube_dl object with
    the specified parameters.
    """
    ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'YDL/%(id)s.%(ext)s',
                'nocheckcertificate': True,
                'noplaylist' : True,
                'quiet': True, #suppress messages in command line
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
    Scrapes youtube for a video that has
    track and artist in the name. Returns the
    first result from the search results.
    """
    query = urllib.parse.quote(track+" "+artist)
    url = "https://www.youtube.com/results?search_query=" + query
    soup = get_soup(url)
    search_results = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        search_results.append('https://www.youtube.com' + vid['href'])
    return search_results[0]

def get_soup(url):
    """
    Returns a BeautifulSoup object.
    A helper function for get_url()
    """
    context = ssl._create_unverified_context()
    req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    resp = urlopen(req, context=context)
    soup = BeautifulSoup(resp.read(), 'lxml')
    return soup

def set_data(path, song):
    """
    Sets the ID3 header data of the MP3 file
    foud at the end of path.
    """
    new_song = ID3(path)
    new_song.delete()
    new_song.add(TIT2(encoding=3, text=song.track_name))
    new_song.add(TPE1(encoding=3, text=song.artist_name))
    new_song.add(TALB(encoding=3, text=song.collection_name))
    new_song.add(TCON(encoding=3, text=song.primary_genre_name))
    new_song.save()
    return

def set_cover_art(path, song):
    """
    Embeds a jpg file into the ID3 header data
    of the mp3 file found at the end of path.
    """
    mutagen_song = MP3(path, ID3=ID3)
    img_url = song.artwork_url_100
    img_save_id = "CoverArt/"+song.collection_name+".jpg"
    img_response = requests.get(img_url)
    img = Image.open(BytesIO(img_response.content))
    img.save(img_save_id)
    mutagen_song.tags.add(APIC(encoding=3, mime="image/jpg",
                           type=3, desc=u"Cover",
                           data=open(img_save_id, "rb").read()))
    mutagen_song.save()
    return

def set_file_path(path, song):
    """
    Sets the file path of song to:
    YDL/[artist]/[album]/[track].mp3
    In order to easily be found.
    """
    # make dir with artist name
    new_dir = '"' + 'Fixed/'+song.artist_name+ '/' + '"'
    os.system("mkdir -p %s" % (new_dir.replace(" ", "_")))

    # make dir with album name
    new_dir = '"' + 'Fixed/'+song.artist_name+ '/'+ song.collection_name+ '/' +'"'

    os.system("mkdir -p %s" % (new_dir.replace(" ", "_")))

    # add song to album dir
    new_path = "Fixed/"+song.artist_name+ "/"+ song.collection_name+ "/"+song.track_name+".mp3"
    new_path = '"'+new_path+'"'
    old_path = '"'+path+'"'
    os.system("mv %s %s" % (old_path, new_path.replace(" ", "_")))
    return

#songs = get_album("future development", 'del the funky homosapien')
#download(songs)
