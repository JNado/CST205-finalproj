import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MainGUI(QWidget):
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

        #create search results text browser
        self.browser = QTextBrowser()
        self.mbox.addWidget(self.browser)

        # create search button
        self.search_button = QPushButton("Search")
        #self.btn.clicked.connect(self.btn_push)
        self.mbox.addWidget(self.search_button)

        #add hbox to mbox and finalize
        self.mbox.addLayout(self.hbox)
        self.setLayout(self.mbox)

"""
Test:
"""
app = QApplication(sys.argv)
gui = MainGUI()
gui.show()
sys.exit(app.exec_())
