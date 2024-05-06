import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap

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
        sprites_individuels = []
        for coordonnees_sprite in coordonnees_sprites:
            sprite_individuel = sprite_sheet.copy(*coordonnees_sprite)
            sprites_individuels.append(sprite_individuel)

        # Créer un label pour afficher l'image
        fond = QLabel(self)
        fond.setPixmap(pixmap)
        fond.setGeometry(50, 50, pixmap.width(), pixmap.height())  # Définir la position et la taille du label
        fond.setScaledContents(True)  # Redimensionner automatiquement l'image pour s'adapter au label

        # Créer un label et afficher le perso
        joueur = QLabel(self)
        joueur.setPixmap(sprites_individuels[2])  # Afficher le sprite individuel au choix
        joueur.setGeometry(50 , 50 , largeur_sprite, hauteur_sprite)  # Définir la position et la taille du joueur
        joueur.show()

        # Redimensionner la fenêtre à la taille de l'image
        self.resize(pixmap.width() + 100, pixmap.height() + 100)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
