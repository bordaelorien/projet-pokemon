import pandas as pd
import numpy as np
import random as rd
import tkinter as tk
from PIL import Image, ImageTk
import glob


class Pokemon():
    def __init__(self,pathPokemon="/Users/leob/Desktop/L3 Eco-MIASHS/Algo/Projet/Partie Pokemon/Pokemon intranet.csv",pathMA="/Users/leob/Desktop/L3 Eco-MIASHS/Algo/Projet/Partie Pokemon/matriceAdjacence.csv",pathAttaques="/Users/leob/Desktop/L3 Eco-MIASHS/Algo/Projet/Partie Pokemon/Attaques.csv"):
        self.df=pd.read_csv(pathPokemon,sep=',',index_col="Name")
        self.df=self.df[~self.df.index.str.contains('Mega')]
        self.dfMatriceAdjacence = pd.read_csv(pathMA, index_col="Type Attaquant")
        self.dfAttaques=pd.read_csv(pathAttaques,sep=',',index_col="Nom_Attaque")
        self.deck1,self.deck2=self.decks()
        ##Graphique
        self.root = tk.Tk()
        self.root.title("Combat Pokémon")
        self.canvas = tk.Canvas(self.root, width=1920, height=1080, bg="#323232")
        self.canvas.pack()
    def decks(self):
        fracPokemon=self.df.sample(120).sort_values(by="Total",ascending=False)
        dfByType = {Type: sous_df for Type, sous_df in fracPokemon.groupby('Type 1')}
        compteur=0
        ltemp=[]
        ltemp2=[]
        for type in dfByType:
            dfByTypeTemp=dfByType.copy()
            if compteur%2==0:
                ltemp.append(dfByTypeTemp[type].iloc[::2])
                ltemp2.append(dfByTypeTemp[type].drop(dfByTypeTemp[type].iloc[::2].index))
            else:
                ltemp2.append(dfByTypeTemp[type].iloc[::2])
                ltemp.append(dfByTypeTemp[type].drop(dfByTypeTemp[type].iloc[::2].index))
            compteur+=1
                
        deck1=pd.concat(ltemp)
        deck2=pd.concat(ltemp2)
        if len(deck1)<60:
            difference=60-len(deck1)
            supplement=deck2.sample(difference)
            deck1=pd.concat([deck1,supplement])
            deck2=deck2.drop(supplement.index)
        else:
            difference=60-len(deck2)
            supplement=deck1.sample(difference)
            deck2=pd.concat([deck2,supplement])
            deck1=deck1.drop(supplement.index)
        deck1["Level"]=1
        deck2["Level"]=1
        return deck1,deck2


    def degat(self,pokemonATT,pokemonDEF,attaquesDispo):
        nom,typeAttaque,puissance=self.attaqueChoisie(attaquesDispo)
        print(puissance)
        damage=((((pokemonATT["Level"]*0.4+2)*pokemonATT["Attack"]*puissance)/(pokemonDEF["Defense"])/15)+2)*np.random.uniform(0.85,1)*self.efficacite(typeAttaque,pokemonDEF["Type 1"],pokemonDEF["Type 2"])
        return round(damage,0)

    def efficacite(self,typeATT1,typeDEF1,typeDEF2=np.nan):
        coeff1=self.dfMatriceAdjacence.loc[typeATT1,typeDEF1]
        if isinstance(typeDEF2,str):
            coeff2=self.dfMatriceAdjacence.loc[typeATT1,typeDEF2]
            return coeff1*coeff2
        return coeff1
    
    
    def premierAttaquant(self,pokemon1,pokemon2):
        if pokemon1["Speed"]<pokemon2["Speed"]:
            return (pokemon2,pokemon1)
        else:
            return (pokemon1,pokemon2)
        
    def combat(self,pokemon1,pokemon2):
        pokemonA,pokemonB=self.premierAttaquant(pokemon1,pokemon2)
        attaquesPA=self.attaquesDisponibles(pokemonA)
        attaquesPB=self.attaquesDisponibles(pokemonB)

        tour=1
        while pokemonA["HP"]>0 and pokemonB["HP"]>0:
            if tour%2!=0:
                damage=self.degat(pokemonA,pokemonB,attaquesPA)
                pokemonB["HP"]=pokemonB["HP"]-damage
                print(f"{pokemonA.name} attaque {pokemonB.name} et lui inflige {damage} points de dégats. Il lui reste {pokemonB['HP']} points de vie.")
            else:
                damage=self.degat(pokemonB,pokemonA,attaquesPB)
                pokemonA["HP"]=pokemonA["HP"]-damage
                print(f"{pokemonB.name} attaque {pokemonA.name} et lui inflige {damage} points de dégats. Il lui reste {pokemonA['HP']} points de vie.")
            tour+=1
        if pokemonA["HP"]<=0:
            pokemonA["Level"]+=1
            pokemonB["Level"]+=1    
            return pokemonB.name
        else:
            pokemonB["Level"]+=1
            pokemonA["Level"]+=1
            return pokemonA.name
    def attaquesDisponibles(self,pokemon):
        type1=pokemon["Type 1"]
        type2=pokemon["Type 2"]
        attaquesType1=self.dfAttaques[self.dfAttaques["Type"]==type1]
        
        if isinstance(type2,str):
            attaquesType2=self.dfAttaques[self.dfAttaques["Type"]==type2]
            attaquesDisponibles=pd.concat([attaquesType1,attaquesType2]).drop_duplicates()
        else:
            attaquesDisponibles=attaquesType1
            
        return attaquesDisponibles

    def attaqueChoisie(self,attaquesdispo):

        nom=rd.choice(attaquesdispo.index.tolist()) ## A modifier pour un bouton sur l'interface graphique
        print(nom)

        typeAttaque=attaquesdispo.loc[nom,"Type"]
        puissance=attaquesdispo.loc[nom,"Puissance"]
        return nom,typeAttaque,puissance

    def strategieAttaque(self,pokemonAtt,pokemonDef,attaquesDispo):        
        l=[]
        for attaque in attaquesDispo.index:
            l.append((attaque,self.degat(pokemonAtt,pokemonDef,attaquesDispo.loc[[attaque]])))
        return max(l,key=lambda x:x[1])
    
    def choixPokemon(self,deck,pokemonAdv):
        bestPokemon=None
        bestDamage=-1
        for i in range(len(deck)):
            pokemon=deck.iloc[i]
            attaquesDispo=self.attaquesDisponibles(pokemon)
            damage=self.strategieAttaque(pokemon,pokemonAdv,attaquesDispo)[1]
            if damage>bestDamage:
                bestDamage=damage
                bestPokemon=pokemon
        return bestPokemon
    
    ##Partie graphique$
    def affichageByType(self,type):
        dfByType = {Type: sous_df for Type, sous_df in self.df.groupby('Type 1')}
        for type in

    def trouverImageType(self,pokemon):

    def trouverImagePokemon(self,pokemon):
        ##os.getcwd()
        print(pokemon.name)
        index=self.df.loc[pokemon.name,"#"]
        print(index)
        pokemonName=pokemon.name.lower()
        imagePokemon="/Users/leob/Desktop/L3 Eco-MIASHS/Algo/Projet/Partie Pokemon/Photos Pokemon/Pokemons/"+str(index)+"-"+pokemonName+".png"
        return imagePokemon
    def afficherPokemon(self,pokemon,x,y):
        ##Affiche le pokemon à la position (x,y)
        image_path=self.trouverImage(pokemon)
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize((600, 600), Image.Resampling.LANCZOS)
        tk_image = ImageTk.PhotoImage(pil_image)
        pokemon_label = tk.Label(self.root, image=tk_image)
        pokemon_label.image = tk_image  # Keep a reference to avoid garbage collection
        pokemon_label.place(x=x, y=y)
        ##Affiche le nom du pokemon


test=Pokemon("/Users/leob/Desktop/L3 Eco-MIASHS/Algo/Projet/Partie Pokemon/Pokemon intranet.csv")
"""print("Deck Joueur 1:")
print(test.deck1)
print("\nDeck Joueur 2:")
print(test.deck2)
##test combat
print("\n---COMBAT---")
print(f"Le gagnant est {test.combat(test.deck1.iloc[0],test.deck2.iloc[0])}")
##test strategie attaque
print("\n---STRATEGIE ATTAQUE---")
attaquesDispo=test.attaquesDisponibles(test.deck1.iloc[0])
print(f"L'attaque la plus efficace pour {test.deck1.iloc[0].name} contre {test.deck2.iloc[0].name} est {test.strategieAttaque(test.deck2.iloc[0],test.deck1.iloc[0],attaquesDispo)[0]} qui inflige {test.strategieAttaque(test.deck2.iloc[0],test.deck1.iloc[0],attaquesDispo)[1]} points de dégats.")
print("\n---CHOIX POKEMON---")
bestPokemon=test.choixPokemon(test.deck1,test.deck2.iloc[0])
print(f"Le meilleur Pokémon pour affronter {test.deck2.iloc[0].name} est {bestPokemon.name}.")"""




