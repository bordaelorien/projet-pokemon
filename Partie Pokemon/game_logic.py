
import pandas as pd
import numpy as np
from paths import pathDf


class GameLogic:
    def __init__(self, df_attacks):
        self.df_attacks = df_attacks
        self.dfMatriceAdjacence= pd.read_csv(pathDf("matriceAdjacence"), index_col=0)

    def attaques_disponibles(self, pokemon):
        """
        Retourne les attaques disponibles pour un Pokémon donné en fonction de ses types.
        """
        type1 = pokemon["Type 1"]
        type2 = pokemon["Type 2"]

        attaques_type1 = self.df_attacks[self.df_attacks["Type"] == type1]

        if isinstance(type2, str):
            attaques_type2 = self.df_attacks[self.df_attacks["Type"] == type2]
            return pd.concat([attaques_type1, attaques_type2])

        return attaques_type1

    def degat(self, attaquant, defenseur, attaque):
        """ 
        Calcule les dégâts infligés par l'attaquant au défenseur en utilisant une attaque spécifique.
        """
        typeAttaque=self.df_attacks.loc[attaque,"Type"]
        puissance=self.df_attacks.loc[attaque,"Puissance"]
        print(self.efficacite(typeAttaque,defenseur["Type 1"],defenseur["Type 2"]),attaquant["Name"])
        damage=((((attaquant["Level"]*0.4+2)*attaquant["Attack"]*puissance)/(defenseur["Defense"])/15)+2)*np.random.uniform(0.85,1)*self.efficacite(typeAttaque,defenseur["Type 1"],defenseur["Type 2"])
        return round(damage,0)
    
    def efficacite(self,typeATT1,typeDEF1,typeDEF2=np.nan):
        """
        Calcule le coefficient d'efficacité d'une attaque en fonction des types de l'attaquant et du défenseur.
        """
        coeff1=self.dfMatriceAdjacence.loc[typeATT1,typeDEF1]
        if isinstance(typeDEF2,str):
            coeff2=self.dfMatriceAdjacence.loc[typeATT1,typeDEF2]
            return coeff1*coeff2
        return coeff1

    def estIlPerdant(self, pokemon):
        """
        Vérifie si un Pokémon a perdu (HP <= 0).
        """
        return pokemon["HP"] <= 0
    def premierAttaquant(self,pokemon1,pokemon2):
        """
        Détermine quel Pokémon attaque en premier en fonction de leur vitesse.
        """
        if pokemon1["Speed"]>=pokemon2["Speed"]:
            return pokemon1,pokemon2
        return pokemon2,pokemon1
   