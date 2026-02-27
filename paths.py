
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



