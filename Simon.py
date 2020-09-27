from PyQt5.QtCore import QTimer
import random

def initSimon(gv):
    gv.simonLum = []
    randomList = []
    for i in range(gv.simonNbEtape):
        randomList.append(random.randint(0,3))
    for i in range(gv.simonNbEtape):
        gv.simonLum.append([])
        for j in range(i+1):
            gv.simonLum[i].append(randomList[j])

    print(gv.simonLum)
    print(gv.serialNumber.lower())
    for voyelle in "aeiouy" :
        if voyelle in gv.serialNumber.lower():
            gv.simonVoyelle = 0
            return
    gv.simonVoyelle = 1

def checkSimon(self):
    gv = self.gameVar

    if gv.moduleWin[0] == 1:
        gv.lumSimon = [1, 1, 1, 1]
        return

    if gv.simonPressed != -1:  # Si un bouton a été pressé le tour d'avant :

        if max(gv.btnSimon) == 0:  # on verifie que le bouton a été relaché avant d'effectuer les actions
            gv.lumSimon = [0, 0, 0, 0]
            gv.simonLumStep = 0
            gv.simonPressed = -1
        if sum(gv.btnSimon) == 2:
            if gv.btnSimon == [1,0,1,0] :
                gv.pause = 1
                if gv.simonErreur > 0 :
                    gv.simonErreur -= 1
                    gv.nbErreur -= 1
                    gv.moduleErr[0] -= 1
                    for i in range(4):
                        if i < self.gameVar.nbErreur:
                            self.gameVar.chronoLedErr[i] = 1
                        else:
                            self.gameVar.chronoLedErr[i] = 0



    else:
        if max(gv.btnSimon) == 1:  # Si un bouton est pressé, on enregistre son numéro, on l'allume, et on regarde l'etat du jeu
            gv.simonErreur = 0
            gv.simonPressed = gv.btnSimon.index(1)
            level = gv.simonStep[0]
            step = gv.simonStep[1]
            print("simonPressed: " + str(gv.simonPressed) + " level: " + str(level) + " step: " + str(step))
            erreurGlobal = gv.nbErreur
            if erreurGlobal > 2:
                erreurGlobal = 2
            gv.lumSimon = [0, 0, 0, 0]
            gv.lumSimon[gv.simonPressed] = 1
            gv.simonLumStep = 0
            print("gv.simonPressed : " + str(gv.simonPressed))
            print("gv.simonVoyelle : " + str(gv.simonVoyelle))
            print("gv.nbErreur : " + str(gv.nbErreur))


            print("level : " + str(level))
            print("step : " +str(step))
            print("gv.simonLum[level][step] : " + str(gv.simonLum[level][step]))
            print("gv.simonSol[gv.simonVoyelle][erreurGlobal][gv.simonLum[level][step]] : " + str(gv.simonSol[gv.simonVoyelle][erreurGlobal][gv.simonLum[level][step]]))

            if gv.simonPressed == gv.simonSol[gv.simonVoyelle][erreurGlobal][gv.simonLum[level][step]]:  # Bon bouton pressé, on continue

                if len(gv.simonLum[level]) == step + 1:  # fin d'une étape, début d'un nouveau niveau
                    gv.simonStep[0] += 1
                    gv.simonStep[1] = 0
                    gv.simonLumOn = 6
                    if len(gv.simonLum) == gv.simonStep[0]:  # Plus d'autre nivdeau, ON A GAGNEEEEEEEEEEEEEEE !!!!!
                        print("Simon Win !")
                        gv.moduleWin[0] = 1
                else:  # il reste au moins 1 etape, on continued
                    gv.simonStep[1] += 1
                    gv.simonLumOn = 9
            else:  # Perdu !! retour au début
                gv.simonStep = [0,0]
                gv.simonLumOn = 9
                self.erreurGlobal(0)
                gv.simonErreur = 1
                QTimer().singleShot(3000, lambda: shutdownErrorLed(gv))


def shutdownErrorLed(gv):
    gv.simonErreur = 0

#        self.simonSol = [[0], [0, 3], [0, 3, 2], [0, 3, 2, 0]]


def lumiereSimon(gv):
    gv.chrono[4] = str(1 - int(gv.chrono[4])) # hack, changement etat 2 points chrono

    if int(gv.moduleWin[0]) == 1:
        gv.lumSimon = [1, 1, 1, 1]
        return

    if gv.simonPressed == -1:
        level = gv.simonStep[0]
        if gv.simonLumOn != 0:  # lumière ON juste avant, ou fin de la repetition du level
            gv.lumSimon = [0, 0, 0, 0]
            gv.simonLumOn -= 1
        else:
            if gv.simonLumStep == len(gv.simonLum[level]):  # fin repetition
                gv.lumSimon = [0, 0, 0, 0]
                gv.simonLumOn = 3
                gv.simonLumStep = 0
            else:  # en cours de repetition
                gv.lumSimon[gv.simonLum[level][gv.simonLumStep]] = 1
                gv.simonLumOn = 1
                gv.simonLumStep += 1
