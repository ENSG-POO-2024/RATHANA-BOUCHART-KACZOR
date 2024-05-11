import pokemon as pk

carapuce = pk.Pokemon("Squirtle")
salameche= pk.Pokemon("Charmander")
bulbizare= pk.Pokemon("Bulbasaur")
dracolosse=pk.Pokemon("Bulbasaur")


equipe_dresseur = [dracolosse, salameche,bulbizare,salameche]
pokemon_allie= equipe_dresseur[0]

pokemon_adverse=pk.PokemonSauvage("Zapdos",0,0)

def find_bottom_position(image):
    image = image.toImage()
    height = image.height()
    width = image.width()

    # Parcourir les lignes de l'image de bas en haut
    for y in range(height - 1, -1, -1):
        # Parcourir les colonnes de gauche à droite
        for x in range(width):
            # Obtenir la couleur du pixel
            color = image.pixelColor(x, y)

            # Si le pixel n'est pas transparent, c'est une ligne contenant des pixels colorés
            if color.alpha() != 0:
                return y  # Retourne la position y de la première ligne contenant des pixels colorés

    return 0


    
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import sys
import os
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
        
        path=os.path.dirname(os.path.abspath(__file__))
        path1=os.path.join(path,"VFX_SFX\combat_pokemon.jpg")
        pixmap = QPixmap(path1)  
        # Redimensionner l'image pour correspondre à la taille de la fenêtre
        pixmap = pixmap.scaled(self.size())  # Redimensionner l'image pour correspondre à la taille de la fenêtre
        background_label.setPixmap(pixmap)
        
        # Ajuster la taille du QLabel à la taille de la fenêtre
        background_label.setGeometry(0, 0, self.width(), self.height())

        #Affichage du pokemon du dresseur
        path2=os.path.join(path, "../documents/images/pokemons")
        self.pokemon_dresseur = QLabel(self)
        self.pokemon_dresseur.setGeometry(0,0,300,300)
        pkm_dresseur = QPixmap(path2 +"/" + pokemon_allie.name.lower() +"_dos.png")  

        pkm_dresseur = pkm_dresseur.scaled(200, 200, Qt.KeepAspectRatio)
        self.pokemon_dresseur.setPixmap(pkm_dresseur)
        image_width = pkm_dresseur.width()
        bottom_position=find_bottom_position(pkm_dresseur)
        # Positionnez l'image en soustrayant la largeur et la hauteur de l'image à partir de la position du coin inférieur gauche souhaitée
        self.pokemon_dresseur.move(0 + int(image_width/2), 483 -bottom_position )
        

        #Affichage du nom du pokemon du Dresseur
        self.nom_pkm = QLabel(pokemon_allie.name, self)
        self.nom_pkm.setGeometry(0,0,200,100)
        self.nom_pkm.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        self.nom_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.nom_pkm.setMinimumWidth(144)
        self.nom_pkm.move(580,290) 

        #Affichage du nombre de pv du pokemon du dresseur
        totalHP=pokemon_allie.HP
        self.pv_pkm= QLabel(str(pokemon_allie.HP) + "/" + str(totalHP), self)
        self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.pv_pkm.setAlignment(Qt.AlignRight)
        self.pv_pkm.setMinimumWidth(144)
        self.pv_pkm.move(682,435) 

        #Affichage du pokemon sauvage
        self.pokemon_sauvage = QLabel(self)
        self.pokemon_sauvage.setGeometry(0,0,300,300)
        pkm_sauvage = QPixmap(path2 + "/" + pokemon_adverse.name.lower() +"_face.png")  

        pkm_sauvage= pkm_sauvage.scaled(200, 200, Qt.KeepAspectRatio)
        bottom_position2 = find_bottom_position(pkm_sauvage)
        self.pokemon_sauvage.setPixmap(pkm_sauvage)
        image2_width=pkm_sauvage.width()
        self.pokemon_sauvage.move(525 + int(image2_width/2), 200-bottom_position2)

        #Affichage du nom du pokemon sauvage
        self.nom_pkm = QLabel(pokemon_adverse.name, self)
        self.nom_pkm.setGeometry(0,0,200,100)
        self.nom_pkm.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        self.nom_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.nom_pkm.setMinimumWidth(144)
        self.nom_pkm.move(200,-5) 

        #Musique des combats
        path_musique=os.path.join(path, "VFX_SFX/Battle! (Wild Pokémon)[Pokémon Diamond & Pearl].mp3")
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path_musique)))
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


