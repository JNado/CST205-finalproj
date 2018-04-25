import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Downloader_Functions import *

class MainGUI(QWidget):
    DOWNLOAD, TRACK, ARTIST, ALBUM = range(4)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Downloader")

        # set the layout
        self.mbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        # create line edit for artist
        self.artist_line = QLineEdit()
        self.artist_line.setPlaceholderText("Enter Artist...")
        self.hbox.addWidget(self.artist_line)

        # create line edit for track
        self.track_line = QLineEdit()
        self.track_line.setPlaceholderText("Enter Track...")
        self.hbox.addWidget(self.track_line)

        # create line edit for album
        self.album_line = QLineEdit()
        self.album_line.setPlaceholderText("Enter Album...")
        self.hbox.addWidget(self.album_line)

        # add QTree view
        self.data_box = QGroupBox("Results")
        self.data_view = QTreeView()
        self.data_view.setRootIsDecorated(False)
        self.data_view.setAlternatingRowColors(True)
        self.mbox.addWidget(self.data_view)

        self.data_layout = QHBoxLayout()
        self.data_layout.addWidget(self.data_view)
        self.data_box.setLayout(self.data_layout)

        self.model = self.create_track_model(self)
        self.data_view.setModel(self.model)

        # save the buttons in this layout
        self.hbtnbox = QHBoxLayout()
        #create search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_button_push)
        self.hbtnbox.addWidget(self.search_button)

        # create dl button
        self.dl_button = QPushButton("Download")
        self.dl_button.clicked.connect(self.search_button_push)
        self.hbtnbox.addWidget(self.dl_button)

        # create strait from youtube dl button
        self.yt_button = QPushButton("Download (No iTunes API)")
        #self.search_button.clicked.connect(self.dl_btn_push)
        self.hbtnbox.addWidget(self.yt_button)

        self.mbox.addLayout(self.hbtnbox)

        #add hbox to mbox and finalize
        self.mbox.addLayout(self.hbox)
        self.setLayout(self.mbox)

    def create_track_model(self, parent):
        model = QStandardItemModel(0, 4, parent)
        model.setHeaderData(self.DOWNLOAD, Qt.Horizontal, "Download")
        model.setHeaderData(self.TRACK, Qt.Horizontal, "Track")
        model.setHeaderData(self.ARTIST, Qt.Horizontal, "Artist")
        model.setHeaderData(self.ALBUM, Qt.Horizontal, "Album")
        return model

    def add_track_to_box(self,track):
        """
        track is a track object
        """
        self.model.insertRow(0)
        check_box = QStandardItem("")
        check_box.setCheckable(True)
        #self.model.appendRow(check_box)
        self.model.setItem(0,0,check_box)
        self.model.setData(self.model.index(0, self.TRACK), track.track_name)
        self.model.setData(self.model.index(0, self.ARTIST), track.artist_name)
        self.model.setData(self.model.index(0, self.ALBUM), track.collection_name)
        return

    def add_no_match_to_box(self):
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, self.TRACK), "NO MATCHES")
        self.model.setData(self.model.index(0, self.ARTIST), "NO MATCHES")
        self.model.setData(self.model.index(0, self.ALBUM), "NO MATCHES")


    def search_button_push(self):
        artist = self.artist_line.text()
        track = self.track_line.text()
        album = self.album_line.text()

        # no fields are entered
        if(not artist and not track and not album):
            self.add_no_match_to_box()
            return

        # only artist entered
        if(artist and not track and not album):
            try:
                used = []
                results = get_artist(user_artist)
                for l in results:
                    for track in l:
                        self.add_track_to_box(track)
                return
            except:
                self.add_no_match_to_box()
            return

        # only track entered
        if(track and not artist and not album):
            try:
                songs = itunespy.search_track(track)
                for song in songs:
                    self.add_track_to_box(song)
                return
            except:
                self.add_no_match_to_box()
            return

        # only album entered
        if(album and not artist and not track):
            #should we print out just the album name and artist,
            #or every song on every album
            try:
                albums = itunespy.search_album(album)
                for album in albums:
                    tracks = album.get_tracks()
                    for track in tracks:
                        self.add_track_to_box(track)
            except:
                self.add_no_match_to_box()

        # only track and artist entered
        if(track and artist):
            try:
                result = get_track(track, artist)
                self.add_track_to_box(result)
                return
            except:
                self.add_no_match_to_box()
                return
            return

        # only album and artist entered
        if(album and artist):
            try:
                results = get_album(album, artist)
                for result in results:
                    self.add_track_to_box(result)
            except:
                self.add_no_match_to_box()

        # only track and albums

        #all three

"""
Test:
"""
app = QApplication(sys.argv)
#app.setStyle("fusion")
gui = MainGUI()
gui.show()
sys.exit(app.exec_())
