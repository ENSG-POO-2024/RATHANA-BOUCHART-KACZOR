"""from PIL import Image
from matplotlib import pyplot as plt

# Charger les images
fond = Image.open("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/fond_pokemon.jpg")
planche = Image.open("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/SpriteSheet.png")

# Découper le Sprite Sheet
liste_personnages = [(1,0,31,36)]

for personnage in liste_personnages:
    perso_sprite = planche.crop(personnage).convert("RGBA")
    perso_redimension = perso_sprite.resize((300, 360))
    # Superposer le sprite sur le fond
    fond.paste(perso_redimension, (15, 20))  # Remplacez x_position et y_position par les coordonnées de position sur votre fond

# Afficher l'image
plt.clf()
plt.imshow(fond, interpolation="none")
plt.axis('off')  # Masquer les axes
plt.show()

"""

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QPainter

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Charger les images
        self.fond = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/fond_pokemon.jpg")
        self.planche = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/SpriteSheet.png")

        # Créer un label pour afficher l'image de fond
        self.fond_label = QLabel(self)
        self.fond_label.setPixmap(self.fond)

        # Découper le Sprite Sheet
        self.liste_personnages = [(1, 0, 31, 36)]

        # Superposer le personnage sur l'image de fond
        for personnage in self.liste_personnages:
            perso_sprite = self.planche.copy(*personnage)
            perso_redimension = perso_sprite.scaled(30, 36)

            # Créer un label pour afficher le personnage
            perso_label = QLabel(self)
            perso_label.setPixmap(perso_redimension)
            perso_label.move(15, 20)  # Position du personnage sur l'image de fond
            perso_label.show()

        # Redimensionner la fenêtre à la taille de l'image de fond
        self.resize(self.fond.width(), self.fond.height())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())