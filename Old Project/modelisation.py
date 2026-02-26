import tkinter as tk
import random


class Jeu():

    def __init__(self, graphique,nombre=100):
        # GRAPHIQUE :

        self.graphique = graphique  # False si on n'affiche pas la fenête graphique (qd on teste notre IA sur 100 parties)
        if self.graphique == True:
            self.fenetre = tk.Tk()

        # STRUCTURE :
        self.grille = [[[['' for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]

        # Statut de victoire pour chaque sous-grille ('', 'X' ou 'O')
        self.gagnants_sousgrilles = [['' for i in range(3)] for i in range(3)]

        # Gagnant du grand morpion
        self.gagnant = None

        # Mode de jeu :
        self.modedejeu = None  # choisi par le menu : soit JvsJ, soit JvsIA, soit IAvsIA

        self.nbcoups = 0  # utilisé dans le mode de jeu IA contre random : nb de coups de l'IA pour gagner

        # VARIABLES POUR LA REGLE DU ULTIMATE TIC TAC TOE :
        #   case dans la sous-grille qui vient d'être jouée
        self.case = None  # (ligne,col)

        #   objet graphique du contour de la case à jouer
        self.case_a_jouer = None

    # ---------------------------------------------------------------------------------------
    # VERIFICATIONS DANS LA STRUCTURE: victoires, grille pleine

    # Regarder les alignement de pions dans une grille donnée
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

    # Vérifier si une grille donnée est pleine:
    def verif_grille_pleine(self, grille):
        for ligne in grille:
            for col in ligne:
                if col == '':
                    return False  # si un élément de la grille est vide alors elle n'est pas pleine
        return True

    # --------------------------------------------------------------------------------------------------
    # MISE A JOUR DES GAGNANTS ET FIN DU JEU

    # Changer le gagnant d'une sous grille dans la structure & le graphique
    def changer_gagnant_sousgrille(self, grande_ligne, grande_col):

        # on change le gagnant graphiquement
        if self.graphique == True:
            for ligne in range(3):
                for col in range(3):
                    if self.boutons[(grande_ligne, grande_col, ligne, col)]:
                        self.boutons[(grande_ligne, grande_col, ligne, col)].destroy()
            self.canvas.create_rectangle(200 + 200 * grande_col, 100 + 200 * grande_ligne, 392 + 200 * grande_col,
                                         292 + 200 * grande_ligne, fill="light blue", outline="light blue", width=1)
            self.canvas.create_text(300 + 200 * grande_col, 200 + 200 * grande_ligne, text=self.joueur,
                                    font=("Arial", 100, "bold"), fill="blue")

        # on change le gagnant dans la structure
        self.gagnants_sousgrilles[grande_ligne][grande_col] = self.joueur

    # Mettre fin à la partie quand un joueur a gagné
    def changer_gagnant_grandegrille(self):
        self.canvas.destroy()
        self.canvasfin = tk.Canvas(self.fenetre, width=1000, height=700, bg="light blue")
        self.canvasfin.pack()
        self.canvasfin.create_text(500, 350, text=f"Félicitations !\n\nLe joueur {self.joueur} remporte la partie",
                                   font=("Times new roman", 25, "bold"), fill="black")
        self.canvasfin.create_text(500, 500, text="Cliquez sur la touche f pour fermer la fenêtre",
                                   font=("Halvetica", 10, "bold italic"), fill="red")
        self.fenetre.bind("<Key-f>", lambda event: self.fenetre.destroy())
        self.fenetre.mainloop()

    # Mettre fin à la partie quand il y a égalité sur la grande grille:
    def findujeu_egalite(self):
        if self.graphique == True:
            self.canvas.destroy()
            self.canvasfin = tk.Canvas(self.fenetre, width=1000, height=700, bg="light blue")
            self.canvasfin.pack()
            self.canvasfin.create_text(500, 350, text=f"Il y a égalité, personne ne remporte la partie",
                                       font=("Times new roman", 25, "bold"), fill="black")
            self.canvasfin.create_text(500, 500, text="Cliquez sur la touche f pour fermer la fenêtre",
                                       font=("Halvetica", 10, "bold italic"), fill="red")
            self.fenetre.bind("<Key-f>", lambda event: self.fenetre.destroy())
            self.fenetre.mainloop()

    # -------------------------------------------------------------------------------------------
    # JOUER : changements dans la structure

    # Changer le tour : passer de 'X' à 'O', prenant en compte le mode de jeu
    def changer_tour(self):
            if self.joueur == self.IA:
                self.joueur = self.random
                self.ia_random()
            else:
                self.joueur = self.IA
                self.ia()

    # Placer le joueur dans la structure, appel des méthodes précédentes:
    # - jouer graphiquement
    # - vérifications de grille pleine ou gagnée
    # - changer le tour de jeu
    def jouer(self, grande_ligne, grande_col, ligne, col):

        # on place le joueur dans la structure
        self.grille[grande_ligne][grande_col][ligne][col] = self.joueur

        # vérification de victoire locale
        if self.verif_victoire(self.grille[grande_ligne][grande_col]) == True:
            self.gagnants_sousgrilles[grande_ligne][grande_col] = self.joueur
            self.changer_gagnant_sousgrille(grande_ligne, grande_col)

        # vérification de victoire globale
        if self.verif_victoire(self.gagnants_sousgrilles):
            self.gagnant = self.joueur
            if self.graphique == True:
                self.changer_gagnant_grandegrille()
            return True  # permet à la fonction jouer() de s'arrêter, pour ne pas dessiner d'encadrement ensuite

        # vérification de grille pleine dans la grande grille:
        if self.verif_grille_pleine(self.gagnants_sousgrilles):
            # le jeu est fini est personne ne gagne
            self.findujeu_egalite()
            return True  # permet à la fonction jouer() de s'arrêter, pour ne pas dessiner d'encadrement ensuite

        # on retient la case qui vient d'être jouée pour obliger le suivant à y jouer
        self.case = (ligne, col)

        # changement de tour
        self.changer_tour()


    # Vérifier si la case est jouable selon les règles ultimate tic tac toe :
    def test_jouer(self, gl, gc, l, c):

        if self.grille[gl][gc][l][c] == '':

            # Le joueur peut joueur où il veut dans les cas suivants:
            # SI c'est le premier tour OU la case où il doit jouer est gagnée OU la case où il doit jouer est pleine
            if self.case == None or self.gagnants_sousgrilles[self.case[0]][
                self.case[1]] != '' or self.verif_grille_pleine(self.grille[self.case[0]][self.case[1]]) == True:
                # il peut jouer où il veut sauf dans une grille gagnée ni une grille pleine:
                if self.gagnants_sousgrilles[gl][gc] == '' and self.verif_grille_pleine(self.grille[gl][gc]) == False:
                    self.jouer(gl, gc, l, c)
                    return True

            # sinon: il a une obligation de jeu : ne peut jouer que dans self.case

            elif (gl, gc) == self.case:
                self.jouer(gl, gc, l, c)
                return True

        return False

    # ------------------------------------------------------------------------------------------------
    # CODE DE LA STRATEGIE DE L'IA ET DE L'ALGO RANDOM

    # Random : joue aléatoirement
    def ia_random(self):

        if self.joueur == self.random:  # on vérifie que c'est bien à son tour
            if self.case == None:  # si le random joue en premier

                gl = random.randint(0, 2)
                gc = random.randint(0, 2)
                l = random.randint(0, 2)
                c = random.randint(0, 2)
                self.test_jouer(gl, gc, l, c)
                return True

            # On essaie d'abord de jouer dans la case obligée:

            gl = self.case[0]
            gc = self.case[1]
            petites_cases = [(l, c) for l in range(3) for c in range(3)]  # ensemble des cases possibles
            random.shuffle(petites_cases)  # on change l'orde aléatoirement
            for (l, c) in petites_cases:
                succes = self.test_jouer(gl, gc, l, c)
                if succes == True:
                    return True  # la fonction s'arrête: c'est à l'autre de jouer

            # Si on ne peut pas, on joue aléatoirement en testant tout:

            grandes_cases = [(l, c) for l in range(3) for c in range(3)]  # ensemble des sous-grilles possibles
            random.shuffle(grandes_cases)  # on change l'orde aléatoirement

            for grande_grille in grandes_cases:
                petites_cases = [(l, c) for l in range(3) for c in range(3)]  # ensemble des cases possibles
                random.shuffle(petites_cases)  # on change l'orde aléatoirement
                for (l, c) in petites_cases:
                    succes = self.test_jouer(grande_grille[0], grande_grille[1], l, c)

                    if succes == True:
                        return True  # la fonction s'arrête: c'est à l'autre de jouer

    def ia(self):

        if self.joueur == self.IA:  # on vérifie que c'est bien son tour
            # Si on est au début de la partie on jouer au milieu
            if self.case == None:
                self.test_jouer(1, 1, 1, 1)
                self.nbcoups += 1
                return True

            # Sinon : stratégie --> Pour l'instant, l'ia joue aléatoirement

            # On essaie d'abord de jouer dans la case obligée
            else:
                gl = self.case[0]
                gc = self.case[1]
                petites_cases = [(l, c) for l in range(3) for c in range(3)]  # ensemble des cases possibles
                random.shuffle(petites_cases)  # on change l'orde aléatoirement
                for (l, c) in petites_cases:
                    succes = self.test_jouer(gl, gc, l, c)

                    if succes == True:
                        self.nbcoups += 1
                        return True  # la fonction s'arrête: c'est à l'autre de jouer

                # Si on ne peut pas, on joue aléatoirement et partout
                grandes_cases = [(l, c) for l in range(3) for c in range(3)]  # ensemble des sous-grilles possibles
                random.shuffle(grandes_cases)  # on change l'orde aléatoirement

                for grande_grille in grandes_cases:
                    petites_cases = [(l, c) for l in range(3) for c in range(3)]  # ensemble des cases possibles
                    random.shuffle(petites_cases)  # on change l'orde aléatoirement
                    for (l, c) in petites_cases:
                        succes = self.test_jouer(grande_grille[0], grande_grille[1], l, c)
                        if succes == True:
                            self.nbcoups += 1
                            return True  # la fonction s'arrête: c'est à l'autre de jouer

    # -------------------------------------------------------------------------------------------
    # MODELISATION DE X PARTIES

    # Mode IA VS random:
    def modelisation(self, x):  # x le nombre de parties

        self.modedejeu = 'IAvsIA'

        nbgains_ia = 0  # nb de parties gagnées
        nb_egalites = 0  # nb parties à égalité
        coups = []  # tableau composé du nb de coups de l'IA à chaque partie gagnée

        # changements graphiques

        self.canvasmodel = tk.Canvas(self.fenetre, width=1000, height=700, bg="light green")
        self.canvasmodel.pack()
        txt_accueil = self.canvasmodel.create_text(500, 350,
                                                   text=f"Une modélisation de {x} parties est faite entre l'IA et un algorithme aléatoire",
                                                   font=("Times new roman", 20, "bold"), fill="black")
        self.fenetre.update()  # mette à jour la fenêtre avec le texte

        # Réalisation des x parties

        for partie in range(x):

            # Initialisation et lancement de la partie:
            jeu = Jeu(False)
            jeu.IA = random.choice(['X', 'O'])
            jeu.modedejeu = 'IAvsIA'
            if jeu.IA == 'X':
                jeu.joueur = jeu.IA
                jeu.random = 'O'  # robot random qui joue contre l'IA
                jeu.ia()
            else:
                jeu.random = 'X'
                jeu.joueur = jeu.random
                jeu.ia_random()
            # On garde les résultats de la partie:
            if jeu.gagnant == jeu.IA:
                nbgains_ia += 1
                coups.append(jeu.nbcoups)
            if jeu.gagnant == None:
                nb_egalites += 1

            self.fenetre.update()  # mette à jour la fenêtre avec le texte
        # Nb de coups moyens:
        if len(coups) != 0:
            moycoups = round(sum(coups) / len(coups), 2)

        # Fenêtre d'annonce des résultats:
        self.canvasmodel.delete(txt_accueil)

        self.canvasmodel.create_text(500, 150,
                                     text=f"Une modélisation de {x} parties à été faite entre l'IA et un algorithme aléatoire",
                                     font=("Times new roman", 20, "bold"), fill="black")
        if len(coups) != 0:
            self.canvasmodel.create_text(500, 300,
                                         text=f"L'IA a gagné {nbgains_ia} parties, avec en moyenne {moycoups} coups",
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


