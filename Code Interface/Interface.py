# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import random as rd
import numpy as np
from pokemon import pokemon_pos_arrondies
from creation_carte import mat_width, mat_height, mat_map

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
        
        self.pokemon_path = "C:/Users/kaczo/Documents/projet CCV/RATHANA-BOUCHART-KACZOR/documents/images/pokemons/"
        
        self.layout = QVBoxLayout()
        
        self.carte()
        
        self.dresseur()
        
        self.button = QPushButton("map", self)
        self.button.setFixedSize(50, 20)  # Définir une taille fixe pour le bouton
        self.button.clicked.connect(self.FullScreen)
        
        self.layout.addWidget(self.fond_collisions)
        self.layout.addWidget(self.fond)
        self.layout.addWidget(self.joueur)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        
        global pokemon_pos_arrondies
        pokemon_pos_arrondies = np.append(pokemon_pos_arrondies, [[pokemon_pos_arrondies[i][0].lower()+"_map.png"]for i in range(len(pokemon_pos_arrondies))], axis=1)
        pokemon_pos_arrondies = np.append(pokemon_pos_arrondies, [[Window.find_left_position(QPixmap(self.pokemon_path + pokemon_pos_arrondies[i][3])) + (Window.find_right_position(QPixmap(self.pokemon_path + pokemon_pos_arrondies[i][3])) - Window.find_left_position(QPixmap(self.pokemon_path + pokemon_pos_arrondies[i][3])))//2]for i in range(len(pokemon_pos_arrondies))], axis=1)
        pokemon_pos_arrondies = np.append(pokemon_pos_arrondies, [[Window.find_top_position(QPixmap(self.pokemon_path + pokemon_pos_arrondies[i][3])) + (Window.find_bottom_position(QPixmap(self.pokemon_path + pokemon_pos_arrondies[i][3])) - Window.find_top_position(QPixmap(self.pokemon_path + pokemon_pos_arrondies[i][3])))//2]for i in range(len(pokemon_pos_arrondies))], axis=1)
        compteur = 0
        while compteur != len(pokemon_pos_arrondies):
            pixmap = QPixmap(self.pokemon_path + pokemon_pos_arrondies[compteur][3])
            width = pixmap.width()
            height = pixmap.height()
            x = rd.randrange(0, self.fond.width() - width)
            y = rd.randrange(0, self.fond.height() - height)
            x_baryc_pokemon = x + pokemon_pos_arrondies[compteur][4]
            y_baryc_pokemon = y + pokemon_pos_arrondies[compteur][5]
            pixel = self.fond_collisions.pixmap().toImage().pixelColor(x_baryc_pokemon, y_baryc_pokemon)
            color = (pixel.red(), pixel.green(), pixel.blue())     
            if color != (0,0,0):
                pokemon_pos_arrondies[compteur][1] = x
                pokemon_pos_arrondies[compteur][2] = y
                compteur += 1
        #pokemon_pos_arrondies[:, 1] = np.random.randint(0, self.fond.width()-112, len(pokemon_pos_arrondies))
        #pokemon_pos_arrondies[:, 2] = np.random.randint(0, self.fond.height()-112, len(pokemon_pos_arrondies))
        pokemon_pos_arrondies[:, 1] += self.x_map
        pokemon_pos_arrondies[:, 2] += self.y_map
        self.inconnus = list(pokemon_pos_arrondies.copy())
        self.dict_connus = {}
        self.connus = []
        self.dict_repet = {}  
        self.discover()
        
        self.col_mat = (self.fond.width() - self.joueur.width())//2
        self.row_mat = (self.fond.height() - self.joueur.height())//2
                
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
        self.fond_collisions.move(x_map, y_map)
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
        pixmap = QPixmap("C:/Users/kaczo/Documents/projet CCV/RATHANA-BOUCHART-KACZOR/documents/images/carte_collisions.png")
        self.fond_collisions = QLabel(self)
        self.fond_collisions.setPixmap(pixmap)
        x_map = (self.width() - pixmap.width())//2
        y_map = (self.height() - pixmap.height())//2
        self.fond_collisions.setGeometry(x_map, y_map, pixmap.width(), pixmap.height())
        
        pixmap = QPixmap("C:/Users/kaczo/Documents/projet CCV/RATHANA-BOUCHART-KACZOR/documents/images/carte.png")
        self.fond = QLabel(self)
        self.fond.setPixmap(pixmap)
        self.x_map = (self.width() - pixmap.width())//2
        self.y_map = (self.height() - pixmap.height())//2
        self.fond.setGeometry(self.x_map, self.y_map, pixmap.width(), pixmap.height())
    

    def discover(self):
        self.compteur_sup = -1
        self.inconnus_intermediaire = self.inconnus.copy()
        for i in range(len(self.inconnus)):
            name, x, y, image_path, x_moy, y_moy = self.inconnus[i]
            pixmap = QPixmap(self.pokemon_path + image_path)
            x_baryc_pokemon = x + x_moy
            y_baryc_pokemon = y + y_moy
            #x_baryc_pokemon = x + pixmap.width()//2
            #y_baryc_pokemon = y + pixmap.height()//2
            x_baryc_joueur = self.joueur.x() + self.joueur.width()//2
            y_baryc_joueur = self.joueur.y() + self.joueur.height()//2
            x_c = x_baryc_joueur - self.vision//2
            y_c = y_baryc_joueur - self.vision//2
            L = self.vision
            if Window.point_dans_rectangle(x_baryc_pokemon, y_baryc_pokemon, x_c, y_c, L, L) :
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
        
    def find_bottom_position(image):
        image = image.toImage()
        height = image.height()
        width = image.width()

        # Parcourir les lignes de l'image de bas en haut
        for y in range(height - 1, -1, -1):
            # Parcourir les colonnes de gauche à droite
            for x in range(width):
                # Obtenir la couleur du pixel
                pixel = image.pixelColor(x, y)
                color = (pixel.red(), pixel.green(), pixel.blue())
                # Si le pixel n'est pas transparent, c'est une ligne contenant des pixels colorés
                if color != (0,0,0):
                    return y  # Retourne la position y de la dernière ligne contenant des pixels colorés

        return 0

    def find_top_position(image):
        image = image.toImage()
        height = image.height()
        width = image.width()

        # Parcourir les lignes de l'image de bas en haut
        for y in range(height):
            # Parcourir les colonnes de gauche à droite
            for x in range(width):
                # Obtenir la couleur du pixel
                pixel = image.pixelColor(x, y)
                color = (pixel.red(), pixel.green(), pixel.blue())
                # Si le pixel n'est pas transparent, c'est une ligne contenant des pixels colorés
                if color != (0,0,0):
                    return y  # Retourne la position y de la première ligne contenant des pixels colorés

        return height

    def find_left_position(image):
        image = image.toImage()
        height = image.height()
        width = image.width()

        # Parcourir les lignes de l'image de gauche à droite
        for x in range(width):
            # Parcourir les colonnes de haut en bas
            for y in range(height):
                # Obtenir la couleur du pixel
                pixel = image.pixelColor(x, y)
                color = (pixel.red(), pixel.green(), pixel.blue())

                # Si le pixel n'est pas transparent, c'est une colonne contenant des pixels colorés
                if color != (0,0,0):
                    return x  # Retourne la position x de la première colonne contenant des pixels colorés

        return width

    def find_right_position(image):
        image = image.toImage()
        height = image.height()
        width = image.width()

        # Parcourir les colonnes de l'image de droite à gauche
        for x in range(width - 1, -1, -1):
            # Parcourir les lignes de haut en bas
            for y in range(height):
                # Obtenir la couleur du pixel
                pixel = image.pixelColor(x, y)
                color = (pixel.red(), pixel.green(), pixel.blue())

                # Si le pixel n'est pas transparent, c'est une colonne contenant des pixels colorés
                if color != (0,0,0):
                    return x  # Retourne la position x de la dernière colonne contenant des pixels colorés

        return 0


    def point_dans_rectangle(x, y, x_c, y_c, L, l):
        # Vérifie si les coordonnées du point sont dans la plage du carré
        if (x >= x_c and x <= x_c + L) and (y >= y_c and y <= y_c + l):
            return True
        else:
            return False
            
    def move_map_y(self, translation, x_map, y_map):
        self.fond_collisions.move(x_map, y_map + translation)
        self.fond.move(x_map, y_map + translation)
        for label in self.dict_connus.values() :
            label.move(label.x(), label.y() + translation)
        for j in range(len(self.connus)):
            self.connus[j][2] += translation
        for j in range(len(self.inconnus)):
            self.inconnus[j][2] += translation
            
    def move_map_x(self, translation, x_map, y_map):
        self.fond_collisions.move(x_map + translation, y_map)
        self.fond.move(x_map + translation, y_map)
        for label in self.dict_connus.values() :
            label.move(label.x() + translation, label.y())
        for j in range(len(self.connus)):
            self.connus[j][1] += translation
        for j in range(len(self.inconnus)):
            self.inconnus[j][1] += translation  

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
                obstacle = False
                
                if key == Qt.Key_Up :
                    if (y_joueur - self.speed < y_map) :
                        for y in range(self.row_mat - 1, self.row_mat - (y_joueur - y_map) - 1, -1):
                            pixels = [self.fond_collisions.pixmap().toImage().pixelColor(x, y) for x in range (self.col_mat, self.col_mat + self.joueur.width())]
                            couleur_pixel = [(pixel.red(), pixel.green(), pixel.blue()) for pixel in pixels]
                            if (0,0,0) in couleur_pixel :
                                obstacle = True
                                self.joueur.move(x_joueur, y_joueur - (self.row_mat - y - 1))
                                self.row_mat = y + 1
                                break
                        if not obstacle :
                            self.joueur.move(x_joueur, y_map)
                            self.row_mat -= y_joueur - y_map     
                    else :
                        for y in range(self.row_mat - 1, self.row_mat - self.speed - 1, -1):
                            pixels = [self.fond_collisions.pixmap().toImage().pixelColor(x, y) for x in range (self.col_mat, self.col_mat + self.joueur.width())]
                            couleur_pixel = [(pixel.red(), pixel.green(), pixel.blue()) for pixel in pixels]
                            if (0,0,0) in couleur_pixel :
                                obstacle = True
                                if (y_joueur - y_min >= self.speed) and (y_joueur <= y_max - self.joueur.height()) :
                                    translation = self.row_mat - y - 1
                                    self.move_map_y(translation, x_map, y_map)
                                    self.row_mat = y + 1
                                    break
                                elif (y_joueur - y_min < self.speed) and (y_joueur - y_min > 0) :
                                    if (self.row_mat - y) > (y_joueur - y_min) :
                                        translation = y_joueur - y_min
                                        self.move_map_y(translation, x_map, y_map)
                                        self.joueur.move(x_joueur,
                                                         y_joueur - ((self.row_mat - y - 1) - translation))
                                        self.row_mat = y + 1    
                                        break
                                    else : 
                                        translation = self.row_mat - y - 1
                                        self.move_map_y(translation, x_map, y_map)
                                        self.row_mat = y + 1    
                                        break
                                elif (y_joueur <= y_min) and (y_joueur - self.speed >= y_map) :
                                    self.joueur.move(x_joueur, y_joueur - (self.row_mat - y - 1))
                                    self.row_mat = y + 1
                                    break
                                elif(y_joueur - self.speed >= y_max - self.joueur.height()):
                                    self.joueur.move(x_joueur, y_joueur - (self.row_mat - y - 1))
                                    self.row_mat = y + 1
                                    break
                                elif (y_joueur - self.speed < y_max - self.joueur.height()) and (y_joueur > y_max - self.joueur.height()):
                                    if (self.row_mat - y) > (y_joueur - (y_max - self.joueur.height())) :
                                        translation = (self.row_mat - y - 1) - (y_joueur - (y_max - self.joueur.height()))
                                        self.joueur.move(x_joueur, y_max - self.joueur.height())
                                        self.move_map_y(translation, x_map, y_map)
                                        self.row_mat = y + 1
                                        break
                                    else :
                                        translation = -(self.row_mat - y - 1)
                                        self.joueur.move(x_joueur, y_joueur + translation)
                                        self.row_mat = y + 1
                                        break
                        if not obstacle :
                            if (y_joueur - y_min >= self.speed) and (y_joueur <= y_max - self.joueur.height()) :
                                translation = self.speed
                                self.move_map_y(translation, x_map, y_map)
                            elif (y_joueur - y_min < self.speed) and (y_joueur - y_min > 0) :
                                translation = y_joueur - y_min
                                self.move_map_y(translation, x_map, y_map)
                                self.joueur.move(x_joueur,
                                                 y_joueur - (self.speed - translation))
                            elif (y_joueur <= y_min) and (y_joueur - self.speed >= y_map) :
                                self.joueur.move(x_joueur, y_joueur - self.speed)
                            elif(y_joueur - self.speed >= y_max - self.joueur.height()):
                                self.joueur.move(x_joueur, y_joueur - self.speed)
                            elif (y_joueur - self.speed < y_max - self.joueur.height()) and (y_joueur > y_max - self.joueur.height()):
                                translation = self.speed - (y_joueur - (y_max - self.joueur.height()))
                                self.joueur.move(x_joueur, y_max - self.joueur.height())
                                self.move_map_y(translation, x_map, y_map)
                            self.row_mat -= self.speed
                                
                if key == Qt.Key_Down :
                    if (y_joueur + self.joueur.height() + self.speed > y_map + self.fond.height()) :
                        for y in range(self.row_mat + self.joueur.height(),
                                       y_map + self.fond.height()) :
                            pixels = [self.fond_collisions.pixmap().toImage().pixelColor(x, y) for x in range (self.col_mat, self.col_mat + self.joueur.width())]
                            couleur_pixel = [(pixel.red(), pixel.green(), pixel.blue()) for pixel in pixels]
                            if (0,0,0) in couleur_pixel :
                                obstacle = True
                                self.joueur.move(x_joueur, y_joueur + (y - self.joueur.height() - self.row_mat))
                                self.row_mat = y - self.joueur.height()
                                break
                        if not obstacle :
                            self.joueur.move(x_joueur, y_map + self.fond.height() - self.joueur.height())
                            self.row_mat = self.fond.height() - self.joueur.height()
                    else :
                        for y in range(self.row_mat + self.joueur.height(),
                                       self.row_mat + self.joueur.height() + self.speed) :
                            pixels = [self.fond_collisions.pixmap().toImage().pixelColor(x, y) for x in range (self.col_mat, self.col_mat + self.joueur.width())]
                            couleur_pixel = [(pixel.red(), pixel.green(), pixel.blue()) for pixel in pixels]
                            if (0,0,0) in couleur_pixel :
                                obstacle = True
                                if (y_joueur + self.joueur.height() + self.speed <= y_max) and (y_joueur >= y_min) :
                                    translation = self.row_mat + self.joueur.height() - y
                                    self.move_map_y(translation, x_map, y_map)
                                    self.row_mat = y - self.joueur.height()
                                    break
                                elif (y_joueur + self.joueur.height() + self.speed > y_max) and (y_joueur + self.joueur.height() < y_max) :
                                    if (y - self.row_mat) >= (y_max - y_joueur) :
                                        translation = -(y_max - self.joueur.height() - y_joueur)
                                        self.move_map_y(translation, x_map, y_map)
                                        self.joueur.move(x_joueur,
                                                         y_joueur + y - self.joueur.height() - (self.row_mat - translation))
                                        self.row_mat = y - self.joueur.height()
                                        break
                                    else : 
                                        translation = y - self.joueur.height() - self.row_mat     
                                        self.move_map_y(translation, x_map, y_map)
                                        self.row_mat = y - self.joueur.height()
                                        break
                                elif (y_joueur + self.joueur.height() >= y_max) and (y_joueur + self.joueur.height() + self.speed <= y_map + self.fond.height()) :
                                    self.joueur.move(x_joueur, y_joueur + (y - self.joueur.height() - self.row_mat))
                                    self.row_mat = y - self.joueur.height()
                                    break
                                elif (y_joueur + self.speed <= y_min):
                                    self.joueur.move(x_joueur, y_joueur + (y - self.joueur.height() - self.row_mat))
                                    self.row_mat = y - self.joueur.height()
                                    break
                                elif (y_joueur + self.speed > y_min) and (y_joueur < y_min) :
                                    if (y - self.row_mat) >= (y_min + self.joueur.height() - y_joueur) :
                                        translation = y_min + self.joueur.height() - y
                                        self.joueur.move(x_joueur, y_min)
                                        self.move_map_y(translation, x_map, y_map)
                                        self.row_mat = y - self.joueur.height()
                                        break
                                    else : 
                                        self.joueur.move(x_joueur, y_joueur + y - (self.row_mat + self.joueur.height()))
                                        self.row_mat = y - self.joueur.height()
                                        break
                        if not obstacle :
                            if (y_joueur + self.joueur.height() + self.speed <= y_max) and (y_joueur >= y_min) :
                                translation = - self.speed
                                self.move_map_y(translation, x_map, y_map)
                            elif (y_joueur + self.joueur.height() + self.speed > y_max) and (y_joueur + self.joueur.height() < y_max) :
                                translation = y_joueur - (y_max - self.joueur.height())
                                self.move_map_y(translation, x_map, y_map)
                                self.joueur.move(x_joueur,
                                                 y_joueur + (self.speed + translation))
                            elif (y_joueur + self.joueur.height() >= y_max) and (y_joueur + self.joueur.height() + self.speed <= y_map + self.fond.height()) :
                                self.joueur.move(x_joueur, y_joueur + self.speed)
                            elif (y_joueur + self.speed <= y_min):
                                self.joueur.move(x_joueur, y_joueur + self.speed)
                            elif (y_joueur + self.speed > y_min) and (y_joueur < y_min) :
                                translation = y_min - y_joueur - self.speed
                                self.joueur.move(x_joueur, y_min)
                                self.move_map_y(translation, x_map, y_map)
                            self.row_mat += self.speed    
                                
                if key == Qt.Key_Left :
                    if (x_joueur - self.speed < x_map) :
                        for x in range(self.col_mat - 1, self.col_mat - (x_joueur - x_map) - 1, -1):
                            pixels = [self.fond_collisions.pixmap().toImage().pixelColor(x, y) for y in range (self.row_mat, self.row_mat + self.joueur.height())]
                            couleur_pixel = [(pixel.red(), pixel.green(), pixel.blue()) for pixel in pixels]
                            if (0,0,0) in couleur_pixel :
                                obstacle = True
                                self.joueur.move(x_joueur - (self.col_mat - x - 1), y_joueur)
                                self.col_mat = x + 1
                                break
                        if not obstacle :
                            self.joueur.move(x_map, y_joueur)
                            self.col_mat -= x_joueur - x_map
                    else :
                        for x in range(self.col_mat - 1, self.col_mat - self.speed - 1, -1):
                            pixels = [self.fond_collisions.pixmap().toImage().pixelColor(x, y) for y in range (self.row_mat, self.row_mat + self.joueur.height())]
                            couleur_pixel = [(pixel.red(), pixel.green(), pixel.blue()) for pixel in pixels]
                            if (0,0,0) in couleur_pixel :
                                obstacle = True
                                if (x_joueur - x_min >= self.speed) and (x_joueur <= x_max - self.joueur.width()) :
                                    translation = self.col_mat - x - 1
                                    self.move_map_x(translation, x_map, y_map)
                                    self.col_mat = x + 1
                                    break
                                elif (x_joueur - x_min < self.speed) and (x_joueur - x_min > 0) :
                                    if (self.col_mat - x) > (x_joueur - x_min) :
                                        translation = x_joueur - x_min
                                        self.move_map_x(translation, x_map, y_map)
                                        self.joueur.move(x_joueur - ((self.col_mat - x - 1) - translation),
                                                         y_joueur)
                                        self.col_mat = x + 1    
                                        break
                                    else : 
                                        translation = self.col_mat - x - 1
                                        self.move_map_x(translation, x_map, y_map)
                                        self.col_mat = x + 1    
                                        break
                                elif (x_joueur <= x_min) and (x_joueur - self.speed >= x_map) :
                                    self.joueur.move(x_joueur - (self.col_mat - x - 1), y_joueur)
                                    self.col_mat = x + 1
                                    break
                                elif(x_joueur - self.speed >= x_max - self.joueur.width()):
                                    self.joueur.move(x_joueur - (self.col_mat - x - 1), y_joueur)
                                    self.col_mat = x + 1
                                    break
                                elif (x_joueur - self.speed < x_max - self.joueur.width()) and (x_joueur > x_max - self.joueur.width()):
                                    if (self.col_mat - x) > (x_joueur - (x_max - self.joueur.width())) :
                                        translation = (self.col_mat - x - 1) - (x_joueur - (x_max - self.joueur.width()))
                                        self.joueur.move(x_max - self.joueur.width(), y_joueur)
                                        self.move_map_x(translation, x_map, y_map)
                                        self.col_mat = x + 1
                                        break
                                    else :
                                        translation = -(self.col_mat - x - 1)
                                        self.joueur.move(x_joueur + translation, y_joueur)
                                        self.col_mat = x + 1
                                        break
                        if not obstacle :
                            if (x_joueur - x_min >= self.speed) and (x_joueur <= x_max - self.joueur.width()) :
                                translation = self.speed
                                self.move_map_x(translation, x_map, y_map)
                            elif (x_joueur - x_min < self.speed) and (x_joueur - x_min > 0) :
                                translation = x_joueur - x_min
                                self.move_map_x(translation, x_map, y_map)
                                self.joueur.move(x_joueur - (self.speed - translation),
                                                 y_joueur)
                            elif (x_joueur <= x_min) and (x_joueur - self.speed >= x_map) :
                                self.joueur.move(x_joueur - self.speed, y_joueur)
                            elif(x_joueur - self.speed >= x_max - self.joueur.width()):
                                self.joueur.move(x_joueur - self.speed, y_joueur)
                            elif (x_joueur - self.speed < x_max - self.joueur.width()) and (x_joueur > x_max - self.joueur.width()):
                                translation = self.speed - (x_joueur - (x_max - self.joueur.width()))
                                self.joueur.move(x_max - self.joueur.width(), y_joueur)
                                self.move_map_x(translation, x_map, y_map)
                            self.col_mat -= self.speed

                if key == Qt.Key_Right :
                    if (x_joueur + self.joueur.width() + self.speed > x_map + self.fond.width()) :
                        for x in range(self.col_mat + self.joueur.width(),
                                       x_map + self.fond.width()) :
                            pixels = [self.fond_collisions.pixmap().toImage().pixelColor(x, y) for y in range (self.row_mat, self.row_mat + self.joueur.height())]
                            couleur_pixel = [(pixel.red(), pixel.green(), pixel.blue()) for pixel in pixels]
                            if (0,0,0) in couleur_pixel :
                                obstacle = True
                                self.joueur.move(x_joueur + (x - self.joueur.width() - self.col_mat), y_joueur)
                                self.col_mat = x - self.joueur.width()
                                break
                        if not obstacle :
                            self.joueur.move(x_map + self.fond.width() - self.joueur.width(), y_joueur)
                            self.col_mat = self.fond.width() - self.joueur.width()       
                    else :
                        for x in range(self.col_mat + self.joueur.width(),
                                       self.col_mat + self.joueur.width() + self.speed) :
                            pixels = [self.fond_collisions.pixmap().toImage().pixelColor(x, y) for y in range (self.row_mat, self.row_mat + self.joueur.height())]
                            couleur_pixel = [(pixel.red(), pixel.green(), pixel.blue()) for pixel in pixels]
                            if (0,0,0) in couleur_pixel :
                                obstacle = True
                                if (x_joueur + self.joueur.width() + self.speed <= x_max) and (x_joueur >= x_min) :
                                    translation = self.col_mat + self.joueur.width() - x
                                    self.move_map_x(translation, x_map, y_map)
                                    self.col_mat = x - self.joueur.width()
                                    break
                                elif (x_joueur + self.joueur.width() + self.speed > x_max) and (x_joueur + self.joueur.width() < x_max) :
                                    if (x - self.col_mat) >= (x_max - x_joueur) :
                                        translation = -(x_max - self.joueur.width() - x_joueur)
                                        self.move_map_x(translation, x_map, y_map)
                                        self.joueur.move(x_joueur + x - self.joueur.width() - (self.col_mat - translation),
                                                         y_joueur)
                                        self.col_mat = x - self.joueur.width()
                                        break
                                    else : 
                                        translation = x - self.joueur.width() - self.col_mat     
                                        self.move_map_x(translation, x_map, y_map)
                                        self.col_mat = x - self.joueur.width()
                                        break
                                elif (x_joueur + self.joueur.width() >= x_max) and (x_joueur + self.joueur.width() + self.speed <= x_map + self.fond.width()) :
                                    self.joueur.move(x_joueur + (x - self.joueur.width() - self.col_mat), y_joueur)
                                    self.col_mat = x - self.joueur.width()
                                    break
                                elif (x_joueur + self.speed <= x_min):
                                    self.joueur.move(x_joueur + (x - self.joueur.width() - self.col_mat), y_joueur)
                                    self.col_mat = x - self.joueur.width()
                                    break
                                elif (x_joueur + self.speed > x_min) and (x_joueur < x_min) :
                                    if (x - self.col_mat) >= (x_min + self.joueur.width() - x_joueur) :
                                        translation = x_min + self.joueur.width() - x
                                        self.joueur.move(x_min, y_joueur)
                                        self.move_map_x(translation, x_map, y_map)
                                        self.col_mat = x - self.joueur.width()
                                        break
                                    else : 
                                        self.joueur.move(x_joueur + x - (self.col_mat + self.joueur.width()), y_joueur)
                                        self.col_mat = x - self.joueur.width()
                                        break
                        if not obstacle :
                            if (x_joueur + self.joueur.width() + self.speed <= x_max) and (x_joueur >= x_min) :
                                translation = - self.speed
                                self.move_map_x(translation, x_map, y_map)
                            elif (x_joueur + self.joueur.width() + self.speed > x_max) and (x_joueur + self.joueur.width() < x_max) :
                                translation = x_joueur - (x_max - self.joueur.width())
                                self.move_map_x(translation, x_map, y_map)
                                self.joueur.move(x_joueur + (self.speed + translation),
                                                 y_joueur)
                            elif (x_joueur + self.joueur.width() >= x_max) and (x_joueur + self.joueur.width() + self.speed <= x_map + self.fond.width()) :
                                self.joueur.move(x_joueur + self.speed, y_joueur)
                            elif (x_joueur + self.speed <= x_min):
                                self.joueur.move(x_joueur + self.speed, y_joueur)
                            elif (x_joueur + self.speed > x_min) and (x_joueur < x_min) :
                                translation = x_min - x_joueur - self.speed
                                self.joueur.move(x_min, y_joueur)
                                self.move_map_x(translation, x_map, y_map)
                            self.col_mat += self.speed
                    
            
                self.discover()
                
                list_keys = list(self.dict_connus.keys())
                for i in range(len(self.connus)) :
                    x_pokemon = self.dict_connus[list_keys[i]].x()
                    x_baryc_pokemon = x_pokemon + self.connus[i][4]
                    y_pokemon = self.dict_connus[list_keys[i]].y()
                    y_baryc_pokemon = y_pokemon + self.connus[i][5]
                    x_dresseur = self.joueur.x()
                    y_dresseur = self.joueur.y()
                    L = self.joueur.width()
                    l = self.joueur.height()
                    if Window.point_dans_rectangle(x_baryc_pokemon, y_baryc_pokemon, 
                                               x_dresseur, y_dresseur,
                                               L, l) :
                        print(True)
                        
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