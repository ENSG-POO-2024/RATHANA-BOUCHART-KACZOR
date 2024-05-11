import pokemon as pk

carapuce = pk.Pokemon("Squirtle")
salameche= pk.Pokemon("Charmander")
bulbizare= pk.Pokemon("Bulbasaur")
dracolosse=pk.Pokemon("Pikachu")


equipe_dresseur = [dracolosse, salameche,bulbizare,salameche]
pokemon_allie= equipe_dresseur[0]

pokemon_adverse=pk.PokemonSauvage("Bulbasaur",0,0)

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


    
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QTimer, QEventLoop
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os

path=os.path.dirname(os.path.abspath(__file__))

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.clicked.emit()
    
    def enterEvent(self,event):
        self.setStyleSheet("QLabel { color: darkgrey; font-size: 17px; font-family: 'Press Start 2P'; }")

    def leaveEvent(self,event):
        self.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")



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
        self.nom_pkm_s = QLabel(pokemon_adverse.name, self)
        self.nom_pkm_s.setGeometry(0,0,200,100)
        self.nom_pkm_s.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        self.nom_pkm_s.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.nom_pkm_s.setMinimumWidth(144)
        self.nom_pkm_s.move(200,-5) 

        #Musique des combats
        path_musique=os.path.join(path, "VFX_SFX/Battle! (Wild Pokémon)[Pokémon Diamond & Pearl].mp3")
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path_musique)))
        self.mediaPlayer.play()


        #Boutons de choix
        self.button1_label = ClickableLabel('FIGHT', self)
        self.button1_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        self.button1_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.button1_label.setMinimumWidth(142)
        self.button1_label.move(470,575) 
        #self.button1_label.hide()

        self.button2_label = ClickableLabel('POKéMON', self)
        self.button2_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        self.button2_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.button2_label.setMinimumWidth(142)
        self.button2_label.move(470,630) 
        #self.button2_label.hide()

        self.button3_label = ClickableLabel('BAG', self)
        self.button3_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        self.button3_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.button3_label.setMinimumWidth(142)
        self.button3_label.move(700,575)
        #self.button3_label.hide()

        self.button4_label = ClickableLabel('RUN', self)
        self.button4_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        self.button4_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.button4_label.setMinimumWidth(142)
        self.button4_label.move(700,630)
        #self.button4_label.hide()
        
        self.attaque1=ClickableLabel(pokemon_allie.attaque_normale.upper(),self)
        self.attaque1.setAlignment(Qt.AlignCenter)
        self.attaque1.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.attaque1.setMinimumWidth(142)
        self.attaque1.move(480,600)
        self.attaque1.hide()

        self.attaque2=ClickableLabel(pokemon_allie.attaque_type.upper(),self)
        self.attaque2.setAlignment(Qt.AlignCenter)
        self.attaque2.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.attaque2.setMinimumWidth(170)
        self.attaque2.move(650,600)
        self.attaque2.hide()
        
        self.retour=ClickableLabel("BACK",self)
        self.retour.setAlignment(Qt.AlignCenter)
        self.retour.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.retour.setMinimumWidth(142)
        self.retour.move(575,650)
        self.retour.hide()

        self.potion=ClickableLabel("USE A POTION",self)
        self.potion.setAlignment(Qt.AlignLeft)
        self.potion.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.potion.setMinimumWidth(210)
        self.potion.move(565,600)
        self.potion.hide()

        #Texte pour la fuite
        if pokemon_adverse.legendary:
            self.escapetxt=QLabel("You can't run away from a Legendary Pokemon!",self)
        else:
            self.escapetxt=QLabel("Got away safely!",self)
        
        self.escapetxt.setAlignment(Qt.AlignLeft)
        self.escapetxt.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.escapetxt.setMinimumWidth(390)
        self.escapetxt.setMinimumHeight(300)
        self.escapetxt.setWordWrap(True) #Permet d'aller à la ligne
        self.escapetxt.move(40,570)
        self.escapetxt.hide()


        self.button1_label.clicked.connect(self.fight)
        self.retour.clicked.connect(self.back)
        self.button3_label.clicked.connect(self.sac)
        self.button4_label.clicked.connect(self.fuite)

    #Definition des methodes
    def fight(self):
        self.button1_label.hide()
        self.button2_label.hide()
        self.button3_label.hide()
        self.button4_label.hide()
        self.attaque1.show()
        self.attaque2.show()
        self.retour.show()

    def back(self):  
        self.attaque1.hide()
        self.attaque2.hide()
        self.potion.hide()
        self.retour.hide()
        self.button1_label.show()
        self.button2_label.show()
        self.button3_label.show()
        self.button4_label.show()
    
    def sac(self):
        self.button1_label.hide()
        self.button2_label.hide()
        self.button3_label.hide()
        self.button4_label.hide()
        self.potion.show()
        self.retour.show()

    def fuite(self):
        #Changement de la musique
        if not pokemon_adverse.legendary:

            #On change la musique pour mettre le bruit de fuite
            path_musique=os.path.join(path, "VFX_SFX\Pokémon RedBlueYellow - Run Away - Sound Effect.mp3")
            self.mediaPlayer = QMediaPlayer()
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path_musique)))
            self.mediaPlayer.play()
            #On met en place l'interface de fuite
            self.button1_label.hide()
            self.button2_label.hide()
            self.button3_label.hide()
            self.button4_label.hide()
            self.escapetxt.show()
            QTimer.singleShot(2000,self.close)
        
        else:
            self.escapetxt.show()
            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            self.escapetxt.hide()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CombatPokemon()
    window.show()
    sys.exit(app.exec_())


