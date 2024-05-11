import pokemon as pk
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout,QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QTimer, QEventLoop
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os

path=os.path.dirname(os.path.abspath(__file__))

carapuce = pk.Pokemon("Squirtle")
salameche= pk.Pokemon("Charmander")
bulbizare= pk.Pokemon("Bulbasaur")
dracolosse=pk.Pokemon("Dragonite")
papilusion=pk.Pokemon("Butterfree")
arcanin=pk.Pokemon("Arcanine")
mewtwo=pk.Pokemon("Mewtwo")
pokemon_au_combat=1

equipe_dresseur = [dracolosse, salameche, bulbizare, papilusion,arcanin,mewtwo]
pokemon_allie= equipe_dresseur[0]

pokemon_adverse=pk.PokemonSauvage("Moltres",0,0)

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



class CombatPokemon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.pokemon_au_combat=1
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
        self.button1_label = ClickableLabel('FIGHT', 17, self)
        self.button1_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        #self.button1_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.button1_label.setMinimumWidth(142)
        self.button1_label.move(470,575) 
        #self.button1_label.hide()

        self.button2_label = ClickableLabel('POKéMON', 17,self)
        self.button2_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        #self.button2_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.button2_label.setMinimumWidth(142)
        self.button2_label.move(470,630) 
        #self.button2_label.hide()

        self.button3_label = ClickableLabel('BAG',17, self)
        self.button3_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        #self.button3_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.button3_label.setMinimumWidth(142)
        self.button3_label.move(700,575)
        #self.button3_label.hide()

        self.button4_label = ClickableLabel('RUN',17, self)
        self.button4_label.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        #self.button4_label.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.button4_label.setMinimumWidth(142)
        self.button4_label.move(700,630)
        #self.button4_label.hide()
        
        #Bouton pour l'attaque normale du pokemon
        self.attaque1=ClickableLabel(pokemon_allie.attaque_normale.upper(),17, self)
        self.attaque1.setAlignment(Qt.AlignCenter)
        #self.attaque1.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.attaque1.setMinimumWidth(142)
        self.attaque1.move(480,600)
        self.attaque1.hide()

        #Bouton pour l'attaque de type du pokemon
        self.attaque2=ClickableLabel(pokemon_allie.attaque_type.upper(),17,self)
        self.attaque2.setAlignment(Qt.AlignCenter)
        #self.attaque2.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.attaque2.setMinimumWidth(186)
        self.attaque2.move(650,600)
        self.attaque2.hide()
        
        #Bouton pour revenir au menu principal
        self.retour=ClickableLabel("BACK",17,self)
        self.retour.setAlignment(Qt.AlignCenter)
        #self.retour.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.retour.setMinimumWidth(142)
        self.retour.move(585,650)
        self.retour.hide()

        #Bouton pour utiliser une potion
        self.potion=ClickableLabel("USE A POTION",17,self)
        self.potion.setAlignment(Qt.AlignLeft)
        #self.potion.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")
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

        #Texte qui indique la possibilité de changer de pokemon
        self.changepkm=QLabel("Change your pokemon",self)
        self.changepkm.setAlignment(Qt.AlignLeft)
        self.changepkm.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.changepkm.setMinimumWidth(390)
        self.changepkm.move(500,570)
        self.changepkm.hide()

        if equipe_dresseur[0]!="Vide":
            
            #Cette partie du code marche mais je la mets en pause

            # self.pokemon1_sprite=QLabel(self)
            # self.pokemon1_sprite.setGeometry(0,0,80,80)
            # pokemon1 = QPixmap(path2 + "/" + equipe_dresseur[0].name.lower() +"_map.png")  
            # pokemon1= pokemon1.scaled(60, 60, Qt.KeepAspectRatio)
            # bottom_position3 = find_bottom_position(pokemon1)
            # self.pokemon1_sprite.setPixmap(pokemon1)
            # pokemon1_width=pkm_sauvage.width()
            # self.pokemon1_sprite.move(360 + int(pokemon1_width/2), 602-bottom_position3)
        
            self.pokemon1=ClickableLabel(equipe_dresseur[0].name.upper(), 13,self)
            self.pokemon1.setAlignment(Qt.AlignLeft)
            self.pokemon1.setMinimumWidth(120)
            self.pokemon1.move(510,600)
            self.pokemon1.hide()

            if equipe_dresseur[1]!="Vide":
        
                self.pokemon2=ClickableLabel(equipe_dresseur[1].name.upper(), 13,self)
                self.pokemon2.setAlignment(Qt.AlignLeft)
                self.pokemon2.setMinimumWidth(130)
                self.pokemon2.move(680,600)
                self.pokemon2.hide()

            if equipe_dresseur[2]!="Vide":
        
                self.pokemon3=ClickableLabel(equipe_dresseur[2].name.upper(), 13,self)
                self.pokemon3.setAlignment(Qt.AlignLeft)
                self.pokemon3.setMinimumWidth(130)
                self.pokemon3.move(510,620)
                self.pokemon3.hide()
            
            if equipe_dresseur[3]!="Vide":
        
                self.pokemon4=ClickableLabel(equipe_dresseur[3].name.upper(), 13,self)
                self.pokemon4.setAlignment(Qt.AlignLeft)
                self.pokemon4.setMinimumWidth(130)
                self.pokemon4.move(680,620)
                self.pokemon4.hide()


            if equipe_dresseur[4]!="Vide":
        
                self.pokemon5=ClickableLabel(equipe_dresseur[4].name.upper(), 13,self)
                self.pokemon5.setAlignment(Qt.AlignLeft)
                self.pokemon5.setMinimumWidth(130)
                self.pokemon5.setMaximumHeight(15)
                self.pokemon5.move(510,640)
                self.pokemon5.hide()

            if equipe_dresseur[5]!="Vide":
        
                self.pokemon6=ClickableLabel(equipe_dresseur[5].name.upper(), 13,self)
                self.pokemon6.setAlignment(Qt.AlignLeft)
                self.pokemon6.setMinimumWidth(130)
                self.pokemon6.setMaximumHeight(15)
                self.pokemon6.move(680,640)
                self.pokemon6.hide()

        



        self.button1_label.clicked.connect(self.fight)
        self.retour.clicked.connect(self.back)
        self.button3_label.clicked.connect(self.sac)
        self.button4_label.clicked.connect(self.fuite)
        self.button2_label.clicked.connect(self.change)
        self.pokemon2.clicked.connect(self.changetopkm2)
        self.pokemon1.clicked.connect(self.changetopkm1)



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
        #Fais disparaitre le menu d'attaque
        self.attaque1.hide()
        self.attaque2.hide()

        #fais disparaitre le menu de potion
        self.potion.hide()
        self.retour.hide()

        #Fais disparaitre le menu de changement de pokemon
        self.changepkm.hide()
        self.pokemon1.hide()
        self.pokemon2.hide()
        self.pokemon3.hide()
        self.pokemon4.hide()
        self.pokemon5.hide()
        self.pokemon6.hide()

        #Fais apparaitre le menu principal
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
    
    def change(self):
        self.button1_label.hide()
        self.button2_label.hide()
        self.button3_label.hide()
        self.button4_label.hide()
        self.changepkm.show()
        self.pokemon1.show()
        self.pokemon2.show()
        self.pokemon3.show()
        self.pokemon4.show()
        self.pokemon5.show()
        self.pokemon6.show()
        self.retour.show()

    def changetopkm2(self):

        #Supprime l'interface de changement de pokemon
        # self.changepkm.hide()
        # self.pokemon1.hide()
        # self.pokemon2.hide()
        # self.pokemon3.hide()
        # self.pokemon4.hide()
        # self.pokemon5.hide()
        # self.pokemon6.hide()
        # self.retour.hide()

        if equipe_dresseur[1].HP==0:
            self.txt1=QLabel(str(equipe_dresseur[1].name).upper() + " is K.O. He can't be sent on the battlefiel.",self)
            self.txt1.setAlignment(Qt.AlignLeft)
            self.txt1.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt1.setMinimumWidth(390)
            self.txt1.setMinimumHeight(300)
            self.txt1.setWordWrap(True) #Permet d'aller à la ligne
            self.txt1.move(40,570)
            self.txt1.show()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txt1.hide()

        elif self.pokemon_au_combat != 2:

            self.changepkm.hide()
            self.pokemon1.hide()
            self.pokemon2.hide()
            self.pokemon3.hide()
            self.pokemon4.hide()
            self.pokemon5.hide()
            self.pokemon6.hide()
            self.retour.hide()

            self.txt1=QLabel(str(equipe_dresseur[self.pokemon_au_combat].name).upper() + ", come back.",self)
            self.txt1.setAlignment(Qt.AlignLeft)
            self.txt1.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt1.setMinimumWidth(390)
            self.txt1.setMinimumHeight(300)
            self.txt1.setWordWrap(True) #Permet d'aller à la ligne
            self.txt1.move(40,570)
            self.txt1.show()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.pokemon_dresseur.hide()
            self.nom_pkm.hide()
            self.pv_pkm.hide()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txt1.hide()
            self.txt2=QLabel(equipe_dresseur[1].name.upper() + ", go!",self)
            self.txt2.setAlignment(Qt.AlignLeft)
            self.txt2.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt2.setMinimumWidth(390)
            self.txt2.setMinimumHeight(300)
            self.txt2.setWordWrap(True) #Permet d'aller à la ligne
            self.txt2.move(40,570)
            self.txt2.show()

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            ###On charge le nouveau pokemon###

            #Apparence
            path2=os.path.join(path, "../documents/images/pokemons")
            self.pokemon_dresseur = QLabel(self)
            self.pokemon_dresseur.setGeometry(0,0,300,300)
            pkm_dresseur = QPixmap(path2 +"/" + equipe_dresseur[1].name.lower() +"_dos.png")  
            pkm_dresseur = pkm_dresseur.scaled(200, 200, Qt.KeepAspectRatio)
            self.pokemon_dresseur.setPixmap(pkm_dresseur)
            image_width = pkm_dresseur.width()
            bottom_position=find_bottom_position(pkm_dresseur)
            # Positionnez l'image en soustrayant la largeur et la hauteur de l'image à partir de la position du coin inférieur gauche souhaitée
            self.pokemon_dresseur.move(0 + int(image_width/2), 483 -bottom_position )
            self.pokemon_dresseur.show()

            #Nom
            self.nom_pkm = QLabel(equipe_dresseur[1].name, self)
            self.nom_pkm.setGeometry(0,0,200,100)
            self.nom_pkm.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
            self.nom_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
            self.nom_pkm.setMinimumWidth(144)
            self.nom_pkm.move(580,290) 
            self.nom_pkm.show()

            #PV
            self.pv_pkm= QLabel(str(equipe_dresseur[1].HP) + "/" + str(equipe_dresseur[1].maxHP), self)
            self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
            self.pv_pkm.setAlignment(Qt.AlignRight)
            self.pv_pkm.setMinimumWidth(144)
            self.pv_pkm.move(682,435) 
            self.pv_pkm.show()

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txt2.hide()
            self.button1_label.show()
            self.button2_label.show()
            self.button3_label.show()
            self.button4_label.show()

            self.pokemon_au_combat=2
            
        else:
            self.txt1=QLabel(str(equipe_dresseur[pokemon_au_combat].name).upper() + " is already on the battlefield.",self)
            self.txt1.setAlignment(Qt.AlignLeft)
            self.txt1.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt1.setMinimumWidth(390)
            self.txt1.setMinimumHeight(300)
            self.txt1.setWordWrap(True) #Permet d'aller à la ligne
            self.txt1.move(40,570)
            self.txt1.show()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            self.txt1.hide()
            self.changepkm.show()
            self.pokemon1.show()
            self.pokemon2.show()
            self.pokemon3.show()
            self.pokemon4.show()
            self.pokemon5.show()
            self.pokemon6.show()
            self.retour.show()




    def changetopkm3(self):

        if equipe_dresseur[0].HP==0:
            self.txt1=QLabel(str(equipe_dresseur[2].name).upper() + " is K.O. He can't be sent on the battlefiel.",self)
            self.txt1.setAlignment(Qt.AlignLeft)
            self.txt1.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt1.setMinimumWidth(390)
            self.txt1.setMinimumHeight(300)
            self.txt1.setWordWrap(True) #Permet d'aller à la ligne
            self.txt1.move(40,570)
            self.txt1.show()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txt1.hide()

        if self.pokemon_au_combat != 3:

            self.changepkm.hide()
            self.pokemon1.hide()
            self.pokemon2.hide()
            self.pokemon3.hide()
            self.pokemon4.hide()
            self.pokemon5.hide()
            self.pokemon6.hide()
            self.retour.hide()

            self.txt1=QLabel(str(equipe_dresseur[pokemon_au_combat].name).upper() + ", come back.",self)
            self.txt1.setAlignment(Qt.AlignLeft)
            self.txt1.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt1.setMinimumWidth(390)
            self.txt1.setMinimumHeight(300)
            self.txt1.setWordWrap(True) #Permet d'aller à la ligne
            self.txt1.move(40,570)
            self.txt1.show()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.pokemon_dresseur.hide()
            self.nom_pkm.hide()
            self.pv_pkm.hide()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txt1.hide()
            self.txt2=QLabel(equipe_dresseur[2].name.upper() + ", go!",self)
            self.txt2.setAlignment(Qt.AlignLeft)
            self.txt2.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt2.setMinimumWidth(390)
            self.txt2.setMinimumHeight(300)
            self.txt2.setWordWrap(True) #Permet d'aller à la ligne
            self.txt2.move(40,570)
            self.txt2.show()

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            ###On charge le nouveau pokemon###

            #Apparence
            path2=os.path.join(path, "../documents/images/pokemons")
            self.pokemon_dresseur = QLabel(self)
            self.pokemon_dresseur.setGeometry(0,0,300,300)
            pkm_dresseur = QPixmap(path2 +"/" + equipe_dresseur[2].name.lower() +"_dos.png")  
            pkm_dresseur = pkm_dresseur.scaled(200, 200, Qt.KeepAspectRatio)
            self.pokemon_dresseur.setPixmap(pkm_dresseur)
            image_width = pkm_dresseur.width()
            bottom_position=find_bottom_position(pkm_dresseur)
            # Positionnez l'image en soustrayant la largeur et la hauteur de l'image à partir de la position du coin inférieur gauche souhaitée
            self.pokemon_dresseur.move(0 + int(image_width/2), 483 -bottom_position )
            self.pokemon_dresseur.show()

            #Nom
            self.nom_pkm = QLabel(equipe_dresseur[2].name, self)
            self.nom_pkm.setGeometry(0,0,200,100)
            self.nom_pkm.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
            self.nom_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
            self.nom_pkm.setMinimumWidth(144)
            self.nom_pkm.move(580,290) 
            self.nom_pkm.show()

            #PV
            self.pv_pkm= QLabel(str(equipe_dresseur[2].HP) + "/" + str(equipe_dresseur[2].maxHP), self)
            self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
            self.pv_pkm.setAlignment(Qt.AlignRight)
            self.pv_pkm.setMinimumWidth(144)
            self.pv_pkm.move(682,435) 
            self.pv_pkm.show()

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txt2.hide()
            self.button1_label.show()
            self.button2_label.show()
            self.button3_label.show()
            self.button4_label.show()

            self.pokemon_au_combat=3
        else:
            self.txt1=QLabel(str(equipe_dresseur[pokemon_au_combat].name).upper() + " is already on the battlefield.",self)
            self.txt1.setAlignment(Qt.AlignLeft)
            self.txt1.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt1.setMinimumWidth(390)
            self.txt1.setMinimumHeight(300)
            self.txt1.setWordWrap(True) #Permet d'aller à la ligne
            self.txt1.move(40,570)
            self.txt1.show()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            self.txt1.hide()
            self.changepkm.show()
            self.pokemon1.show()
            self.pokemon2.show()
            self.pokemon3.show()
            self.pokemon4.show()
            self.pokemon5.show()
            self.pokemon6.show()
            self.retour.show()

    def changetopkm1(self):

        if equipe_dresseur[0].HP==0:
            self.txt1=QLabel(str(equipe_dresseur[0].name).upper() + " is K.O. He can't be sent on the battlefiel.",self)
            self.txt1.setAlignment(Qt.AlignLeft)
            self.txt1.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt1.setMinimumWidth(390)
            self.txt1.setMinimumHeight(300)
            self.txt1.setWordWrap(True) #Permet d'aller à la ligne
            self.txt1.move(40,570)
            self.txt1.show()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txt1.hide()

        if self.pokemon_au_combat != 1:

            self.changepkm.hide()
            self.pokemon1.hide()
            self.pokemon2.hide()
            self.pokemon3.hide()
            self.pokemon4.hide()
            self.pokemon5.hide()
            self.pokemon6.hide()
            self.retour.hide()

            self.txt1=QLabel(str(equipe_dresseur[self.pokemon_au_combat].name).upper() + ", come back.",self)
            self.txt1.setAlignment(Qt.AlignLeft)
            self.txt1.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt1.setMinimumWidth(390)
            self.txt1.setMinimumHeight(300)
            self.txt1.setWordWrap(True) #Permet d'aller à la ligne
            self.txt1.move(40,570)
            self.txt1.show()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.pokemon_dresseur.hide()
            self.nom_pkm.hide()
            self.pv_pkm.hide()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txt1.hide()
            self.txt2=QLabel(equipe_dresseur[0].name.upper() + ", go!",self)
            self.txt2.setAlignment(Qt.AlignLeft)
            self.txt2.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt2.setMinimumWidth(390)
            self.txt2.setMinimumHeight(300)
            self.txt2.setWordWrap(True) #Permet d'aller à la ligne
            self.txt2.move(40,570)
            self.txt2.show()

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            ###On charge le nouveau pokemon###

            #Apparence
            path2=os.path.join(path, "../documents/images/pokemons")
            self.pokemon_dresseur = QLabel(self)
            self.pokemon_dresseur.setGeometry(0,0,300,300)
            pkm_dresseur = QPixmap(path2 +"/" + equipe_dresseur[0].name.lower() +"_dos.png")  
            pkm_dresseur = pkm_dresseur.scaled(200, 200, Qt.KeepAspectRatio)
            self.pokemon_dresseur.setPixmap(pkm_dresseur)
            image_width = pkm_dresseur.width()
            bottom_position=find_bottom_position(pkm_dresseur)
            # Positionnez l'image en soustrayant la largeur et la hauteur de l'image à partir de la position du coin inférieur gauche souhaitée
            self.pokemon_dresseur.move(0 + int(image_width/2), 483 -bottom_position )
            self.pokemon_dresseur.show()

            #Nom
            self.nom_pkm = QLabel(equipe_dresseur[0].name, self)
            self.nom_pkm.setGeometry(0,0,200,100)
            self.nom_pkm.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
            self.nom_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
            self.nom_pkm.setMinimumWidth(144)
            self.nom_pkm.move(580,290) 
            self.nom_pkm.show()

            #PV
            self.pv_pkm= QLabel(str(equipe_dresseur[0].HP) + "/" + str(equipe_dresseur[0].maxHP), self)
            self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
            self.pv_pkm.setAlignment(Qt.AlignRight)
            self.pv_pkm.setMinimumWidth(144)
            self.pv_pkm.move(682,435) 
            self.pv_pkm.show()

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txt2.hide()
            self.button1_label.show()
            self.button2_label.show()
            self.button3_label.show()
            self.button4_label.show()
            
            self.pokemon_au_combat=1
        else:
            self.txt1=QLabel(str(equipe_dresseur[pokemon_au_combat].name).upper() + " is already on the battlefield.",self)
            self.txt1.setAlignment(Qt.AlignLeft)
            self.txt1.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
            self.txt1.setMinimumWidth(390)
            self.txt1.setMinimumHeight(300)
            self.txt1.setWordWrap(True) #Permet d'aller à la ligne
            self.txt1.move(40,570)
            self.txt1.show()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            self.txt1.hide()
            self.changepkm.show()
            self.pokemon1.show()
            self.pokemon2.show()
            self.pokemon3.show()
            self.pokemon4.show()
            self.pokemon5.show()
            self.pokemon6.show()
            self.retour.show()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CombatPokemon()
    window.show()
    sys.exit(app.exec_())





