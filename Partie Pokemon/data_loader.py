
import pandas as pd
from paths import pathDf

def dfPokemon():
    df = pd.read_csv(pathDf("pokemon"))
    return df

def dfAttaques():
    df = pd.read_csv(pathDf("attaques"))
    return df
