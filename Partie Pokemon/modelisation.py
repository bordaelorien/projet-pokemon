import tkinter as tk
import random
import deck_builder as db
import data_loader as dl
from MCTS import MCTS
from affichageCombatIAvsIA import combatIAvsIA
from paths import *


class IAVSIA:

    def __init__(self):
        # GRAPHIQUE :
        self.fenetre = tk.Tk()

        # STRUCTURE :
        self.grille = [[[['' for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]

        # Statut de victoire pour chaque sous-grille ('', 'X' ou 'O')
        self.gagnants_sousgrilles = [['' for i in range(3)] for i in range(3)]

        # Gagnant du grand morpion
        self.gagnant = None

        self.nbcoups = 0  # utilisé dans le mode de jeu IA contre random : nb de coups de l'IA pour gagner

        # VARIABLES POUR LA REGLE DU ULTIMATE TIC TAC TOE :
        #   case dans la sous-grille qui vient d'être jouée
        self.case = None  # (ligne,col)

        # VARIABLES POUR LA PARTIE POKEMONS:
        # place des pokemons:
        self.pokemons_places = [[[[None for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]

        # deck :
        self.deck1, self.deck2 = db.decks(dl.dfPokemon(), deck_size=100)
        self.matriceAdj = dl.dfMatriceAdjacence()


    # ---------------------------------------------------------------------------------------
    # REINITIALISATION A LA FIN D'UNE PARTIE

    def reinitialiser(self):
        self.grille = [[[['' for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
        self.gagnants_sousgrilles = [['' for i in range(3)] for i in range(3)]
        self.gagnant = None
        self.nbcoups = 0
        self.case = None
        self.pokemons_places = [[[[None for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
        self.deck1, self.deck2 = db.decks(dl.dfPokemon(), deck_size=100)

    # ---------------------------------------------------------------------------------------
    # VERIFICATIONS DANS LA STRUCTURE: victoires, grille pleine

    def verif_victoire(self, grille):
        # Vérification des lignes
        for i in range(3):
            if grille[i][0] == self.joueur and grille[i][1] == self.joueur and grille[i][2] == self.joueur:
                return True

        # Vérification des colonnes
        for j in range(3):
            if grille[0][j] == self.joueur and grille[1][j] == self.joueur and grille[2][j] == self.joueur:
                return True

        # Vérification diagonale principale
        if grille[0][0] == self.joueur and grille[1][1] == self.joueur and grille[2][2] == self.joueur:
            return True

        # Vérification diagonale secondaire
        if grille[0][2] == self.joueur and grille[1][1] == self.joueur and grille[2][0] == self.joueur:
            return True
        if len(self.deck1)==0 or len(self.deck2)==0:
            print("Un des decks est vide")
            return -1
        return False

    # Vérifier si une grille donnée est pleine:
    def verif_grille_pleine(self, grille):
        for ligne in grille:
            for col in ligne:
                if col == '':
                    return False  # si un élément de la grille est vide alors elle n'est pas pleine
        return True

    # -------------------------------------------------------------------------------------------
    # JOUER : changements dans la structure

    def jouer(self, gl, gc, l, c, pokemon=None):
        """Place un pion ou un pokémon sur la case choisie selon les règles du jeu.
        Vérifie si il y a match nul ou victoire.
        Change le joueur actuel."""

        #si il n'y a pas de pokémon sur la case, placement simple
        if self.pokemons_places[gl][gc][l][c] == None:
            self.pokemons_places[gl][gc][l][c] = (self.joueur, pokemon, pokemon["#"])
            self.grille[gl][gc][l][c] = self.joueur
        
        #si il y en a un, on commence un combat avec le pokémon de l'adversaire
        else:
            self.initierCombat(gl, gc, l, c)
        
        
        #verification victoire locale
        if self.verif_victoire(self.grille[gl][gc]) == True:
            self.gagnants_sousgrilles[gl][gc] = self.joueur
        
        #verification match nul local
        elif self.verif_grille_pleine(self.grille[gl][gc]) == True:
            self.gagnants_sousgrilles[gl][gc] = "Nul"

        #verification victoire globale
        if self.verif_victoire(self.gagnants_sousgrilles) == True:
            self.gagnant = self.joueur

        #verification match nul global
        elif self.verif_grille_pleine(self.gagnants_sousgrilles) == True:
            self.gagnant = "Nul"

        # on retient la case qui vient d'être jouée pour obliger le suivant à y jouer
        self.case = (l, c)

        #changement de joueur
        if self.joueur == "X":
            self.joueur = "O"
        else:
            self.joueur = "X"

    # ------------------------------------------------------------------------------------------------
    # CODE DE LA STRATEGIE DE L'IA ET DE L'ALGO RANDOM

    # Random : joue aléatoirement
    def IARandomDecision(self):
        # Construction de la liste des coups possibles
        coups_possibles = []

        # Détermination des sous-grilles autorisées
        #Si c'est le premier tour OU la sous_grille ou elle doit jouer est gagnée ou pleine...
        if self.case == None or self.gagnants_sousgrilles[self.case[0]][self.case[1]] != "":
            #...l'IA peut jouer dans n'importe quelle sous-grille non gagnée et non pleine
            sous_grilles = [(gl, gc) for gl in range(3) for gc in range(3) if self.gagnants_sousgrilles[gl][gc] == ""]
        else:
            sous_grilles = [self.case]

        # Pour chaque sous-grille autorisée, on regarde les cases encore disponibles
        for gl, gc in sous_grilles:
            for l in range(3):
                for c in range(3):
                    #si la case est vide on peut jouer dessus
                    if self.grille[gl][gc][l][c] == "" and self.pokemons_places[gl][gc][l][c] == None:
                        coups_possibles.append((gl, gc, l, c))
                    # On ne joue pas sur une case déjà résolue (valeur -1) ou sur une case où on a déjà placé un pokemon
                    elif self.pokemons_places[gl][gc][l][c] != -1 and self.pokemons_places[gl][gc][l][c][0] != self.joueur:
                        coups_possibles.append((gl, gc, l, c))
        
        coup = random.choice(coups_possibles)
        pokemon = self.pokemonChoisiRandom(self.joueur)
        return (coup, pokemon)

    def IAOptiDecision(self):
        # Si on est au début de la partie on jouer au milieu
        if self.case == None:
            return ((1, 1, 1, 1), self.pokemonChoisiRandom(self.joueur))
        # Sinon : stratégie
        coup = MCTS(self.grille, self.gagnants_sousgrilles, self.pokemons_places, self.joueur, self.case)
        (gl, gc, l, c) = coup
        #si la case est vide on met un pokemon au hasard
        if self.pokemons_places[gl][gc][l][c] == None:
            
            pokemon = self.pokemonChoisiRandom(self.joueur)
        #si la case est occupée par un pokémon adverse on choisit un pokémon qui va le contrer
        elif self.pokemons_places[gl][gc][l][c] != self.joueur:
            
            pokemon = self.pokemonChoisiOpti(self.joueur, self.pokemons_places[gl][gc][l][c][1])
        return (coup, pokemon)
    

    def initierCombat(self, gl, gc, l, c):
        """IA contre IA"""  
        pokemon1=self.pokemons_places[gl][gc][l][c][1]
        gagnant=combatIAvsIA(pokemon1,self.pokemonChoisiOpti(self.joueur,pokemon1))
        if gagnant["#"]==pokemon1["#"]:
            if self.joueur=="X":
                self.pokemons_places[gl][gc][l][c]=("O",pokemon1,pokemon1["#"])
            else:
                self.pokemons_places[gl][gc][l][c]=("X",pokemon1,pokemon1["#"])
        else:
            self.pokemons_places[gl][gc][l][c]=(self.joueur,gagnant,gagnant["#"])

    def pokemonChoisiOpti(self, joueur, pokemon_adverse):
        """renvoie un pokémon du deck du joueur de type opposé à celui du pokemon adverse"""
        if joueur == "X":
            deck = self.deck1
        else:
            deck = self.deck2
        if len(deck) == 0:
            return None
        type1adverse=pokemon_adverse["Type 1"]
        type2adverse=pokemon_adverse["Type 2"]
        bestTypes=[]
        
        bestType1=self.matriceAdj[self.matriceAdj[type1adverse]>1].index.tolist()
        bestTypes=bestType1
    
        if isinstance(type2adverse,str):
            bestType2=self.matriceAdj[self.matriceAdj[type2adverse]>1].index.tolist()
            bestTypes=bestType1+bestType2
            possiblePokemons=deck[(deck["Type 1"].isin(bestTypes) | deck["Type 2"].isin(bestTypes)) & (deck["Total"]>=pokemon_adverse["Total"])]
        else:
            possiblePokemons=deck[(deck["Type 1"].isin(bestTypes)) & (deck["Total"]>=pokemon_adverse["Total"])]
        if len(possiblePokemons)>0:
            idx = random.choice(possiblePokemons.index.tolist())
            return possiblePokemons.loc[idx]
        else:
            possiblePokemons=deck[(deck["Type 1"].isin(bestTypes) | deck["Type 2"].isin(bestTypes))].sort_values(by="Total",ascending=False)
            if len(possiblePokemons)==0:
                possiblePokemons=deck[(deck["Total"]>=pokemon_adverse["Total"])]
                if len(possiblePokemons)==0:
                    idx = random.choice(deck.index.tolist())
                    return deck.loc[idx]
                idx = random.choice(possiblePokemons.index.tolist())
                return possiblePokemons.loc[idx]
            return possiblePokemons.loc[possiblePokemons.index[0]]
    

        pass
    
    
    def pokemonChoisiRandom(self, joueur):
        """
        Retourne un Pokémon aléatoire du deck et le retire du deck.
        """
        if joueur == "X":
            deck = self.deck1
        else:
            deck = self.deck2
        
        if len(deck) == 0:
            return None
        
        idx = random.choice(deck.index.tolist())
        pokemon = deck.loc[idx]
        deck.drop(deck[deck["#"] == pokemon["#"]].index, inplace=True)
        return pokemon

    # -------------------------------------------------------------------------------------------
    # MODELISATION DE X PARTIES

    # Mode IA VS random:
    def modelisation(self, x):  # x le nombre de parties

        nbgains_iaopti = 0  # nb de parties gagnées par l'IA opti
        nb_egalites = 0  # nb parties à égalité
        coups = []  # tableau composé du nb de coups de l'IA opti à chaque partie gagnée

        # changements graphiques

        self.canvasmodel = tk.Canvas(self.fenetre, width=1000, height=700, bg="light green")
        self.canvasmodel.pack()

        # Réalisation des x parties

        for partie in range(x):
            print(f"Partie {partie + 1} sur {x}")
            # Initialisation et lancement de la partie:
            self.IAOpti = random.choice(['X', 'O'])
            if self.IAOpti == 'X':
                self.joueur = self.IAOpti
                self.IARandom = 'O'  # robot random qui joue contre l'IA
            else:
                self.IARandom = 'X'
                self.joueur = self.IARandom
            
            #déroulement de la partie
            while self.gagnant == None:
                if self.joueur == self.IAOpti:
                    
                    (coup, pokemon) = self.IAOptiDecision()
                    self.nbcoups += 1
                else:
                    
                    (coup, pokemon) = self.IARandomDecision()
                self.jouer(*coup, pokemon)

            # On garde les résultats de la partie:
            print(self.gagnant == self.IAOpti)
            if self.gagnant == self.IAOpti:
                nbgains_iaopti += 1
                coups.append(self.nbcoups)

            if self.gagnant == "Nul":
                nb_egalites += 1

            self.reinitialiser()

        # Nb de coups moyens:
        if len(coups) != 0:
            moycoups = round(sum(coups) / len(coups), 2)

        # annonce des résultats:

        self.canvasmodel.create_text(500, 150,
                                     text=f"Une modélisation de {x} parties à été faite entre l'IA et un algorithme aléatoire",
                                     font=("Times new roman", 20, "bold"), fill="black")
        if len(coups) != 0:
            self.canvasmodel.create_text(500, 300,
                                         text=f"L'IA a gagné {nbgains_iaopti} parties, avec en moyenne {moycoups} coups",
                                         font=("Halvetica", 20, "bold"), fill="black")
            self.canvasmodel.create_text(500, 350,
                                         text=f"\nIl y a eu {nb_egalites} parties à égalité",
                                         font=("Halvetica", 15, "bold"), fill="black")

        else:
            self.canvasmodel.create_text(500, 300,
                                         text=f"L'IA n'a gagné aucune partie \n Il y a eu {nb_egalites} partie à égalité ",
                                         font=("Halvetica", 20, "bold "), fill="black")
        self.canvasmodel.create_text(500, 500, text=f" Cliquez sur la touche f pour fermer",
                                     font=("Halvetica", 10, "bold italic"), fill="green")
        self.fenetre.bind("<Key-f>", lambda event: self.fenetre.destroy())
        self.fenetre.mainloop()
