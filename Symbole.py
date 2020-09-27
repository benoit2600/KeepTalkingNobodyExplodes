from PyQt5 import QtCore
from PyQt5.QtCore import QTimer

def initSymbole(gv): # trouve la solution des symboles, en fonction de la position et de l'ID des 4 symboles installés, et des colonnes du manuel

    for col in gv.symboleColonnes: # colonne du manuel
        if all(elem in col for elem in gv.symboleInstalle): # Si les 4 symboles se trouve dans la colonne
            copycol = col.copy()
            if gv.escapeGame == 1:
                copycol.reverse()
            for pos in copycol:
                for val in gv.symboleInstalle:
                    if pos == val:
                        gv.symboleOrdre.append(gv.symboleInstalle.index(val))
            print("symbole ordre : " + str(gv.symboleOrdre))
            return
    raise Exception # Aucune correspondance trouvé.


def checkSymbole(self):
    gv = self.gameVar


    if gv.symboleStep == 4 :
        gv.moduleWin[3] = 1
        gv.symboleLum = [1,1,1,1]
        return

    if gv.symboleBlink == 1:
        return
    if gv.symbolePressed != -1:  # Si un bouton est pressé et non relaché, on attend :
        if max(gv.symboleBtn) == 0:  # on verifie que le bouton a été relaché avant d'effectuer les actions
            gv.symbolePressed = -1
    elif max(gv.symboleBtn) == 1:
        print("Symbole : Bouton appuyé : " + str(gv.symboleBtn))
        gv.symboleErreur = 0
        gv.symbolePressed = gv.symboleBtn.index(1)

        print("gv.symbolePressed : " + str(gv.symbolePressed))
        if gv.symbolePressed == gv.symboleOrdre[gv.symboleStep] :
            gv.symboleStep += 1
            gv.symboleLum[gv.symbolePressed] = 1
        else :  # Erreur
            gv.symboleStep = 0
            gv.symboleErreur = 1
            self.erreurGlobal(3)
            gv.symboleBlinkTimer = QtCore.QTimer()
            gv.symboleBlinkTimer.timeout.connect(lambda: blink(gv))
            gv.symboleBlinkTimer.start(100)
            gv.symboleBlink = 1
            QTimer().singleShot(3000, lambda: shutdownErrorLed(gv))


def blink(gv):
    if gv.symboleBlink == 1:
        if(gv.symboleBlinkEtat == 1):
            gv.symboleLum[gv.symbolePressed] = 1
            gv.symboleBlinkEtat = 0

        else:
            gv.symboleLum[gv.symbolePressed] = 0

            gv.symboleBlinkEtat = 1


def shutdownErrorLed(gv):
    gv.symboleErreur = 0
    gv.symboleBlink = 0
    gv.symboleBlinkTimer.stop()
    gv.symboleLum = [0, 0, 0, 0]