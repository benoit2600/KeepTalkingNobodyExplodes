import random

from PyQt5.QtCore import QTimer


def checkBouton(self):
    gv= self.gameVar

    if gv.moduleWin[4] == 1:
       return
    if gv.boutonErreur == 1:
        return

    if gv.boutonPressed == 1 and gv.boutonRelache == 0:  # Si un bouton est pressé et non relaché, on attend :
        if gv.boutonContact == 0:  # on verifie que le bouton a été relaché avant d'effectuer les actions
            try:
                numChrono = gv.BandeNumChrono[str(gv.boutonNextBande)]
            except:
                numChrono = 3
            print(numChrono)
            if str(numChrono) in gv.chrono[:-1] :
                victoire(gv)
            else:
                print(gv.chrono[:-1])
                erreur(self, gv)
            gv.boutonNextBande = next(gv.boutonCycleCouleurBande)

            gv.boutonBande = [0, 0, 0]
            gv.boutonPressed = 0

    elif gv.boutonPressed == 0 and gv.boutonContact == 1:

        if gv.modeleBtn == 0: #bleu/Annuler:
            bande(gv)
        elif gv.nbPile > 3 and gv.modeleBtn == 1 : # jaune/Exploser
            relache(gv)
        elif gv.modeleBtn == 2 and "CAR" in gv.mentionInstalle == 1 : # Blanc/STOP
            bande(gv)
        elif gv.nbPile > 2 and "FRK" in gv.mentionInstalle == 1 :
            relache(gv)
        elif  gv.modeleBtn == 1:
            bande(gv)
        elif gv.modelBtn == 3: # rouge Maintenir
            relache(gv)
        else:
            bande(gv)

    elif gv.boutonRelache == 1 and gv.boutonContact == 0:
        gv.boutonPressed = 0
        gv.boutonRelache = 0


def victoire(gv):
    gv.moduleWin[4] = 1
    gv.boutonErreur = 0
    print("bouton gagné")


def erreur(self, gv):
    gv.boutonErreur = 1
    print("bouton perdu")
    self.erreurGlobal(4)

    QTimer().singleShot(3000, lambda: stopErreur(gv))

def stopErreur(gv):
    gv.boutonErreur = 0

def bande(gv):
    gv.boutonBande = gv.boutonNextBande

    gv.boutonPressed = 1


def relache(gv):
    gv.boutonPressed = 1
    gv.boutonRelache = 1
    QTimer().singleShot(300, lambda: relacheCallback(gv))


def relacheCallback(gv):
    if gv.boutonContact == 1:
        erreur(gv)
    else:
        victoire(gv)
