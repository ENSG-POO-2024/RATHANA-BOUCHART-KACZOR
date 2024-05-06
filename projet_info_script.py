# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import random as rd

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.L_window = 500
        self.l_window = 500
        
        self.setGeometry(400, 400, self.l_window, self.L_window)
        
        self.UiComponents()
        
        self.show()
        
        self.speed = 10
            
    def draw_disk(self):
        pixmap = QPixmap(self.diametre_dresseur, self.diametre_dresseur)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dessiner le disque rouge
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(0, 0, self.diametre_dresseur, self.diametre_dresseur)
        
        # Dessiner le carré au centre
        painter.setBrush(QColor(0, 0, 255))
        painter.drawRect((self.diametre_dresseur-10)/2, (self.diametre_dresseur-10)/2, 10, 10)

        painter.end()

        self.dresseur.setPixmap(pixmap)        
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
        
    def UiComponents(self):
        self.dresseur = QLabel(self)
        self.diametre_dresseur = 30
        self.dresseur.setGeometry((self.l_window-self.diametre_dresseur)/2, 
                                  (self.l_window-self.diametre_dresseur)/2, 
                                  self.diametre_dresseur, self.diametre_dresseur)
        self.draw_disk()
        """
        self.nb_pokemons = 30
        self.diametre_pokemon = 20
        for i in range(self.nb_pokemons):
            exec(f"self.p{i} = QLabel(self)")
            exec(f"self.p{i}.setGeometry(rd.randrange(500), rd.randrange(500), self.diametre_pokemon, self.diametre_pokemon)")
        """
    def keyPressEvent(self, event):
        x = self.dresseur.x()
        y = self.dresseur.y()
        
        if event.key() == Qt.Key_Up :
            if y > self.speed :
                self.dresseur.move(x, y - self.speed)
                
        if event.key() == Qt.Key_Down :
            if y <= self.L_window - self.diametre_dresseur - self.speed :
                self.dresseur.move(x, y + self.speed)
                
        if event.key() == Qt.Key_Left :
            if x > self.speed :
                self.dresseur.move(x - self.speed, y)
    
        if event.key() == Qt.Key_Right :
            if x <= self.l_window - self.diametre_dresseur - self.speed :
                self.dresseur.move(x + self.speed, y)
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
            