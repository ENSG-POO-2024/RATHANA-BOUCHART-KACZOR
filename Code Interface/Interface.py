# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import random as rd
import numpy as np
from pokemon import pokemon_pos_arrondies


class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.plein_ecran = QDesktopWidget().screenGeometry()
        self.taille_fen = 400
        
        #fenêtre principale
        self.setGeometry((self.plein_ecran.width() - self.taille_fen)//2, 
                         (self.plein_ecran.height() - self.taille_fen)//2, 
                         self.taille_fen, 
                         self.taille_fen) 
        
        self.layout = QVBoxLayout()
        
        self.carte()
        
        self.dresseur()
        
        self.button = QPushButton("map", self)
        self.button.setFixedSize(50, 20)  # Définir une taille fixe pour le bouton
        self.button.clicked.connect(self.FullScreen)
        
        self.layout.addWidget(self.fond)
        self.layout.addWidget(self.joueur)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        
        global pokemon_pos_arrondies
        pokemon_pos_arrondies[:, 1] = np.random.randint(0, self.fond.width()-112, len(pokemon_pos_arrondies))
        pokemon_pos_arrondies[:, 2] = np.random.randint(0, self.fond.height()-112, len(pokemon_pos_arrondies))
        pokemon_pos_arrondies = np.append(pokemon_pos_arrondies, [[pokemon_pos_arrondies[i][0].lower()+"_map.png"]for i in range(len(pokemon_pos_arrondies))], axis=1)
        pokemon_pos_arrondies[:, 1] += self.x_map
        pokemon_pos_arrondies[:, 2] += self.y_map
        self.inconnus = list(pokemon_pos_arrondies.copy())
        self.dict_connus = {}
        self.connus = []
        self.dict_repet = {}  
        self.discover()
                
        self.speed = 10
        
        self.show()
        
                
    def FullScreen(self):
        if self.width() == self.taille_fen and self.height() == self.taille_fen :
            self.resize(self.plein_ecran.width(), self.plein_ecran.height())
            self.move(0,0)
            
            translation_x = (self.plein_ecran.width() - self.taille_fen)//2
            translation_y = (self.plein_ecran.height() - self.taille_fen)//2
            
        else:
            self.resize(self.taille_fen, self.taille_fen)
            self.move((self.plein_ecran.width() - self.taille_fen)//2, 
                      (self.plein_ecran.height() - self.taille_fen)//2)
            
            translation_x = -(self.plein_ecran.width() - self.taille_fen)//2
            translation_y = -(self.plein_ecran.height() - self.taille_fen)//2
            
        x_map = self.fond.x() + translation_x
        y_map = self.fond.y() + translation_y
        self.fond.move(x_map, y_map)
        
        x_joueur = self.joueur.x() + translation_x
        y_joueur = self.joueur.y() + translation_y
        self.joueur.move(x_joueur, y_joueur)
        
        for label in self.dict_connus.values() :
            x_pokemon = label.x() + translation_x
            y_pokemon = label.y() + translation_y
            label.move(x_pokemon, y_pokemon)
        for i in range(len(self.connus)):
            self.connus[i][1] += translation_x
            self.connus[i][2] += translation_y
        for i in range(len(self.inconnus)):
            self.inconnus[i][1] += translation_x
            self.inconnus[i][2] += translation_y
            
        
    def dresseur(self):
        sprite_sheet = QPixmap("C:/Users/kaczo/Documents/projet CCV/RATHANA-BOUCHART-KACZOR/documents/images/SpriteSheet.png")

        hauteur_sprite = sprite_sheet.height()//4
        largeur_sprite = sprite_sheet.width()//4
        
        # Découper le sprite sheet
        coordonnees_sprites = [(x, y, largeur_sprite, hauteur_sprite) for x in range(0, sprite_sheet.width(), largeur_sprite) for y in range(0, sprite_sheet.height(), hauteur_sprite)]
        self.sprites_individuels = []
        for coordonnees_sprite in coordonnees_sprites:
            sprite_individuel = sprite_sheet.copy(*coordonnees_sprite)
            self.sprites_individuels.append(sprite_individuel)
        sprite = QPixmap(self.sprites_individuels[0])
                
        self.vision = 200
        self.joueur = QLabel(self)
        self.joueur.setGeometry((self.taille_fen - largeur_sprite)//2, 
                                (self.taille_fen - hauteur_sprite)//2, 
                                largeur_sprite, hauteur_sprite)
        self.joueur.setPixmap(sprite)
        
            
    def carte(self):
        pixmap = QPixmap("C:/Users/kaczo/Documents/projet CCV/RATHANA-BOUCHART-KACZOR/documents/images/map.png")
        self.fond = QLabel(self)
        self.fond.setPixmap(pixmap)
        self.x_map = (self.width() - pixmap.width())//2
        self.y_map = (self.height() - pixmap.height())//2
        self.fond.setGeometry(self.x_map, self.y_map, pixmap.width(), pixmap.height())
    

    def discover(self):
        self.compteur_sup = -1
        self.inconnus_intermediaire = self.inconnus.copy()
        for i in range(len(self.inconnus)):
            name, x, y, image_path = self.inconnus[i]
            pixmap = QPixmap("C:/Users/kaczo/Documents/projet CCV/RATHANA-BOUCHART-KACZOR/documents/images/pokemons/"+image_path)
            x_baryc_pokemon = x + pixmap.width()//2
            y_baryc_pokemon = y + pixmap.height()//2
            x_baryc_joueur = self.joueur.x() + self.joueur.width()//2
            y_baryc_joueur = self.joueur.y() + self.joueur.height()//2
            x_c = x_baryc_joueur - self.vision//2
            y_c = y_baryc_joueur - self.vision//2
            L = self.vision
            if Window.point_dans_carre(x_baryc_pokemon, y_baryc_pokemon, x_c, y_c, L) :
                self.compteur_sup += 1
                if name in self.dict_repet :
                    self.dict_repet[name] += 1
                else : 
                    self.dict_repet[name] = 1
                name += str(self.dict_repet[name])
                
                label_pokemon = QLabel(self)
                label_pokemon.setPixmap(pixmap)
                label_pokemon.move(x, y)
                label_pokemon.setFixedSize(pixmap.size())
                label_pokemon.show()
                self.layout.addWidget(label_pokemon)
                self.joueur.raise_()
                self.button.raise_()
                
                self.dict_connus[name] = label_pokemon
                self.connus.append(self.inconnus[i])
                del self.inconnus_intermediaire[i-self.compteur_sup]
        self.inconnus = self.inconnus_intermediaire.copy()


    def point_dans_carre(x, y, x_c, y_c, L):
        # Vérifie si les coordonnées du point sont dans la plage du carré
        if (x >= x_c and x <= x_c + L) and (y >= y_c and y <= y_c + L):
            return True
        else:
            return False


    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
                x_map = self.fond.x()
                y_map = self.fond.y()
                x_joueur = self.joueur.x()
                y_joueur = self.joueur.y()
                x_min = x_map + (self.taille_fen - self.joueur.width())//2
                x_max = x_map + self.fond.width() + (self.joueur.width() - self.taille_fen)//2
                y_min = y_map + (self.taille_fen - self.joueur.height())//2
                y_max = y_map + self.fond.height() + (self.joueur.height() - self.taille_fen)//2
                
                if key == Qt.Key_Up :
                    if (y_joueur - y_min >= self.speed) and (y_joueur <= y_max - self.joueur.height()) :
                        self.fond.move(x_map, y_map + self.speed)
                        for label in self.dict_connus.values() :
                            label.move(label.x(), label.y() + self.speed)
                        for i in range(len(self.connus)):
                            self.connus[i][2] += self.speed
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][2] += self.speed
                    elif (y_joueur - y_min < self.speed) and (y_joueur - y_min > 0) :
                        translation = y_joueur - y_min
                        self.fond.move(x_map, y_map + translation)
                        for label in self.dict_connus.values() :
                            label.move(label.x(), label.y() + translation)
                        for i in range(len(self.connus)):
                            self.connus[i][2] += translation
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][2] += translation
                        self.joueur.move(x_joueur,
                                         y_joueur - (self.speed - translation))
                    elif (y_joueur <= y_min) and (y_joueur - self.speed >= y_map) :
                        self.joueur.move(x_joueur, y_joueur - self.speed)
                    elif (y_joueur - self.speed < y_map) :
                        self.joueur.move(x_joueur, y_map)
                    elif(y_joueur - self.speed >= y_max - self.joueur.height()):
                        self.joueur.move(x_joueur, y_joueur - self.speed)
                    elif (y_joueur - self.speed < y_max - self.joueur.height()) and (y_joueur > y_max - self.joueur.height()):
                        translation = y_joueur - (y_max - self.joueur.height())
                        self.joueur.move(x_joueur, y_max - self.joueur.height())
                        self.fond.move(x_map, y_map + translation)
                        for label in self.dict_connus.values() :
                            label.move(label.x(), label.y() + translation)
                        for i in range(len(self.connus)):
                            self.connus[i][2] += translation
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][2] += translation
                    
                        
                if key == Qt.Key_Down :
                    if (y_joueur + self.joueur.height() + self.speed <= y_max) and (y_joueur >= y_min) :
                        self.fond.move(x_map, y_map - self.speed)
                        for label in self.dict_connus.values() :
                            label.move(label.x(), label.y() - self.speed)
                        for i in range(len(self.connus)):
                            self.connus[i][2] -= self.speed
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][2] -= self.speed
                    elif (y_joueur + self.joueur.height() + self.speed > y_max) and (y_joueur + self.joueur.height() < y_max) :
                        translation = y_joueur - (y_max - self.joueur.height())
                        self.fond.move(x_map, y_map + translation)
                        for label in self.dict_connus.values() :
                            label.move(label.x(), label.y() + translation)
                        for i in range(len(self.connus)):
                            self.connus[i][2] += translation
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][2] += translation
                        self.joueur.move(x_joueur,
                                         y_joueur + (self.speed + translation))
                    elif (y_joueur + self.joueur.height() >= y_max) and (y_joueur + self.joueur.height() + self.speed <= y_map + self.fond.height()) :
                        self.joueur.move(x_joueur, y_joueur + self.speed)
                    elif (y_joueur + self.joueur.height() + self.speed > y_map + self.fond.height()) :
                        self.joueur.move(x_joueur, y_map + self.fond.height() - self.joueur.height())
                    elif (y_joueur + self.speed <= y_min):
                        self.joueur.move(x_joueur, y_joueur + self.speed)
                    elif (y_joueur + self.speed > y_min) and (y_joueur < y_min) :
                        translation = y_joueur - y_min
                        self.joueur.move(x_joueur, y_min)
                        self.fond.move(x_map, y_map + translation)
                        for label in self.dict_connus.values() :
                            label.move(label.x(), label.y() + translation)
                        for i in range(len(self.connus)):
                            self.connus[i][2] += translation
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][2] += translation
                            
                            
                if key == Qt.Key_Left :
                    if (x_joueur - x_min >= self.speed) and (x_joueur <= x_max - self.joueur.width()) :
                        self.fond.move(x_map + self.speed, y_map)
                        for label in self.dict_connus.values() :
                            label.move(label.x() + self.speed, label.y())
                        for i in range(len(self.connus)):
                            self.connus[i][1] += self.speed
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][1] += self.speed
                    elif (x_joueur - x_min < self.speed) and (x_joueur - x_min > 0) :
                        translation = x_joueur - x_min
                        self.fond.move(x_map + translation, y_map)
                        for label in self.dict_connus.values() :
                            label.move(label.x() + translation, label.y())
                        for i in range(len(self.connus)):
                            self.connus[i][1] += translation
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][1] += translation
                        self.joueur.move(x_joueur - (self.speed - translation),
                                         y_joueur)
                    elif (x_joueur <= x_min) and (x_joueur - self.speed >= x_map) :
                        self.joueur.move(x_joueur - self.speed, y_joueur)
                    elif (x_joueur - self.speed < x_map) :
                        self.joueur.move(x_map, y_joueur)
                    elif(x_joueur - self.speed >= x_max - self.joueur.width()):
                        self.joueur.move(x_joueur - self.speed, y_joueur)
                    elif (x_joueur - self.speed < x_max - self.joueur.width()) and (x_joueur > x_max - self.joueur.width()):
                        translation = x_joueur - (x_max - self.joueur.width())
                        self.joueur.move(x_max - self.joueur.width(), y_joueur)
                        self.fond.move(x_map + translation, y_map)
                        for label in self.dict_connus.values() :
                            label.move(label.x() + translation, label.y())
                        for i in range(len(self.connus)):
                            self.connus[i][1] += translation
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][1] += translation
        
            
                if key == Qt.Key_Right :
                    if (x_joueur + self.joueur.width() + self.speed <= x_max) and (x_joueur >= x_min) :
                        self.fond.move(x_map - self.speed, y_map)
                        for label in self.dict_connus.values() :
                            label.move(label.x() - self.speed, label.y())
                        for i in range(len(self.connus)):
                            self.connus[i][1] -= self.speed
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][1] -= self.speed
                    elif (x_joueur + self.joueur.width() + self.speed > x_max) and (x_joueur + self.joueur.width() < x_max) :
                        translation = x_joueur - (x_max - self.joueur.width())
                        self.fond.move(x_map + translation, y_map)
                        for label in self.dict_connus.values() :
                            label.move(label.x() + translation, label.y())
                        for i in range(len(self.connus)):
                            self.connus[i][1] += translation
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][1] += translation
                        self.joueur.move(x_joueur + (self.speed + translation),
                                         y_joueur)
                    elif (x_joueur + self.joueur.width() >= x_max) and (x_joueur + self.joueur.width() + self.speed <= x_map + self.fond.width()) :
                        self.joueur.move(x_joueur + self.speed, y_joueur)
                    elif (x_joueur + self.joueur.width() + self.speed > x_map + self.fond.width()) :
                        self.joueur.move(x_map + self.fond.width() - self.joueur.width(), y_joueur)
                    elif (x_joueur + self.speed <= x_min):
                        self.joueur.move(x_joueur + self.speed, y_joueur)
                    elif (x_joueur + self.speed > x_min) and (x_joueur < x_min) :
                        translation = x_joueur - x_min
                        self.joueur.move(x_min, y_joueur)
                        self.fond.move(x_map + translation, y_map)
                        for label in self.dict_connus.values() :
                            label.move(label.x() + translation, label.y())
                        for i in range(len(self.connus)):
                            self.connus[i][1] += translation
                        for i in range(len(self.inconnus)):
                            self.inconnus[i][1] += translation
                        
                        
                self.discover()
                return True
        elif event.type() == QEvent.Close:
            return super().eventFilter(obj, event)  # Laisser le traitement de l'événement de fermeture de fenêtre par défaut
        return False  # Ne rien faire pour les autres types d'événements
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    app.installEventFilter(window)
    window.show()
    sys.exit(app.exec_())