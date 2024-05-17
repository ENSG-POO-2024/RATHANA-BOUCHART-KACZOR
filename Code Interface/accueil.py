import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap

class Fenetre(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setGeometry(80, 50, 1200, 600) #fenêtre principale
        
        self.afficherFond()
        self.afficherSorbier()
        self.dialogues()
        self.bouton()
        self.show()
        
        self.music_player = Musique()  # Ajout de l'objet Music

    def afficherFond(self):

        pixmap = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/accueil.png")
        self.fond = QLabel(self)
        self.fond.setPixmap(pixmap)
        self.fond.setGeometry(0, 0, pixmap.width(), pixmap.height())

        pixmap = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/dialogue.png")
        self.dialogue = QLabel(self)
        self.dialogue.setPixmap(pixmap)
        self.dialogue.setGeometry(100, 405, pixmap.width(), pixmap.height())

    def afficherSorbier(self):
        pixmap = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/sorbier.png")
        self.sorbier = QLabel(self)
        self.sorbier.setPixmap(pixmap)
        self.sorbier.setGeometry(100, 200, pixmap.width(), pixmap.height())

    def bouton(self):
        self.bouton = QPushButton('Next', self)
        self.bouton.setGeometry(1042, 530, 40, 30)
        self.bouton.clicked.connect(self.dialogue_suivant)
        self.bouton.clicked.connect(self.pokeballs)
    
    def dialogues(self):
        # Dialogues Rowan
        self.txt_noir("Hi ! My name is Rowan. You are going to start a very long journey...")

    def dialogue_suivant(self):
        self.txt_noir("Choose your first Pokémon")

    def pokeballs(self):
        self.poke_bulb_fermee = PokeballFermee(self)
        self.poke_bulb_fermee.setGeometry(320, 200, self.poke_bulb_fermee.width(), self.poke_bulb_fermee.height())
        self.poke_bulb_fermee.show()

        self.poke_bulb_ouverte = PokeballOuverte(self)
        self.poke_bulb_ouverte.setGeometry(320, 200, self.poke_bulb_ouverte.width(), self.poke_bulb_ouverte.height())
        self.poke_bulb_ouverte.hide()   



    def ouvre_pokeball(self, event):
        self.pokeb1.setPixmap(QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/pokeballFermee.png"))

    def ferme_pokeball(self, event):
        self.pokeb1.setPixmap(QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/pokeballOuverte.png"))

    def txt_noir(self,txt):
        if hasattr(self, 'txtnoir'):
            self.txtnoir.deleteLater()
        self.txtnoir=QLabel(txt,self)
        self.txtnoir.setAlignment(Qt.AlignLeft)
        self.txtnoir.setStyleSheet("QLabel { color: black ; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.txtnoir.setMinimumWidth(800)
        self.txtnoir.setMinimumHeight(90)
        self.txtnoir.setWordWrap(True) 
        self.txtnoir.move(150,425)
        self.txtnoir.show()

class Musique():
    def __init__(self):
        self.intro = QMediaPlayer()
        self.chargerEtJouerMusique()

    def chargerEtJouerMusique(self):
        chemin_intro = "C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/son/intro.mp3"
        self.intro.setMedia(QMediaContent(QUrl.fromLocalFile(chemin_intro)))
        self.intro.setVolume(50)
        self.intro.play()

class PokeballOuverte(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/pokeballOuverte.png"))

    def enterEvent(self, event):
        self.setPixmap(QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/pokeballOuverte.png"))

    def leaveEvent(self, event):
        self.hide()

class PokeballFermee(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/pokeballFermee.png"))

    def enterEvent(self, event):
        self.hide()

    def leaveEvent(self, event):
        self.setPixmap(QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/pokeballFermee.png"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = Fenetre()
    interface.show()
    sys.exit(app.exec_())