# toutes les variables utilisés par la bombe
import random
from itertools import cycle

from PyQt5.QtMultimedia import QSound


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class GameVar(metaclass=Singleton):

    def __init__(self):
        # Position des boutons : 0 Haut Gauche, 1 Haut Droit, 2 Milieu Gauche, 3 Milieu Droit, 4 Bas Gauche, 5 Bas Droit.

        self.listeMots= ["PRÊT","PREMIER", "NON","VIDE", "RIEN", "OUI", "EUX", "EUHHH", "GAUCHE", "DROITE", "MILIEU", "E", "ATTENDS", "APPUIE", "TOI", "THON", "TON", "TONS", "T'ES","TES", "AVANT", "QUOI", "QUOI ?", "FAIT", "SUIVANT", "MAINTIENS", "OK", "COMME"]
        self.listeMatrice = [['OUI', 'E', 'EUX', 'MILIEU', 'GAUCHE', 'APPUIE', 'DROITE', 'VIDE', 'PRÊT', 'NON', 'PREMIER', 'EUHHH', 'RIEN', 'ATTENDS'],
                            ['GAUCHE', 'E', 'OUI', 'MILIEU', 'NON', 'DROITE', 'RIEN', 'EUHHH', 'ATTENDS', 'PRÊT', 'VIDE', 'EUX', 'APPUIE', 'PREMIER'],
                            ['VIDE', 'EUHHH', 'ATTENDS', 'PREMIER', 'EUX', 'PRÊT', 'DROITE', 'OUI', 'RIEN', 'GAUCHE', 'APPUIE', 'E', 'NON', 'MILIEU'],
                            ['ATTENDS', 'DROITE', 'E', 'MILIEU', 'VIDE', 'APPUIE', 'PRÊT', 'RIEN', 'NON', 'EUX', 'GAUCHE', 'EUHHH', 'OUI', 'PREMIER'],
                            ['EUHHH', 'DROITE', 'E', 'MILIEU', 'OUI', 'VIDE', 'NON', 'APPUIE', 'GAUCHE', 'EUX', 'ATTENDS', 'PREMIER', 'RIEN', 'PRÊT'],
                            ['E', 'DROITE', 'EUHHH', 'MILIEU', 'PREMIER', 'EUX', 'APPUIE', 'PRÊT', 'RIEN', 'OUI', 'GAUCHE', 'VIDE', 'NON', 'ATTENDS'],
                            ['EUHHH', 'EUX', 'GAUCHE', 'RIEN', 'PRÊT', 'VIDE', 'MILIEU', 'NON', 'E', 'PREMIER', 'ATTENDS', 'OUI', 'APPUIE', 'DROITE'],
                            ['PRÊT', 'RIEN', 'GAUCHE', 'EUX', 'E', 'OUI', 'DROITE', 'NON', 'APPUIE', 'VIDE', 'EUHHH', 'MILIEU', 'ATTENDS', 'PREMIER'],
                            ['DROITE', 'GAUCHE', 'PREMIER', 'NON', 'MILIEU', 'OUI', 'VIDE', 'EUX', 'EUHHH', 'ATTENDS', 'APPUIE', 'PRÊT', 'E', 'RIEN'],
                            ['OUI', 'RIEN', 'PRÊT', 'APPUIE', 'NON', 'ATTENDS', 'EUX', 'DROITE', 'MILIEU', 'GAUCHE', 'EUHHH', 'VIDE', 'E', 'PREMIER'],
                            ['VIDE', 'PRÊT', 'E', 'EUX', 'RIEN', 'APPUIE', 'NON', 'ATTENDS', 'GAUCHE', 'MILIEU', 'DROITE', 'PREMIER', 'EUHHH', 'OUI'],
                            ['MILIEU', 'NON', 'PREMIER', 'OUI', 'EUHHH', 'RIEN', 'ATTENDS', 'E', 'GAUCHE', 'PRÊT', 'VIDE', 'APPUIE', 'EUX', 'DROITE'],
                            ['EUHHH', 'NON', 'VIDE', 'E', 'OUI', 'GAUCHE', 'PREMIER', 'APPUIE', 'EUX', 'ATTENDS', 'RIEN', 'PRÊT', 'DROITE', 'MILIEU'],
                            ['DROITE', 'MILIEU', 'OUI', 'PRÊT', 'APPUIE', 'E', 'RIEN', 'EUHHH', 'VIDE', 'GAUCHE', 'PREMIER', 'EUX', 'NON', 'ATTENDS'],
                            ['OK', 'THON', 'TON', 'TONS', 'SUIVANT', 'AVANT', "T'ES", 'MAINTIENS', 'QUOI ?', 'TOI', 'QUOI', 'COMME', 'FAIT', 'TES'],
                            ['TON', 'SUIVANT', 'COMME', 'AVANT', 'QUOI ?', 'FAIT', 'QUOI', 'MAINTIENS', 'TOI', 'TES', 'TONS', 'OK', "T'ES", 'THON'],
                            ['QUOI', 'THON', 'AVANT', 'TON', 'SUIVANT', "T'ES", 'OK', 'TES', 'TONS', 'TOI', 'QUOI ?', 'MAINTIENS', 'COMME', 'FAIT'],
                            ['TOI', 'TONS', "T'ES", 'SUIVANT', 'QUOI', 'THON', 'TES', 'TON', 'QUOI ?', 'AVANT', 'OK', 'FAIT', 'COMME', 'MAINTIENS'],
                            ['FAIT', 'TES', "T'ES", 'AVANT', 'QUOI ?', 'OK', 'TON', 'MAINTIENS', 'TONS', 'COMME', 'SUIVANT', 'QUOI', 'THON', 'TOI'],
                            ['AVANT', 'OK', 'SUIVANT', 'QUOI ?', 'TONS', "T'ES", 'QUOI', 'FAIT', 'TES', 'TOI', 'COMME', 'MAINTIENS', 'THON', 'TON'],
                            ['AVANT', 'TON', 'THON', 'TOI', 'FAIT', 'MAINTIENS', 'QUOI', 'SUIVANT', 'OK', 'COMME', 'TONS', "T'ES", 'TES', 'QUOI ?'],
                            ["T'ES", 'TES', 'THON', 'TONS', 'SUIVANT', 'QUOI', 'FAIT', 'TOI', 'AVANT', 'COMME', 'TON', 'OK', 'MAINTIENS', 'QUOI ?'],
                            ['TOI', 'MAINTIENS', 'TONS', 'TON', 'TES', 'FAIT', 'QUOI', 'COMME', 'THON', 'AVANT', "T'ES", 'SUIVANT', 'QUOI ?', 'OK'],
                            ['OK', 'AVANT', 'SUIVANT', 'QUOI ?', 'TON', "T'ES", 'TONS', 'MAINTIENS', 'COMME', 'TOI', 'TES', 'THON', 'QUOI', 'FAIT'],
                            ['QUOI ?', 'AVANT', 'QUOI', 'TON', 'MAINTIENS', 'OK', 'SUIVANT', 'COMME', 'FAIT', 'THON', "T'ES", 'TONS', 'TES', 'TOI'],
                            ['THON', 'TES', 'FAIT', 'QUOI', 'TOI', "T'ES", 'OK', 'QUOI ?', 'TONS', 'SUIVANT', 'MAINTIENS', 'AVANT', 'TON', 'COMME'],
                            ['THON', 'FAIT', 'COMME', 'TONS', 'TOI', 'MAINTIENS', 'AVANT', "T'ES", 'OK', 'TES', 'QUOI ?', 'SUIVANT', 'TON', 'QUOI'],
                            ['TONS', 'SUIVANT', 'TES', "T'ES", 'MAINTIENS', 'FAIT', 'QUOI', 'QUOI ?', 'AVANT', 'TOI', 'COMME', 'OK', 'THON', 'TON']] # Correspond aux mots du manuel

        # ListeLibelle trié par position du bouton annonçant la liste de mot (ex : Mot a trouvé au bouton Milieu gauche (2) -> choix de mot ["RIEN","MOT", "VERT"]
        self.listeLibelle = [["THON"], ["PREMIER", "OK", "C"],["RIEN","MOT", "VERT"],["VIDE","BOUGE","ROUGE", "TES", "TON", "TONS", "VERS"],["AU", "EAU", "HAUT"],["VERRE", "MOTS", "NON", "MAUX","ATTENDS","T'ES","TU ES","C'EST","VER"]]

        self.simonLum = [[0], [0, 3], [0, 3, 2], [0, 3, 2, 1]] # Lumière a affiché (exemple donné ici, la génération se fait dans Simon.initSimon() )
        self.simonSol = [ [[3,2,1,0],[2,3,0,1],[3,0,1,2]]  ,  [[1,3,2,0],[0,2,1,3],[2,3,0,1]] ]  #voyelle, nb erreur, correspondance numero clignotant -> bouton appuyé
        self.simonNbEtape = 5
        self.filBlanc = ["blanc", ["b","r","v"]] # Bleu, Rouge, Vert
        self.filBleu = ["bleu", ["b","w","v"]] # Bleu, Blanc (White), Vert
        self.filMarron = ["marron", ["b","j","r"]] #Bleu, Jaune, Rouge
        self.filNoir = ["noir", ["n","w","r"]] # Noir, Blanc, Rouge
        self.filGris = ["gris", ["b","j","w"]] # Bleu, Jaune, Blanc
        self.filRien = ["", ""]  # pas de fil

        self.filDispo = [self.filNoir, self.filBlanc,self.filMarron ,self.filGris, self.filBleu]
        self.ordreFils = [] # fil placé sur la bombe. Exemple ici, modifiable dans le menu paramètre.
        self.nbFilConnecte = 0 # calculé en fonction du nombre de fils connecté (voir ordreFils)
        self.indexFilsConnecte = []
        self.symboleColonnes = [[28, 13, 30, 12, 7, 9, 23],[16, 28, 23, 26, 3, 9, 20],[1, 8, 26, 5, 15, 30, 3],[11, 21, 31, 7, 5, 20, 4],[24,4, 31, 22, 21, 19, 2],[11, 16, 27, 14, 24, 18, 6]] # colonne du manuel
        self.symboleInstalle = [0, 0, 0, 0]  # ID des Symboles installe sur la bombe dans cette ordre : haut gauche, haut droit, bas droit, bas gauche
        self.listeBouton = ["Bleu Annuler", "Jaune Exploser", "Blanc Stop", "Rouge Maintenir"]

        self.boutonListeCouleur = [[1,0,0],[0,1,0],[0,0,1],[1,1,0],[1,0,1],[1,1,1]]  # couleurs (R,G,B) disponibles pour la bande du module Bouton
        self.modeleBtn = 0
        random.shuffle(self.boutonListeCouleur)
        self.boutonCycleCouleurBande = cycle(self.boutonListeCouleur)
        self.boutonNextBande = next(self.boutonCycleCouleurBande)  # Bidouille utilisé pour eviter qu'une meme couleur de bande soit utilisé dans une partie (pas obligatoire, mais plus rigolo)

        self.BandeNumChrono = {"[0, 0, 1]" : 4,"[1, 1, 1]" : 1,"[0, 1, 0]" : 5, "[1, 0, 0]" : 7} # correspondance couleur -> chiffre devant etre présent dans le chrono (selon le manuel). Si la couleur n'est pas dans la liste, defaut a 3 (voir Bouton.checkBouton)
        self.nbErreurMax = 4 # Nombre d'erreur autorisé avant explosion (modifiable dans paramètres)
        self.listeSerialNumber = ["AG54V6K-DF4SKV5E","DGH4-HV36-ULM4LV", "XD7FSRD/SFPJCMLZ","1547-439-17H3-28"] # liste des numéro de série imprimé en 3D disponibles
        self.serialNumber = ""  # Numéro de série choisi. Définit dans le setup, avant le lancement du jeu
        self.nbPile = 0 # nb de pile sur la bombe. Réglable dans paramètres
        self.mentionDispo = ["FRK","FRQ","CAR","MSA","BOB","TRN"]
        self.mentionInstalle = []
        self.chronoBoutonSon = 0  # etat du bouton du module chrono. Emet un son si à 1 (voir main.bip() )
        self.nbSecGlobal = 0  # S'incrémente independament du chrono. Utilise par l'escape game pour connaitre le temps total, sans compter les erreurs.
        self.errBlink = False # Si nbErreurMax = 5 et nbErreur = 5, on fait clignoter les LEDs d'erreurs. errBlink determine le dernier etat des LEDs.
        self.escapeGame = 0 # Active des options en fonction de si on est en mode jeu, ou en mode escape game (ex : mode stress)

        self.stressBlink = 0 # permet de faire clignoter le texte PIRATAGE DETECTE sur l'ecran
        self.stressModeListeBouton = [["si", 0],["sy",0],["b",0],["sy",2],["si", 3]]  # Combinaison a faire lors du mode stress (si = simon, sy = symbole, b = bouton)

        self.sounds = {
            'error': QSound("assets/Sons/error.wav"),
            'bip': QSound("assets/Sons/bip.wav"),
            'bip2': QSound("assets/Sons/bip2.wav"),
            'stress' :  QSound("assets/Sons/stress.wav"),
            'defaite': QSound("assets/Sons/defaite.wav"),
            'victoire': QSound("assets/Sons/win.wav"),
        }
        self.reset()


    def reset(self):
        self.calcTour = 0 # niveau actuelle du screen game
        self.calcErreur = 0
        self.PlaceMotEtape2 = -1 # id du mot etape 2 du manuel
        self.motEtape2 = "" # mot etape 2 du manuel
        self.calcMotBtns = []  # Liste des mots affichés sur les boutons (utilisé a des fin de debuggage uniquement)
        self.screenGameReady = True # permet d'eviter d'appuyer sur un bouton alors que le texte n'a pas encore chargé

        self.error = "" # texte des erreurs imprévu (ex : deconnexion de la arduino)
        self.serialOK = 0 # Test si la Arduino est bien connecte (1) ou non (0)
        self.btnSimon = [0, 0, 0, 0] # etat des boutons du Simon
        self.lumSimon = [0, 0, 0, 0] # etat des Lumieres du Simon
        self.simonStep = [0, 0] # Niveau, etape dans le niveau
        self.simonPressed = -1  # définit si un bouton du Simon est pressé (dans ce cas, on attends qu'il soit relaché)

        self.simonVoyelle = -1  # Etat si il y a une voyelle dans le numéro de série.
        self.simonLumStep = 0  # Etape d'eclairage du Simon
        self.simonLumOn = 0   # Hack pour les lumières. Les lumières du Simon ne s'allume que si cette valeur vaut 0. Est décrementé toutes les 0,5s. Permets de faire une pause de l'eclairage en mettant une grande valeur
        self.simonErreur = 0  # Led d'erreur du Simon

        self.filErreur = 0 # Led d'erreur des fils
        self.etatFils = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}  # etat de connexion des Fils
        self.filDeco = []  # recenses les fils déconnectés.

        self.filADeco = -1 # Solution. attention, commence a 0 (cable n°5 = 4)
        self.logiqueMsg = ""  # description de la solution. indique quelle logique a été choisi pour determiner quelle fils est a coupé (affiché sur la page web)

        self.symboleBtn = [0, 0, 0, 0]  # Etat d'appuie des bouton symbole, dans cet ordre : haut gauche, haut droit, bas droit, bas gauche
        self.symboleLum = [0, 0, 0, 0] # etat des lumières des boutons des symboles
        self.symboleErreur = 0 # etat led rouge symbole
        self.symboleOrdre = [] # ID des symboles installés
        self.symboleStep = 0  # niveau des symboles (2 symboles correct d'appuyé -> symboleStep = 2
        self.symbolePressed = -1
        self.symboleBlink = 0  # indique si les boutons sont entrain de clignoté ou non
        self.symboleBlinkEtat = 0 # indique leur etat de clignotement 0 eteint, 1 allumé

        self.boutonErreur = 0 # led rouge du bouton
        self.boutonBande = [0, 0, 0] # couleur de la bande (R,G,B)
        self.boutonContact = 0 # Indique l'etat d'appuie du bouton
        self.boutonPressed = 0

        self.boutonRelache = 0 # Bidouille pour traiter le cas ou le bouton doit etre appuyer et relacher immediatement.
        self.moduleWin = [0, 0, 0, 0, 0]  # Led verte pour : Simon, ScreenGame, fils, symbole, bouton
        self.moduleErr = [0, 0, 0, 0, 0, 0]  # Etat des erreurs faites pour : Simon, ScreenGame, fils, symbole, bouton, stress
        self.nbErreur = 0 # Nb erreur total
        self.chrono = [0, 0, 0, 0, 0]  # Min, Min, Sec, Sec, point
        self.chronoLedErr = [0, 0, 0, 0] # Etat des led d'erreur
        self.chronoBlink = 0  # 0 : pas de blink, 1: blink rapide, 2: blink moyen, 3: blink lent
        self.chronoLum = 1  # 0 : eteint, 1 : semi eclairé, 2 luminosité max.
        self.erreurChrono = False
        self.nbSecGlobal = 0 # Chrono indépendant

        self.pause = 0 # indique si le jeu est en pause ou non
        self.defaite = False
        self.stressMode = 0 # démarrage du mode stress. On bloque l'action sur les autres boutons
        self.stressModeStep = 0
        self.stressPressed = 0
        self.stressModeStarted = 0 # début de la pagaille (demarrage du chrono)

    def sendArduino(self):
        msg = ""
        msg += "".join(map(str, self.lumSimon))
        msg += str(self.moduleWin[0])
        msg += str(self.simonErreur)
        msg += str(self.calcErreur)
        msg += str(self.moduleWin[1])
        for i in range(4):
            if(int(self.calcTour) <= i ):
                msg += "0"
            else:
                msg += "1"

        msg += str(self.symboleErreur)
        msg += str(self.moduleWin[3])
        msg += "".join(map(str, self.symboleLum))

        msg += str(self.moduleWin[2])
        msg += str(self.filErreur)
        msg += "".join(map(str, self.chrono))
        msg += str(self.moduleWin[4])
        msg += str(self.boutonErreur)
        msg += "".join(map(str, self.boutonBande))
        msg += "".join(map(str, self.chronoLedErr))
        msg += str(self.chronoBlink)
        msg += str(self.chronoLum)

        msg += "\n"
        return msg

    def interprete(self, line):
        try:
            self.btnSimon[0] = 1 - int(line[0])
            self.btnSimon[1] = 1 - int(line[1])
            self.btnSimon[2] = 1 - int(line[2])
            self.btnSimon[3] = 1 - int(line[3])

            self.symboleBtn[0] = 1 - int(line[4])
            self.symboleBtn[1] = 1 - int(line[5])
            self.symboleBtn[2] = 1 - int(line[6])
            self.symboleBtn[3] = 1 - int(line[7])

            self.etatFils["1"] = int(line[8])
            self.etatFils["2"] = int(line[9])
            self.etatFils["3"] = int(line[10])
            self.etatFils["4"] = int(line[11])
            self.etatFils["5"] = int(line[12])
            self.boutonContact = int(line[13])
            self.chronoBoutonSon = int(line[14])
        except:
            print("Erreur communication Arduino")
