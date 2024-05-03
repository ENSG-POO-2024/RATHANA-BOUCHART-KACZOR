import pandas as pd
import numpy as np

pokemon_csv = pd.read_csv("pokemon_first_gen.csv", skiprows=1)
pokemon_position=pd.read_csv("pokemon_coordinates.csv",skiprows=1)

pokemon_stat=pokemon_csv.values
pokemon_pos=pokemon_position.values

pokemon_pos=np.round(np.multiply(pokemon_pos,10))

dico_pokemon={row[1]:row[0] for row in pokemon_stat}


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
        




class PokemonSauvage(Pokemon):
    def __init__(self,x,y):
        self.x=x
        self.y=y 







#class Pokemon:
#    def __init__(self,):

