from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel
from PyQt5.QtGui import QPixmap, QImage
import PyQt5

from srgan_compute import srgan_compute
import numpy as np
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "image-resolution-enhancer"
        self.top = 200
        self.left = 500
        self.width = 600
        self.height = 800

        self.imagePath = ""

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        vbox = QVBoxLayout()

        self.btn1 = QPushButton("Open Image")
        self.btn1.clicked.connect(self.getImage)

        self.btn2 = QPushButton("Upscale Image")
        self.btn2.clicked.connect(self.resImage)

        vbox.addWidget(self.btn1)
        vbox.addWidget(self.btn2)

        self.label1 = QLabel("")
        vbox.addWidget(self.label1)

        self.label2 = QLabel("")
        vbox.addWidget(self.label2)

        vbox.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.setLayout(vbox)

        self.show()

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        self.imagePath = fname[0]
        pixmap = QPixmap(self.imagePath).scaled(self.size(), PyQt5.QtCore.Qt.KeepAspectRatio)
        self.label1.setPixmap(QPixmap(pixmap))

    def resImage(self):
        sr = srgan_compute(self.imagePath)
        qimage = QImage(sr, sr.shape[1], sr.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(self.size(), PyQt5.QtCore.Qt.KeepAspectRatio) 
        self.label2.setPixmap(QPixmap(pixmap))


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
