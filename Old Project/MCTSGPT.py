from math import sqrt, log
import random
from copy import deepcopy

# ============================================================
#                        PLATEAU
# ============================================================

class Plateau:
    """État du plateau de jeu pour l'Ultimate Tic-Tac-Toe Pokémon."""

    def __init__(self, grille, gagnantsSousGrilles, pokemons_places, joueur, case):
        self.grille = deepcopy(grille)
        self.gagnantsSousGrilles = deepcopy(gagnantsSousGrilles)
        self.pokemons_places = deepcopy(pokemons_places)
        self.joueur = joueur
        self.case = case
        self.gagnant = None

    # ---------------------------------------------------------
    # Détermine si une case appartient au joueur
    # ---------------------------------------------------------
    def _case_appartient_joueur(self, gl, gc, l, c):
        cell = self.pokemons_places[gl][gc][l][c]

        if cell == -1:
            return True
        if isinstance(cell, tuple) and cell[0] == self.joueur:
            return True
        return False

    # ---------------------------------------------------------
    # Vérifie les alignements 3-en-ligne avec la règle Pokémon
    # ---------------------------------------------------------
    def verif_victoire_pokemon(self, gl, gc):
        """Un alignement complet de cases appartenant au joueur ⇒ victoire."""

        # Lignes
        for i in range(3):
            if all(self._case_appartient_joueur(gl, gc, i, col) for col in range(3)):
                return True

        # Colonnes
        for col in range(3):
            if all(self._case_appartient_joueur(gl, gc, row, col) for row in range(3)):
                return True

        # Diagonale principale
        if all(self._case_appartient_joueur(gl, gc, d, d) for d in range(3)):
            return True

        # Diagonale secondaire
        if all(self._case_appartient_joueur(gl, gc, d, 2 - d) for d in range(3)):
            return True

        return False

    # ---------------------------------------------------------

    def coupsPossibles(self):
        coups = []

        # Détermine les sous-grilles autorisées
        if self.case is None or self.gagnantsSousGrilles[self.case[0]][self.case[1]] != "":
            sous_grilles = [
                (gl, gc)
                for gl in range(3)
                for gc in range(3)
                if self.gagnantsSousGrilles[gl][gc] == ""
            ]
        else:
            sous_grilles = [self.case]

        # Cases jouables
        for gl, gc in sous_grilles:
            for l in range(3):
                for c in range(3):
                    cell = self.pokemons_places[gl][gc][l][c]
                    if cell is None:
                        coups.append((gl, gc, l, c))
                    elif cell != -1 and cell[0] != self.joueur:
                        coups.append((gl, gc, l, c))

        return coups

    # ---------------------------------------------------------

    def verif_grille_pleine(self, grille):
        for row in grille:
            for cell in row:
                if cell == "":
                    return False
        return True

    # ---------------------------------------------------------

    def verif_victoire(self, grille):
        j = self.joueur

        # Lignes
        for i in range(3):
            if grille[i][0] == j and grille[i][1] == j and grille[i][2] == j:
                return True

        # Colonnes
        for col in range(3):
            if grille[0][col] == j and grille[1][col] == j and grille[2][col] == j:
                return True

        # Diagonales
        if grille[0][0] == j and grille[1][1] == j and grille[2][2] == j:
            return True
        if grille[0][2] == j and grille[1][1] == j and grille[2][0] == j:
            return True

        return False

    # ---------------------------------------------------------

    def jouer(self, gl, gc, l, c):
        cell = self.pokemons_places[gl][gc][l][c]

        # Combat ?
        est_combat = (cell is not None) and (cell != -1) and (cell[0] != self.joueur)

        # Placement
        if cell is None:
            self.pokemons_places[gl][gc][l][c] = (self.joueur, None, None)
            self.grille[gl][gc][l][c] = self.joueur

        # Combat
        elif est_combat:
            self.pokemons_places[gl][gc][l][c] = -1
            self.grille[gl][gc][l][c] = self.joueur

        # ------------------------------------------------------
        # Victoire locale (règle Pokémon avec alignement)
        if self.verif_victoire_pokemon(gl, gc):
            self.gagnantsSousGrilles[gl][gc] = self.joueur

        # Match nul local
        elif self.verif_grille_pleine(self.grille[gl][gc]):
            self.gagnantsSousGrilles[gl][gc] = "Nul"

        # ------------------------------------------------------
        # Victoire globale
        if self.verif_victoire(self.gagnantsSousGrilles):
            self.gagnant = self.joueur
        elif self.verif_grille_pleine(self.gagnantsSousGrilles):
            self.gagnant = "Nul"

        # Prochaine sous-grille
        self.case = (l, c)

        # Changement de joueur
        self.joueur = "O" if self.joueur == "X" else "X"

    # ---------------------------------------------------------

    def copie(self):
        return Plateau(self.grille, self.gagnantsSousGrilles, self.pokemons_places, self.joueur, self.case)


# ============================================================
#                        NOEUD MCTS
# ============================================================

class Noeud:
    def __init__(self, plateau, parent=None, coup_precedent=None):
        self.plateau = plateau
        self.parent = parent
        self.coup_precedent = coup_precedent
        self.enfants = []
        self.score = 0
        self.visites = 0

    def estFinal(self):
        return self.plateau.gagnant is not None

    def expansion(self):
        if self.enfants:
            return
        for coup in self.plateau.coupsPossibles():
            p = self.plateau.copie()
            p.jouer(*coup)
            self.enfants.append(Noeud(p, self, coup))

    def simulation(self):
        plateau = self.plateau.copie()

        while plateau.gagnant is None:
            coups = plateau.coupsPossibles()
            if not coups:
                plateau.gagnant = "Nul"
                break
            plateau.jouer(*random.choice(coups))

        return plateau.gagnant

    def backpropagation(self, resultat):
        self.visites += 1
        self.score += resultat
        if self.parent is not None:
            self.parent.backpropagation(resultat)

    def scoreUCB1(self, c):
        if self.visites == 0:
            return float("inf")
        return (self.score / self.visites) + c * sqrt(log(self.parent.visites) / self.visites)

    def meilleurEnfant(self, c):
        return max(self.enfants, key=lambda e: e.scoreUCB1(c))

    def pireEnfant(self, c):
        return min(self.enfants, key=lambda e: e.scoreUCB1(c))


# ============================================================
#                            MCTS
# ============================================================

def MCTS(grille, gagnantsSousGrilles, pokemons_places, joueur, case, iterations=300, c=sqrt(2)):
    racine = Noeud(Plateau(grille, gagnantsSousGrilles, pokemons_places, joueur, case))

    for _ in range(iterations):
        noeud = racine

        # Sélection
        while not noeud.estFinal() and noeud.enfants:
            noeud = (
                noeud.meilleurEnfant(c)
                if noeud.plateau.joueur == joueur
                else noeud.pireEnfant(c)
            )

        # Expansion
        if not noeud.estFinal():
            noeud.expansion()
            if noeud.enfants:
                noeud = random.choice(noeud.enfants)

        # Simulation
        gagnant = noeud.simulation()

        if gagnant == "Nul":
            resultat = 0.5
        elif gagnant == joueur:
            resultat = 1
        else:
            resultat = 0

        # Backpropagation
        noeud.backpropagation(resultat)

    # Exploitation pure
    return racine.meilleurEnfant(c=0).coup_precedent
