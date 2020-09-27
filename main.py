import getopt
import random
import sys
from itertools import cycle

import serial
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import (QWidget, QApplication, QMainWindow, QStackedWidget)
import signal

import Chrono
import ScreenGame
import Setup
import Simon
import ui
from ScreenGame import guess, paintButton, eraseAll, win
from gameVar import GameVar
from WebServer import WebServer
import Fils
import StressMode
import Symbole
from Bouton import checkBouton

signal.signal(signal.SIGINT, signal.SIG_DFL)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setStyleSheet(open('assets/style.qss').read())

        self.setWindowTitle("Bombe")
        self.game = Game(self)
        ui.initUi(self.game)

        self.setup = Setup.Setup(self)
        self.setupSymbole = Setup.SetupSymbole(self)
        self.bios = QWidget()
        self.desamorcage = QWidget()

        self.win = StressMode.winEscape(self)
        self.stackSetup = QStackedWidget()
        self.stackSetup.addWidget(self.setup)
        self.stackSetup.addWidget(self.setupSymbole)
        self.stackSetup.addWidget(self.game)
        self.stackSetup.addWidget(self.bios)
        self.stackSetup.addWidget(self.win)
        self.stackSetup.addWidget(self.desamorcage)
        self.bios.setStyleSheet("border-image: url(assets/Images/biosurgence.png) 0 0 0 0 stretch stretch");
        self.desamorcage.setStyleSheet("border-image: url(assets/Images/desamorcage.png) 0 0 0 0 stretch stretch");

        self.setGeometry(0, 0, 480, 720)

        self.setCentralWidget(self.stackSetup)



class Game(QWidget):

    def __init__(self, m):
        QWidget.__init__(self)

        self.gameVar = GameVar()  # Contient tout les variables du jeu
        self.MW = m
        self.on_click
        try:
            self.initSerial()
        except serial.SerialException as e:
            print("Erreur connexion Arduino")
            self.gameVar.error += str(e)
            print(e)

        self.ws = WebServer(self.gameVar, self)
        self.ws.start()


    def checkSensor(self):
        gv = self.gameVar
        try:
            self.ser.write(gv.sendArduino().encode())
            line = self.ser.readline()
            gv.interprete(line.decode('utf-8').rstrip())
        except Exception as e:
            self.gameVar.error = str(e)


        if not gv.defaite and not gv.pause and not gv.stressMode:
            Simon.checkSimon(self)
            Fils.checkFils(self)
            Symbole.checkSymbole(self)
            checkBouton(self)
        if gv.stressMode and gv.stressModeStarted:
            StressMode.checkStressMode(self)


    def erreurGlobal(self, module):
        self.gameVar.moduleErr[module] += 1
        self.gameVar.nbErreur = sum(self.gameVar.moduleErr)
        self.gameVar.sounds["error"].play()

        if self.gameVar.nbErreur > self.gameVar.nbErreurMax:
            self.defaite()
        else:
            for i in range(4):
                if i < self.gameVar.nbErreur :
                    self.gameVar.chronoLedErr[i] = 1
                else:
                    self.gameVar.chronoLedErr[i] = 0

            if self.gameVar.moduleErr[module] == 1 and module != 5:
                Chrono.removeXmMin(self, 3)
            elif self.gameVar.moduleErr[module] > 1 and module != 5:
                Chrono.removeXmMin(self, 1)

    def bip(self):
        if self.gameVar.pause:
            return
        if self.gameVar.stressMode:
            self.gameVar.sounds["bip2"].play()
        elif self.gameVar.chronoBoutonSon:
            self.gameVar.sounds["bip"].play()

        Chrono.chrono(self)

    def initSerial(self):
        self.ser = ""
        try:
            self.ser = serial.Serial('/dev/ttyUSB0', 19200, timeout=1)
        except:
            try:
                self.ser = serial.Serial('/dev/ttyUSB1', 19200, timeout=1)
            except Exception as e:
                raise e

        print(self.ser.write("initialisation\n".encode()))
        line = self.ser.readline()
        self.gameVar.serialOK = 1

    def start(self):

        Fils.initFils(self.gameVar)
        Symbole.initSymbole(self.gameVar)
        Simon.initSimon(self.gameVar)
        ScreenGame.paintButton(self)

        self.timerBip = QtCore.QTimer()
        self.timerBip.timeout.connect(self.bip)
        self.timerBip.start(1000)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.checkSensor)
        self.timer.start(50)

        self.timerLumiere = QtCore.QTimer()
        self.timerLumiere.timeout.connect(lambda: Simon.lumiereSimon(self.gameVar))
        self.timerLumiere.start(500)



    @pyqtSlot()
    def on_click(self):
        print("lala")
        btn = self.sender()
        guess(self, btn)

    def victoire(self):
        self.gameVar.pause = 1

        self.gameVar.sounds["victoire"].play()
        self.timerBip.stop()
        self.gameVar.moduleWin = [1, 1, 1, 1, 1]
        self.gameVar.lumSimon = [0, 0, 0, 0]
        self.gameVar.symboleLum = [0, 0, 0, 0]
        self.gameVar.boutonBande = [0, 1, 0]
        self.gameVar.chronoLum = 1
        self.gameVar.chronoBlink = 0
        if self.gameVar.escapeGame:
            self.timerStress.stop()
            self.gameVar.stressModeStarted = 0

        self.MW.stackSetup.setCurrentIndex(4)
        self.MW.win.reloadChrono()



    def defaite(self):
        if self.gameVar.defaite : # defaite() déjà appelé
            return
        print("defaite")
        if self.gameVar.stressModeStarted == 1 :
            try :
                self.gameVar.sounds["stress"].stop()
            except :
                pass

        self.gameVar.chronoBlink = 1
        self.gameVar.chronoLum = 2
        self.gameVar.defaite = True
        self.timerLumiere.stop()
        self.timerBip.stop()
        self.gameVar.sounds["defaite"].play()
        QTimer().singleShot(14000, self.retourMenu)
        QTimer().singleShot(3200, self.callbackDefaite)
        self.gameVar.moduleWin = [0, 0, 0, 0, 0]

        self.blink = 30

    def callbackDefaite(self):
        self.gameVar.chronoLum = 0
        self.gameVar.chronoBlink = 0
        self.gameVar.chronoLedErr = [1,1,1,1]
        self.gameVar.simonErreur = 1
        self.gameVar.calcErreur = 1
        self.gameVar.symboleErreur = 1
        self.gameVar.boutonErreur = 1
        self.gameVar.filErreur = 1
        self.gameVar.lumSimon = [1, 1, 1, 1]
        self.gameVar.symboleLum = [1, 1, 1, 1]
        self.gameVar.boutonBande = [1, 1, 1]
        QTimer().singleShot(50, self.callbackDefaiteBlink)


    def callbackDefaiteBlink(self):
        self.gameVar.chronoLedErr = [0, 0, 0, 0]
        self.gameVar.simonErreur = 0
        self.gameVar.calcErreur = 0
        self.gameVar.symboleErreur = 0
        self.gameVar.boutonErreur = 0
        self.gameVar.filErreur = 0
        self.gameVar.moduleErr = [1, 1, 1, 1, 1]
        self.gameVar.lumSimon = [0, 0, 0, 0]
        self.gameVar.symboleLum = [0, 0, 0, 0]
        self.gameVar.boutonBande = [0, 0, 0]
        self.blink -= 1
        if self.blink > 0:
            QTimer().singleShot(50, self.callbackDefaite)


    def retourMenu(self):
        self.gameVar.reset()

        self.MW.stackSetup.setCurrentIndex(0)
        self.MW.setup.mPrincipal()

    def slot_repaint(self):
        eraseAll(self)
        paintButton(self)

    def slot_win_screenGame(self):
        win(self)

    def exit(self):
        self.ws.exit()



if __name__ == "__main__":
    fullScreen = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "f")
    except getopt.GetoptError:
        print("Option inconnu")
        sys.exit(2)

    for opt, arg in opts:
        print(opt)
        if opt == '-f':
            fullScreen = True

    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    m = MainWindow()
    if fullScreen :
        m.showFullScreen()
    else:
        m.show()
    app.exec_()
