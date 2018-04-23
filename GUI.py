import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
QLineEdit, QHBoxLayout, QVBoxLayout, QComboBox, QMessageBox)
from PyQt5.QtCore import pyqtSlot

class Window(QWidget):
	def __init__(self):
		super().__init__()

		self.lab1 = QLabel("Search")
		self.search = QLineEdit()
		self.song = QPushButton("Song")
		self.artist = QPushButton("Artist")
		self.album = QPushButton("Album")
		self.dis = QLineEdit("Song displayed here")
		self.setGeometry(300, 300, 280, 100)

		hbox = QHBoxLayout()
		hbox.addWidget(self.lab1)
		hbox.addWidget(self.search)

		hbox2 = QHBoxLayout()
		hbox2.addWidget(self.song)
		hbox2.addWidget(self.artist)
		hbox2.addWidget(self.album)

		vbox = QVBoxLayout()
		vbox.addWidget(self.dis)

		mbox = QVBoxLayout()
		mbox.addLayout(hbox)
		mbox.addLayout(hbox2)
		mbox.addLayout(vbox)
		self.setLayout(mbox)

app = QApplication(sys.argv)
main = Window()
main.show()
sys.exit(app.exec_())
