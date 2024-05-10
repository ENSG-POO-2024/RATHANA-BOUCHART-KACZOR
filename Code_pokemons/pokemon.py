import pandas as pd
import numpy as np
import ast
from abc import ABC, abstractmethod
import os 
import random as rd


path=os.path.dirname(os.path.abspath(__file__))
path1=os.path.join(path,"..\data\pokemon_first_gen.csv")
path2=os.path.join(path,"..\data\pokemon_coordinates.csv")
path3=os.path.join(path,"..\data\Table_des_types.csv")
path4=os.path.join(path,"..\data\Attaques.csv")
# On recupere les données dont j'ai besoin qu'on met dans un dataframe
pokemon_stat_df = pd.read_csv(path1)
pokemon_stat_df=pokemon_stat_df.fillna('Rien') #Remplacer les valeurs NaN par 'Rien'
pokemon_position_df=pd.read_csv(path2)
table_des_types_df=pd.read_csv(path3)
nom_attaques_df=pd.read_csv(path4)

# Je les convertis en matrices pour mieux les manipuler
pokemon_stat=pokemon_stat_df.values
pokemon_pos=pokemon_position_df.values
table_types=table_des_types_df.values
nom_attaques=nom_attaques_df.values

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
        nb_pkm=dico_pokemon[nom] -1
        self.npokedex=nb_pkm
        self.name=pokemon_stat[nb_pkm][1]
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

        if self.attack>=self.sp_atk:
            nom_attaque_normale=nom_attaques[0][0]
            nom_attaque_type=nom_attaques[dico_types[self.type1]][0]
        else:
            nom_attaque_normale=nom_attaques[0][1]
            nom_attaque_type=nom_attaques[dico_types[self.type1]][1]

        self.attaque_normale =nom_attaque_normale
        self.attaque_type = nom_attaque_type

    def attaque(self,pokemon_adverse):
        if self.attack>=self.sp_atk:
            stat_attaque=self.attack
            stat_defense=pokemon_adverse.defense
        else:
            stat_attaque=self.sp_atk
            stat_defense=pokemon_adverse.spe_def
        attaque=int(input("Quelle attaque choisir: L'attaque 1 (type normal) ou l'attaque 2 (type de votre pokemon)? :"))
        while attaque != 1 and attaque !=2:
            attaque=int(input("Choississez soit l'attaque 1 soit l'attaque 2 (écrivez 1 ou 2):"))
        if attaque==1:  #On recupere le type de l'attaque
            type_attaque=dico_types["Normal"]
        else:
            type_attaque=dico_types[self.type1]
            if self.type1=="Normal" and not self.type2 != "Rien": # Definir le type de l'attaque comme le type 2, s'il existe et que le type 1 est "Normal"
                type_attaque=self.type2

        type_defense1=dico_types[pokemon_adverse.type1] #On recupere le type de defense
        if pokemon_adverse.type2 != "Rien":
            type_defense2=dico_types[pokemon_adverse.type2]
        #On applique la formule officielle des degats des attaques, mais sans prendre en compte les niveaux
        CM=table_types[type_attaque][type_defense1]
        if pokemon_adverse.type2 != "Rien":
            CM*=table_types[type_attaque][type_defense2]
        degats= np.trunc((np.trunc((5*stat_attaque * 55)/(stat_defense *50))+2) * CM)
        pokemon_adverse.HP=pokemon_adverse.HP - degats
        if pokemon_adverse.HP<0:
            pokemon_adverse.HP=0
        return pokemon_adverse.HP, degats,
        




class PokemonSauvage(Pokemon):
    def __init__(self,name,x,y):
        super().__init__(name)
        self.x=x
        self.y=y 

    def attaque(self,pokemon_adverse):
        type_attaque=""
        nb_aleatoire=rd.randint(1,2)
        if nb_aleatoire==1:
            type_attaque=dico_types["Normal"]
        if nb_aleatoire==2:
            type_attaque=dico_types[self.type1]
        if self.type1=="Normal" and self.type2 !="Rien":
            type_attaque=dico_types[self.type2]
        
        if self.attack>=self.sp_atk:
            stat_attaque=self.attack
            stat_defense=pokemon_adverse.defense
        else:
            nom_attaque_normale=nom_attaques[0][1]
            nom_attaque_type=nom_attaques[dico_types[self.type1]][1]
            stat_attaque=self.sp_atk
            stat_defense=pokemon_adverse.spe_def
        type_defense1=dico_types[pokemon_adverse.type1] #On recupere le type de defense
        if pokemon_adverse.type2 != "Rien":
            type_defense2=dico_types[pokemon_adverse.type2]
        #On applique la formule officielle des degats des attaques, mais sans prendre en compte les niveaux
        CM=table_types[type_attaque][type_defense1]
        if pokemon_adverse.type2 != "Rien":
            CM*=table_types[type_attaque][type_defense2]
        degats= np.trunc((np.trunc((5*stat_attaque * 55)/(stat_defense *50))+2) * CM)
        pokemon_adverse.HP=pokemon_adverse.HP - degats
        if pokemon_adverse.HP<0:
            pokemon_adverse.HP=0
        return pokemon_adverse.HP, degats, nom_attaque_normale, nom_attaque_type

if __name__=="__main__":
    mew=Pokemon("Mew")
    florizare=Pokemon("Venusaur")
    print(mew.attaque(florizare))
    print(florizare.attaque(mew))






