import pandas as pd
import numpy as np
import ast
from abc import ABC, abstractmethod

# On recupere les données dont j'ai besoin qu'on met dans un dataframe
pokemon_stat_df = pd.read_csv("C:\ENSG\Projet_Info\RATHANA-BOUCHART-KACZOR\data\pokemon_first_gen.csv", skiprows=1)
pokemon_position_df=pd.read_csv("C:\ENSG\Projet_Info\RATHANA-BOUCHART-KACZOR\data\pokemon_coordinates.csv",skiprows=1)
table_des_types_df=pd.read_csv("C:\ENSG\Projet_Info\RATHANA-BOUCHART-KACZOR\data\table_des_types.csv",skiprows=1)

# Je les convertis en matrices pour mieux les manipuler
pokemon_stat=pokemon_stat_df.values
pokemon_pos=pokemon_position_df.values
table_types=table_des_types_df.values

#J'arrondis les valeurs des coordonnées des pokemons après les avoir multipliées par 10 pour éviter les conflits (2 pokemons par case par exemple):
pokemon_pos_arrondies=np.copy(pokemon_pos)
coord=np.array([ast.literal_eval(pos) for pos in pokemon_pos[:, 1]]) # ast.literal_eval va transformer les chaînes de caractère de listes en listes
pokemon_pos_arrondies= np.round(coord * 10, decimals=0).astype(int)


#Création d'un dictionnaire avec comme clés les noms des pokemons auxquels on associe leur numéro dans le Pokedex, pour pouvoir optimiser les recherches
dico_pokemon={row[1]:row[0] for row in pokemon_stat}

#Création d'un dictionnaire avec comme clés les types auxquels on associe leur place dans le tableau des types 
dico_types={table_types[0][i+1]: i for i in range(len(table_types)-1)}

class Pokemon:
    #Initialisation des pokemons
    def __init__(self,nom):
        nb_pkm=dico_pokemon[nom]
        self.nom=nom
        self.type1= pokemon_stat[nb_pkm][3]
        self.attack=pokemon_stat[nb_pkm][5]
        self.defense=pokemon_stat[nb_pkm][6]
        self.sp_atk=pokemon_stat[nb_pkm][7]
        self.spe_def=pokemon_stat[nb_pkm][8]
        self.speed=pokemon_stat[nb_pkm][9]
        self.generation=pokemon_stat[nb_pkm][10]
        self.legendary=pokemon_stat[nb_pkm][11]

    @abstractmethod
    def attaque(self,pokemon_adverse):
        pass
        




class PokemonSauvage(Pokemon):
    def __init__(self,x,y):
        self.x=x
        self.y=y 









