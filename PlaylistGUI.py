from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Downloader_Functions import *
import sys, subprocess
"""
CST 205 Final Project
Torin Foss | Jeff Nadolna | Marc Alejandro | Benoit Millet

PlaylistGUI:
A secondary GUI that allows users to create, edit, and
play playlists.
"""
class PlaylistGUI(QWidget):
    ADD, TRACK, ARTIST, ALBUM, ID = range(5)

    def __init__(self):
        """
        Constructs PlaylistGUI object.
        """
        super().__init__()
        self.initialize()
        self.add_tree_view()
        self.add_pl_line_edit()
        self.add_view_songs_btn()
        self.add_create_pl_btn()
        self.add_view_pl_button()
        self.add_del_from_pl_btn()
        self.add_play_btn()
        self.finalize_layout()

    """
    All functions below are associated with
    adding QWidgets to this PlaylistGUI.
    """
    def initialize(self):
        """
        Initializes this PlaylistGUI. Sets the window title,
        geometry, and the main layouts.
        """
        self.setWindowTitle("Playlist Maker")
        self.setGeometry(100,100, 800, 494)
        self.mbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbtnbox = QHBoxLayout()

    def add_tree_view(self):
        """
        Adds a QTreeView to this PlaylistGUI. For
        storing songs found in each playlist.
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
        Returns a QStandardItemModel object. A model
        to store data inside the associated QTreeView.

        Adds the header data: Donwload, Track, Artist, Album, ID.
        """
        model = QStandardItemModel(0, 5, parent)
        model.setHeaderData(self.ADD, Qt.Horizontal, "Add To Playlist")
        model.setHeaderData(self.TRACK, Qt.Horizontal, "Track")
        model.setHeaderData(self.ARTIST, Qt.Horizontal, "Artist")
        model.setHeaderData(self.ALBUM, Qt.Horizontal, "Album")
        model.setHeaderData(self.ID, Qt.Horizontal, "ID")
        return model

    def add_pl_line_edit(self):
        """
        Adds a QLineEdit into this PlaylistGUI. Where you
        can enter playlist to edit, create, or play.
        """
        self.pl_line_edit = QLineEdit()
        self.pl_line_edit.setPlaceholderText("Enter name of new playlist...")
        self.hbox.addWidget(self.pl_line_edit)

    def add_view_songs_btn(self):
        """
        Creates a QPushButton to view songs found
        inside the Fixed directory.
        """
        self.view_songs = QPushButton("View Songs")
        self.view_songs.clicked.connect(self.view_songs_push)
        self.hbtnbox.addWidget(self.view_songs)

    def add_create_pl_btn(self):
        """
        Creates a QPushButton to add checked songs
        to a playlist.
        """
        self.create_pl = QPushButton("Add to playlist")
        self.create_pl.clicked.connect(self.pl_btn_push)
        self.hbtnbox.addWidget(self.create_pl)

    def add_view_pl_button(self):
        """
        Creates a QPushButton to view songs found
        inside the given playlist.
        """
        self.view_pl = QPushButton("View Playlist")
        self.view_pl.clicked.connect(self.view_pl_btn_push)
        self.hbtnbox.addWidget(self.view_pl)

    def add_del_from_pl_btn(self):
        """
        Adds a QPushButton to delete checked
        songs from a given playlist.
        """
        self.delete_pl = QPushButton("Delete from playlist")
        self.delete_pl.clicked.connect(self.delete_pl_btn_push)
        self.hbtnbox.addWidget(self.delete_pl)

    def add_play_btn(self):
        """
        Adds a QPushButton to play a
        given playlist in your operating
        system's default music player.
        """
        self.play_btn = QPushButton("Play Selected Songs")
        self.play_btn.clicked.connect(self.play_btn_push)
        self.hbtnbox.addWidget(self.play_btn)

    def finalize_layout(self):
        """
        Finalizes this PlaylistGUI by setting the
        main layouts.
        """
        self.mbox.addLayout(self.hbtnbox)
        self.mbox.addLayout(self.hbox)
        self.setLayout(self.mbox)

    """
    All functions below are linked to
    events.
    """
    def add_track_to_box(self,track):
        """
        track is a track object.

        Inserts track's data members in the
        QStandardItemModel.
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

    def view_songs_push(self):
        """
        Adds all songs inside the Fixed directory
        into the QStandardItemModel. These songs can
        then be added to a specified playlist.
        """
        #clear all data first
        self.model.removeRows(0, self.model.rowCount())
        songs = glob.glob("Fixed/*/*/*")
        for song in songs:
            data = mutagen.File(song, easy=True)
            track = get_track(data['title'][0], data['artist'][0])
            self.add_track_to_box(track)

    def pl_btn_push(self):
        """
        Adds checked songs to a given playlist.
        If no playlist exists, one will be created.
        """
        try:
            pl_name = self.pl_line_edit.text().replace(" ", "_")
            path = os.path.abspath("Playlists/"+pl_name+".m3u")
            pl_file = open(path, 'a')

            songs = glob.glob("Fixed/*/*/*")
            for row in range(self.model.rowCount()):
                if self.model.item(row).checkState():
                    index = self.model.index(row, 4)
                    for song in songs:
                        data = mutagen.File(song, easy=True)
                        track = get_track(data['title'][0], data['artist'][0])
                        if int(track.track_id) == int(self.model.data(index)):
                            mp3_path = os.path.abspath(song)
                            pl_file.write(mp3_path+"\n")
            QMessageBox.about(self, "Playlist Updated",
                            'Playlist "%s" has been updated.'%(self.pl_line_edit.text()))
            pl_file.close()
        except:
            QMessageBox.about(self, "Playlist Not Updated",
                              'Playlist "%s" could not be updated.'%(self.pl_line_edit.text()))

    def view_pl_btn_push(self):
        """
        Adds a playlists songs to the QStandardItemModel.
        """
        try:
            self.model.removeRows(0, self.model.rowCount())
            pl_name = self.pl_line_edit.text().replace(" ", "_")
            path = "Playlists/"+ pl_name+".m3u"
            pl_file = open(path, "r")
            for line in pl_file:
                data = mutagen.File(line[:-1], easy=True)
                track = get_track(data['title'][0], data['artist'][0])
                self.add_track_to_box(track)
        except:
            QMessageBox.about(self, "Playlist Not Found",
                              "Could not find playlist %s." % (self.pl_line_edit.text()))

    def delete_pl_btn_push(self):
        """
        Removes selected songs from a given playlist.
        """
        try:
            pl_name = self.pl_line_edit.text().replace(" ", "_")
            path = os.path.abspath("Playlists/"+ pl_name+".m3u")
            to_keep = {}
            for row in range(self.model.rowCount()):
                if not self.model.item(row).checkState():
                    title = str(self.model.data(self.model.index(row, 1)))
                    artist = str(self.model.data(self.model.index(row, 2)))
                    to_keep[title] = artist
            os.system("rm %s" % (path))

            pl_file = open(path, "w")
            for mp3 in glob.glob("Fixed/*/*/*"):
                data = mutagen.File(mp3, easy=True)
                if (data["title"][0] in to_keep.keys() and
                    to_keep[data["title"][0]] == data["artist"][0]):
                    pl_file.write(mp3+"\n")
            QMessageBox.about(self, "Playlist Updated",
                            'Playlist "%s" has been updated, please view again to see changes.'% (self.pl_line_edit.text()))
        except:
            QMessageBox.about(self, "Playlist Not Updated",
                            'Playlist "%s" could not be updated, please view again to see changes.'% (self.pl_line_edit.text()))

    def play_btn_push(self):
        """
        Plays a given playlist by opening your
        operating systems default music player.
        """
        try:
            pl_name = self.pl_line_edit.text().replace(" ", "_")
            path = os.path.abspath("Playlists/"+ pl_name+".m3u")

            #if sys.platform == "linux" or sys.platform == "linux2":
                #print("linux")

            if sys.platform == "darwin":
                subprocess.call(["open", path])

            elif sys.platform == "win32":
                os.startfile(path)
        except:
            QMessageBox.about(self, "OS not recognized",
                            'Could not recognize operating system.')
