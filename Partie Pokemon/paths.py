
from pathlib import Path

root = Path(__file__).parent

def path():
    """
    Renvoie le path d'un fichier donné
    """
    return str(root)
def pathType(name):
    """
    Renvoie le path d'un type donné
    """
    return path()+ "/Type/" + name + ".png"
def pathPokemon(id, name):
    """
    Renvoie le path d'un pokémon donné
    """
    return path()+ "/Photos Pokemon/" + str(id)+"-"+ name + ".png" 

def pathDf(name):
    """
    Renvoie le path d'une DataFrame donnée
    """
    return path()+ "/DataFrames/" + name + ".csv"

def pathType1(pokemon):
    """
    Retourne le chemin de l'image du premier type d'un Pokémon
    """
    type=pokemon["Type 1"]
    path_type1=pathType(type)
    return path_type1
    
def pathType2(pokemon):
    """
    Retourne le chemin de l'image du second type d'un Pokémon, ou False s'il n'en a pas
    """
    type=pokemon["Type 2"]
    if isinstance(type,str):
        path_type2=pathType(type)
    else:
        path_type2=False
    return path_type2




