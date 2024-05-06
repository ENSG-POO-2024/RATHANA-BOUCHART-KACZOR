import pandas as pd
import numpy as np
import ast
from abc import ABC, abstractmethod
import os 

# On recupere les données dont j'ai besoin qu'on met dans un dataframe
pokemon_stat_df = pd.read_csv("../data/pokemon_first_gen.csv", skiprows=1)
pokemon_position_df=pd.read_csv("../data/pokemon_coordinates.csv",skiprows=1)
table_des_types_df=pd.read_csv("../data/Table_des_types.csv")

# Je les convertis en matrices pour mieux les manipuler
pokemon_stat=pokemon_stat_df.values
pokemon_pos=pokemon_position_df.values
table_types=table_des_types_df.values

#J'arrondis les valeurs des coordonnées des pokemons après les avoir multipliées par 10 pour éviter les conflits (2 pokemons par case par exemple):
pokemon_pos_arrondies=np.copy(pokemon_pos)
coord=np.array([ast.literal_eval(pos) for pos in pokemon_pos[:, 1]]) # ast.literal_eval va transformer les chaînes de caractère de listes en listes
pokemon_pos_arrondies[:, 1]= np.round(coord[:,0]* 10, decimals=0).astype(int)
pokemon_pos_arrondies=np.hstack((pokemon_pos_arrondies,np.round(coord[:,1]* 10, decimals=0).astype(int).reshape(-1,1)))

#Création d'un dictionnaire avec comme clés les noms des pokemons auxquels on associe leur numéro dans le Pokedex, pour pouvoir optimiser les recherches
dico_pokemon={row[1]:row[0] for row in pokemon_stat}

#Création d'un dictionnaire avec comme clés les types auxquels on associe leur place dans le tableau des types 
dico_types={table_types[i][0]: i for i in range(len(table_types))}

#Je supprime la premiere colonne de la matrice qui ne me sert plus a rien 
table_types= np.delete(table_types, 0, axis=1)

class Pokemon:
    #Initialisation des pokemons
    def __init__(self,nom):
        nb_pkm=dico_pokemon[nom]
        self.nom=nom
        self.type1= pokemon_stat[nb_pkm][2]
        self.type2=pokemon_stat[nb_pkm][3]
        self.HP=pokemon_stat[nb_pkm][5]
        self.attack=pokemon_stat[nb_pkm][6]
        self.defense=pokemon_stat[nb_pkm][7]
        self.sp_atk=pokemon_stat[nb_pkm][8]
        self.spe_def=pokemon_stat[nb_pkm][9]
        self.speed=pokemon_stat[nb_pkm][10]
        self.generation=pokemon_stat[nb_pkm][11]
        self.legendary=pokemon_stat[nb_pkm][12]

    def attaque(self,pokemon_adverse):
        attaque=int(input("Quelle attaque choisir: L'attaque 1 (type normal) ou l'attaque 2 (type de votre pokemon)? :"))
        while attaque != 1 and attaque !=2:
            attaque=int(input("Choississez soit l'attaque 1 soit l'attaque 2 (écrivez 1 ou 2):"))
        if attaque==1:  #On recupere le type de l'attaque
            type_attaque=dico_types["Normal"]
        else:
            type_attaque=dico_types[self.type1]
        type_defense1=dico_types[pokemon_adverse.type1]  #On recupere le type de defense
        #type_defense2=dico_types[pokemon_adverse.type2]
        #On applique la formule officielle des degats des attaques, mais sans prendre en compte les niveaux
        degats= np.trunc((np.trunc((self.attack * 40)/(pokemon_adverse.defense *50))+2) * table_types[type_attaque][type_defense1])
        pokemon_adverse.HP=pokemon_adverse.HP - degats
        if pokemon_adverse.HP<0:
            pokemon_adverse.HP=0
        return pokemon_adverse.HP, degats
        




class PokemonSauvage(Pokemon):
    def __init__(self,name,x,y):
        super().__init__(name)
        self.x=x
        self.y=y 

    def attaque(self,pokemon_adverse):
        return super().attaque(pokemon_adverse)

if __name__=="__main__":
    print(pokemon_pos_arrondies)









