from math import sqrt, log
import random
from copy import deepcopy

class Plateau:
    """état du plateau de jeu"""

    def __init__(self, grille, gagnantsSousGrilles, pokemons_places, joueur, case):
        self.grille = deepcopy(grille) #grande grille, matrice 9x9
        self.gagnantsSousGrilles = deepcopy(gagnantsSousGrilles) #statut de victoire pour chaque sous-grille
        self.pokemons_places = deepcopy(pokemons_places) #matrice qui contient les positions des pokemons dans la grille
        self.joueur = joueur #joueur actuel
        self.case = case #coordonnées (l,c) de la case qui vient d'être sélectionnée dans sa sous-grille
        self.gagnant = None #gagnant de la partie

    def coupsPossibles(self):
        """Renvoie une liste de tous les coups possibles dans ce plateau"""
        # Construction de la liste des coups possibles
        coups_possibles = []

        # Détermination des sous-grilles autorisées
        #Si c'est le premier tour OU la sous_grille ou elle doit jouer est gagnée ou pleine...
        if self.case == None or self.gagnantsSousGrilles[self.case[0]][self.case[1]] != "":
            #...l'IA peut jouer dans n'importe quelle sous-grille non gagnée et non pleine
            sous_grilles = [(gl, gc) for gl in range(3) for gc in range(3) if self.gagnantsSousGrilles[gl][gc] == ""]
        else:
            sous_grilles = [self.case]

        # Pour chaque sous-grille autorisée, on regarde les cases encore disponibles
        for gl, gc in sous_grilles:
            for l in range(3):
                for c in range(3):
                    # On ne joue pas sur une case déjà résolue (valeur -1) ou sur une case où on a déjà placé un pokemon
                    if self.pokemons_places[gl][gc][l][c] == None:
                        coups_possibles.append((gl, gc, l, c))
                    
                    elif self.pokemons_places[gl][gc][l][c] != -1 and self.pokemons_places[gl][gc][l][c][0] != self.joueur:
                        coups_possibles.append((gl, gc, l, c))

        return coups_possibles
    
    def jouer(self, gl, gc, l, c):
        """Place un pion ou un pokémon sur la case choisie selon les règles du jeu.
        Vérifie si il y a match nul ou victoire.
        Change le joueur actuel."""

        #si il n'y a pas de pokémon sur la case, placement simple
        if self.pokemons_places[gl][gc][l][c] == None:
            self.pokemons_places[gl][gc][l][c] = (self.joueur, None, None) #pas besoin de spécifier le pokémon
        
        #si il y en a un, on considère que le joueur remporte automatiquement le combat contre l'adversaire
        #pour simplifier l'IA
        else:
            self.pokemons_places[gl][gc][l][c] = -1
            self.grille[gl][gc][l][c] = self.joueur
        
        # Verifications victoire locale
        if self.verif_victoire(self.grille[gl][gc]) == True:
            self.gagnantsSousGrilles[gl][gc] = self.joueur
        
        #verification match nul local
        elif self.verif_grille_pleine(self.grille[gl][gc]) == True:
            self.gagnantsSousGrilles[gl][gc] = "Nul"

        #verification victoire globale
        if self.verif_victoire(self.gagnantsSousGrilles) == True:
            self.gagnant = self.joueur

        #verification match nul global
        elif self.verif_grille_pleine(self.gagnantsSousGrilles) == True:
            self.gagnant = "Nul"

        # on retient la case qui vient d'être jouée pour obliger le suivant à y jouer
        self.case = (l, c)

        #changement de joueur
        if self.joueur == "X":
            self.joueur == "O"
        else:
            self.joueur == "X"

    def verif_victoire(self, grille):
        """Renvoie True si le joueur actuel est le gagnant sur la grille/sous-grille"""
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
        
    def verif_grille_pleine(self, grille):
        """Renvoie True si la grille est pleine"""
        for ligne in grille:
            for case in ligne:
                if case == "":
                    return False  # si un élément de la grille est vide alors elle n'est pas pleine
        return True
        
    def copie(self):
        return Plateau(self.grille, self.gagnantsSousGrilles, self.pokemons_places, self.joueur, self.case)


#--------------------------------------------------------------------------------------------------------------------------------


class Noeud:

    def __init__(self, plateau, parent=None, coup_precedent=None):
        self.plateau = plateau
        self.parent = parent
        self.enfants = [] 
        self.score = 0 
        self.visites = 0            

    def expansion(self):
        """Ajoute des enfants au noeud (toutes les positions valides atteignables à partir de ce noeud)"""
        coups_possibles = self.plateau.coupsPossibles()
        for coup in coups_possibles:
            plateau_enfant = self.plateau.copie()
            plateau_enfant.jouer(*coup)
            enfant = Noeud(plateau_enfant, parent=self, coup_precedent=coup)
            self.enfants.append(enfant)
    
    def simulation(self):
        """Simule une partie aléatoire à partir du noeud.
        Renvoie le gagnant de la partie ('Nul' si il y a match nul)"""

        plateau = self.plateau.copie()

        while plateau.gagnant == None:
            coups_possibles = plateau.coupsPossibles()
            coup = random.choice(coups_possibles)
            plateau.jouer(*coup)

        return plateau.gagnant

    def backpropagation(self, resultat):
        """Met à jour les scores des noeuds précédents en fonction du résultat de la simulation"""
        self.visites += 1       
        self.score += resultat
        if self.parent: 
            self.parent.backpropagation(resultat)

    def scoreUCB1(self, c):
        if self.visites > 0:
            return (self.score/self.visites) + c*sqrt(log(self.parent.visites)/self.visites)
        else:
            return c*sqrt(log(self.parent.visites))
        
    def meilleurEnfant(self, c):
        """Renvoie l'enfant avec le meilleur score UCB1. Utile pour l'étape de sélection."""
        meilleur_enfant = self.enfants[0]
        for enfant in self.enfants:
            if enfant.scoreUCB1(c) > meilleur_enfant.scoreUCB1(c):
                meilleur_enfant = enfant
        return meilleur_enfant
    
    def pireEnfant(self, c):
        """Renvoie l'enfant avec le pire score UCB1. Utile pour l'étape de sélection."""
        pire_enfant = self.enfants[0]
        for enfant in self.enfants:
            if enfant.scoreUCB1(c) < pire_enfant.scoreUCB1(c):
                pire_enfant = enfant
        return pire_enfant
    
    def estFinal(self):
        if self.plateau.gagnant != None:
            return True


#----------------------------------------------------------------------------------------------------------------------------------


def MCTS(grille, gagnantsSousGrilles, pokemons_places, joueur, case, iterations=100, c=sqrt(2)):
    """Algorithme de recherche de Monte Carlo. Renvoie le coup que l'IA va jouer."""

    plateau_racine = Plateau(grille, gagnantsSousGrilles, pokemons_places, joueur, case)
    racine = Noeud(plateau_racine)

    for i in range(iterations):
        noeud = racine

        #sélection
        while not noeud.estFinal() and len(noeud.enfants) > 0:
            if noeud.plateau.joueur == joueur:
                noeud = noeud.meilleurEnfant(c)
            else:
                noeud = noeud.pireEnfant(c)
        
        #expansion
        if not noeud.estFinal():
            noeud.expansion()
            noeud = random.choice(noeud.enfants)

        #simulation
        gagnant = noeud.simulation()
        if gagnant == "Nul":
            resultat = 0.5
        elif gagnant == joueur:
            resultat = 1
        else:
            resultat = 0
        
        #backpropagation
        noeud.backpropagation(resultat)

    #on renvoie le meilleur coup
    return racine.meilleurEnfant(c=0).coup_precedent