import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QPixmap

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
        
        self.music_player = Music()  # Ajout de l'objet Music

    def dresseur(self):
        sprite_sheet = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/SpriteSheet.png")

        self.hauteur_sprite = sprite_sheet.height()//4
        self.largeur_sprite = sprite_sheet.width()//4
        
        # Découper le sprite sheet
        coordonnees_sprites = [(x, y, self.largeur_sprite, self.hauteur_sprite) for x in range(2, sprite_sheet.width(), self.largeur_sprite + 15) for y in range(0, sprite_sheet.height(), self.hauteur_sprite)]
        self.sprites_individuels = []
        for coordonnees_sprite in coordonnees_sprites:
            sprite_individuel = sprite_sheet.copy(*coordonnees_sprite)
            self.sprites_individuels.append(sprite_individuel)
        sprite = QPixmap(self.sprites_individuels[4])
        
        self.joueur = QLabel(self)
        self.joueur.setGeometry(248, 108, self.largeur_sprite, self.hauteur_sprite)
        self.joueur.setPixmap(sprite)
        
            
    def carte(self):
        pixmap = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/collisions.png")
        self.fond_collisions = QLabel(self)
        self.fond_collisions.setPixmap(pixmap)
        self.fond_collisions.setGeometry(0, 0, pixmap.width(), pixmap.height())

        pixmap = QPixmap("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/fond.png")
        self.fond_visible = QLabel(self)
        self.fond_visible.setPixmap(pixmap)
        self.fond_visible.setGeometry(0, 0, pixmap.width(), pixmap.height())
    
    def keyPressEvent(self, event):
        x = self.fond_collisions.x()
        y = self.fond_collisions.y()
        x_joueur = self.joueur.x() - self.fond_collisions.x()
        y_joueur = self.joueur.y() - self.fond_collisions.y() 

        if event.key() == Qt.Key_Up :
            couleur_pixel = [self.fond_collisions.pixmap().toImage().pixelColor(x_joueur + i , y_joueur-1 ) for i in range (0,self.largeur_sprite)]
            for i in range(self.largeur_sprite):
                if (couleur_pixel[i] == Qt.black) :
                    self.music_player.bruit_bump()
                    self.apparence_actuelle = 6
                    self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])
                    break
                elif (couleur_pixel[i] != Qt.black) and (i == self.largeur_sprite - 1) :
                    self.fond_collisions.move(x, y + self.hauteur_sprite)
                    self.fond_visible.move(x, y + self.hauteur_sprite)
                    if (self.apparence_actuelle == 2) or (self.apparence_actuelle == 6) or (self.apparence_actuelle == 10) :
                        self.changer_apparence()
                    else : 
                        self.apparence_actuelle = 6
                    self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])

        if event.key() == Qt.Key_Down :
            couleur_pixel = [self.fond_collisions.pixmap().toImage().pixelColor(x_joueur + i , y_joueur -1 + self.hauteur_sprite + self.hauteur_sprite) for i in range (0,self.largeur_sprite)]
            for i in range(self.largeur_sprite):
                if (couleur_pixel[i] == Qt.black) :
                    self.music_player.bruit_bump()
                    self.apparence_actuelle = 4
                    self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])
                    break
                elif (couleur_pixel[i] != Qt.black) and (i == self.largeur_sprite - 1) :
                    self.fond_collisions.move(x, y - self.hauteur_sprite)
                    self.fond_visible.move(x, y - self.hauteur_sprite)
                    if (self.apparence_actuelle == 0) or (self.apparence_actuelle == 4) or (self.apparence_actuelle == 8) :
                        self.changer_apparence()
                    else : 
                        self.apparence_actuelle = 4
                    self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])

        if event.key() == Qt.Key_Left :
            couleur_pixel = [self.fond_collisions.pixmap().toImage().pixelColor(x_joueur - self.largeur_sprite, y_joueur + i) for i in range (0, self.hauteur_sprite)]
            for i in range(self.hauteur_sprite) :
                if (couleur_pixel[i] == Qt.black) :
                    self.music_player.bruit_bump()
                    self.apparence_actuelle = 7
                    self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])
                    break
                elif (couleur_pixel[i] != Qt.black) and (i == self.hauteur_sprite - 1):
                    self.fond_collisions.move(x + self.largeur_sprite, y)
                    self.fond_visible.move(x + self.largeur_sprite, y)
                    if (self.apparence_actuelle == 3) or (self.apparence_actuelle == 7) or (self.apparence_actuelle == 11) :
                        self.changer_apparence()
                    else : 
                        self.apparence_actuelle = 7
                    self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])
    
        if event.key() == Qt.Key_Right :
            couleur_pixel = [self.fond_collisions.pixmap().toImage().pixelColor(x_joueur + self.largeur_sprite-1 + self.largeur_sprite, y_joueur + i) for i in range (0, self.hauteur_sprite)]
            for i in range(self.hauteur_sprite):
                if (couleur_pixel[i] == Qt.black) :
                    self.music_player.bruit_bump()
                    self.apparence_actuelle = 5
                    self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])
                    break
                elif (couleur_pixel[i] != Qt.black) and (i == self.hauteur_sprite - 1):
                    self.fond_collisions.move(x - self.largeur_sprite, y)
                    self.fond_visible.move(x - self.largeur_sprite, y)
                    if (self.apparence_actuelle == 1) or (self.apparence_actuelle == 5) or (self.apparence_actuelle == 9) :
                        self.changer_apparence()
                    else : 
                        self.apparence_actuelle = 5
                    self.joueur.setPixmap(self.apparences_joueur[self.apparence_actuelle])
    
    def changer_apparence(self):
        self.apparence_actuelle = (self.apparence_actuelle + 4) % len(self.apparences_joueur)


class Music():
    def __init__(self):
        self.player = QMediaPlayer()
        self.bump = QMediaPlayer()
        self.loadAndPlayMusic()

    def loadAndPlayMusic(self):
        # Chemin vers le fichier audio
        music_file_path = "C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/son/son.mp3" # Remplacez par le chemin de votre musique
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(music_file_path)))
        self.player.setVolume(50)  # Réglez le volume (0-100)
        self.player.play()  # Commence à jouer

        # Connectez le signal stateChanged à une fonction pour gérer la fin de la musique
        self.player.stateChanged.connect(self.checkState)

    def checkState(self, state):
        if state == QMediaPlayer.EndOfMedia:
            # Si la musique est terminée, remettez la lecture au début
            self.player.setPosition(0)
            self.player.play()

    def bruit_bump(self):
        son_bump = "C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/son/bump.mp3"
        self.bump.setMedia(QMediaContent(QUrl.fromLocalFile(son_bump)))
        self.bump.setVolume(50)
        self.bump.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
    