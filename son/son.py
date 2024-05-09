import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Music Player')
        self.setGeometry(100, 100, 300, 200)

        self.player = QMediaPlayer()
        self.loadAndPlayMusic()

    def loadAndPlayMusic(self):
        # Chemin vers le fichier audio
        music_file_path = "C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/son/son.mp3"
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

def main():
    app = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()