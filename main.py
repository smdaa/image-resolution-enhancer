from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QFileDialog , QLabel, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
import PyQt5

from srgan_compute import srgan_compute
import numpy as np
from PIL import Image
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
        self.sr = None
        self.upscaleimagePath = ""

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()

        self.btn1 = QPushButton("Open Image")
        self.btn1.clicked.connect(self.getImage)

        self.btn2 = QPushButton("Upscale Image (x4)")
        self.btn2.clicked.connect(self.resImage)
    
        self.btn3 = QPushButton("Save Image")
        self.btn3.clicked.connect(self.saveImage)

        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)


        layout.addWidget(self.btn1, 0, 0)
        layout.addWidget(self.btn2, 1, 0)
        layout.addWidget(self.btn3, 2, 0)

        self.label1 = QLabel("")
        layout.addWidget(self.label1, 0, 1)

        self.label2 = QLabel("")
        layout.addWidget(self.label2, 0, 2)

        #layout.setAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.setLayout(layout)

        self.show()

    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        if fname==('', ''):
            return 
        self.imagePath = fname[0]
        pixmap = QPixmap(self.imagePath).scaled(self.size(), PyQt5.QtCore.Qt.KeepAspectRatio)
        self.label1.setPixmap(QPixmap(pixmap))

    def resImage(self):
        try:
            self.sr = srgan_compute(self.imagePath)
        except AttributeError:
            self.msg.setText("Load Image First")
            self.msg.setWindowTitle("Error")
            self.msg.exec_()
            return 
        qimage = QImage(self.sr, self.sr.shape[1], self.sr.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap(qimage)
        pixmap = pixmap.scaled(self.size(), PyQt5.QtCore.Qt.KeepAspectRatio) 
        self.label2.setPixmap(QPixmap(pixmap))

    def saveImage(self):
        fname = QFileDialog.getSaveFileName(self, 'Save File')
        if fname==('', ''):
            return 
        self.upscaleimagePath = fname[0]
        try:
            im = Image.fromarray(self.sr)
        except AttributeError:
            self.msg.setText("Upscale Image First")
            self.msg.setWindowTitle("Error")
            self.msg.exec_()
            return 
        im.save(fname[0])


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
