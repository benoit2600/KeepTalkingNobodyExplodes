from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QPushButton, QSizePolicy

from gameVar import GameVar


def StressModeInit(self):
    self.MW.stackSetup.setCurrentIndex(5)

    self.gameVar.stressMode = 1
    self.gameVar.pause = 1
    self.gameVar.stressModeStep = 0

    QTimer().singleShot(5000, lambda: StressModeInitCallback(self))


def blinkStressBios(self):
    self.gameVar.nbSecGlobal += 1
    if self.gameVar.stressBlink == 0:
        self.MW.bios.setStyleSheet("border-image: url(assets/Images/biosurgence.png) 0 0 0 0 stretch stretch");
        self.gameVar.stressBlink = 1
    else :
        self.MW.bios.setStyleSheet("border-image: url(assets/Images/biosurgence2.png) 0 0 0 0 stretch stretch");
        self.gameVar.stressBlink = 0



def StressModeInitCallback(self):
    self.gameVar.sounds["stress"].play()
    QTimer().singleShot(4000, lambda: StressModeInitCallbackbis(self))
    self.MW.stackSetup.setCurrentIndex(3)

    self.timerStress = QtCore.QTimer()
    self.timerStress.timeout.connect(lambda: blinkStressBios(self))
    self.timerStress.start(1000)


def StressModeInitCallbackbis(self):
    self.gameVar.chrono = [0, 5, 0, 0, 0]
    self.gameVar.chronoBlink = 1
    self.gameVar.chronoLum = 2
    self.gameVar.stressModeStarted = 1
    self.gameVar.pause = 0
    self.gameVar.moduleWin = [0, 0, 0, 0, 0]
    self.gameVar.lumSimon = [0, 0, 0, 0]
    self.gameVar.symboleLum = [0, 0, 0, 0]
    self.gameVar.boutonBande = [0, 0, 0]

    self.timerLumiere.stop()
    self.timerBip.stop()
    self.timerBip.start(750)


def checkStressMode(self):
    gv = self.gameVar


    if gv.stressModeStep == 5 : # win !
        self.gameVar.sounds["victoire"].play()
        self.timerBip.stop()
        self.gameVar.moduleWin = [1, 1, 1, 1, 1]
        self.gameVar.lumSimon = [0, 0, 0, 0]
        self.gameVar.symboleLum = [0, 0, 0, 0]
        self.gameVar.moduleErr = [0, 0, 0, 0, 0, 0]

        self.gameVar.boutonBande = [0, 1, 0]
        self.timerStress.stop()
        self.gameVar.sounds["stress"].stop()
        self.gameVar.chronoLum = 0
        self.gameVar.chronoBlink = 0
        self.MW.stackSetup.setCurrentIndex(4)
        self.gameVar.stressModeStarted = 0
        self.MW.win.reloadChrono()
        print("MW.stackSetup.setCurrentIndex(4)")
        return

    if gv.stressPressed != 0:  # Si un bouton est pressé et non relaché, on attend :
        if max(gv.btnSimon) == 0 and max(gv.symboleBtn) == 0 and gv.boutonContact == 0 :  # on verifie que le bouton a été relaché avant d'effectuer les actions
            gv.stressPressed = 0

    elif max(gv.btnSimon) == 1 or max(gv.symboleBtn) == 1 or gv.boutonContact == 1 :
        gv.stressPressed = 1
        tBtn = gv.stressModeListeBouton[gv.stressModeStep][0]
        idBtn = gv.stressModeListeBouton[gv.stressModeStep][1]
        if tBtn == "si" and gv.btnSimon[idBtn] == 1 :
            gv.lumSimon[idBtn] = 1
            gv.stressModeStep += 1
        elif tBtn == "sy" and gv.symboleBtn[idBtn] == 1 :
            gv.symboleLum[idBtn] = 1
            gv.stressModeStep += 1
        elif tBtn == "b" and gv.boutonContact == 1:
            gv.boutonBande = [1,1,1]
            gv.stressModeStep += 1
        else:

            self.erreurGlobal(5)
            self.gameVar.lumSimon = [0, 0, 0, 0]
            self.gameVar.symboleLum = [0, 0, 0, 0]
            self.gameVar.boutonBande = [0, 0, 0]

            gv.stressModeStep = 0


class winEscape(QWidget):
    def __init__(self, m):
        QWidget.__init__(self)
        self.MW = m
        self.g = m.game
        self.setWindowTitle("Setup")
        self.gameVar = GameVar()

        self.btn = QPushButton()
        f = self.btn.font()
        f.setPointSize(30)
        self.btn.setFont(f)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.btn)
        self.btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setLayout(self.vbox)
        self.setStyleSheet("border-image: url(assets/Images/win.png) 0 0 0 0 stretch stretch");
        self.btn.clicked.connect(self.g.retourMenu)

    def reloadChrono(self):
        min = str(int(self.gameVar.nbSecGlobal / 60))
        sec = str(int(self.gameVar.nbSecGlobal % 60))
        self.btn.setText("Bravo !!!\nTemps : " + min + ":" + sec+"\nNb Erreur : " + str(self.gameVar.nbErreur))
