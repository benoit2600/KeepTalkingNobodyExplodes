from PyQt5.QtCore import QTimer

import StressMode

def chrono(self):
    if self.gameVar.pause:
        return

    self.gameVar.nbSecGlobal += 1

    if self.gameVar.nbErreur == 5 :
        if self.gameVar.errBlink :
            self.gameVar.chronoLedErr = [1,1,1,1]
            self.gameVar.errBlink = False
        else :
            self.gameVar.chronoLedErr = [0, 0, 0, 0]
            self.gameVar.errBlink = True

    if self.gameVar.erreurChrono:
        return

    if sum(self.gameVar.moduleWin) == 5 and self.gameVar.escapeGame == 1:
        StressMode.StressModeInit(self)

    elif sum(self.gameVar.moduleWin) == 5 and self.gameVar.escapeGame == 0:
        self.victoire()

    min = int(self.gameVar.chrono[0]) * 10 + int(self.gameVar.chrono[1])
    sec = int(self.gameVar.chrono[2]) * 10 + int(self.gameVar.chrono[3])
    if (min < 0 and sec < 0):
        return

    if (sec > 0):
        sec -= 1
    else:
        min -= 1
        sec = 59

    if sec == 0 and min == 0 :
        self.gameVar.chrono = [0,0,0,0,1]
        self.defaite()

    self.gameVar.chrono[0] = str(int(min / 10))
    self.gameVar.chrono[1] = str(int(min % 10))
    self.gameVar.chrono[2] = str(int(sec / 10))
    self.gameVar.chrono[3] = str(int(sec % 10))



def chronoPlus(self, min, sec = 0):
    minT = int(self.gameVar.chrono[0]) * 10 + int(self.gameVar.chrono[1])
    minT += min
    self.gameVar.chrono[0] = str(int(minT / 10))
    self.gameVar.chrono[1] = str(int(minT % 10))


def chronoMoins(self, min, sec = 0):
    minT = int(self.gameVar.chrono[0]) * 10 + int(self.gameVar.chrono[1])
    minT -= min

    if minT < 0 :
        self.gameVar.chrono = [0, 0, 0, 1, 1]
    else:
        self.gameVar.chrono[0] = str(int(minT / 10))
        self.gameVar.chrono[1] = str(int(minT % 10))


def removeXmMin(self, minR, secR=0):
    if self.gameVar.chrono[0] == "-" or self.gameVar.erreurChrono == True: # déjà en erreur
        return

    self.gameVar.erreurChrono = True

    min = int(self.gameVar.chrono[0]) * 10 + int(self.gameVar.chrono[1])
    min -= minR
    sec = int(self.gameVar.chrono[2]) * 10 + int(self.gameVar.chrono[3]) - 3
    sec -= secR
    if sec < 0 :
        sec = 59
        min -= 1

    if (min < 0):
        self.gameVar.chrono = [0, 0, 0, 0, 0]
        self.gameVar.erreurChrono = False
        self.defaite()
    else:
        self.gameVar.chronoBlink = 1
        self.gameVar.chronoLum = 2
        QTimer().singleShot(3000, lambda: removeXmMinCallback(self, min, sec))

        self.gameVar.chrono = ["-", str(minR), "0", "0", "1"]


def removeXmMinCallback(self, min, sec):
    self.gameVar.chronoBlink = 0
    self.gameVar.chronoLum = 1

    self.gameVar.erreurChrono = False
    self.gameVar.chrono[0] = str(int(min / 10))
    self.gameVar.chrono[1] = str(int(min % 10))
    self.gameVar.chrono[2] = str(int(sec / 10))
    self.gameVar.chrono[3] = str(int(sec % 10))