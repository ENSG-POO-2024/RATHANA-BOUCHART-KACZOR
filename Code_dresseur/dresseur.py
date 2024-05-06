class Dresseur:
    def __init__(self, pseudo, x, y):
        self.pseudo = pseudo
        self.x = x
        self.y = y
    
    # Méthodes de déplacement
    def gauche(self):
        self.x += -1
    def droite(self):
        self.x += 1
    def haut(self):
        self.y += 1
    def bas(self):
        self.y += -1

    # Méthodes de combat
    def fuite(self):
        pass

