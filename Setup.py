# Génération de l'UI
import random
import sys

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import (QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QWidget, QTextEdit)

import ScreenGame
import ui
from gameVar import GameVar
import Chrono


# 2 class : Setup et SetupSymbole

# Setup crée un QWidget, appelé dans la classe MainWindow de main.py. Il est mis dans un QStackedWidget pour pouvoir alterné avec SetupSymbole

# Setup crée un Qwidget composé de 2 colonnes, alors que Setupe Symbole en à 3.

#S'en suit un enchainement de menu :
# Paramètre, Piles, NuméroSerie, Mentions, Fils, Bouton Symbole.
# Chaque appel a un menu démarre par un resetBtn.


class Setup(QWidget):

    def __init__(self, m):
        QWidget.__init__(self)

        self.MW = m
        self.g = m.game
        self.setWindowTitle("Setup")
        self.gameVar = GameVar()
        self.menu = 0
        self.lastSymClicked = -1
        self.lineEdit = QTextEdit()
        font = self.lineEdit.font()  # lineedit current font
        font.setPointSize(20)  # change it's size
        self.lineEdit.setFont(font)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setFixedHeight(100)
        self.lineEdit.setFixedWidth(400)
        self.lineEdit.setStyleSheet("border: 1px solid #1e1e1e;")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        if (self.gameVar.serialOK == 0):
            self.lineEdit.setText("Err Arduino")
        self.btns = []
        self.boxs = []

        for i in range(5):
            box = QHBoxLayout()
            for j in range(2):
                btn= QPushButton("")
                btn.setMaximumHeight(400)
                btn.setFixedHeight(100)
                f = btn.font()
                f.setPointSize(18)
                btn.setFont(f)
                self.btns.append(btn)
                box.addWidget(btn)
            self.boxs.append(box)



        self.linehbox = QHBoxLayout()
        self.linehbox.addWidget(self.lineEdit)
        self.vbox = QVBoxLayout()

        self.vbox.addLayout(self.linehbox)
        for box in self.boxs:
            self.vbox.addLayout(box)

        self.setGeometry(0, 0, 480, 720)
        self.setLayout(self.vbox)
        self.mPrincipal()


    @pyqtSlot()
    def mParametreInstalle(self, nextMenu='mPrincipal'):

        self.resetBtn()
        self.g.checkSensor()

        msg = "Chrono: " + str(self.gameVar.chrono[0])+str(self.gameVar.chrono[1])  + ":" + str(self.gameVar.chrono[2]) + str(self.gameVar.chrono[3])

        if not self.gameVar.chronoBoutonSon :
            msg = "Volume désactivé !"

        nbFilDeco = 0
        for c in self.gameVar.ordreFils :
            if c[0] == "":
                nbFilDeco +=1
        if sum(self.gameVar.etatFils.values()) != nbFilDeco :
            msg = "Fil déconnecté !"
        else:
            couleur = []
            for cables in self.gameVar.ordreFils:
                couleur.append(cables[0][:3])
            self.btns[4].setText("Fils : " + couleur[0] + ", " + couleur[1] + "\n" + str(couleur[2:]))


        self.lineEdit.setText(msg)
        self.btns[0].setText("pile : " + str(self.gameVar.nbPile))
        self.btns[1].setText("S/N : " + str(self.gameVar.serialNumber[:5]) + "...")
        self.btns[2].setText("Symb : " + str(self.gameVar.symboleInstalle[0]) + "   " + str(self.gameVar.symboleInstalle[1]) + " \n            " + str(self.gameVar.symboleInstalle[3]) + "    " + str(self.gameVar.symboleInstalle[2]))
        self.btns[3].setText("Bouton :\n" +  str(self.gameVar.listeBouton[self.gameVar.modeleBtn]))

        self.btns[5].setText("Nb Erreurs :\n" + str(self.gameVar.nbErreurMax))
        self.btns[6].setText("Mentions :\n" + str(self.gameVar.mentionInstalle))
        self.btns[-2].setText("Retour")
        self.btns[-2].clicked.connect(self.mPrincipal)
        self.btns[-1].setText("Suivant")
        self.btns[-1].clicked.connect(getattr(self, nextMenu))



    @pyqtSlot()
    def mEscapeGame(self):
        gv = self.gameVar
        gv.nbPile = 3
        gv.serialNumber = "AG54V6K-DF4SKV5E"
        gv.mentionInstalle = ["FRQ","CAR"]
        gv.ordreFils = [gv.filNoir, gv.filBlanc,gv.filMarron ,gv.filGris, gv.filBleu]
        gv.modeleBtn = 1
        gv.symboleInstalle = [31, 21, 19, 24]
        gv.chrono = [6, 0, 0, 0, 0]
        gv.nbErreurMax = 5
        gv.pause = 1
        gv.escapeGame = 1
        self.simonNbEtape = 5
        self.mParametreInstalle("startGame")

    @pyqtSlot()
    def startGame(self):
        self.resetBtn()
        self.g.start()
        self.MW.stackSetup.setCurrentIndex(2)

    @pyqtSlot()
    def mBombe(self):
        self.resetBtn()
        self.gameVar.escapeGame = 0
        self.mParametreInstalle("startGame")

    def resetBtn(self):
        self.lineEdit.setPalette(self.lineEdit.style().standardPalette())
        self.lineEdit.setStyleSheet("color: #ffffff;border: 1px solid #1e1e1e;")

        for btn in self.btns :
            btn.setText("")
            btn.clicked.connect(self.mRien)
            btn.clicked.disconnect()

        self.repaint()


    @pyqtSlot()
    def mRien(self):
        pass

    @pyqtSlot()
    def setValue(self, var, ret):
        btn = self.sender()
        setattr(self.gameVar, var, btn.value)
        getattr(self, ret)()

    @pyqtSlot()
    def toggleValueFromList(self, var, ret):
        btn = self.sender()
        mVar = getattr(self.gameVar, var)
        if btn.value in mVar:
            mVar.remove(btn.value)
        else:
            mVar.append(btn.value)
        getattr(self, ret)()


    @pyqtSlot()
    def mPrincipal(self):
        self.resetBtn()
        self.lineEdit.setText("Menu Principal")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.btns[0].setText("Paramètres")
        self.btns[0].clicked.connect(self.mParametres)


        self.btns[1].setText("Voir\nParamètres")
        self.btns[1].clicked.connect(self.mParametreInstalle)
        self.btns[2].setText("niveau 1")
        self.btns[2].clicked.connect(lambda : self.niveau(1))
        self.btns[3].setText("niveau 2")
        self.btns[3].clicked.connect(lambda: self.niveau(2))
        self.btns[4].setText("niveau 3")
        self.btns[4].clicked.connect(lambda: self.niveau(3))
        self.btns[5].setText("niveau 4")
        self.btns[5].clicked.connect(lambda: self.niveau(4))
        self.btns[6].setText("niveau 5")
        self.btns[6].clicked.connect(lambda: self.niveau(5))
        self.btns[-3].setText("Jouer")
        self.btns[-3].clicked.connect(self.mBombe)
        self.btns[-2].setText("Quitter")
        self.btns[-2].clicked.connect(self.exit)
        self.btns[-1].setText("Escape Game")
        self.btns[-1].clicked.connect(self.mEscapeGame)

    @pyqtSlot()
    def niveau(self,lvl):
        gv = self.gameVar

        if lvl == 1 :
            gv.nbPile = 2
            gv.serialNumber = "XD7FSRD/SFPJCMLZ"
            gv.mentionInstalle = ["BOB", "CAR"]
            gv.ordreFils = [gv.filNoir, gv.filBlanc, gv.filMarron, gv.filGris, gv.filBleu]
            gv.modeleBtn = 1
            gv.symboleInstalle = [9, 12, 7, 28]
            gv.chrono = [0, 5, 0, 0, 0]
            gv.moduleWin = [1,1,0,0,0]
            gv.nbErreurMax = 5
        if lvl == 2 :
            gv.nbPile = 3
            gv.serialNumber = "AG54V6K-DF4SKV5E"
            gv.mentionInstalle = ["FRK", "FRQ"]
            gv.ordreFils = [gv.filBleu, gv.filRien, gv.filMarron, gv.filGris, gv.filRien]
            gv.modeleBtn = 1
            gv.symboleInstalle = [5, 21, 31, 7]
            gv.chrono = [0, 5, 0, 0, 0]
            gv.moduleWin = [0,1,0,0,0] # Led verte pour : Simon, ScreenGame, fils, symbole, bouton
            gv.nbErreurMax = 5
            gv.simonNbEtape = 3
        if lvl == 3 :
            gv.nbPile = 0
            gv.serialNumber = "1547-439-17H3-28"
            gv.mentionInstalle = ["MSA", "TRN"]
            gv.ordreFils = [gv.filRien,gv.Noir, gv.filRien, gv.filGris, gv.filBlanc]
            gv.modeleBtn = 1
            gv.symboleInstalle = [15, 3, 26, 8]
            gv.chrono = [0, 6, 0, 0, 0]
            gv.moduleWin = [0,0,0,0,0] # Led verte pour : Simon, ScreenGame, fils, symbole, bouton
            gv.nbErreurMax = 4
            gv.simonNbEtape = 4
        if lvl == 4 :
            gv.nbPile = 4
            gv.serialNumber = "DGH4-HV36-ULM4LV"
            gv.mentionInstalle = ["CAR"]
            gv.ordreFils = [gv.filRien, gv.filRien,gv.filRien, gv.filGris, gv.filBlanc]
            gv.modeleBtn = 1
            gv.symboleInstalle = [31, 21, 22, 4]
            gv.chrono = [0, 4, 3, 0, 0]
            gv.moduleWin = [0,0,0,0,0] # Led verte pour : Simon, ScreenGame, fils, symbole, bouton
            gv.nbErreurMax = 3
            gv.simonNbEtape = 4
        if lvl == 5 :
            gv.nbPile = 1
            gv.serialNumber = "1547-439-17H3-28"
            gv.mentionInstalle = ["BOB", "MSA"]
            gv.ordreFils = [gv.filGris, gv.filBlanc,gv.filNoir, gv.filMarron, gv.filBleu]
            gv.modeleBtn = 1
            gv.symboleInstalle = [31, 21, 22, 4]
            gv.chrono = [0, 4, 0, 0, 0]
            gv.moduleWin = [0,0,0,0,0] # Led verte pour : Simon, ScreenGame, fils, symbole, bouton
            gv.nbErreurMax = 2
            gv.simonNbEtape = 5

        self.mBombe()


    @pyqtSlot()
    def exit(self):
        sys.exit(0)

    @pyqtSlot()
    def mParametres(self):
        self.resetBtn()
        self.lineEdit.setText("Accessoires")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.btns[0].setText("piles")
        self.btns[0].clicked.connect(self.mPile)
        self.btns[1].setText("Num Série")
        self.btns[1].clicked.connect(self.mNumSerie)
        self.btns[2].setText("Mentions")
        self.btns[2].clicked.connect(self.mMentions)
        self.btns[3].setText("Fils")
        self.btns[3].clicked.connect(self.mFils)
        self.btns[4].setText("Bouton")
        self.btns[4].clicked.connect(self.mBouton)
        self.btns[5].setText("Symbole")
        self.btns[5].clicked.connect(self.mSymbole)
        self.btns[6].setText("Chrono")
        self.btns[6].clicked.connect(self.mChrono)
        self.btns[7].setText("Nb Erreur")
        self.btns[7].clicked.connect(self.mNbErreur)

        self.btns[-2].setText("Retour")
        self.btns[-2].clicked.connect(self.mPrincipal)
        self.btns[-1].setText("Suivant")
        self.btns[-1].clicked.connect(self.mPrincipal)


    @pyqtSlot()
    def mPile(self):
        self.resetBtn()
        self.lineEdit.setText("Pile : "+str(self.gameVar.nbPile))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.resetBtn()
        self.menu = 2
        for i in range(5):
            self.btns[i].setText(str(i))
            self.btns[i].value = i
            self.btns[i].clicked.connect(lambda: self.setValue("nbPile", "mPile"))

        self.btns[-2].setText("Retour")
        self.btns[-2].clicked.connect(self.mParametres)
        self.btns[-1].setText("Suivant")
        self.btns[-1].clicked.connect(self.mNumSerie)


    @pyqtSlot()
    def mNumSerie(self):
        self.resetBtn()
        self.lineEdit.setText("ID Num Série : " + str(self.gameVar.serialNumber))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        for sn,btn in zip(self.gameVar.listeSerialNumber,self.btns[:-2]):
            btn.setText(sn[:5] + "...")
            btn.value = sn
            btn.clicked.connect(lambda: self.setValue("serialNumber", "mNumSerie"))
        self.btns[-2].setText("Retour")
        self.btns[-2].clicked.connect(self.mParametres)
        self.btns[-1].setText("Suivant")
        self.btns[-1].clicked.connect(self.mMentions)


    @pyqtSlot()
    def mMentions(self):
        self.resetBtn()
        self.lineEdit.setText("Mention Active : " + str(self.gameVar.mentionInstalle))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        for ment, btn in zip(self.gameVar.mentionDispo, self.btns[:-2]):
            btn.setText(ment)
            btn.value = ment
            btn.clicked.connect(lambda: self.toggleValueFromList("mentionInstalle","mMentions"))
        self.btns[-2].setText("Retour")
        self.btns[-2].clicked.connect(self.mParametres)
        self.btns[-1].setText("Suivant")
        self.btns[-1].clicked.connect(self.mFils)

    @pyqtSlot()
    def mFils(self):
        self.resetBtn()
        couleur = []
        for cables in self.gameVar.ordreFils:
            couleur.append(cables[0])
        self.lineEdit.setText("Ordre Cables : " + str(couleur))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        for i, btn in zip(range(5), self.btns[:-3]):
            btn.setText("Emplacement " + str(i + 1))
            btn.value =  i
            btn.clicked.connect(self.mCouleurFils)

        self.btns[-3].clicked.connect(self.setCouleurFil)
        self.btns[-2].setText("Retour")
        self.btns[-2].clicked.connect(self.mParametres)
        self.btns[-1].setText("Suivant")
        self.btns[-1].clicked.connect(self.mBouton)


    @pyqtSlot()
    def mCouleurFils(self):
        btnClicked = self.sender()
        print(btnClicked.value)
        self.resetBtn()
        for fil,btn in zip(self.gameVar.filDispo, self.btns[:-2]):
            btn.setText(str(fil[0]))
            btn.value = btnClicked.value
            btn.fil = fil
            btn.clicked.connect(self.setCouleurFil)

        self.btns[-3].setText("Rien")
        self.btns[-3].fil = -1
        self.btns[-3].value = btnClicked.value
        self.btns[-3].clicked.connect(self.setCouleurFil)


    @pyqtSlot()
    def setCouleurFil(self):
        btnClicked = self.sender()
        print(btnClicked.value)
        if btnClicked.fil == -1:
            print("btnClicked.value == -1")
            self.gameVar.ordreFils[btnClicked.value] = self.gameVar.filRien
        else:
            print("else")
            if len(self.gameVar.ordreFils) <= btnClicked.value :
                self.gameVar.ordreFils.append(btnClicked.fil)
            else:
                self.gameVar.ordreFils[btnClicked.value] = btnClicked.fil
        self.mFils()

    @pyqtSlot()
    def mBouton(self):
        self.resetBtn()
        self.lineEdit.setText("Modèle Bouton :\n" + str(self.gameVar.listeBouton[self.gameVar.modeleBtn]))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        for idBtn,btn in zip(self.gameVar.listeBouton,self.btns[:-2]):
            btn.setText(idBtn)
            btn.value = self.gameVar.listeBouton.index(idBtn)
            btn.clicked.connect(lambda: self.setValue("modeleBtn", "mBouton"))

        self.btns[-2].setText("Retour")
        self.btns[-2].clicked.connect(self.mParametres)
        self.btns[-1].setText("Suivant")
        self.btns[-1].clicked.connect(self.mSymbole)

    def chkSymbole(self):
        gv = self.gameVar
        for col in gv.symboleColonnes:  # colonne du manuel
            if all(elem in col for elem in gv.symboleInstalle):  # Si les 4 symboles se trouve dans la colonne
                return True
        return False

    @pyqtSlot()
    def symboleAleatoire(self):
        self.gameVar.symboleInstalle = random.sample(random.choice(self.gameVar.symboleColonnes), 4)
        self.mSymbole()

    @pyqtSlot()
    def mSymbole(self):
        self.resetBtn()
        if self.chkSymbole(): # Si les 4 symboles se trouve dans la colonne
            self.lineEdit.setText("Symbole OK")
            self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        else:
            if not 0 in self.gameVar.symboleInstalle :
                print(self.gameVar.symboleInstalle)
                pRed = QPalette()
                pRed.setColor(QPalette.Base, Qt.red)
                self.lineEdit.setPalette(pRed)
                self.lineEdit.setText("Combinaison de symbole impossible")
            elif self.gameVar.symboleInstalle.count(0) <= 3 : # aide si tout les symboles ne sont pas encore choisi
                symbolePossible = []
                for col in self.gameVar.symboleColonnes:
                    listSansZero = list(filter((0).__ne__, self.gameVar.symboleInstalle))
                    if all(x in col for x in listSansZero) :
                        symbolePossible.extend([x for x in col if x not in listSansZero])
                if len(symbolePossible) != 0:
                    symbolePossibleAleatoire = random.sample(symbolePossible, len(symbolePossible))
                    self.lineEdit.setText("Sym possible : " + str(symbolePossibleAleatoire))
                else:
                    self.lineEdit.setText("Aucune combinaison possible")
            else:
                self.lineEdit.setText("Symbole")
            self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.btns[0].setText(str(self.gameVar.symboleInstalle[0]))
        self.btns[0].value = 0
        self.btns[0].clicked.connect(self.callmSymbole)

        self.btns[1].setText(str(self.gameVar.symboleInstalle[1]))
        self.btns[1].value = 1
        self.btns[1].clicked.connect(self.callmSymbole)

        self.btns[2].setText(str(self.gameVar.symboleInstalle[3]))
        self.btns[2].value = 3
        self.btns[2].clicked.connect(self.callmSymbole)

        self.btns[3].setText(str(self.gameVar.symboleInstalle[2]))
        self.btns[3].value = 2
        self.btns[3].clicked.connect(self.callmSymbole)

        self.btns[-3].setText("Aleatoire")
        self.btns[-3].clicked.connect(self.symboleAleatoire)
        self.btns[-2].setText("Retour")
        self.btns[-2].clicked.connect(self.mParametres)
        self.btns[-1].setText("Suivant")
        self.btns[-1].clicked.connect(self.mChrono)


    @pyqtSlot()
    def callmSymbole(self):
        btnClicked = self.sender()
        self.resetBtn()
        self.lastSymClicked = btnClicked.value
        self.MW.stackSetup.setCurrentIndex(1)
        self.MW.setupSymbole.mSetSymbole()

    @pyqtSlot()
    def mChrono(self):
        self.resetBtn()
        self.lineEdit.setText("Chrono: " + str(self.gameVar.chrono[0])+str(self.gameVar.chrono[1])  + ":" + str(self.gameVar.chrono[2]) + str(self.gameVar.chrono[3]))
        self.btns[0].setText("-1")
        self.btns[0].value = ("chronoMoins", 1)
        self.btns[0].clicked.connect(self.msetChrono)
        self.btns[1].setText("+1")
        self.btns[1].value = ("chronoPlus", 1)
        self.btns[1].clicked.connect(self.msetChrono)
        self.btns[2].setText("-5")
        self.btns[2].value = ("chronoMoins", 5)
        self.btns[2].clicked.connect(self.msetChrono)
        self.btns[3].setText("+5")
        self.btns[3].value = ("chronoPlus", 5)
        self.btns[3].clicked.connect(self.msetChrono)
        self.btns[4].setText("-10")
        self.btns[4].value = ("chronoMoins", 10)
        self.btns[4].clicked.connect(self.msetChrono)
        self.btns[5].setText("+10")
        self.btns[5].value = ("chronoPlus", 10)
        self.btns[5].clicked.connect(self.msetChrono)
        self.btns[-2].setText("Retour")
        self.btns[-2].clicked.connect(self.mParametres)
        self.btns[-1].setText("Suivant")
        self.btns[-1].clicked.connect(self.mNbErreur)
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

    @pyqtSlot()
    def msetChrono(self):
        btnClicked = self.sender()
        c = Chrono
        s = getattr(c, btnClicked.value[0])
        s(self.g, btnClicked.value[1])
        self.mChrono()

    @pyqtSlot()
    def mNbErreur(self):
        self.resetBtn()
        self.lineEdit.setText("Nb erreur : " + str(self.gameVar.nbErreurMax))
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)

        for i, btn in zip(range(1,6),self.btns[:-2]):
            btn.setText(str(i))
            btn.value = i
            btn.clicked.connect(self.mSetNbErreur)

        self.btns[-2].setText("Retour")
        self.btns[-2].clicked.connect(self.mParametres)
        self.btns[-1].setText("Suivant")
        self.btns[-1].clicked.connect(self.mParametres)

    @pyqtSlot()
    def mSetNbErreur(self):
        btnClicked = self.sender()
        self.gameVar.nbErreurMax = btnClicked.value
        self.mNbErreur()

class SetupSymbole(QWidget):
    def __init__(self, m):
        QWidget.__init__(self)
        self.MW = m
        self.chiffreTemp = ""
        self.gameVar = GameVar()
        self.lineEdit = QLineEdit("")
        font = self.lineEdit.font()  # lineedit current font
        font.setPointSize(30)  # change it's size
        self.lineEdit.setFont(font)

        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setFixedHeight(100)
        self.lineEdit.setFixedWidth(400)
        self.btnsSymbole = []
        self.boxsSymbole = []

        for i in range(4):
            box = QHBoxLayout()
            for j in range(3):
                btn= QPushButton("")
                f = btn.font()
                f.setPointSize(20)
                btn.setFont(f)
                btn.setMaximumHeight(400)
                btn.setFixedHeight(100)

                self.btnsSymbole.append(btn)
                box.addWidget(btn)
            self.boxsSymbole.append(box)

        self.linehboxSymbole = QHBoxLayout()
        self.linehboxSymbole.addWidget(self.lineEdit)
        self.vboxSymbole = QVBoxLayout()

        self.vboxSymbole.addLayout(self.linehboxSymbole)
        for box in self.boxsSymbole:
            self.vboxSymbole.addLayout(box)

        self.setGeometry(0, 0, 416, 720)
        self.setLayout(self.vboxSymbole)

    def resetBtn(self):
        for btn in self.btnsSymbole :
            btn.setText("")
            btn.clicked.connect(self.mRien)
            btn.clicked.disconnect()
        self.repaint()

    @pyqtSlot()
    def mRien(self):
        pass

    @pyqtSlot()
    def mSetSymbole(self):
        self.resetBtn()

        self.chiffreTemp = ""
        self.lineEdit.setText(self.chiffreTemp)

        print(self.MW.setup.lastSymClicked)
        for i in range(0,9) :
            self.btnsSymbole[i].setText(str(i+1))
            self.btnsSymbole[i].value = i+1
            self.btnsSymbole[i].clicked.connect(self.chiffre)

        self.btnsSymbole[i + 1].setText("0")
        self.btnsSymbole[i + 1].value = 0
        self.btnsSymbole[i + 1].clicked.connect(self.chiffre)

        self.btnsSymbole[i+2].setText("<-")
        self.btnsSymbole[i+2].value = -1
        self.btnsSymbole[i+2].clicked.connect(self.chiffre)

        self.btnsSymbole[i+3].setText("Valider")
        self.btnsSymbole[i+3].value = -2
        self.btnsSymbole[i+3].clicked.connect(self.chiffre)


    @pyqtSlot()
    def chiffre(self):
        btnClicked = self.sender()
        try:
            if btnClicked.value == -2: # OK
                print("clic")
                if self.chiffreTemp != "" :
                    for col in self.gameVar.symboleColonnes :
                        if int(self.chiffreTemp) in col or int(self.chiffreTemp) == 0: # Ajout si Numéro symbole existant
                            self.gameVar.symboleInstalle[self.MW.setup.lastSymClicked] = int(self.chiffreTemp)
                            print("break")
                            break
                    self.chiffreTemp = ""
                self.mRetourSetupSymbole()
                return
            elif btnClicked.value == -1: # effacer
                self.chiffreTemp = self.chiffreTemp[:-1]
            else:
                self.chiffreTemp += str(btnClicked.value)
        except:
            pass
        self.lineEdit.setText(self.chiffreTemp)

    @pyqtSlot()
    def mRetourSetupSymbole(self):
        self.resetBtn()
        self.MW.stackSetup.setCurrentIndex(0)
        self.MW.setup.mSymbole() # retour au setup avec 2 colonnes

    @pyqtSlot()
    def mRetourSetupPrincipal(self):
        self.resetBtn()
        self.MW.stackSetup.setCurrentIndex(0)
        self.MW.setup.mPrincipal()