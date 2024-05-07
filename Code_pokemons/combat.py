#import pokemon.py as pk
#import PyQT5 as pyqt

#carapuce = pk.Pokemon("Squirtle")
#salameche= pk.Pokemon("Charmander")
#bulbizare= pk.Pokemon("Bulbazor")


#equipe_dresseur = [carapuce, salameche, bulbizare]

#pokemon_adverse="Rattata"

#class Interface:

    
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import sys

class CombatPokemon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Combat Pokémon')
        self.setGeometry(100, 100, 900, 700) 
        # Création du QLabel pour afficher l'image en fond
        background_label = QLabel(self)
        
        # Charger l'image dans le QLabel
        pixmap = QPixmap("C:\ENSG\Projet_Info\RATHANA-BOUCHART-KACZOR\Code_pokemons\images_combat\combat_pokemon.jpg")  
        # Redimensionner l'image pour correspondre à la taille de la fenêtre
        pixmap = pixmap.scaled(self.size())  # Redimensionner l'image pour correspondre à la taille de la fenêtre
        background_label.setPixmap(pixmap)
        
        # Ajuster la taille du QLabel à la taille de la fenêtre
        background_label.setGeometry(0, 0, self.width(), self.height())

        button_label = QLabel('Attaques', self)
        button_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        font = QFont()
        font.setFamily("Press Start 2P")  # Utiliser la police "Press Start 2P"
        font.setPointSize(24)  # Taille de la police
        button_label.setFont(font)
        button_label.move(480,570)
        # Ajoutez d'autres éléments à votre fenêtre ici # Taille de la fenêtre

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CombatPokemon()
    window.show()
    sys.exit(app.exec_())


