#import pokemon.py as pk
#import PyQT5 as pyqt

#carapuce = pk.Pokemon("Squirtle")
#salameche= pk.Pokemon("Charmander")
#bulbizare= pk.Pokemon("Bulbazor")


#equipe_dresseur = [carapuce, salameche, bulbizare]

#pokemon_adverse="Rattata"

#class Interface:

    
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget

class CombatPokemon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Combat Pokémon")
        self.setGeometry(100, 100, 400, 300)

        # Widgets
        self.label_info = QLabel("C'est le tour du joueur 1")
        self.button_attaque1 = QPushButton("Attaque 1")
        self.button_attaque2 = QPushButton("Attaque 2")
        self.label_hp_joueur1 = QLabel("HP Joueur 1 : 100/100")
        self.label_hp_joueur2 = QLabel("HP Joueur 2 : 100/100")

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label_info)
        layout.addWidget(self.button_attaque1)
        layout.addWidget(self.button_attaque2)
        layout.addWidget(self.label_hp_joueur1)
        layout.addWidget(self.label_hp_joueur2)

        # Widget principal
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connexion des signaux aux slots
        self.button_attaque1.clicked.connect(self.attaquer1)
        self.button_attaque2.clicked.connect(self.attaquer2)

        self.setStyleSheet("QMainWindow {background-image: url('C:\ENSG\Projet_Info\RATHANA-BOUCHART-KACZOR\Code_pokemons\images_combat\fond_combat_pokemon.png'); background-repeat: no-repeat; background-position: center;}")

    def attaquer1(self):
        # Code pour l'attaque 1
        self.label_info.setText("Le joueur 1 utilise Attaque 1")

    def attaquer2(self):
        # Code pour l'attaque 2
        self.label_info.setText("Le joueur 1 utilise Attaque 2")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = CombatPokemon()
    fenetre.show()
    sys.exit(app.exec_())

