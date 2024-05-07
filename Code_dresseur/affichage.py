import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Charger l'image depuis un fichier
        pixmap = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/chemin.png")
        sprite_sheet = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/SpriteSheet.png")
        
        # Dimensions 
        hauteur_sprite_sheet = 144
        largeur_sprite_sheet = 124
        hauteur_sprite = 36
        largeur_sprite = 31


        # Découper le sprite sheet
        coordonnees_sprites = [(x, y, largeur_sprite, hauteur_sprite) for x in range(0, largeur_sprite_sheet, largeur_sprite) for y in range(0, hauteur_sprite_sheet, hauteur_sprite)]
        self.sprites_individuels = []
        for coordonnees_sprite in coordonnees_sprites:
            sprite_individuel = sprite_sheet.copy(*coordonnees_sprite)
            self.sprites_individuels.append(sprite_individuel)

        # Créer un label pour afficher l'image
        self.fond = QLabel(self)
        self.fond.setPixmap(pixmap)
        self.fond.setGeometry(50, 50, pixmap.width()//2, pixmap.height()//2)  # Définir la position et la taille du label
        #self.fond.setScaledContents(True)  # Redimensionner automatiquement l'image pour s'adapter au label

        # Créer un label et afficher le perso

        # Réduire la taille de chaque sprite de moitié
        for i in range(len(self.sprites_individuels)):
            sprite_reduit = self.sprites_individuels[i].scaled(self.sprites_individuels[i].width() // 2, self.sprites_individuels[i].height() // 2)
            self.sprites_individuels[i] = sprite_reduit

        """self.joueur = QLabel(self)
        self.joueur.setPixmap(self.sprites_individuels[0])  # Afficher le sprite individuel au choix
        self.joueur.setGeometry(50 , 50 , largeur_sprite, hauteur_sprite)  # Définir la position et la taille du joueur
        self.joueur.show()"""

        # Redimensionner la fenêtre à la taille de l'image
        self.resize(pixmap.width() + 100, pixmap.height() + 100)

        self.UiComponents()

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
        sprite = QPixmap(self.sprites_individuels[0])
        painter.drawPixmap(int((self.diametre_dresseur - sprite.width()) / 2),int((self.diametre_dresseur - sprite.height()) / 2),sprite)

        painter.end()

        self.joueur.setPixmap(pixmap)

    def UiComponents(self):
        self.joueur = QLabel(self)
        self.diametre_dresseur = 30
        largeur_fenetre = int(self.width())
        self.joueur.setGeometry((largeur_fenetre - self.diametre_dresseur) // 2, 
                               (largeur_fenetre - self.diametre_dresseur) // 2, 
                               self.diametre_dresseur, self.diametre_dresseur)
        self.draw_disk()

    def keyPressEvent(self, event):
        x = self.joueur.x()
        y = self.joueur.y()
        
        if event.key() == Qt.Key_Up :
            if y > self.speed :
                self.joueur.move(x, y - self.speed)
                self.joueur.setPixmap(self.sprites_individuels[2])
                
        if event.key() == Qt.Key_Down :
            if y <= self.height() - self.diametre_dresseur - self.speed :
                self.joueur.move(x, y + self.speed)
                self.joueur.setPixmap(self.sprites_individuels[0])
                
        if event.key() == Qt.Key_Left :
            if x > self.speed :
                self.joueur.move(x - self.speed, y)
                self.joueur.setPixmap(self.sprites_individuels[3])
    
        if event.key() == Qt.Key_Right :
            if x <= self.width() - self.diametre_dresseur - self.speed :
                self.joueur.move(x + self.speed, y)
                self.joueur.setPixmap(self.sprites_individuels[1])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

