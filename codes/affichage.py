from PIL import Image
from matplotlib import pyplot as plt

# Charger l'image depuis le fichier
image = Image.open("../documents/images/fond.jpg")

# Afficher l'image
plt.imshow(image)
plt.axis('off')  # Masquer les axes
plt.show()