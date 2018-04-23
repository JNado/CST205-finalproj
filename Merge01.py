import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Downloader_Functions import *

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
        self.search_button.clicked.connect(self.btn_push)
        self.mbox.addWidget(self.search_button)


        #add hbox to mbox and finalize
        self.mbox.addLayout(self.hbox)
        self.setLayout(self.mbox)

    def btn_push(self):
        results = []
        result_str = ""

        user_artist = self.artist_line.text()
        user_track = self.track_line.text()
        user_album = self.album_line.text()

        if(not user_artist and not user_track and not user_album):
            self.browser.setText("No Info Entered!")
            return

        if(user_track and user_artist):
            result = get_track(user_track, user_artist)
            self.browser.append(result.track_name + " - " + result.artist_name)
            return

        if(user_album and user_artist):
            results = get_album(user_album, user_artist)
            for result in results:
                self.browser.append(result.track_name + " - " + result.artist_name)

        if(user_artist and not user_track and not user_album):
            used = []
            results = get_artist(user_artist)
            for result in results:
                self.browser.append("Album: "+result[0].collection_name)
                if(result[0].collection_name.lower() not in used):
                    used.append(result[0].collection_name.lower())
                    for r in result:
                        if(r.track_name.lower() not in used):
                            self.browser.append("\t"+r.track_name)
                            used.append(r.track_name.lower())
                    self.browser.append("\n")


"""
Test:
"""
app = QApplication(sys.argv)
gui = MainGUI()
gui.show()
sys.exit(app.exec_())
