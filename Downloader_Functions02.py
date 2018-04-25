from __future__ import unicode_literals
import youtube_dl, mutagen, itunespy, os, re, requests
import urllib, ssl, os, glob
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TCON
from mutagen.mp3 import MP3
from PIL import Image
from io import BytesIO

"""
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
    data = {}
    songs = itunespy.search_track(track)
    for song in songs:
        if song.artist_name.lower() == artist.lower():
        #may need additional checks here, I need help with this
            #print(song)
            return song

def get_album(album, artist):
    """
    Returns a list of track objects
    """
    songs = []
    albums = itunespy.search_album(album)
    for album in albums:
        if album.artist_name.lower() == artist.lower():
            return album.get_tracks()

def get_artist(artist):
    """
    Finds all songs affiliated with artist.
    """
    results = []
    artists = itunespy.search_artist(artist)
    albums = artists[0].get_albums()
    for album in albums:
        results.append(album.get_tracks())
    return results


# need to make a function to download a song
# without it being a track file, in case the
# song is not on the iTunes API

def download(songs):
    """
    Downloads songs from youtube.
    Songs must be a list of track objects.
    """
    ydl = get_ydl_obj()

    for song in songs:
        url = get_url(song)
        #id = url.split("watch?v=")[-1]
        ydl.download([url])

        path = glob.glob("YDL/*.mp3")[0]
        set_data(path, song)
        set_cover_art(path, song)
        set_file_path(path, song)

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
                'quiet':True, #suppress messages in command line
                'postprocessors':
                    [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                    }]
                }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    return ydl

def get_url(song):
    """
    Scrapes youtube for a video that has
    track and artist in the name. Returns the
    URL of the best hit.

    Song is a track object.
    """
    query = urllib.parse.quote(song.track_name+" "+song.artist_name)
    url = "https://www.youtube.com/results?search_query=" + query
    soup = get_soup(url)

    search_results = []
    for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
        search_results.append('https://www.youtube.com' + vid['href'])

    return check_url(search_results, song.track_name, song.artist_name)

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

def get_soup(url):
    context = ssl._create_unverified_context()
    req = Request(url, headers={'User-Agent':'Mozilla/5.0'})
    resp = urlopen(req, context=context)
    soup = BeautifulSoup(resp.read(), 'lxml')
    return soup

def set_data(path, song):
    new_song = ID3(path)
    new_song.delete()
    new_song.add(TIT2(encoding=3, text=song.track_name))
    new_song.add(TPE1(encoding=3, text=song.artist_name))
    new_song.add(TALB(encoding=3, text=song.collection_name))
    new_song.add(TCON(encoding=3, text=song.primary_genre_name))
    new_song.save()
    return


    #print(song.artwork_url_100)

def set_cover_art(path, song):
    mutagen_song = MP3(path, ID3=ID3)
    img_url = song.artwork_url_100
    img_save_id = "CoverArt/"+song.collection_name+".jpg"
    img_response = requests.get(img_url)
    img = Image.open(BytesIO(img_response.content))
    img.save(img_save_id)
    mutagen_song.tags.add(APIC(encoding=3,
                           mime="image/jpg",
                           type=3,
                           desc=u"Cover",
                           data=open(img_save_id, "rb").read())
                     )
    mutagen_song.save()
    return

def set_file_path(path, song):
    # make dir with artist name
    new_dir = '"' + 'Fixed/'+song.artist_name+ '/' + '"'
    os.system("mkdir -p %s" % (new_dir))

    # make dir with album name
    new_dir = '"' + 'Fixed/'+song.artist_name+ '/'+ song.collection_name+ '/' +'"'
    os.system("mkdir -p %s" % (new_dir))

    # add song to album dir
    new_path = "Fixed/"+song.artist_name+ "/"+ song.collection_name+ "/"+song.track_name+".mp3"
    new_path = '"'+new_path+'"'
    old_path = '"'+path+'"'
    os.system("mv %s %s" % (old_path, new_path))
    return
