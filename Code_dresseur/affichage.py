from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import random as rd

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.vision = 400
        
        self.setGeometry(400, 100, self.vision, self.vision) #fenêtre principale
        
        self.carte()
        self.dresseur()
        
        self.show()
        self.apparences_joueur = self.sprites_individuels
        self.apparence_actuelle = 4
        
    def dresseur(self):
        sprite_sheet = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/SpriteSheet.png")

        hauteur_sprite = sprite_sheet.height()//4
        largeur_sprite = sprite_sheet.width()//4
        
        # Découper le sprite sheet
        coordonnees_sprites = [(x, y, largeur_sprite, hauteur_sprite) for x in range(2, sprite_sheet.width(), largeur_sprite + 15) for y in range(0, sprite_sheet.height(), hauteur_sprite)]
        self.sprites_individuels = []
        for coordonnees_sprite in coordonnees_sprites:
            sprite_individuel = sprite_sheet.copy(*coordonnees_sprite)
            self.sprites_individuels.append(sprite_individuel)
        sprite = QPixmap(self.sprites_individuels[4])
        
        self.joueur = QLabel(self)
        self.joueur.setGeometry(self.vision//2, self.vision//2, largeur_sprite, hauteur_sprite)
        self.joueur.setPixmap(sprite)
        
        self.speed = 20
            
    def carte(self):
        pixmap = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/map.png")
        self.fond = QLabel(self)
        self.fond.setPixmap(pixmap)
        self.fond.setGeometry(0, 0, pixmap.width(), pixmap.height())
          
        
    def dist(self, indice_pokemon):
        x_baryc_dresseur = self.dresseur.x() + self.diametre_dresseur/2
        y_baryc_dresseur = self.dresseur.y() + self.diametre_dresseur/2
        exec(f"x_baryc_pokemon = self.p{indice_pokemon}.x() + self.diametre_pokemon/2")
        exec(f"y_baryc_pokemon = self.p{indice_pokemon}.y() + self.diametre_pokemon/2")
        dist_euclid = ((x_baryc_pokemon-x_baryc_dresseur)**2 +
                       (y_baryc_pokemon-y_baryc_dresseur)**2)**0.5
        return dist_euclid


    def keyPressEvent(self, event):
        x = self.fond.x()
        y = self.fond.y()
        
        if event.key() == Qt.Key_Up :
            self.fond.move(x, y + self.speed)
            if (self.apparence_actuelle == 2) or (self.apparence_actuelle == 6) or (self.apparence_actuelle == 10) :
                self.changer_apparence()
            else : 
                self.apparence_actuelle = 6
            self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])
                

        if event.key() == Qt.Key_Down :
            self.fond.move(x, y - self.speed)
            if (self.apparence_actuelle == 0) or (self.apparence_actuelle == 4) or (self.apparence_actuelle == 8) :
                self.changer_apparence()
            else : 
                self.apparence_actuelle = 4
            self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])

        if event.key() == Qt.Key_Left :
            self.fond.move(x + self.speed, y)
            if (self.apparence_actuelle == 3) or (self.apparence_actuelle == 7) or (self.apparence_actuelle == 11) :
                self.changer_apparence()
            else : 
                self.apparence_actuelle = 7
            
            self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])
    
        if event.key() == Qt.Key_Right :
            self.fond.move(x - self.speed, y)
            if (self.apparence_actuelle == 1) or (self.apparence_actuelle == 5) or (self.apparence_actuelle == 9) :
                self.changer_apparence()
            else : 
                self.apparence_actuelle = 5
            self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])
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
    def changer_apparence(self):
        self.apparence_actuelle = (self.apparence_actuelle + 4) % len(self.apparences_joueur)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
            