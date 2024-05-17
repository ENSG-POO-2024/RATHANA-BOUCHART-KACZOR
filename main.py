import sys
import os
from PyQt5.QtWidgets import QApplication

from Interface import Window

sys.path.append(os.path.abspath('Code Interface'))
import accueil
from accueil import Fenetre


def main():
    app = QApplication(sys.argv)
    
    # Lancer la première fenêtre
    fenetre = Fenetre()
    fenetre.show()

    
    # Lancer la deuxième fenêtre
    mainWin = Window()
    mainWin.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
