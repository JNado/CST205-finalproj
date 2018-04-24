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

        """
        #create search results text browser
        self.browser = QTextBrowser()
        self.mbox.addWidget(self.browser)
        """

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

        # create search button
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.btn_push)
        self.mbox.addWidget(self.search_button)


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
        Track is a track object
        """
        self.model.insertRow(0)
        self.model.setData(self.model.index(0, self.DOWNLOAD), QCheckBox())
        self.model.setData(self.model.index(0, self.TRACK), track.track_name)
        self.model.setData(self.model.index(0, self.ARTIST), track.artist_name)
        self.model.setData(self.model.index(0, self.ALBUM), track.collection_name)
        return

    def btn_push(self):
        user_artist = self.artist_line.text()
        user_track = self.track_line.text()
        user_album = self.album_line.text()

        if(not user_artist and not user_track and not user_album):
            self.browser.setText("No Info Entered!")
            return


        if(user_track and user_artist):
            result = get_track(user_track, user_artist)
            self.add_track_to_box(result)
            return

        if(user_album and user_artist):
            results = get_album(user_album, user_artist)
            for result in results:
                self.add_track_to_box(result)
            return


        if(user_artist and not user_track and not user_album):
            used = []
            results = get_artist(user_artist)
            for l in results:
                for track in l:
                    self.add_track_to_box(track)
            return


"""
Test:
"""
app = QApplication(sys.argv)
gui = MainGUI()
gui.show()
sys.exit(app.exec_())
