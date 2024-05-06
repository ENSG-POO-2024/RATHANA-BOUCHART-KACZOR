from PIL import Image
from matplotlib import pyplot as plt

# Charger l'image depuis le fichier
image = Image.open("C:/Users/dell/OneDrive/Bureau/Projet Pokémon/RATHANA-BOUCHART-KACZOR/documents/images/fond_pokemon.jpg")

# Afficher l'image
plt.imshow(image)
plt.axis('off')  # Masquer les axes
plt.show()