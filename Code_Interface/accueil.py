import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap

path = os.path.dirname(os.path.abspath(__file__))

class Fenetre(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setGeometry(80, 50, 1200, 600)  # Fenêtre principale
        
        self.afficherFond()
        self.afficherSorbier()
        self.dialogues()
        self.bouton()
        self.show()
        
        self.music_player = Musique()  # Ajout de l'objet Music

    def afficherFond(self):
        pixmap = QPixmap(os.path.join(path, "../documents/images/accueil.png"))
        self.fond = QLabel(self)
        self.fond.setPixmap(pixmap)
        self.fond.setGeometry(0, 0, pixmap.width(), pixmap.height())

        pixmap = QPixmap(os.path.join(path, "../documents/images/dialogue.png"))
        self.dialogue = QLabel(self)
        self.dialogue.setPixmap(pixmap)
        self.dialogue.setGeometry(100, 405, pixmap.width(), pixmap.height())

    def afficherSorbier(self):
        pixmap = QPixmap(os.path.join(path, "../documents/images/sorbier.png"))
        self.sorbier = QLabel(self)
        self.sorbier.setPixmap(pixmap)
        self.sorbier.setGeometry(100, 200, pixmap.width(), pixmap.height())

    def bouton(self):
        self.bouton = ClickableLabel('Next', 17, self)
        self.bouton.setGeometry(940, 540, 70, 20)
        self.bouton.clicked.connect(self.dialogue_suivant)
        self.bouton.clicked.connect(self.pokeballs)
    
    def dialogues(self):
        # Dialogues Rowan
        self.txt_noir("Hi ! My name is Rowan. You are going to start a very long journey...")

    def dialogue_suivant(self):
        self.txt_noir("Choose your first Pokémon")

    def pokeballs(self):
        self.poke_bulb = Pokeball(self, "bulb")
        self.poke_bulb.setGeometry(370, 200, self.poke_bulb.width(), self.poke_bulb.height())
        self.poke_bulb.show()

        self.poke_sala = Pokeball(self, "sala")
        self.poke_sala.setGeometry(570, 200, self.poke_sala.width(), self.poke_sala.height())
        self.poke_sala.show()

        self.poke_cara = Pokeball(self, "cara")
        self.poke_cara.setGeometry(770, 200, self.poke_cara.width(), self.poke_cara.height())
        self.poke_cara.show()

    def txt_noir(self, txt):
        if hasattr(self, 'txtnoir'):
            self.txtnoir.deleteLater()
        self.txtnoir = QLabel(txt, self)
        self.txtnoir.setAlignment(Qt.AlignLeft)
        self.txtnoir.setStyleSheet("QLabel { color: black ; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.txtnoir.setMinimumWidth(800)
        self.txtnoir.setMinimumHeight(90)
        self.txtnoir.setWordWrap(True) 
        self.txtnoir.move(150, 425)
        self.txtnoir.show()

class Musique():
    def __init__(self):
        self.intro = QMediaPlayer()
        self.chargerEtJouerMusique()

    def chargerEtJouerMusique(self):
        chemin_intro = os.path.join(path,"../son/intro.mp3")
        self.intro.setMedia(QMediaContent(QUrl.fromLocalFile(chemin_intro)))
        self.intro.setVolume(50)
        self.intro.play()

class Pokeball(QLabel):
    def __init__(self, parent=None, poke_type=""):
        super().__init__(parent)
        self.poke_type = poke_type
        self.setPixmap(QPixmap(os.path.join(path, f"../documents/images/pokeballFermee.png")))
        self.setMinimumHeight(129)

    def enterEvent(self, event):
        self.setPixmap(QPixmap(os.path.join(path, f"../documents/images/{self.poke_type}Ouverte.png")))

    def leaveEvent(self, event):
        self.setPixmap(QPixmap(os.path.join(path, f"../documents/images/pokeballFermee.png")))

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text, taille, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("QLabel { color: black; font-size: " + str(taille)+"px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.taille=taille

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.clicked.emit()
    
    def enterEvent(self,event):
        self.setStyleSheet("QLabel { color: darkgrey; font-size: " +str(self.taille) +"px; font-family: 'Press Start 2P'; }")

    def leaveEvent(self,event):
        self.setStyleSheet("QLabel { color: black; font-size: " + str(self.taille) +"px; font-family: 'Press Start 2P'; }")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = Fenetre()
    interface.show()
    sys.exit(app.exec_())