# a renommer ?
# Contient la logique du jeu calculette

from PyQt5.QtCore import QTimer

import random

def guess(self, btn):
    gv = self.gameVar
    if not gv.screenGameReady :
        return

    if  gv.defaite or gv.stressMode:
        return

    if gv.pause :
        gv.pause = 0
        return


    gv.calcErreur = 0
    gv.screenGameReady = False

    if (btn == self.btns[gv.placeMotVictoire]):
        print("good guess")
        if gv.calcTour < 3 :
            goodGuess(self)
        else:
            win(self)

    else:
        print("bad guess")
        badGuess(self)



def shutdownErrorLed(self):
    self.gameVar.calcErreur = 0

def win(self):
    eraseAll(self, 0)
    self.lineEdit.setText("Module OK")
    self.gameVar.moduleWin[1] = 1
    self.gameVar.calcTour = 4

def badGuess(self):
    eraseAll(self)
    self.gameVar.calcErreur = 1
    self.erreurGlobal(1)

    QTimer().singleShot(3000, lambda: shutdownErrorLed(self))

    if self.gameVar.calcTour > 0:
        self.gameVar.calcTour -= 1
    QTimer().singleShot(2000, lambda: paintButton(self))
    # paintButton(self)


def goodGuess(self):
    eraseAll(self)
    self.gameVar.calcTour += 1
    QTimer().singleShot(1000, lambda: paintButton(self))


def eraseAll(self, delay=0.1):
    self.lineEdit.setText("")
    for btn in self.btns:
        btn.setText("")
        self.repaint()


def paintButton(self, delay=0.1):
    gv = self.gameVar
    #
    #  |--------------------------------|
    #  |        motEtape1               |
    #  |                                |
    #  |  Alea1          motVictoire    |
    #  |                                |
    #  |  Alea2          Alea3          |
    #  |                                |
    #  |  motEtape2      Alea4          |
    #  |                                |
    #  |--------------------------------|

    # Grande étapes :
    # 1   Choix du mot de l'étape 2 depuis une liste
    # 2 Choix du mot de l'etape 1 en fonction du placement (aleatoire du mot etape2)
    # 3 définition du mot victoire
    # 4 recherches des autres mots aleatoires sachant que :
    #    a. Ces mot doivent se trouver après le mot victoire dans la liste (d'ou le listeMotsTronque pour choisir le mot victoire, afin d'etre sur d'avoir encore des mots aleatoires
    #    b. Le mot victoire peut être le meme que le mot etape2
    #    c.
    motsBtn = ["","","","","",""]
    idMotEtape2 = random.randint(0,len(self.gameVar.listeMots) - 1)
    gv.motEtape2 =  motEtape2 = self.gameVar.listeMots[idMotEtape2]
    print("idMotEtape2 : " + str(idMotEtape2))
    print("motEtape2 : " + str(motEtape2))

    listeMots = self.gameVar.listeMatrice[idMotEtape2] # Liste à suivre pour le choix des mots a afficher
    print("listeMot : " + str(listeMots))

    gv.PlaceMotEtape2 = PlaceMotEtape2 = random.randint(0, 5)
    print("PlaceMotEtape2 : " + str(PlaceMotEtape2))

    motsBtn[PlaceMotEtape2] = motEtape2

    gv.motEtape1 = motEtape1 = random.choice(self.gameVar.listeLibelle[PlaceMotEtape2])
    print("motEtape1 : " + str(motEtape1))
    self.lineEdit.setText(motEtape1)

    listeMotsTronque = listeMots[:-7]
    if motEtape2 in listeMotsTronque: # Si le motEtape2 est encore dans la liste, le mot victoire doit se trouver avant la place du motEtape2
        motVictoire = random.choice(listeMotsTronque[:listeMotsTronque.index(motEtape2)+1])
    else:
        motVictoire = random.choice(listeMotsTronque)
    print("mot Victoire : " + str(motVictoire))
    gv.motVictoire = motVictoire
    if motVictoire == motEtape2 :
        self.gameVar.placeMotVictoire = PlaceMotEtape2
    else:
        self.gameVar.placeMotVictoire = random.choice([i for i, value in enumerate(motsBtn) if value == ""])  # On place le mot victoire dans un bouton encore non attribué
        motsBtn[self.gameVar.placeMotVictoire] = motVictoire
    print("placeMotVictoire : " + str(self.gameVar.placeMotVictoire))

    ListeMotRestant = listeMots[listeMots.index(motVictoire) +1 :]
    try:
        ListeMotRestant.remove(motEtape2)
    except:
        pass
    random.shuffle(ListeMotRestant)
    print("ListeMotRestant Shuffle : " + str(ListeMotRestant))
    iterListeMotRestantShuffle = iter(ListeMotRestant)

    while(len([j for j, value in enumerate(motsBtn) if value == ""]) != 0): # tant qu'il y a des boutons sans mots:
        motsBtn[random.choice([j for j, value in enumerate(motsBtn) if value == ""])] = next(iterListeMotRestantShuffle)

    print("motsBtn  : " + str(motsBtn))
    self.gameVar.calcMotBtns = motsBtn
    self.repaint()
    print("repaint")
    QTimer().singleShot(2000, lambda: paintButtonAfterDelay(self, motsBtn))

    def paintButtonAfterDelay(self, lesMots, delay=0.1):
        for btn, mot in zip(self.btns,lesMots) :
            btn.setText(mot)
            self.repaint()
        self.gameVar.screenGameReady = True
