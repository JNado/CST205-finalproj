from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Downloader_Functions import *
import pygame


class PlaylistGUI(QWidget):
    ADD, TRACK, ARTIST, ALBUM, ID = range(5)

    def __init__(self):
        """
        Constructs a MainGUI function.
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
    adding QWidgets to this MainGUI. And linking
    those QWidgets to their proper functions.
    """
    def initialize(self):
        """
        Initializes this MainGUI. Sets the window title,
        geometry, and the main layouts.
        """
        self.setWindowTitle("Playlist Maker")
        self.setGeometry(0,0, 800, 494)
        self.mbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbtnbox = QHBoxLayout()

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
        model.setHeaderData(self.ADD, Qt.Horizontal, "Add To Playlist")
        model.setHeaderData(self.TRACK, Qt.Horizontal, "Track")
        model.setHeaderData(self.ARTIST, Qt.Horizontal, "Artist")
        model.setHeaderData(self.ALBUM, Qt.Horizontal, "Album")
        model.setHeaderData(self.ID, Qt.Horizontal, "ID")
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
        self.model.setData(self.model.index(0, self.ID), track.track_id)
        return

    def add_pl_line_edit(self):
        self.pl_line_edit = QLineEdit()
        self.pl_line_edit.setPlaceholderText("Enter name of new playlist...")
        self.hbox.addWidget(self.pl_line_edit)

    def add_view_songs_btn(self):
        """
        Creates a QPushButton to add songs to stored playlist
        """
        self.view_songs = QPushButton("View Songs")
        self.view_songs.clicked.connect(self.view_songs_push)
        self.hbtnbox.addWidget(self.view_songs)

    def add_create_pl_btn(self):
        """
        Creates a QPushButton to add songs to stored playlist
        """
        self.create_pl = QPushButton("Add to playlist")
        self.create_pl.clicked.connect(self.pl_btn_push)
        self.hbtnbox.addWidget(self.create_pl)

    def add_view_pl_button(self):
        self.view_pl = QPushButton("View Playlist")
        self.view_pl.clicked.connect(self.view_pl_btn_push)
        self.hbtnbox.addWidget(self.view_pl)

    def add_del_from_pl_btn(self):
        self.delete_pl = QPushButton("Delete from playlist")
        self.delete_pl.clicked.connect(self.delete_pl_btn_push)
        self.hbtnbox.addWidget(self.delete_pl)

    def add_play_btn(self):
        self.play_btn = QPushButton("Play Selected Songs")
        self.play_btn.clicked.connect(self.play_btn_push)
        self.hbtnbox.addWidget(self.play_btn)

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
    def view_songs_push(self):
        #clear all data first
        self.model.removeRows(0, self.model.rowCount())
        songs = glob.glob("Fixed/*/*/*")
        for song in songs:
            data = mutagen.File(song, easy=True)
            track = get_track(data['title'][0], data['artist'][0])
            self.add_track_to_box(track)

    def pl_btn_push(self):
        pl_name = self.pl_line_edit.text().replace(" ", "_")
        path = 'Playlists/'+pl_name+ '.txt'
        pl_file = open(path, 'a')
        for row in range(self.model.rowCount()):
            if self.model.item(row).checkState():
                index = self.model.index(row, 4)
                pl_file.write(str(self.model.data(index))+"\n")
        QMessageBox.about(self, "Playlist Updated",
                        "Your playlist has been updated.")

    """
    Not that efficient
    """
    def view_pl_btn_push(self):
        self.model.removeRows(0, self.model.rowCount())
        pl_name = self.pl_line_edit.text().replace(" ", "_")
        playlist = open("Playlists"+"/"+pl_name+".txt", "r")
        for id in playlist:
            for path in glob.glob("Fixed/*/*/*"):
                data = mutagen.File(path, easy=True)
                track = get_track(data['title'][0], data['artist'][0])
                if int(id) == int(track.track_id):
                    self.add_track_to_box(track)

    def delete_pl_btn_push(self):
        pl_name = self.pl_line_edit.text().replace(" ", "_")
        path = 'Playlists/'+pl_name+ '.txt'
        print(path)
        saved = []
        for row in range(self.model.rowCount()):
            if not self.model.item(row).checkState():
                index = self.model.index(row, 4)
                saved.append(str(self.model.data(index)))

        os.system("rm %s" % (path))
        pl_file = open(path, 'a')
        for id in saved:
            pl_file.write(str(id)+"\n")

        QMessageBox.about(self, "Playlist Updated",
                        "Your playlist has been updated, please view agan to see changes.")

    def play_btn_push(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        to_play = []
        paths = glob.glob("Fixed/*/*/*")
        for row in range(self.model.rowCount()):
            if self.model.item(row).checkState():
                index = self.model.index(row, 4)
                id = int(self.model.data(index))

                for path in paths:
                    data = mutagen.File(path, easy=True)
                    track = get_track(data['title'][0], data['artist'][0])
                    if int(id) == int(track.track_id):
                        to_play.append(path)
                        sound = pygame.mixer.Sound(path)
                        sound.play()
