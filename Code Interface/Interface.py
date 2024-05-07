# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import random as rd
from pokemon import pokemon_pos_arrondies

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.vision = 200
        
        self.setGeometry(400, 400, self.vision, self.vision) #fenêtre principale
        
        self.carte()
        
        self.dresseur()
        
        self.inconnus = list(pokemon_pos_arrondies.copy())
        self.dict_connus = {}
        self.connus = []
        self.dict_repet = {}  
        self.discover()
        
        self.show()
        
        self.speed = 10
        
        
    def dresseur(self):
        sprite_sheet = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/SpriteSheet.png")

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
        self.joueur.setGeometry(self.taille_fen//2, self.taille_fen//2,
                                largeur_sprite, hauteur_sprite)
        self.joueur.setPixmap(sprite)
        
            
    def carte(self):
        pixmap = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/map.png")
        self.fond = QLabel(self)
        self.fond.setPixmap(pixmap)
        self.x_map = -120
        self.y_map = -120
        self.fond.setGeometry(self.x_map, self.y_map, pixmap.width(), pixmap.height())
    """    
    def pokemon(self):
        sprite = QPixmap("C:/Users/kaczo/Documents/projet CCV/RATHANA-BOUCHART-KACZOR/documents/images/pokemons/abra_map.png")
        self.pokemon = QLabel(self)
        self.pokemon.setGeometry(pokemon_pos_arrondies[0][0],
                                pokemon_pos_arrondies[0][0],
                                sprite.width(), sprite.height())  
        self.pokemon.setPixmap(sprite)
    """    
    def affichage_pokemon(self, indice_inconnus):
        name, x, y, image_path = self.inconnus[indice_inconnus]
        if name in self.dict_repet :
            self.dict_repet[name] += 1
        else : 
            self.dict_repet[name] = 1
        name += str(self.dict_repet[name])
        
        pixmap = QPixmap("C:/Users/kaczo/Documents/projet CCV/RATHANA-BOUCHART-KACZOR/documents/images/pokemons/"+image_path)
        label_pokemon = QLabel(self)
        label_pokemon.setPixmap(pixmap)
        label_pokemon.move(x, y)
        label_pokemon.setFixedSize(pixmap.size())
        
        self.dict_connus[name] = label_pokemon
        self.connus.append(self.inconnus[indice_inconnus])
        del self.inconnus_intermediaire[indice_inconnus-self.compteur_sup]
    """    
    def display_pokemons(self):
        self.pokemons_labels = {}
        for pokemon_info in pokemon_pos_arrondies :
            name, x, y, image_path = pokemon_info

            # Charger l'image du pokemon
            pixmap = QPixmap("C:/Users/kaczo/Documents/projet CCV/RATHANA-BOUCHART-KACZOR/documents/images/pokemons/"+image_path)
            pixmap_label = QLabel(self)
            pixmap_label.setPixmap(pixmap)
            pixmap_label.move(x, y)
            pixmap_label.setFixedSize(pixmap.size())
            self.pokemons_labels[pixmap_label] = (name, x, y, image_path)
    """        
    def discover(self):
        print("discover")
        self.compteur_sup = -1
        self.inconnus_intermediaire = self.inconnus.copy()
        for i in range(len(self.inconnus)):
            name, x, y, image_path = self.inconnus[i]
            x_baryc_joueur = self.joueur.x() + self.joueur.width()//2
            y_baryc_joueur = self.joueur.y() + self.joueur.height()//2
            x_c = x_baryc_joueur - self.vision//2
            y_c = y_baryc_joueur - self.vision//2
            L = self.vision
            if Window.point_dans_carre(x, y, x_c, y_c, L) :
                self.compteur_sup += 1
                self.affichage_pokemon(i)
        self.inconnus = self.inconnus_intermediaire.copy()
    """    
    def dist(self, indice_pokemon):
        x_baryc_dresseur = self.dresseur.x() + self.diametre_dresseur/2
        y_baryc_dresseur = self.dresseur.y() + self.diametre_dresseur/2
        exec(f"x_baryc_pokemon = self.p{indice_pokemon}.x() + self.diametre_pokemon/2")
        exec(f"y_baryc_pokemon = self.p{indice_pokemon}.y() + self.diametre_pokemon/2")
        dist_euclid = ((x_baryc_pokemon-x_baryc_dresseur)**2 +
                       (y_baryc_pokemon-y_baryc_dresseur)**2)**0.5
        return dist_euclid
    """
    def point_dans_carre(x, y, x_c, y_c, L):
        # Vérifie si les coordonnées du point sont dans la plage du carré
        if (x >= x_c and x <= x_c + L) and (y >= y_c and y <= y_c + L):
            return True
        else:
            return False


    def keyPressEvent(self, event):
        x = self.fond.x()
        y = self.fond.y()
        x_baryc_joueur = self.joueur.x() + self.joueur.width()//2
        y_baryc_joueur = self.joueur.y() + self.joueur.height()//2
        
        if event.key() == Qt.Key_Up :
            #if y > self.speed :
            self.fond.move(x, y + self.speed)
                
        if event.key() == Qt.Key_Down :
            #if y <= self.L_window - self.diametre_fond - self.speed :
            self.fond.move(x, y - self.speed)
                
        if event.key() == Qt.Key_Left :
            #if x > self.speed :
            self.fond.move(x + self.speed, y)
    
        if event.key() == Qt.Key_Right :
            #if x <= self.l_window - self.diametre_fond - self.speed :
            self.fond.move(x - self.speed, y)
        """
        for i in range(self.nb_pokemons):
                if Window.dist(self, i) <= (self.diametre_dresseur + self.diametre_pokemon)/2 :
                    pixmap = QPixmap(self.diametre_pokemon, self.diametre_pokemon)
                    pixmap.fill(Qt.transparent)
                    painter = QPainter(pixmap)
                    painter.setRenderHint(QPainter.Antialiasing)
                    
                    # Dessiner le disque noir
                    painter.setPen(Qt.NoPen)
                    painter.setBrush(QColor(0, 0, 0))
                    painter.drawEllipse(0, 0, self.diametre_pokemon, self.diametre_pokemon)
                    
                    painter.end()
            
                    exec(f"self.p{i}.setPixmap(pixmap)")
                                        
        """                          

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())