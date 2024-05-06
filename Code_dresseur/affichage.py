from PIL import Image
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
