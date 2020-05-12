#!/usr/bin/python3.8
from PyQt5.QtWidgets import QLabel, QMainWindow, QDesktopWidget, QApplication
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
import sys


class Incubator(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setFixedSize(700, 700)
        self.centering()
        self.content()
        self.show()

    def centering(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def content(self):
        self.setWindowTitle('Chess Board Representation')
        pixmap = QPixmap('pos.svg')
        label = QLabel(self)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Incubator()
    sys.exit(app.exec_())