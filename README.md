# Pokémon: projet informatique

* Kaczor Virgile ING1
* Bouchart Celia ING1
* Rathana Clément ING1

## Comment est organisé le projet: 

Voici la liste des différents dossiers:

- **Code Interface**: contient *accueil.py* qui affiche l'écran d'accueil

- **Code_dresseur**: contient *fusion.py* qui gère le comportement du dresseur dans la map ainsi que le son généré dans la map

- **Code_pokemons contient**: contient un dossier *VFX/SFX* avec tous les effets sonores et les images nécessaires pour l'interface de combat, *combat.py* qui s'occupe d'afficher les combats et *pokemon* qui contient la définition des classes des pokemons ainsi que leurs méthodes

- **data**: contient les données de départ et deux CSV que nous avons ajoutés pour en extraire les informations

- **Designer**: est apparu un beau matin sans que nous en sachions l'origine...

- **documents**: contient les documents fournis au début des TP, ainsi que toutes les images nécessaires pour les pokemons et la map dans *images*, et également les diagrammes UML du projet

- **son**: contient tous les sons de la map

- **Interface.py: le code à lancer pour démarrer le jeu**

## Comment fonctionne le jeu:

1) On arrive sur l'écran d'accueuil dans lequel on peut choisir son pokemon de depart

2) On se déplace sur la map avec les flèches du clavier. Des pokemons apparaissent quand on s'en approche: pour lancer le combat il suffit de marcher dessus. il y a deux boutons: "map" qui permet de mettre la map en plein écran (ne pas utiliser l'outil de mise en plein écran de la fenêtre) et le bouton "inventaire" qui permet d'afficher les pokemons de son inventaire et les échanger avec les pokemons de son équipe. L'inventaire est vide pour le moment.

3) Une fois le combat lancé, on peut choisir entre attaquer (deux attaques disponibles, une normale et une typée comme le pokemon), soigner son pokemon grâce au sac, changer de pokemon et fuire. Pour capturer un pokemon, il faut le vaincre, une fois le pokemon vaincu, il arrive soit dans l'équipe du dresseur, soit dans l'inventaire si l'équipe est complète.
Le but est bien entendu de capturer tous les Pokemons de la map, le boss final étant un petit Easter Egg dissimulé dans le jeu, que vous remarquerez bien aisément si vous tombez dessus (nous vous conseillons de bâtir une équipe puissante avant de vous y frotter, faute de quoi vous essuierez sans doute une défaite). Lorsque l'un de vos pokemon est KO, il ne peut plus être envoyé au combat, et lorsque toute votre équipe est KO, vous êtes téléporté au point d'apparition, avec vos pokemons soignés.




