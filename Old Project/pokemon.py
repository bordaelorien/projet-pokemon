import pandas as pd
import numpy as np
import random as rd
import tkinter as tk
from PIL import Image, ImageTk
from os import getcwd
from pathlib import Path


def path():
    return str(Path(__file__).parent)


policePath=path()+"/Police/arial.ttf"



class Pokemon():
    def __init__(self,pathPokemon="Partie Pokemon/Pokemon intranet.csv",pathMA="Partie Pokemon/matriceAdjacence.csv",pathAttaques="Partie Pokemon/Attaques.csv"):
        self.df=pd.read_csv(pathPokemon,sep=',',index_col="Name")
        self.dfMatriceAdjacence = pd.read_csv(pathMA, index_col="Type Attaquant")
        self.dfAttaques=pd.read_csv(pathAttaques,sep=',',index_col="Nom_Attaque")
        self.deck1,self.deck2=self.decks()
        self.pokemonActif=None
        self.pokemonPassif=None
        ##Graphique
        self.couleurPolicePokemon="#F2CF46"
        self.root = tk.Tk()
        self.root.title("Combat Pokémon")
    
        self.canvas = tk.Canvas(self.root, width=1920, height=1080, bg="#323232")
        self.objet={}
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


    def degat(self,pokemonATT,pokemonDEF,attaque):
        typeAttaque=self.dfAttaques.loc[attaque,"Type"]
        puissance=self.dfAttaques.loc[attaque,"Puissance"]
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
    
    def estilgagnant(self,pokemon):
        if pokemon["HP"]<=0:
            return True
    def faireDegats(self,attaquant,defenseur,attaque):
        if attaquant.name!=self.pokemonActif.name:
            return
        
        if self.estilgagnant(defenseur):
            return self.affichageGagnant(attaquant)
        
        damage=self.degat(attaquant,defenseur,attaque)
        defenseur["HP"]=defenseur["HP"]-damage
        self.objet['hp'+defenseur.name][0].set(f"HP: {defenseur['HP']}")

        if self.estilgagnant(defenseur):
            return self.affichageGagnant(attaquant)
        
        self.pokemonActif, self.pokemonPassif = self.pokemonPassif, self.pokemonActif
        self.affichagePokemonAttaquant(self.pokemonActif)
        return damage
    
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

    def JeuCombat(self,pokemonJoueur1,pokemonJoueur2):
        pokemonJoueur1=pokemonJoueur1.copy()
        pokemonJoueur2=pokemonJoueur2.copy()
        self.affichagePokemonCombat([pokemonJoueur1,pokemonJoueur2])
        pokemonA,pokemonB=self.premierAttaquant(pokemonJoueur1,pokemonJoueur2)
        self.pokemonActif=pokemonA
        self.pokemonPassif=pokemonB
        self.affichagePokemonAttaquant(pokemonA)
        
        pass
    ##Partie IA
    def strategieAttaqueIA(self,pokemonAtt,pokemonDef,attaquesDispo):        
        l=[]
        for attaque in attaquesDispo.index:
            l.append((attaque,self.degat(pokemonAtt,pokemonDef,attaque)))
        return max(l,key=lambda x:x[1])
    
    def choixPokemonIA(self,deck,pokemonAdv):
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
    ##Partie graphique
    
    
    def affichagePokemonRestant(self,deck):
        for i in range(len(deck)):
            pokemon=deck.iloc[i]
            image_path=self.trouverImagePokemon(pokemon)
            pil_image = Image.open(image_path)
            pil_image = pil_image.resize((50, 50), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)
            pokemon_label = tk.Label(self.root, image=tk_image)
            pokemon_label.image = tk_image  # Keep a reference to avoid garbage collection
            pokemon_label.place(x=50 + i*110, y=50)
            ##Affichage nom pokemon
            self.affichageNomPokemon(pokemon,50 + i*110,10,10)
    
    def affichageGagnant(self,pokemon):
        """Affichage du nom du pokemon gagnant"""
        nom=pokemon.name
        label_nom = tk.Label(self.root, text=f"{nom} a gagné le combat!", font=("Pokemon Solid", 20), bg="#323232", fg="white")
        label_nom.place(x=500, y=400)
        return label_nom

    ##Affichage du nom du pokemon qui attaque
    def affichagePokemonAttaquant(self,pokemon,x=600,y=50):
        """Affichage du nom du pokemon qui attaque"""
        nom=pokemon.name
        label_nom = tk.Label(self.root, text=f"{nom} attaque!", font=("Pokemon Solid", 20), bg="#323232", fg="white")
        label_nom.place(x=x, y=y)
        return label_nom
    
    ##Partie affichage pokemon
    def choixPokemonGraphique(self,deck,pokemonAdv):
        """
        Fonction permettant a l'utilisateur de choisir son pokemon via l'interface graphique
        """
    def affichagePokemonCombat(self,listePokemon):
        for i,pokemon in enumerate(listePokemon):
            
            deltaX=i*800
            deltaY=0
            image_path=self.trouverImagePokemon(pokemon)
            pil_image = Image.open(image_path)
            pil_image = pil_image.resize((400, 400), Image.Resampling.LANCZOS)
            tk_image = ImageTk.PhotoImage(pil_image)
            pokemon_label = tk.Label(self.root, image=tk_image)
            pokemon_label.image = tk_image  # Keep a reference to avoid garbage collection
            pokemon_label.place(x=100+deltaX, y=150+deltaY)
            self.affichageNomPokemon(pokemon,100+deltaX,50+deltaY,24)
            self.pointsViePokemon(pokemon,100+deltaX,90+deltaY)
            self.affichageTypePokemon(pokemon,100+deltaX,130+deltaY)
        self.affichageAttaquesDisponibles(listePokemon[0], 100, 600, listePokemon[1])
        self.affichageAttaquesDisponibles(listePokemon[1], 900, 600, listePokemon[0])


    def affichageNomPokemon(self,pokemon,x,y,size):
        nom=pokemon.name
        label_nom = tk.Label(self.root, text=nom, font=("Pokemon Solid", size), bg="#323232", fg=self.couleurPolicePokemon)
        label_nom.place(x=x, y=y)
    def pointsViePokemon(self,pokemon,x,y):
        texte=tk.StringVar()
        texte.set(f"HP: {pokemon['HP']}")
        label_hp = tk.Label(self.root, textvariable=texte, font=("Pokemon Solid", 16), bg="#323232", fg=self.couleurPolicePokemon)
        
        self.objet['hp'+pokemon.name]=(texte, label_hp)
        label_hp.place(x=x, y=y)
        return label_hp

    def affichageTypePokemon(self,pokemon,x,y):
        imageType1_path=self.trouverImageType1(pokemon)
        imageType1_path=Image.open(imageType1_path)
        tk_image1 = ImageTk.PhotoImage(imageType1_path)
        type1_label = tk.Label(self.root, image=tk_image1, bg="#323232")
        type1_label.image = tk_image1  # Keep a reference to avoid garbage collection
        type1_label.place(x=x, y=y)
        imageType2_path=self.trouverImageType2(pokemon)
        if imageType2_path:
            imageType2_path = Image.open(imageType2_path)
            tk_image2 = ImageTk.PhotoImage(imageType2_path)
            type2_label = tk.Label(self.root, image=tk_image2, bg="#323232")
            type2_label.image = tk_image2  # Keep a reference to avoid garbage collection
            type2_label.place(x=x+144, y=y)
    
    def trouverImageType1(self,pokemon):
        type=pokemon["Type 1"]
        imageType=path()+"/Photos Pokemon/Type/"+type+".png"
        return imageType
    def trouverImageType2(self,pokemon):
        type=pokemon["Type 2"]
        if isinstance(type,str):
            imageType=path()+"/Photos Pokemon/Type/"+type+".png"
        else:
            imageType=False
        return imageType

    def trouverImagePokemon(self,pokemon):
        index=self.df.loc[pokemon.name,"#"]
        pokemonName=pokemon.name.lower()
        imagePokemon=path()+"/Photos Pokemon/Pokemons/"+str(index)+"-"+pokemonName+".png"
        return imagePokemon
    
    ##Partie affichage attaques disponibles
    def affichageAttaquesDisponibles(self,pokemon,x,y,pokemon2):
        attaquesDispo=self.attaquesDisponibles(pokemon)
        for i,attaque in enumerate(attaquesDispo.index):
            if i%2==0:
                attaque_button = tk.Button(self.root, text=attaque, font=("Pokemon Solid", 14), bg="#555555", fg="black",
                                          command=lambda atk=attaque: self.faireDegats(pokemon, pokemon2, atk))
                attaque_button.place(x=x, y=y + (i//2)*50)
            else:
                attaque_button = tk.Button(self.root, text=attaque, font=("Pokemon Solid", 14), bg="#555555", fg="black",
                                          command=lambda atk=attaque: self.faireDegats(pokemon, pokemon2, atk))
                attaque_button.place(x=x + 200, y=y + (i//2)*50)
        return
##Tests

test=Pokemon("Partie Pokemon/Pokemon intranet.csv")


##test affichage jeucombat
pokemonJ1=test.deck1.iloc[0]
pokemonJ2=test.deck2.iloc[0]
test.JeuCombat(pokemonJ1,pokemonJ2)
test.root.mainloop()






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




