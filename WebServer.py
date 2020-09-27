from flask import Flask, render_template, request
from PyQt5.QtCore import QThread, QObject, pyqtSignal
import Chrono

class WebServer(QThread):
    trigger = pyqtSignal()

    def __init__(self, gv, mainSelf):
        QThread.__init__(self)
        self.gv = gv
        self.MS = mainSelf



    def setGVValue(self,form):
        for elt in form:
            if (elt.find(',') != -1):
                eltt, arg = elt.split(',')
                at = getattr(self.gv, eltt)
                at[int(arg)] = int(form[elt])
            else:
                setattr(self.gv, elt, int(form[elt]))

    def run(self):
        app = Flask(__name__)
        self.app = app
        gv = self.gv
        @app.route('/',methods=['POST', 'GET'])
        @app.route('/index', methods=['POST', 'GET'])
        def index():

            if request.method == 'POST':
                self.setGVValue(request.form)
            elif request.method == 'GET':
                if request.args.get('chrono'):
                    if request.args.get('chrono') == "start":
                        self.gv.pause = 0
                    if request.args.get('chrono') == "pause":
                        self.gv.pause = 1
                    if request.args.get('chrono') == "p5":
                        Chrono.chronoPlus(self.MS, 5)
                    if request.args.get('chrono') == "p1":
                        Chrono.chronoPlus(self.MS, 1)
                    if request.args.get('chrono') == "m5":
                        Chrono.chronoMoins(self.MS, 5)
                    if request.args.get('chrono') == "m1":
                        Chrono.chronoMoins(self.MS, 1)
                if request.args.get('fils'):
                    if request.args.get('fils') == "reset":
                        self.gv.filErreur = 0
                        self.gv.filDeco = []
                if request.args.get('symbole'):
                    if request.args.get('symbole') == "reset":
                        self.gv.symboleErreur = 0
                        self.gv.symboleStep = 0
                        gv.symboleLum = [0, 0, 0, 0]
                if request.args.get('simon'):
                    if request.args.get('simon') == "reset":
                        self.gv.simonStep = [0, 0]
                        self.gv.simonErreur = 0
                        gv.lumSimon = [0, 0, 0, 0]


            return render_template('index.html', gv = gv)

        @app.route('/screenGame', methods=['POST', 'GET'])
        def screenGame():

            if request.method == 'POST':
                if("refresh" in request.form):
                    self.trigger.connect(self.MS.slot_repaint)
                    self.trigger.emit()
                if("win" in request.form):
                    self.trigger.connect(self.MS.slot_win_screenGame)
                    self.trigger.emit()
                else:
                    self.setGVValue(request.form)
            return render_template('screenGame.html', gv=gv)



        app.run(host= '0.0.0.0')
