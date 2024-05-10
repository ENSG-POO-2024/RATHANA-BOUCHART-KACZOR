import pokemon as pk

carapuce = pk.Pokemon("Squirtle")
salameche= pk.Pokemon("Charmander")
bulbizare= pk.Pokemon("Bulbasaur")


equipe_dresseur = [salameche,bulbizare,salameche]

pokemon_adverse=pk.PokemonSauvage("Mewtwo",0,0)



    
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
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

        #Affichage du pokemon du dresseur
        self.pokemon_dresseur = QLabel(self)
        self.pokemon_dresseur.setGeometry(0,0,300,300)
        pkm_dresseur = QPixmap("C:/ENSG/Projet_Info/RATHANA-BOUCHART-KACZOR/documents/images/pokemons/" + equipe_dresseur[0].name.lower() +"_dos.png")  

        pkm_dresseur = pkm_dresseur.scaled(200, 200, Qt.KeepAspectRatio)

        self.pokemon_dresseur.setPixmap(pkm_dresseur)
        self.pokemon_dresseur.move(100, 312)

        #Affichage du nom du pokemon du Dresseur
        self.nom_pkm = QLabel(equipe_dresseur[0].name, self)
        self.nom_pkm.setGeometry(0,0,200,100)
        self.nom_pkm.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        self.nom_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.nom_pkm.setMinimumWidth(144)
        self.nom_pkm.move(580,290) 

        #Affichage du pokemon sauvage
        self.pokemon_sauvage = QLabel(self)
        self.pokemon_sauvage.setGeometry(0,0,300,300)
        overlay_pixmap = QPixmap("C:/ENSG/Projet_Info/RATHANA-BOUCHART-KACZOR/documents/images/pokemons/" + pokemon_adverse.name.lower() +"_face.png")  

        overlay_pixmap = overlay_pixmap.scaled(200, 200, Qt.KeepAspectRatio)

        self.pokemon_sauvage.setPixmap(overlay_pixmap)
        self.pokemon_sauvage.move(610, 45)

        #Affichage du nom du pokemon sauvage
        self.nom_pkm = QLabel(pokemon_adverse.name, self)
        self.nom_pkm.setGeometry(0,0,200,100)
        self.nom_pkm.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        self.nom_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.nom_pkm.setMinimumWidth(144)
        self.nom_pkm.move(200,0) 

        #Musique des combats
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("C:\ENSG\Projet_Info\RATHANA-BOUCHART-KACZOR\Code_pokemons\Battle! (Wild Pokémon)[Pokémon Diamond & Pearl].mp3")))
        self.mediaPlayer.play()


        #Boutons de choix
        button1_label = QLabel('FIGHT', self)
        button1_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        button1_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        button1_label.setMinimumWidth(142)
        button1_label.move(470,575) 

        button2_label = QLabel('POKéMON', self)
        button2_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        button2_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        button2_label.setMinimumWidth(142)
        button2_label.move(470,630) 

        button3_label = QLabel('BAG', self)
        button3_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        button3_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        button3_label.setMinimumWidth(142)
        button3_label.move(700,575)

        button4_label = QLabel('RUN', self)
        button4_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        button4_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        button4_label.setMinimumWidth(142)
        button4_label.move(700,630)
        # Ajoutez d'autres éléments à votre fenêtre ici # Taille de la fenêtre



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CombatPokemon()
    window.show()
    sys.exit(app.exec_())


