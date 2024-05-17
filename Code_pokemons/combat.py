import pokemon as pk
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QVBoxLayout,QWidget
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QTimer, QEventLoop
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
import os

path=os.path.dirname(os.path.abspath(__file__))
path2=os.path.join(path, "../documents/images/pokemons")


mew = pk.Pokemon("Dratini")
salameche= pk.Pokemon("Mewtwo")
bulbizare= pk.Pokemon("Bulbasaur")
dracolosse=pk.Pokemon("Dragonite")
papilusion=pk.Pokemon("Butterfree")
arcanin=pk.Pokemon("Arcanine")
mewtwo=pk.Pokemon("Ditto")
vide=pk.Pokemon("Vide")



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
    def __init__(self,equipe_pokemon,pokemon_adverse,inventaire):
        super().__init__()
        self.equipe_dresseur=equipe_pokemon
        self.pokemon_adverse=pokemon_adverse
        self.inventaire=inventaire
        self.initUI()

    def initUI(self):
        self.pokemon_au_combat=1
        k=0
        while self.equipe_dresseur[k].HP ==0:
            k+=1
        pokemon_allie=self.equipe_dresseur[k]
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
        self.affiche_pkm_dresseur(pokemon_allie)

        #Affichage de la barre d'HP du pokemon du dresseur
        self.hpbar_dresseur=QLabel(self)
        self.hpbar_dresseur.setGeometry(0,0,300,50)
        self.hpbar_dresseur.setAlignment(Qt.AlignRight)
        path_hpbar=os.path.join(path,"VFX_SFX\Barre_hp.png")
        barre = QPixmap(path_hpbar)  
        pourcentage=pokemon_allie.HP/pokemon_allie.maxHP
        taille_barre=int(148-148*pourcentage)
        barre= barre.scaled(taille_barre, 150)  #148
        self.hpbar_dresseur.setPixmap(barre)
        self.hpbar_dresseur.move(527,367)

        #Affichage du pokemon sauvage
        self.pokemon_sauvage = QLabel(self)
        self.pokemon_sauvage.setGeometry(0,0,300,300)
        pkm_sauvage = QPixmap(path2 + "/" + self.pokemon_adverse.name.lower() +"_face.png")  

        pkm_sauvage= pkm_sauvage.scaled(200, 200, Qt.KeepAspectRatio)
        bottom_position2 = find_bottom_position(pkm_sauvage)
        self.pokemon_sauvage.setPixmap(pkm_sauvage)
        image2_width=pkm_sauvage.width()
        self.pokemon_sauvage.move(525 + int(image2_width/2), 200-bottom_position2)

        #Barre d'HP
        self.hpbar_sauvage=QLabel(self)
        self.hpbar_sauvage.setGeometry(0,0,300,300)
        self.hpbar_sauvage.setAlignment(Qt.AlignRight)
        path_hpbar=os.path.join(path,"VFX_SFX\Barre_hp.png")
        barre = QPixmap(path_hpbar)  
        barre= barre.scaled(0, 170)       #167
        self.hpbar_sauvage.setPixmap(barre)
        self.hpbar_sauvage.move(183,72)



        #Affichage du nom du pokemon sauvage
        self.nom_pkm_s = QLabel(self.pokemon_adverse.name, self)
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


        #Texte qui indique la possibilité de changer de pokemon
        self.changepkm=QLabel("Change your pokemon",self)
        self.changepkm.setAlignment(Qt.AlignLeft)
        self.changepkm.setStyleSheet("QLabel { color: black; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.changepkm.setMinimumWidth(390)
        self.changepkm.move(500,570)
        self.changepkm.hide()


        if self.equipe_dresseur[0].generation!=2:
        
            self.pokemon1=ClickableLabel(self.equipe_dresseur[0].name.upper(), 13,self)
            self.pokemon1.setAlignment(Qt.AlignLeft)
            self.pokemon1.setMinimumWidth(130)
            self.pokemon1.setMaximumHeight(15)
            self.pokemon1.move(510,600)
            self.pokemon1.hide()
            self.pokemon1.clicked.connect(self.changetopkm1)

            if self.equipe_dresseur[1].generation!=2:
        
                self.pokemon2=ClickableLabel(self.equipe_dresseur[1].name.upper(), 13,self)
                self.pokemon2.setAlignment(Qt.AlignLeft)
                self.pokemon2.setMinimumWidth(130)
                self.pokemon2.setMaximumHeight(15)
                self.pokemon2.move(680,600)
                self.pokemon2.hide()
                self.pokemon2.clicked.connect(self.changetopkm2)

            if self.equipe_dresseur[2].generation!=2:
        
                self.pokemon3=ClickableLabel(self.equipe_dresseur[2].name.upper(), 13,self)
                self.pokemon3.setAlignment(Qt.AlignLeft)
                self.pokemon3.setMinimumWidth(130)
                self.pokemon3.setMaximumHeight(15)
                self.pokemon3.move(510,620)
                self.pokemon3.hide()
                self.pokemon3.clicked.connect(self.changetopkm3)
            
            if self.equipe_dresseur[3].generation!=2:
        
                self.pokemon4=ClickableLabel(self.equipe_dresseur[3].name.upper(), 13,self)
                self.pokemon4.setAlignment(Qt.AlignLeft)
                self.pokemon4.setMinimumWidth(130)
                self.pokemon4.setMaximumHeight(15)
                self.pokemon4.move(680,620)
                self.pokemon4.hide()
                self.pokemon4.clicked.connect(self.changetopkm4)


            if self.equipe_dresseur[4].generation!=2:
        
                self.pokemon5=ClickableLabel(self.equipe_dresseur[4].name.upper(), 13,self)
                self.pokemon5.setAlignment(Qt.AlignLeft)
                self.pokemon5.setMinimumWidth(130)
                self.pokemon5.setMaximumHeight(15)
                self.pokemon5.move(510,640)
                self.pokemon5.hide()
                self.pokemon5.clicked.connect(self.changetopkm5)

            if self.equipe_dresseur[5].generation!=2:
        
                self.pokemon6=ClickableLabel(self.equipe_dresseur[5].name.upper(), 13,self)
                self.pokemon6.setAlignment(Qt.AlignLeft)
                self.pokemon6.setMinimumWidth(130)
                self.pokemon6.setMaximumHeight(15)
                self.pokemon6.move(680,640)
                self.pokemon6.hide()
                self.pokemon6.clicked.connect(self.changetopkm6)

        self.txt_blanc("")
        self.pokemon_justKO=False
        self.pokemon_au_combat=1

        self.button1_label.clicked.connect(self.fight)
        self.retour.clicked.connect(self.back)
        self.button3_label.clicked.connect(self.sac)
        self.button4_label.clicked.connect(self.fuite)
        self.button2_label.clicked.connect(self.change)
        self.potion.clicked.connect(self.use_potion)
        self.attaque1.clicked.connect(self.atk1)
        self.attaque2.clicked.connect(self.atk2)


    #Definition des methodes
    def fight(self):
        self.cache_menu_principal()
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
        self.cache_menu_changepkm()

        #Fais apparaitre le menu principal
        self.affiche_menu_principal()

    def sac(self):
        self.cache_menu_principal()
        self.potion.show()
        self.retour.show()

    def fuite(self):
        #Changement de la musique
        if not self.pokemon_adverse.legendary:

            #On change la musique pour mettre le bruit de fuite
            path_musique=os.path.join(path, "VFX_SFX\Pokémon RedBlueYellow - Run Away - Sound Effect.mp3")
            self.mediaPlayer = QMediaPlayer()
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path_musique)))
            self.mediaPlayer.play()
            #On met en place l'interface de fuite
            self.cache_menu_principal()
            self.txt_blanc("Got away safely!")
            QTimer.singleShot(2000,self.close)
        
        else:
            self.txt_blanc("You can't run away from a Legendary Pokemon!")
            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            self.txtblanc.hide()
    
    def change(self):
        self.cache_menu_principal()
        self.affiche_menu_changepkm()
    
    def affiche_menu_principal(self):
        self.button1_label.show()
        self.button2_label.show()
        self.button3_label.show()
        self.button4_label.show()
    
    def cache_menu_principal(self):
        self.button1_label.hide()
        self.button2_label.hide()
        self.button3_label.hide()
        self.button4_label.hide()
    
    def affiche_menu_changepkm(self):
        self.changepkm.show()
        self.pokemon1.show()
        if self.equipe_dresseur[1].generation!=2:
            self.pokemon2.show()
        if self.equipe_dresseur[2].generation!=2:
            self.pokemon3.show()
        if self.equipe_dresseur[3].generation!=2:
            self.pokemon4.show()
        if self.equipe_dresseur[4].generation!=2:
            self.pokemon5.show()
        if self.equipe_dresseur[5].generation!=2:
            self.pokemon6.show()
        self.retour.show()

    def cache_menu_changepkm(self):
        self.changepkm.hide()
        self.pokemon1.hide()
        if self.equipe_dresseur[1].generation!=2:
            self.pokemon2.hide()
        if self.equipe_dresseur[2].generation!=2:
            self.pokemon3.hide()
        if self.equipe_dresseur[3].generation!=2:
            self.pokemon4.hide()
        if self.equipe_dresseur[4].generation!=2:
            self.pokemon5.hide()
        if self.equipe_dresseur[5].generation!=2:
            self.pokemon6.hide()
        self.retour.hide()

    def changetopkm2(self):
        self.txtblanc.hide()
        if self.equipe_dresseur[1].HP==0:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[1].name).upper() + " is K.O. He can't be sent on the battlefield.")
            
            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

        elif self.pokemon_au_combat != 2:

            self.txtblanc.hide()
            self.cache_menu_changepkm()

            if not self.pokemon_justKO:
                self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + ", come back.")

                loop=QEventLoop()
                QTimer.singleShot(1500,loop.quit)
                loop.exec_()

            #Enleve le sprite du pokemon, ses PV, son nom
            self.pokemon_dresseur.hide()
            self.nom_pkm.hide()
            self.pv_pkm.hide()
            self.hpbar_dresseur.hide()

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txtblanc.hide()
            self.txt_blanc(self.equipe_dresseur[1].name.upper() + ", go!")

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            ###On charge le nouveau pokemon###
            self.affiche_pkm_dresseur(self.equipe_dresseur[1])
            self.hpbar_dresseur.hide()
            self.maj_barre_hp_dresseur(self.equipe_dresseur[1])

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

            self.affiche_menu_principal()
            #Le pokemon adverse attaque
            if  not self.pokemon_justKO:
                self.txtblanc.hide()
                self.cache_menu_principal()
                result=self.pokemon_adverse.attaque(self.equipe_dresseur[1]) # Renvoie les PV du pokemon apres avoir subit l'attaque, le nom de l'attaque, le coefficient multiplicateur
                self.txt_blanc("Ennemy " + str(self.pokemon_adverse.name).upper() +" uses " + result[1] +".")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()
            
                self.txtblanc.hide()
                #Mise a jour des PV
                self.pv_pkm.hide()
                self.pv_pkm= QLabel(str(int(self.equipe_dresseur[1].HP)) + "/" + str(self.equipe_dresseur[1].maxHP), self)
                self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
                self.pv_pkm.setAlignment(Qt.AlignRight)
                self.pv_pkm.setMinimumWidth(144)
                self.pv_pkm.move(682,435) 
                self.pv_pkm.show()

                self.hpbar_dresseur.hide()
                self.maj_barre_hp_dresseur(self.equipe_dresseur[1])

                if result[2]<1:
                    self.txt_blanc("This isn't very effective...")

                elif result[2]==0:
                    self.txt_blanc("It doesn't affect " + self.equipe_dresseur[self.pokemon_au_combat-1].name +".")

                elif result[2]>1:
                    self.txt_blanc("It's super effective !")
                

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_principal()
                self.txtblanc.hide()

            self.pokemon_justKO=False
             #Si le pokemon est KO:
            if self.equipe_dresseur[1].HP==0:
                self.txtblanc.hide()
                self.cache_menu_principal()
                self.pokemon_justKO[0]=True
                self.cache_menu_principal()
                self.pokemon_dresseur.hide()
                self.txt_blanc(self.equipe_dresseur[1].name.upper() + " is K.O. Choose an other pokemon.")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_changepkm()
                self.retour.hide()
                
            self.pokemon_au_combat=2
            
        else:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + " is already on the battlefield.")

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            
            self.txtblanc.hide()
            self.affiche_menu_changepkm()

    def changetopkm1(self):
        self.txtblanc.hide()
        if self.equipe_dresseur[0].HP==0:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[0].name).upper() + " is K.O. He can't be sent on the battlefiel.")
            
            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

        elif self.pokemon_au_combat != 1:
            self.txtblanc.hide()
            self.cache_menu_changepkm()
            if not self.pokemon_justKO:
                self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + ", come back.")

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            #Enleve le sprite du pokemon, ses PV, son nom
            self.pokemon_dresseur.hide()
            self.nom_pkm.hide()
            self.pv_pkm.hide()

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txtblanc.hide()
            self.txt_blanc(self.equipe_dresseur[0].name.upper() + ", go!")

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            ###On charge le nouveau pokemon###
            self.affiche_pkm_dresseur(self.equipe_dresseur[0])
            self.hpbar_dresseur.hide()
            self.maj_barre_hp_dresseur(self.equipe_dresseur[0])

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

            self.affiche_menu_principal()
            #Le pokemon adverse attaque
            if  not self.pokemon_justKO:
                self.txtblanc.hide()
                self.cache_menu_principal()
                result=self.pokemon_adverse.attaque(self.equipe_dresseur[0]) # Renvoie les PV du pokemon apres avoir subit l'attaque, le nom de l'attaque, le coefficient multiplicateur
                self.txt_blanc("Ennemy " + str(self.pokemon_adverse.name).upper() +" uses " + result[1] +".")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()
            
                self.txtblanc.hide()
                #Mise a jour des PV
                self.pv_pkm.hide()
                self.pv_pkm= QLabel(str(int(self.equipe_dresseur[0].HP)) + "/" + str(self.equipe_dresseur[0].maxHP), self)
                self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
                self.pv_pkm.setAlignment(Qt.AlignRight)
                self.pv_pkm.setMinimumWidth(144)
                self.pv_pkm.move(682,435) 
                self.pv_pkm.show()

                self.hpbar_dresseur.hide()
                self.maj_barre_hp_dresseur(self.equipe_dresseur[0])

                if result[2]<1:
                    self.txt_blanc("This isn't very effective...")

                elif result[2]==0:
                    self.txt_blanc("It doesn't affect " + self.equipe_dresseur[self.pokemon_au_combat-1].name +".")

                elif result[2]>1:
                    self.txt_blanc("It's super effective !")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_principal()
                self.txtblanc.hide()
            self.pokemon_justKO=False

             #Si le pokemon est KO:
            if self.equipe_dresseur[0].HP==0:
                self.txtblanc.hide()
                self.cache_menu_principal()
                self.pokemon_justKO=True
                self.cache_menu_principal()
                self.pokemon_dresseur.hide()
                self.txt_blanc(self.equipe_dresseur[0].name.upper() + " is K.O. Choose an other pokemon.")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_changepkm()
                self.retour.hide()

            
            self.pokemon_au_combat=1
            
        else:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + " is already on the battlefield.")

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            
            self.txtblanc.hide()
            self.affiche_menu_changepkm()

    def changetopkm3(self):
        self.txtblanc.hide()
        if self.equipe_dresseur[2].HP==0:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[2].name).upper() + " is K.O. He can't be sent on the battlefiel.")
            
            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

        elif self.pokemon_au_combat != 3:
            self.txtblanc.hide()
            self.cache_menu_changepkm()
            if not self.pokemon_justKO:
                self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + ", come back.")

                loop=QEventLoop()
                QTimer.singleShot(1500,loop.quit)
                loop.exec_()

            #Enleve le sprite du pokemon, ses PV, son nom
            self.pokemon_dresseur.hide()
            self.nom_pkm.hide()
            self.pv_pkm.hide()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()
            self.txt_blanc(self.equipe_dresseur[2].name.upper() + ", go!")

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            ###On charge le nouveau pokemon###
            self.affiche_pkm_dresseur(self.equipe_dresseur[2])
            self.hpbar_dresseur.hide()
            self.maj_barre_hp_dresseur(self.equipe_dresseur[2])

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

            self.affiche_menu_principal()
            #Le pokemon adverse attaque
            if  not self.pokemon_justKO:
                self.txtblanc.hide()
                self.cache_menu_principal()
                result=self.pokemon_adverse.attaque(self.equipe_dresseur[2]) # Renvoie les PV du pokemon apres avoir subit l'attaque, le nom de l'attaque, le coefficient multiplicateur
                self.txt_blanc("Ennemy " + str(self.pokemon_adverse.name).upper() +" uses " + result[1] +".")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()
            
                self.txtblanc.hide()
                #Mise a jour des PV
                self.pv_pkm.hide()
                self.pv_pkm= QLabel(str(int(self.equipe_dresseur[2].HP)) + "/" + str(self.equipe_dresseur[2].maxHP), self)
                self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
                self.pv_pkm.setAlignment(Qt.AlignRight)
                self.pv_pkm.setMinimumWidth(144)
                self.pv_pkm.move(682,435) 
                self.pv_pkm.show()
                self.hpbar_dresseur.hide()
                self.maj_barre_hp_dresseur(self.equipe_dresseur[2])

                if result[2]<1:
                    self.txt_blanc("This isn't very effective...")

                elif result[2]==0:
                    self.txt_blanc("It doesn't affect " + self.equipe_dresseur[self.pokemon_au_combat-1].name +".")

                elif result[2]>1:
                    self.txt_blanc("It's super effective !")


                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_principal()
                self.txtblanc.hide()

            self.pokemon_justKO=False
             #Si le pokemon est KO:
            if self.equipe_dresseur[2].HP==0:
                self.txtblanc.hide()
                self.cache_menu_principal()
                self.pokemon_justKO=True
                self.cache_menu_principal()
                self.pokemon_dresseur.hide()
                self.txt_blanc(self.equipe_dresseur[2].name.upper() + " is K.O. Choose an other pokemon.")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_changepkm()
                self.retour.hide()


            self.pokemon_au_combat=3
            
        else:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + " is already on the battlefield.")

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            
            self.txtblanc.hide()
            self.affiche_menu_changepkm()

    def changetopkm4(self):
        self.txtblanc.hide()
        if self.equipe_dresseur[3].HP==0:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[3].name).upper() + " is K.O. He can't be sent on the battlefiel.")
            
            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

        elif self.pokemon_au_combat != 4:
            self.txtblanc.hide()
            self.cache_menu_changepkm()
            if not self.pokemon_justKO:
                self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + ", come back.")

                loop=QEventLoop()
                QTimer.singleShot(1500,loop.quit)
                loop.exec_()

            #Enleve le sprite du pokemon, ses PV, son nom
            self.pokemon_dresseur.hide()
            self.nom_pkm.hide()
            self.pv_pkm.hide()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()
            self.txt_blanc(self.equipe_dresseur[3].name.upper() + ", go!")

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            ###On charge le nouveau pokemon###
            self.affiche_pkm_dresseur(self.equipe_dresseur[3])
            self.hpbar_dresseur.hide()
            self.maj_barre_hp_dresseur(self.equipe_dresseur[3])

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

            self.affiche_menu_principal()
            #Le pokemon adverse attaque
            if  not self.pokemon_justKO:
                self.txtblanc.hide()
                self.cache_menu_principal()
                result=self.pokemon_adverse.attaque(self.equipe_dresseur[3]) # Renvoie les PV du pokemon apres avoir subit l'attaque, le nom de l'attaque, le coefficient multiplicateur
                self.txt_blanc("Ennemy " + str(self.pokemon_adverse.name).upper() +" uses " + result[1] +".")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()
            
                self.txtblanc.hide()
                #Mise a jour des PV
                self.pv_pkm.hide()
                self.pv_pkm= QLabel(str(int(self.equipe_dresseur[3].HP)) + "/" + str(self.equipe_dresseur[3].maxHP), self)
                self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
                self.pv_pkm.setAlignment(Qt.AlignRight)
                self.pv_pkm.setMinimumWidth(144)
                self.pv_pkm.move(682,435) 
                self.pv_pkm.show()
                self.hpbar_dresseur.hide()
                self.maj_barre_hp_dresseur(self.equipe_dresseur[3])

                if result[2]<1:
                    self.txt_blanc("This isn't very effective...")

                elif result[2]==0:
                    self.txt_blanc("It doesn't affect " + self.equipe_dresseur[self.pokemon_au_combat-1].name +".")

                elif result[2]>1:
                    self.txt_blanc("It's super effective !")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_principal()
                self.txtblanc.hide()

            self.pokemon_justKO=False
             #Si le pokemon est KO:
            if self.equipe_dresseur[3].HP==0:
                self.txtblanc.hide()
                self.cache_menu_principal()
                self.pokemon_justKO=True
                self.cache_menu_principal()
                self.pokemon_dresseur.hide()
                self.txt_blanc(self.equipe_dresseur[3].name.upper() + " is K.O. Choose an other pokemon.")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_changepkm()
                self.retour.hide()


            self.pokemon_au_combat=4
            
        else:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + " is already on the battlefield.")

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            
            self.txtblanc.hide()
            self.affiche_menu_changepkm()

    def changetopkm5(self):
        self.txtblanc.hide()
        if self.equipe_dresseur[4].HP==0:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[4].name).upper() + " is K.O. He can't be sent on the battlefiel.")
            
            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

        elif self.pokemon_au_combat != 5:
            self.txtblanc.hide()
            self.cache_menu_changepkm()
            if not self.pokemon_justKO:
                self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + ", come back.")

                loop=QEventLoop()
                QTimer.singleShot(1500,loop.quit)
                loop.exec_()

            #Enleve le sprite du pokemon, ses PV, son nom
            self.pokemon_dresseur.hide()
            self.nom_pkm.hide()
            self.pv_pkm.hide()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()
            self.txt_blanc(self.equipe_dresseur[4].name.upper() + ", go!")

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            ###On charge le nouveau pokemon###
            self.affiche_pkm_dresseur(self.equipe_dresseur[4])
            self.hpbar_dresseur.hide()
            self.maj_barre_hp_dresseur(self.equipe_dresseur[4])

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

            self.affiche_menu_principal()
            #Le pokemon adverse attaque
            if  not self.pokemon_justKO:
                self.txtblanc.hide()
                self.cache_menu_principal()
                result=self.pokemon_adverse.attaque(self.equipe_dresseur[4]) # Renvoie les PV du pokemon apres avoir subit l'attaque, le nom de l'attaque, le coefficient multiplicateur
                self.txt_blanc("Ennemy " + str(self.pokemon_adverse.name).upper() +" uses " + result[1] +".")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()
            
                self.txtblanc.hide()
                #Mise a jour des PV
                self.pv_pkm.hide()
                self.pv_pkm= QLabel(str(int(self.equipe_dresseur[4].HP)) + "/" + str(self.equipe_dresseur[4].maxHP), self)
                self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
                self.pv_pkm.setAlignment(Qt.AlignRight)
                self.pv_pkm.setMinimumWidth(144)
                self.pv_pkm.move(682,435) 
                self.pv_pkm.show()
                self.hpbar_dresseur.hide()
                self.maj_barre_hp_dresseur(self.equipe_dresseur[4])

                if result[2]<1:
                    self.txt_blanc("This isn't very effective...")

                elif result[2]==0:
                    self.txt_blanc("It doesn't affect " + self.equipe_dresseur[self.pokemon_au_combat-1].name +".")

                elif result[2]>1:
                    self.txt_blanc("It's super effective !")
                

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_principal()
                self.txtblanc.hide()

            self.pokemon_justKO=False
             #Si le pokemon est KO:
            if self.equipe_dresseur[4].HP==0:
                self.txtblanc.hide()
                self.cache_menu_principal()
                self.pokemon_justKO=True
                self.cache_menu_principal()
                self.pokemon_dresseur.hide()
                self.txt_blanc(self.equipe_dresseur[4].name.upper() + " is K.O. Choose an other pokemon.")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_changepkm()
                self.retour.hide()


            self.pokemon_au_combat=5
            
        else:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + " is already on the battlefield.")

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            
            self.txtblanc.hide()
            self.affiche_menu_changepkm()

    def changetopkm6(self):
        self.txtblanc.hide()
        if self.equipe_dresseur[5].HP==0:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[5].name).upper() + " is K.O. He can't be sent on the battlefiel.")
            
            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

        elif self.pokemon_au_combat != 6:
            self.txtblanc.hide()
            self.cache_menu_changepkm()
            if not self.pokemon_justKO:
                self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + ", come back.")

                loop=QEventLoop()
                QTimer.singleShot(1500,loop.quit)
                loop.exec_()

            #Enleve le sprite du pokemon, ses PV, son nom
            self.pokemon_dresseur.hide()
            self.nom_pkm.hide()
            self.pv_pkm.hide()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()
            self.txt_blanc(self.equipe_dresseur[5].name.upper() + ", go!")

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            ###On charge le nouveau pokemon###
            self.affiche_pkm_dresseur(self.equipe_dresseur[5])
            self.hpbar_dresseur.hide()
            self.maj_barre_hp_dresseur(self.equipe_dresseur[5])

            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

            self.txtblanc.hide()

            self.affiche_menu_principal()
            #Le pokemon adverse attaque
            if  not self.pokemon_justKO:
                self.txtblanc.hide()
                self.cache_menu_principal()
                result=self.pokemon_adverse.attaque(self.equipe_dresseur[5]) # Renvoie les PV du pokemon apres avoir subit l'attaque, le nom de l'attaque, le coefficient multiplicateur
                self.txt_blanc("Ennemy " + str(self.pokemon_adverse.name).upper() +" uses " + result[1] +".")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()
            
                self.txtblanc.hide()
                #Mise a jour des PV
                self.pv_pkm.hide()
                self.pv_pkm= QLabel(str(int(self.equipe_dresseur[5].HP)) + "/" + str(self.equipe_dresseur[5].maxHP), self)
                self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
                self.pv_pkm.setAlignment(Qt.AlignRight)
                self.pv_pkm.setMinimumWidth(144)
                self.pv_pkm.move(682,435) 
                self.pv_pkm.show()
                self.hpbar_dresseur.hide()
                self.maj_barre_hp_dresseur(self.equipe_dresseur[5])

                if result[2]<1:
                    self.txt_blanc("This isn't very effective...")

                elif result[2]==0:
                    self.txt_blanc("It doesn't affect " + self.equipe_dresseur[self.pokemon_au_combat-1].name +".")

                elif result[2]>1:
                    self.txt_blanc("It's super effective !")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_principal()
                self.txtblanc.hide()

            self.pokemon_justKO=False
             #Si le pokemon est KO:
            if self.equipe_dresseur[5].HP==0:
                self.txtblanc.hide()
                self.cache_menu_principal()
                self.pokemon_justKO=True
                self.cache_menu_principal()
                self.pokemon_dresseur.hide()
                self.txt_blanc(self.equipe_dresseur[5].name.upper() + " is K.O. Choose an other pokemon.")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.affiche_menu_changepkm()
                self.retour.hide()


            self.pokemon_au_combat=6
            
        else:
            self.txtblanc.hide()
            self.txt_blanc(str(self.equipe_dresseur[self.pokemon_au_combat-1].name).upper() + " is already on the battlefield.")

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            
            self.txtblanc.hide()
            self.affiche_menu_changepkm()

    def affiche_pkm_dresseur(self,pokemon):
         #Affichage du pokemon du dresseur
        self.pokemon_dresseur = QLabel(self)
        self.pokemon_dresseur.setGeometry(0,0,300,300)
        pkm_dresseur = QPixmap(path2 +"/" + pokemon.name.lower() +"_dos.png")  

        pkm_dresseur = pkm_dresseur.scaled(200, 200, Qt.KeepAspectRatio)
        self.pokemon_dresseur.setPixmap(pkm_dresseur)
        image_width = pkm_dresseur.width()
        bottom_position=find_bottom_position(pkm_dresseur)
        # Positionnez l'image en soustrayant la largeur et la hauteur de l'image à partir de la position du coin inférieur gauche souhaitée
        self.pokemon_dresseur.move(0 + int(image_width/2), 483 -bottom_position )
        self.pokemon_dresseur.show()

        #Affichage du nom du pokemon du Dresseur
        self.nom_pkm = QLabel(pokemon.name, self)
        self.nom_pkm.setGeometry(0,0,200,100)
        self.nom_pkm.setAlignment(Qt.AlignLeft | Qt.AlignBottom)  # Alignement en bas à gauche
        self.nom_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.nom_pkm.setMinimumWidth(144)
        self.nom_pkm.move(580,290) 
        self.nom_pkm.show()

        #Affichage du nombre de pv du pokemon du dresseur
        self.pv_pkm= QLabel(str(int(pokemon.HP)) + "/" + str(pokemon.maxHP), self)
        self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.pv_pkm.setAlignment(Qt.AlignRight)
        self.pv_pkm.setMinimumWidth(144)
        self.pv_pkm.move(682,435) 
        self.pv_pkm.show()

        #Change ses attaques
        self.attaque1=ClickableLabel(pokemon.attaque_normale.upper(),17, self)
        self.attaque1.setAlignment(Qt.AlignCenter)
        self.attaque1.setMinimumWidth(142)
        self.attaque1.move(480,600)
        self.attaque1.hide()
        self.attaque1.clicked.connect(self.atk1)

        self.attaque2=ClickableLabel(pokemon.attaque_type.upper(),17, self)
        self.attaque2.setAlignment(Qt.AlignCenter)
        self.attaque2.setMinimumWidth(186)
        self.attaque2.move(650,600)
        self.attaque2.hide()
        self.attaque2.clicked.connect(self.atk2)

    def txt_blanc(self,txt):
        self.txtblanc=QLabel(txt,self)
        self.txtblanc.setAlignment(Qt.AlignLeft)
        self.txtblanc.setStyleSheet("QLabel { color: white; font-size: 17px; font-family: 'Press Start 2P'; }")
        self.txtblanc.setMinimumWidth(390)
        self.txtblanc.setMinimumHeight(300)
        self.txtblanc.setWordWrap(True) #Permet d'aller à la ligne
        self.txtblanc.move(40,570)
        self.txtblanc.show()

    def use_potion(self):
        self.potion.hide()
        self.retour.hide()
        if self.equipe_dresseur[self.pokemon_au_combat-1].HP == self.equipe_dresseur[self.pokemon_au_combat-1].maxHP:
            self.txt_blanc("You can't use a potion, " + self.equipe_dresseur[self.pokemon_au_combat-1].name + " is already full health.")

            loop=QEventLoop()
            QTimer.singleShot(2000,loop.quit)
            loop.exec_()

            self.txtblanc.hide()
            self.affiche_menu_principal()

        else:
            result=self.equipe_dresseur[self.pokemon_au_combat-1].potion()
            self.txt_blanc("You restaured " + str(result) + "HP to " + self.equipe_dresseur[self.pokemon_au_combat-1].name +".")

            #Mise a jour des HP
            self.pv_pkm.hide()
            self.pv_pkm= QLabel(str(int(self.equipe_dresseur[self.pokemon_au_combat -1].HP)) + "/" + str(self.equipe_dresseur[self.pokemon_au_combat -1].maxHP), self)
            self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
            self.pv_pkm.setAlignment(Qt.AlignRight)
            self.pv_pkm.setMinimumWidth(144)
            self.pv_pkm.move(682,435) 
            self.pv_pkm.show()
            #Mise a jour de la barre des HP du dresseur
            self.hpbar_dresseur.hide()
            self.maj_barre_hp_dresseur(self.equipe_dresseur[self.pokemon_au_combat -1])


            loop=QEventLoop()
            QTimer.singleShot(2000,loop.quit)
            loop.exec_()

            self.txtblanc.hide()
            
            #Au tour du pokemon adverse d'attaquer
            self.attaque_sauvage()
            self.is_KO()
            self.affiche_menu_principal()

    def attaque_sauvage(self):

        self.txtblanc.hide()
        self.cache_menu_principal()
        result=self.pokemon_adverse.attaque(self.equipe_dresseur[self.pokemon_au_combat -1]) # Renvoie les PV du pokemon apres avoir subit l'attaque, le nom de l'attaque, le coefficient multiplicateur
        self.txt_blanc("Ennemy " + str(self.pokemon_adverse.name).upper() +" uses " + result[1] +".")

        loop=QEventLoop()
        QTimer.singleShot(1500,loop.quit)
        loop.exec_()
            
        self.txtblanc.hide()
        #Mise a jour des PV
        self.pv_pkm.hide()
        self.pv_pkm= QLabel(str(int(self.equipe_dresseur[self.pokemon_au_combat-1].HP)) + "/" + str(self.equipe_dresseur[self.pokemon_au_combat -1].maxHP), self)
        self.pv_pkm.setStyleSheet("QLabel { color: black; font-size: 19px; font-family: 'Press Start 2P'; }")  # Style du texte
        self.pv_pkm.setAlignment(Qt.AlignRight)
        self.pv_pkm.setMinimumWidth(144)
        self.pv_pkm.move(682,435) 
        self.pv_pkm.show()
        self.hpbar_dresseur.hide()
        self.maj_barre_hp_dresseur(self.equipe_dresseur[self.pokemon_au_combat -1])

        if result[2]>1:
            self.txtblanc.hide()
            self.txt_blanc("It's super effective!")
            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()
            
        elif result[2]==0:
            self.txtblanc.hide()
            self.txt_blanc("It doesn't affect ennemy " + self.equipe_dresseur[self.pokemon_au_combat -1].name +".")
            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

        elif result[2]<1:
            self.txtblanc.hide()
            self.txt_blanc("It's not very effective...")
            loop=QEventLoop()
            QTimer.singleShot(1000,loop.quit)
            loop.exec_()

        #self.affiche_menu_principal()
        self.txtblanc.hide()

    def is_KO(self):

        k=0
        for i in range(6):
            if self.equipe_dresseur[i].HP==0:
                k+=1
        if k==6:
            self.txtblanc.hide()
            self.cache_menu_changepkm()
            self.cache_menu_principal()
            self.potion.hide()
            self.txt_blanc(self.equipe_dresseur[self.pokemon_au_combat -1].name.upper() + " is K.O.")
            self.pokemon_dresseur.hide()
            self.pokemon_dresseur.hide()
            self.nom_pkm.hide()
            self.pv_pkm.hide()

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.txtblanc.hide()
            self.txt_blanc("All your Pokemons are K.O. You run back home to heal them.")

            QTimer.singleShot(3000,self.close)

        elif self.equipe_dresseur[self.pokemon_au_combat -1].HP==0:
            self.txtblanc.hide()
            self.cache_menu_changepkm()
            self.cache_menu_principal()
            self.potion.hide()
            self.pokemon_justKO=True
            self.pokemon_dresseur.hide()
            self.txt_blanc(self.equipe_dresseur[self.pokemon_au_combat -1].name.upper() + " is K.O. Choose an other pokemon.")

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            self.affiche_menu_changepkm()
            self.cache_menu_principal()
            self.txtblanc.hide()
            self.retour.hide()
        else:
            self.affiche_menu_principal()

    def atk1(self):
        self.attaque1.hide()
        self.attaque2.hide()
        self.retour.hide()
        self.txtblanc.hide()
        allie=self.equipe_dresseur[self.pokemon_au_combat -1]
        ennemi=self.pokemon_adverse
        if allie.speed>=ennemi.speed:
            result=allie.attaque(ennemi,1)
            self.txt_blanc(allie.name.upper() + " uses " +allie.attaque_normale +"!")

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()
            ennemi.HP=result[0]
            if ennemi.HP<0:
                    ennemi.HP=0
            self.hpbar_sauvage.hide()
            self.maj_barre_hp_sauvage(ennemi)

            if result[1]>1:
                self.txtblanc.hide()
                self.txt_blanc("It's super effective!")
                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()
            
            elif result[1]==0:
                self.txtblanc.hide()
                self.txt_blanc("It doesn't affect ennemy " + ennemi.name +".")
                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

            elif result[1]<1:
                self.txtblanc.hide()
                self.txt_blanc("It's not very effective...")
                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

            else:
                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

            
            self.txtblanc.hide()

            if ennemi.HP<=0:
                path_musique=os.path.join(path, "VFX_SFX\Victory! Wild Pokemon - Pokémon Diamond & Pearl.mp3")
                self.mediaPlayer = QMediaPlayer()
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path_musique)))
                self.mediaPlayer.play()
                self.cache_menu_principal
                self.pokemon_sauvage.hide()
                self.nom_pkm_s.hide()
                self.txt_blanc(ennemi.name.upper() + "is K.O. You catch him!")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.txtblanc.hide()
                self.txt_blanc("He got sent in your inventory")
                self.inventaire.append(ennemi.name)

                QTimer.singleShot(2000,self.close)
            
            else:
                self.attaque_sauvage()
                self.is_KO()

        else:
            self.attaque_sauvage()
            self.is_KO()
            if self.equipe_dresseur[self.pokemon_au_combat -1].HP!=0:
                result=allie.attaque(ennemi,1)
                self.txt_blanc(allie.name.upper() + " uses " +allie.attaque_normale +"!")

                loop=QEventLoop()
                QTimer.singleShot(1500,loop.quit)
                loop.exec_()

                ennemi.HP=result[0]
                if ennemi.HP<0:
                    ennemi.HP=0
                self.hpbar_sauvage.hide()
                self.maj_barre_hp_sauvage(ennemi)

                if result[1]>1:
                    self.txtblanc.hide()
                    self.txt_blanc("It's super effective!")
                    loop=QEventLoop()
                    QTimer.singleShot(1000,loop.quit)
                    loop.exec_()

                elif result[1]==0:
                    self.txtblanc.hide()
                    self.txt_blanc("It doesn't affect ennemy " + ennemi.name +".")
                    loop=QEventLoop()
                    QTimer.singleShot(1000,loop.quit)
                    loop.exec_()
            
                elif result[1]<1:
                    self.txtblanc.hide()
                    self.txt_blanc("It's not very effective...")
                    loop=QEventLoop()
                    QTimer.singleShot(1000,loop.quit)
                    loop.exec_()
            
                self.txtblanc.hide()

                if ennemi.HP<=0:
                    path_musique=os.path.join(path, "VFX_SFX\Victory! Wild Pokemon - Pokémon Diamond & Pearl.mp3")
                    self.mediaPlayer = QMediaPlayer()
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path_musique)))
                    self.mediaPlayer.play()
                    self.pokemon_sauvage.hide()
                    self.nom_pkm_s.hide()
                    self.txt_blanc(ennemi.name.upper() + " is K.O. You catched him!")

                    loop=QEventLoop()
                    QTimer.singleShot(3000,loop.quit)
                    loop.exec_()

                    self.txtblanc.hide()
                    self.txt_blanc("He got sent in your inventory")
                    k=0
                    while self.equipe_dresseur[k].name!='Vide':
                        k+=1
                    if k==6:
                        self.inventaire.append(ennemi.name)
                    else:

                        self.equipe_dresseur[k]=pk.Pokemon(ennemi.name)

                    QTimer.singleShot(4000,self.close)
                else:
                    self.affiche_menu_principal()

    def atk2(self):
        self.attaque1.hide()
        self.attaque2.hide()
        self.retour.hide()
        self.txtblanc.hide()
        allie=self.equipe_dresseur[self.pokemon_au_combat -1]
        ennemi=self.pokemon_adverse
        if allie.speed>=ennemi.speed:
            result=allie.attaque(ennemi,2)
            self.txt_blanc(allie.name.upper() + " uses " +allie.attaque_type +"!")

            loop=QEventLoop()
            QTimer.singleShot(1500,loop.quit)
            loop.exec_()

            ennemi.HP=result[0]
            if ennemi.HP<0:
                ennemi.HP=0
            self.hpbar_sauvage.hide()
            self.maj_barre_hp_sauvage(ennemi)
            print(result[1])
            if result[1]>1:
                self.txtblanc.hide()
                self.txt_blanc("It's super effective!")
                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()
            elif result[1]==0:
                self.txtblanc.hide()
                self.txt_blanc("It doesn't affect " + ennemi.name +".")
                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

            elif result[1]<1:
                self.txtblanc.hide()
                self.txt_blanc("It's not very effective...")
                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

            
            if result[1]==1:
                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

            
            self.txtblanc.hide()

            if ennemi.HP<=0:
                path_musique=os.path.join(path, "VFX_SFX\Victory! Wild Pokemon - Pokémon Diamond & Pearl.mp3")
                self.mediaPlayer = QMediaPlayer()
                self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path_musique)))
                self.mediaPlayer.play()
                self.cache_menu_principal()
                self.pokemon_sauvage.hide()
                self.nom_pkm_s.hide()
                self.txt_blanc(ennemi.name.upper() + "is K.O. You catch him!")

                loop=QEventLoop()
                QTimer.singleShot(1000,loop.quit)
                loop.exec_()

                self.txtblanc.hide()
                self.txt_blanc("He got sent in your inventory.")
                self.inventaire.append(ennemi.name)

                QTimer.singleShot(2000,self.close)
            
            else:
                self.attaque_sauvage()
                self.is_KO()
                

        else:
            self.attaque_sauvage()
            self.is_KO()

            if self.equipe_dresseur[self.pokemon_au_combat -1].HP!=0:
                result=allie.attaque(ennemi,2)
                self.txt_blanc(allie.name.upper() + " uses " +allie.attaque_type +"!")

                loop=QEventLoop()
                QTimer.singleShot(1500,loop.quit)
                loop.exec_()

                ennemi.HP=result[0]
                if ennemi.HP<0:
                    ennemi.HP=0
                self.hpbar_sauvage.hide()
                self.maj_barre_hp_sauvage(ennemi)

                if result[1]>1:
                    self.txtblanc.hide()
                    self.txt_blanc("It's super effective!")
                    loop=QEventLoop()
                    QTimer.singleShot(1000,loop.quit)
                    loop.exec_()
            
                elif result[1]==0:
                    self.txtblanc.hide()
                    self.txt_blanc("It doesn't affect " + ennemi.name +".")
                    loop=QEventLoop()
                    QTimer.singleShot(1000,loop.quit)
                    loop.exec_()

                elif result[1]<1:
                    self.txtblanc.hide()
                    self.txt_blanc("It's not very effective...")
                    loop=QEventLoop()
                    QTimer.singleShot(1000,loop.quit)
                    loop.exec_()


                self.txtblanc.hide()
            

                if ennemi.HP<=0:
                    path_musique=os.path.join(path, "VFX_SFX\Victory! Wild Pokemon - Pokémon Diamond & Pearl.mp3")
                    self.mediaPlayer = QMediaPlayer()
                    self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(path_musique)))
                    self.mediaPlayer.play()
                    self.pokemon_sauvage.hide()
                    self.nom_pkm_s.hide()
                    self.txt_blanc(ennemi.name.upper() + " is K.O. You catched him!")

                    loop=QEventLoop()
                    QTimer.singleShot(1500,loop.quit)
                    loop.exec_()

                    self.txtblanc.hide()
                    self.txt_blanc("He got sent in your inventory.")
                    while self.equipe_dresseur[k].name!='Vide':
                        k+=1
                    if k==6:
                        self.inventaire.append(ennemi.name)
                    else:
                        str()
                        self.equipe_dresseur[k]=pk.Pokemon(ennemi.name)

                    QTimer.singleShot(4000,self.close)

                else:
                    self.affiche_menu_principal()

    def maj_barre_hp_dresseur(self,pokemon):
        self.hpbar_dresseur.hide()
        self.hpbar_dresseur=QLabel(self)
        self.hpbar_dresseur.setGeometry(0,0,300,50)
        self.hpbar_dresseur.setAlignment(Qt.AlignRight)
        path_hpbar=os.path.join(path,"VFX_SFX\Barre_hp.png")
        barre = QPixmap(path_hpbar)  

        #Calcul du pourcentage de PV qui restent au pokemon:
        pourcentage=pokemon.HP/pokemon.maxHP
        taille_barre=148 - 148*pourcentage
        taille_barre=int(taille_barre)
        barre= barre.scaled(taille_barre, 150)  #148
        self.hpbar_dresseur.setPixmap(barre)
        self.hpbar_dresseur.move(527,367)
        self.hpbar_dresseur.show()

    def maj_barre_hp_sauvage(self,pokemon):
        self.hpbar_sauvage.hide()
        self.hpbar_sauvage=QLabel(self)
        self.hpbar_sauvage.setGeometry(0,0,300,300)
        self.hpbar_sauvage.setAlignment(Qt.AlignRight)
        path_hpbar=os.path.join(path,"VFX_SFX\Barre_hp.png")
        barre = QPixmap(path_hpbar)  

        #Calcul du pourcentage de PV qui restent au pokemon:
        pourcentage=pokemon.HP/pokemon.maxHP
        taille_barre=int(167 - 167*pourcentage)
        barre= barre.scaled(taille_barre, 170) 
        self.hpbar_sauvage.setPixmap(barre)
        self.hpbar_sauvage.move(183,72)
        self.hpbar_sauvage.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CombatPokemon([pk.Pokemon("Mewtwo"),pk.Pokemon("Mewtwo"),pk.Pokemon("Mewtwo"),pk.Pokemon("Mewtwo"),pk.Pokemon("Mewtwo"),pk.Pokemon("Mewtwo")],pk.PokemonSauvage("Machop",0,0),[])
    window.show()
    sys.exit(app.exec_())





