# Génération de l'UI


from PyQt5 import QtCore
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import (QPushButton, QSizePolicy,
                             QHBoxLayout, QVBoxLayout, QLineEdit)
import ScreenGame

def initUi(self):
    self.setWindowTitle("Bombe")
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('assets/trs-million rg.ttf')
    fontDB.addApplicationFont('assets/Square.ttf')

    fontLine = QFont("trs million")
    fontLine.setPointSize(40)
    fontBtn = QFont("SquareFont")
    fontBtn.setPointSize(20)

    self.lineEdit = QLineEdit("")
    self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
    self.lineEdit.setFixedHeight(100)
    self.lineEdit.setFixedWidth(400)
    self.lineEdit.setFont(fontLine)
    if (self.gameVar.serialOK == 0):
        self.lineEdit.setText("Err Arduino")

    self.hg = QPushButton("")
    self.hg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    self.hg.adjustSize()
    self.hd = QPushButton("")
    self.mg = QPushButton("")
    self.md = QPushButton("")
    self.bg = QPushButton("")
    self.bd = QPushButton("")
    self.btns = [self.hg, self.hd, self.mg, self.md, self.bg, self.bd]

    i = 0
    for btn in self.btns:
        btn.clicked.connect(self.on_click)
        btn.setMaximumHeight(400)
        btn.setFixedHeight(100)
        btn.setFont(fontBtn)
        i = i + 1
    self.linehbox = QHBoxLayout()
    self.linehbox.addStretch(1)
    self.linehbox.addWidget(self.lineEdit)
    self.linehbox.addStretch(1)

    self.hhbox = QHBoxLayout()
    self.hhbox.addWidget(self.hg, stretch=4)
    self.hhbox.addWidget(self.hd, stretch=4)

    self.mhbox = QHBoxLayout()
    self.mhbox.addWidget(self.mg)
    self.mhbox.addWidget(self.md)

    self.bhbox = QHBoxLayout()
    self.bhbox.addWidget(self.bg)
    self.bhbox.addWidget(self.bd)

    self.vbox = QVBoxLayout()
    self.vbox.addStretch(1)

    self.vbox.addLayout(self.linehbox)
    self.vbox.addStretch(5)
    self.vbox.addLayout(self.hhbox)
    self.vbox.addLayout(self.mhbox)
    self.vbox.addLayout(self.bhbox)
    self.vbox.addStretch(1)

    self.setGeometry(0, 0, 416, 656)

    self.setLayout(self.vbox)
    self.setStyleSheet(open('assets/style.qss').read())

    #ScreenGame.paintButton(self)
