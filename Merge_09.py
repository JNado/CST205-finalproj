import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Downloader_Functions import *

class MainGUI(QWidget):
    DOWNLOAD, TRACK, ARTIST, ALBUM, ID = range(5)
    songs = {}
    playlist = []

    def __init__(self):
        """
        Constructs a MainGUI function.
        """
        super().__init__()
        self.initialize_main_gui()
        self.add_artist_line()
        self.add_track_line()
        self.add_album_line()
        self.add_tree_view()
        self.add_search_button()
        self.add_dl_button()
        self.add_playlist_buttons()
        self.finalize_layout()
        """
        Loads the playlist and song data from JSON files for persistence
        """
        self.loadAppData()

    """
    What does this do?
    """
    def closeEvent(self, event):
        self.dumpAppData()

    """
    All functions below are associated with
    adding QWidgets to this MainGUI. And linking
    those QWidgets to their proper functions.
    """
    def initialize_main_gui(self):
        """
        Initializes this MainGUI. Sets the window title,
        geometry, and the main layouts.
        """
        self.setWindowTitle("Music Downloader")
        self.setGeometry(0,0, 800, 494)
        self.mbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbtnbox = QHBoxLayout()

    def add_artist_line(self):
        """
        Adds a QLineEdit for the artist input
        to this MainGUI.
        """
        self.artist_line = QLineEdit()
        self.artist_line.setPlaceholderText("Enter Artist...")
        self.hbox.addWidget(self.artist_line)

    def add_track_line(self):
        """
        Adds a QLineEdit for the track input
        to this MainGUI.
        """
        self.track_line = QLineEdit()
        self.track_line.setPlaceholderText("Enter Track...")
        self.hbox.addWidget(self.track_line)

    def add_album_line(self):
        """
        Adds a QLineEdit for album input
        to this MainGUI.
        """
        self.album_line = QLineEdit()
        self.album_line.setPlaceholderText("Enter Album...")
        self.hbox.addWidget(self.album_line)

    def add_tree_view(self):
        """
        Adds a QTreeView to this MainGUI.
        """
        self.data_view = QTreeView()
        self.data_view.setRootIsDecorated(False)
        self.data_view.setAlternatingRowColors(True)
        self.mbox.addWidget(self.data_view)

        self.data_layout = QHBoxLayout()
        self.data_layout.addWidget(self.data_view)

        self.model = self.create_track_model(self)
        self.data_view.setModel(self.model)

    def create_track_model(self, parent):
        """
        Creates a model to organize the data inside
        the associated QTreeView.
        Adds the header data: Donwload, Track, Artist, Album.
        """
        model = QStandardItemModel(0, 5, parent)
        model.setHeaderData(self.DOWNLOAD, Qt.Horizontal, "Download")
        model.setHeaderData(self.TRACK, Qt.Horizontal, "Track")
        model.setHeaderData(self.ARTIST, Qt.Horizontal, "Artist")
        model.setHeaderData(self.ALBUM, Qt.Horizontal, "Album")
        model.setHeaderData(self.ID, Qt.Horizontal, "ID")
        return model

    def add_search_button(self):
        """
        Adds a QPushButton to this MainGUI to
        search against user input.
        """
        self.search_button = QPushButton("Search")
        self.search_button.setFixedWidth(95)
        self.search_button.clicked.connect(self.search_button_push)
        self.hbtnbox.addWidget(self.search_button)

    def add_dl_button(self):
        """
        Adds a QPushButton to this MainGUI to
        download checked boxes after the search
        has taken place.
        """
        self.dl_button = QPushButton("Download")
        self.dl_button.setFixedWidth(95)
        self.dl_button.clicked.connect(self.download_button_push)
        self.hbtnbox.addWidget(self.dl_button)

    def add_playlist_buttons(self):
        """
        Creates a QPushButton to add songs to stored playlist
        """
        self.add_playlist_button = QPushButton("Add To Playlist")
        self.remove_playlist_button = QPushButton("Remove From Playlist")
        self.view_playlist_button = QPushButton("View Playlist")
        self.play_playlist_button = QPushButton("Play Playlist")
        self.add_playlist_button.clicked.connect(self.add_playlist_button_push)
        self.remove_playlist_button.clicked.connect(self.remove_playlist_button_push)
        self.view_playlist_button.clicked.connect(self.view_playlist_button_push)
        self.play_playlist_button.clicked.connect(self.play_playlist_button_push)
        self.hbtnbox.addWidget(self.add_playlist_button)
        self.hbtnbox.addWidget(self.remove_playlist_button)
        self.hbtnbox.addWidget(self.view_playlist_button)
        self.hbtnbox.addWidget(self.play_playlist_button)

    def finalize_layout(self):
        """
        Finalizes this MainGUI by setting the
        main layouts.
        """
        self.mbox.addLayout(self.hbtnbox)
        self.mbox.addLayout(self.hbox)
        self.setLayout(self.mbox)

    """
    All functions below are the functions
    that take place when a button is pushed.
    """
    def add_playlist_button_push(self):
        for item in range(self.model.rowCount()):
            if self.model.item(item).checkState():
                self.playlist.append(self.model.data(self.model.index(item, 4)))

    def remove_playlist_button_push(self):
        for item in range(self.model.rowCount()):
            if self.model.item(item).checkState():
                hold = self.model.data(self.model.index(item, 4))
                if hold in self.playlist:
                    self.playlist.remove(hold)

    def view_playlist_button_push(self):
        hold = ''
        for item in self.playlist:
            try:
                hold += self.songs[str(item)] + '\n'
            except:
                hold += ''

        QMessageBox.about(self, 'Playlist Songs', hold)

    def play_playlist_button_push(self):
        return
        #self.dumpAppData()
        #self.loadAppData()

    def add_track_to_box(self,track):
        """
        track is a track object
        """
        self.model.insertRow(0)
        self.check_box = QStandardItem("")
        self.check_box.setCheckable(True)
        self.check_box
        self.model.setItem(0,0,self.check_box)
        self.model.setData(self.model.index(0, self.TRACK), track.track_name)
        self.model.setData(self.model.index(0, self.ARTIST), track.artist_name)
        self.model.setData(self.model.index(0, self.ALBUM), track.collection_name)
        self.model.setData(self.model.index(0, self.ID), track.track_id)
        return

    def add_track_list(self, track_list):
        added = []
        for track in track_list:
            if(track.track_id not in added):
                self.add_track_to_box(track)
                added.append(track.track_id)
        return

    def search_button_push(self):
        #clear all data first
        self.model.removeRows(0, self.model.rowCount())

        artist = self.artist_line.text()
        track = self.track_line.text()
        album = self.album_line.text()

        # no fields are entered
        if(not artist and not track and not album):
            #self.add_no_match_to_box()
            QMessageBox.about(self, "Search Failed",
                            "Sorry, no results for your search.")

        # only artist entered
        elif(artist and not track and not album):
            try:
                results = get_artist(artist)
                self.add_track_list(results)
            except:
                QMessageBox.about(self, "Search Failed",
                                "Sorry, no results for your search.")

        # only track entered
        elif(track and not artist and not album):
            try:
                results = itunespy.search_track(track)
                self.add_track_list(results)
            except:
                QMessageBox.about(self, "Search Failed",
                                "Sorry, no results for your search.")

        # only album entered
        elif(album and not artist and not track):
            try:
                results = get_album_no_artist(album)
                self.add_track_list(results)
            except:
                QMessageBox.about(self, "Search Failed",
                                "Sorry, no results for your search.")

        # only track and artist entered
        elif(track and artist):
            try:
                result = get_track(track, artist)
                self.add_track_list([result])
            except:
                QMessageBox.about(self, "Search Failed",
                                "Sorry, no results for your search.")

        # only album and artist entered
        elif(album and artist):
            try:
                results = get_album(album, artist)
                self.add_track_list(results)
            except:
                QMessageBox.about(self, "Search Failed",
                                "Sorry, no results for your search.")

        # only track and album
        elif(track and album):
            try:
                result = get_track_on_album(track, album)
                self.add_track_list([result])
            except:
                QMessageBox.about(self, "Search Failed",
                                "Sorry, no results for your search.")

    def download_button_push(self):
        try:
            for row in range(self.model.rowCount()):
                if self.model.item(row).checkState():
                    song = []
                    for column in range(1, self.model.columnCount()):
                        index = self.model.index(row, column)
                        song.append(str(self.model.data(index)))
                    track = get_track(song[0], song[1])
                    download([track])
        except:
            QMessageBox.about(self, "Download Failed",
                            "Sorry, could not locate your song on youtube.")

    """
    Load functions described earlier in the python file
    """
    def dumpAppData(self):
        try:
            if (len(self.songs) != 0):
                hold = json.dumps(self.songs)
            else:
                hold = ' '

            hold += '?'

            if (len(self.playlist) != 0):
                hold += json.dumps(self.playlist)
            else:
                hold += ' '

            with open('AppData.json', 'w') as outfile:
                outfile.write(hold)
        except:
            QMessageBox.about(self, "Error", "Error")

    def loadAppData(self):
        try:
            with open('AppData.json', 'r') as infile:
                hold = infile.read()

            hold1, hold2 = hold.split('?')
            self.songs = json.loads(hold1)
            self.playlist = json.loads(hold2)

        except:
            QMessageBox.about(self ,"User Info", "No previous data exists.")

"""
Run:
"""
app = QApplication(sys.argv)
gui = MainGUI()
gui.show()
sys.exit(app.exec_())
