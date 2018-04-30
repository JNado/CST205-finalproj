import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Downloader_Functions import *

class MainGUI(QWidget):
    DOWNLOAD, TRACK, ARTIST, ALBUM = range(4)

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
        self.add_yt_button()
        self.add_clear_button()
        self.finalize_layout()

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

        self.setGeometry(100,100, 800, 494) # Gives the window a gradient background. 
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor('#8EF0F0'))
        gradient.setColorAt(1.0, QColor('#F0A0A0'))
        p = self.palette()
        p.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(p)

        self.mbox = QVBoxLayout() # main layout
        self.hbox = QHBoxLayout()
        self.hbtnbox = QHBoxLayout() # layout for the buttons

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
        Adds a QGroupBox to this MainGUI.

        """
        self.data_view = QTreeView()
        self.data_view.setRootIsDecorated(False)
        self.data_view.setAlternatingRowColors(True)
        self.data_view.setAutoFillBackground(True)

        self.mbox.addWidget(self.data_view)

        self.data_layout = QHBoxLayout()
        self.data_layout.addWidget(self.data_view)
        p = self.palette()
        p.setColor(QPalette.Base, QColor('#F1DEFF'))
        self.setPalette(p)
        self.model = self.create_track_model(self)
        self.data_view.setModel(self.model)



    def create_track_model(self, parent):
        """
        Creates a model to organize the data inside
        the associated QTreeView.
        Adds the header data: Donwload, Track, Artist, Album.
        """
        model = QStandardItemModel(0, 4, parent)
        model.setHeaderData(self.DOWNLOAD, Qt.Horizontal, "Download")
        model.setHeaderData(self.TRACK, Qt.Horizontal, "Track")
        model.setHeaderData(self.ARTIST, Qt.Horizontal, "Artist")
        model.setHeaderData(self.ALBUM, Qt.Horizontal, "Album")
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

    def add_yt_button(self):
        """
        Creates a QPushButton to download directly
        from youtube for search results that have no
        match from the iTunes API. Songs donwloaded this
        way have no ID3 header data embedded inside thier
        mo3 file.
        """
        self.yt_button = QPushButton("No Match Download")
        self.yt_button.setFixedWidth(150)
        self.yt_button.clicked.connect(self.yt_button_push)
        self.hbtnbox.addWidget(self.yt_button)

    def add_clear_button(self):
        """
        Creates a QPushButton to clear the data from
        the QItemStandardModel.
        """
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedWidth(95)
        self.clear_button.clicked.connect(self.clear_button_push)
        self.hbtnbox.addWidget(self.clear_button)

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

    def clear_button_push(self):
        """
        Clears the data from the
        QItemStandardModel.
        """
        self.model.removeRows(0, self.model.rowCount())

"""
Test:
"""
app = QApplication(sys.argv)
#app.setStyle("fusion")
gui = MainGUI()
# gui.setBackgroundRole(QPalette.Base)
gui.show()
sys.exit(app.exec_())
