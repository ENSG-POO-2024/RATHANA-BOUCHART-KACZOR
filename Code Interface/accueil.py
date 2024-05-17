import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import QUrl, Qt, pyqtSignal, QRect, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSound, QSoundEffect
from PyQt5.QtGui import QMouseEvent, QPixmap, QIcon


class Fenetre(QMainWindow):
    lancerJeux = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.setGeometry(80, 50, 1200, 600)  # Fenêtre principale

        self.zone_bulb = QRect(370, 200, 100, 100)
        self.zone_sala = QRect(570, 200, 100, 100)
        self.zone_cara = QRect(770, 200, 100, 100)
        self.choix_possible = False



        self.afficherFond()
        self.afficherSorbier()
        self.dialogues()        
        self.bouton_next = ClickableLabel('Next', 17, self)
        self.bouton()

        self.show()

        self.poke_bulb = Pokeball(self, "bulb")

        self.poke_sala = Pokeball(self, "sala")

        self.poke_cara = Pokeball(self, "cara")


        self.music_player = Musique()  # Ajout de l'objet Music
        self.click = QMediaPlayer()
        self.aquisition = QMediaPlayer()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start)

    def mousePressEvent(self, event):
        # Vérifier si le clic est dans la zone définie
        if self.zone_bulb.contains(event.pos()) and self.choix_possible:
            self.txt_noir("Congratulations! You choose Bulbasaur.")
            self.jouer_acquisition()
            self.poke_sala.hide()
            self.poke_cara.hide()
            self.choix_possible = False
            self.timer.start(3000)
            self.bouton_next.hide()
            
        elif self.zone_sala.contains(event.pos()) and self.choix_possible:
            self.txt_noir("Congratulations! You choose Charmander.")
            self.jouer_acquisition()
            self.poke_cara.hide()
            self.poke_bulb.hide()
            self.choix_possible = False
            self.timer.start(3000)
            self.bouton_next.hide()

        elif self.zone_cara.contains(event.pos()) and self.choix_possible:
            self.txt_noir("Congratulations! You choose Squirtle.")
            self.jouer_acquisition()
            self.poke_bulb.hide()
            self.poke_sala.hide()
            self.choix_possible = False
            self.timer.start(3000)
            self.bouton_next.hide()

    def start(self):
        self.txt_noir("Press START to begin your journey.")
        self.bouton_start = ClickableLabel('START', 25, self)
        self.bouton_start.setGeometry(550, 100, 130, 35)
        self.bouton_start.show()
        self.bouton_start.clicked.connect(self.lancerSignal)

    def lancerSignal(self):
        self.lancerJeux.emit()

    def jouer_acquisition(self):
        chemin_son = "C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/son/acquisition.mp3"
        self.aquisition.setMedia(QMediaContent(QUrl.fromLocalFile(chemin_son)))
        self.aquisition.setVolume(100)
        self.aquisition.play()

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
        self.bouton_next.setGeometry(940, 540, 70, 20)
        self.bouton_next.clicked.connect(self.dialogue_suivant)
        self.bouton_next.clicked.connect(self.pokeballs)
        self.bouton_next.clicked.connect(self.jouer_son)
        self.bouton_next.clicked.connect(self.setchoix_possible)

    def setchoix_possible(self):
        self.choix_possible = True


    def jouer_son(self):
        chemin_son = "C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/son/click.mp3"
        self.click.setMedia(QMediaContent(QUrl.fromLocalFile(chemin_son)))
        self.click.setVolume(50)
        self.click.play()

    def dialogues(self):
        # Dialogues Rowan
        self.txt_noir("Hi ! My name is Rowan. You are going to start a very long journey...")

    def dialogue_suivant(self):
        self.txt_noir("Choose your first Pokémon")

    def pokeballs(self):
        # self.poke_bulb = Pokeball(self, "bulb")
        self.poke_bulb.setGeometry(370, 200, self.poke_bulb.width(), self.poke_bulb.height())
        self.poke_bulb.show()

        # self.poke_sala = Pokeball(self, "sala")
        self.poke_sala.setGeometry(570, 200, self.poke_sala.width(), self.poke_sala.height())
        self.poke_sala.show()

        # self.poke_cara = Pokeball(self, "cara")
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
        chemin_intro = "C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/son/intro.mp3"
        self.intro.setMedia(QMediaContent(QUrl.fromLocalFile(chemin_intro)))
        self.intro.setVolume(50)
        self.intro.play()


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text, taille, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("QLabel { color: black; font-size: " + str(taille)+"px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.taille=taille
        self.sound = QSound("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/son/click.mp3")

    def mousePressEvent(self, event):
        self.sound.play()
        self.clicked.emit()
    
    def enterEvent(self,event):
        self.setStyleSheet("QLabel { color: darkgrey; font-size: " +str(self.taille) +"px; font-family: 'Press Start 2P'; }")


    def leaveEvent(self,event):
        self.setStyleSheet("QLabel { color: black; font-size: " + str(self.taille) +"px; font-family: 'Press Start 2P'; }")

class Pokeball(QLabel):
    def __init__(self, parent=None, poke_type=""):
        super().__init__(parent)
        self.poke_type = poke_type
        self.setPixmap(QPixmap(f"C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/pokeballFermee.png"))
        self.setMinimumHeight(129)

    def enterEvent(self, event):
        self.setPixmap(QPixmap(f"C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/{self.poke_type}Ouverte.png"))

    def leaveEvent(self, event):
        self.setPixmap(QPixmap(f"C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/pokeballFermee.png"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = Fenetre()
    interface.show()
    sys.exit(app.exec_())