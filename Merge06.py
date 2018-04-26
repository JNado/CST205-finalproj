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
        self.setGeometry(0,0, 800, 494)
        #self.setFixedSize(self.size()) # good idea?

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
        self.search_button.setFixedWidth(95)
        self.search_button.clicked.connect(self.search_button_push)
        self.hbtnbox.addWidget(self.search_button)

        # create dl button
        self.dl_button = QPushButton("Download")
        self.dl_button.setFixedWidth(95)
        self.dl_button.clicked.connect(self.download_button_push)
        self.hbtnbox.addWidget(self.dl_button)

        # create straight from youtube dl button
        self.yt_button = QPushButton("No Match Download")
        self.yt_button.setFixedWidth(150)
        self.yt_button.clicked.connect(self.yt_button_push)
        self.hbtnbox.addWidget(self.yt_button)

        self.mbox.addLayout(self.hbtnbox)

        #add hbox to mbox
        self.mbox.addLayout(self.hbox)

        #add progress bar
        self.pbar = QProgressBar()
        self.mbox.addWidget(self.pbar)
        #finalize
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
        self.check_box = QStandardItem("")
        self.check_box.setCheckable(True)
        self.check_box
        self.model.setItem(0,0,self.check_box)
        self.model.setData(self.model.index(0, self.TRACK), track.track_name)
        self.model.setData(self.model.index(0, self.ARTIST), track.artist_name)
        self.model.setData(self.model.index(0, self.ALBUM), track.collection_name)
        return

    def add_track_list(self, track_list):
        added = []
        for track in track_list:
            if(track.track_name.lower() not in added):
                self.add_track_to_box(track)
                added.append(track.track_name.lower())
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
        elif(artist and not track and not album):
            try:
                results = get_artist(artist)
                self.add_track_list(results)
            except:
                self.add_no_match_to_box()

        # only track entered
        elif(track and not artist and not album):
            try:
                results = itunespy.search_track(track)
                self.add_track_list(results)
            except:
                self.add_no_match_to_box()

        # only album entered
        elif(album and not artist and not track):
            try:
                results = get_album_no_artist(album)
                self.add_track_list(results)
            except:
                self.add_no_match_to_box()

        # only track and artist entered
        elif(track and artist):
            try:
                result = get_track(track, artist)
                self.add_track_list([result])
            except:
                self.add_no_match_to_box()

        # only album and artist entered
        elif(album and artist):
            try:
                results = get_album(album, artist)
                self.add_track_list([result])
            except:
                self.add_no_match_to_box()

        # only track and album
        elif(track and album):
            try:
                result = get_track_on_album(track, album)
                self.add_track_list([result])
            except:
                self.add_no_match_to_box()

    def download_button_push(self):
        #self.pbar.setMaximum(self.model.rowCount())
        for row in range(self.model.rowCount()):
            if self.model.item(row).checkState():
                song = []
                for column in range(self.model.columnCount()):
                    index = self.model.index(row, column)
                    if(index != 0):
                        song.append(str(self.model.data(index)))
                #self.pbar.setValue(row+1)
                track = get_track(song[1], song[2])
                #print(track)
                download([track])
                #self.pbar.setValue(row+1)
        #self.pbar.reset()

    def yt_button_push(self):
        artist = self.artist_line.text()
        track = self.track_line.text()
        try:
            download_no_itunes(track, artist)
        except:
            self.add_no_match_to_box()

"""
Test:
"""
app = QApplication(sys.argv)
#app.setStyle("fusion")
gui = MainGUI()
gui.show()
sys.exit(app.exec_())
