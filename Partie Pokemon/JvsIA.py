
import tkinter as tk
import deck_builder as db
import data_loader as dl
from paths import *
from tkinter import ttk
from PIL import Image, ImageTk
from affichageCombatJvsIA import PokemonJVSIA
import pandas as pd
import random
import MCTS


class JoueurVSIA():

    def __init__(self, nbrePokemons=60):
        # GRAPHIQUE :
        self.fenetre = tk.Tk()
        self.canvas = tk.Canvas(self.fenetre, width=1920, height=1080, bg="light blue")
        self.canvas.pack()

        # STRUCTURE :

        self.grille = [[[['' for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]

        # Statut de victoire pour chaque sous-grille (None, 'X' ou 'O')
        self.gagnantsSousGrilles = [['' for i in range(3)] for i in range(3)]

        # Gagnant du grand morpion
        self.gagnant = None

        # Joueur actuel, initialié à X
        self.joueur = 'X'
        self.humain = 'X'
        self.IA = 'O'
        self.coupsJoueurX = []

        # Annonce graphique du joueur en cours
        self.annonce_joueur = self.canvas.create_text(500, 20, text="Placer votre Pokemon pour commencer",
                                                      font=("Times new roman", 15, "bold"), fill="black")

        # VARIABLES POUR LA REGLE DU ULTIMATE TIC TAC TOE :
        #   case dans la sous-grille qui vient d'être jouée
        self.case = None  # (ligne,col)

        #   objet graphique du contour de la case à jouer
        self.case_a_jouer = None

        # POKEMON :
        self.pokemons_places = [[[[None for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
        self.nbrePokemons=nbrePokemons
        self.deck1, self.deck2 = db.decks(dl.dfPokemon(), self.nbrePokemons)
        self.matriceAdj = dl.dfMatriceAdjacence()

        # BOUTONS Pokemon:
        self.bouton_deck()
        self.afficherDecks()

        self.pokeChoisiDeck1 = None
        self.pokeChoisiDeck2 = None
        self.color = None
        self.dessiner_lignes()
        self.cases()
        self.afficher()
        self.fenetre.mainloop()

    # ---------------------------------------------------------------------------------------------------------------------
    # Partie Pokemons:

    def tailleImage(self, path, sizeX, sizeY):
        """
        Redimensionne une image à une taille donnée et la convertit en PhotoImage pour Tkinter.
        """
        try:
            image = Image.open(path)
            image = image.resize((sizeX, sizeY), Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except:
            return None

    def bouton_deck(self):
        """
        Crée les labels pour les decks des joueurs et les Pokémon sélectionnés.
        """
        label_deck = tk.Label(self.fenetre, text="Votre Deck", bg="light blue", fg="red", font=("Arial", 16, "bold"))
        label_deck.place(x=950, y=10)
        label_deck = tk.Label(self.fenetre, text="Deck IA", bg="light blue", fg="blue", font=("Arial", 16, "bold"))
        label_deck.place(x=1250, y=10)
        self.selected_label_j1 = tk.Label(self.fenetre, text="Aucun Pokémon ", bg="light blue", fg="red",
                                          font=("Arial", 16, "bold"))
        self.selected_label_j1.place(x=900, y=60)
        self.selected_label_j2 = tk.Label(self.fenetre, text="Aucun Pokémon ", bg="light blue", fg="blue",
                                          font=("Arial", 16, "bold"))
        self.selected_label_j2.place(x=1200, y=60)

    def afficherDecks(self):
        """
        Affiche les boutons pour chaque type de Pokémon dans les decks des joueurs.
        """
        for i in range(2):
            if i == 0:
                deck = self.deck1
            else:
                deck = self.deck2
            grouped = deck.groupby("Type 1")
            j = 0
            for typename, group in grouped:
                deltaY = 40
                if i == 0:
                    type_name = typename
                    imageType = self.tailleImage(pathType(type_name.lower()), 144, 32)

                    btn = tk.Button(self.fenetre, image=imageType, font=("Arial", 16, "bold"), bg="#1e1e1e", fg="white",
                                    padx=10, pady=10,
                                    command=lambda t=type_name, d=deck: self.afficher_pokemons_type(t, d))
                    btn.image = imageType
                    btn.place(x=900, y=100 + deltaY * j)
                    j += 1
                else:
                    type_name = typename
                    imageType = self.tailleImage(pathType(type_name.lower()), 144, 32)

                    btn = tk.Button(self.fenetre, image=imageType, font=("Arial", 16, "bold"), bg="#1e1e1e", fg="white",
                                    padx=10, pady=10,
                                    command=lambda t=type_name, d=deck: self.afficher_pokemons_type(t, d, IA_turn=True))
                    btn.image = imageType
                    btn.place(x=1200, y=100 + deltaY * j)
                    j += 1

    def afficher_pokemons_type(self, type_name, deck, IA_turn=False):
        """
        Affiche une nouvelle fenêtre avec les Pokémon du type spécifié.
        """
        pokemonsType = deck[deck["Type 1"] == type_name]

        root = tk.Toplevel(self.fenetre)
        root.title(f"Pokémons de type {type_name}")
        root.geometry("600x800")

        frame = tk.Frame(root, bg="#2b2b2b")
        frame.pack(fill="both", expand=True)

        for col in range(3):
            frame.columnconfigure(col, weight=1)
        rowGrid = 0
        col = 0

        for num, rowPokemon in pokemonsType.iterrows():
            try:
                img_pokemon = tk.PhotoImage(file=pathPokemon(rowPokemon["#"], rowPokemon["Name"].lower()))
                img_pokemon = self.tailleImage(pathPokemon(rowPokemon["#"], rowPokemon["Name"].lower()), 100, 100)
            except:
                img_pokemon = None
            btn = tk.Button(frame, text=rowPokemon["Name"], image=img_pokemon, compound="top",
                            font=("Pokemon Solid", 14), bg="white", fg="#3c3c3c", padx=5, pady=5,
                            state="disabled" if IA_turn else "normal",
                            command=lambda window=root, rowP=rowPokemon, name=rowPokemon["Name"],
                                           player=1 if rowPokemon["Name"] in self.deck1["Name"].values else 2: (
                                window.destroy(), self.pokemonChoisi(name, player, rowP)))
            btn.image = img_pokemon
            btn.grid(row=rowGrid, column=col, padx=10, pady=10, sticky="nsew")
            col += 1
            if col >= 3:
                col = 0
                rowGrid += 1

    def pokemonChoisi(self, pokemonName, joueur, row=None):
        """
        Met à jour le label du Pokémon sélectionné pour le joueur spécifié.
        """
        if joueur == 1:
            self.selected_label_j1.config(text=pokemonName)
            self.pokeChoisiDeck1 = row
        else:
            self.selected_label_j2.config(text=pokemonName)
            self.pokeChoisiDeck2 = row

    # ---------------------------------------------------------------------------------------------------------------------------
    # INITIALISATION GRAPHIQUE

    def dessiner_mini_morpion(self, ligne, col):
        """
        Dessine un mini morpion à la position spécifiée par ligne et colonne.
        """
        # on récupère les coordonnées graphiques haut-gauche du mini morpion
        x_coord = 200 + 200 * col
        y_coord = 100 + 200 * ligne

        # verticales
        self.canvas.create_line(x_coord + 67, y_coord + 7, x_coord + 67, y_coord + 187, width=3, fill="red")
        self.canvas.create_line(x_coord + 130, y_coord + 7, x_coord + 130, y_coord + 187, width=3, fill="red")

        # horizontales
        self.canvas.create_line(x_coord + 7, y_coord + 67, x_coord + 187, y_coord + 67, width=3, fill="red")
        self.canvas.create_line(x_coord + 7, y_coord + 130, x_coord + 187, y_coord + 130, width=3, fill="red")

    # Dessiner tout le morpion
    def dessiner_lignes(self):
        """
        Dessine les lignes principales du morpion et les mini morpions."""
        self.canvas.create_line(396, 100, 396, 700, width=6, fill="red")
        self.canvas.create_line(596, 100, 596, 700, width=6, fill="red")
        self.canvas.create_line(200, 296, 800, 296, width=6, fill="red")
        self.canvas.create_line(200, 496, 800, 496, width=6, fill="red")
        for ligne in range(3):
            for col in range(3):
                self.dessiner_mini_morpion(ligne, col)

    # ----------------------------------------------------------------------------------------
    # VERIFICATIONS DANS LA STRUCTURE: victoires, grille pleine

    # Regarder les alignements de pions dans une grille donnée
    def verif_victoire(self, grille):
        """
        Vérifie si le joueur actuel a gagné dans une grille donnée.
        """
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

    # Ajouter dans la sous-grille le gagnant et y détruire les boutons :
    def changer_gagnant_sousgrille(self, grande_ligne, grande_col):
        """
        Met à jour la sous-grille gagnée par le joueur actuel et détruit les boutons correspondants.
        """
        for ligne in range(3):
            for col in range(3):
                if self.boutons[(grande_ligne, grande_col, ligne, col)]:
                    self.boutons[(grande_ligne, grande_col, ligne, col)].destroy()
        self.canvas.create_rectangle(200 + 200 * grande_col, 100 + 200 * grande_ligne, 392 + 200 * grande_col,
                                     292 + 200 * grande_ligne, fill="light blue", outline="light blue", width=1)
        self.canvas.create_text(300 + 200 * grande_col, 200 + 200 * grande_ligne, text=self.joueur,
                                font=("Arial", 100, "bold"), fill=self.color)

        # changement du gagnant dans la structure
        self.gagnantsSousGrilles[grande_ligne][grande_col] = self.joueur

        # Mettre fin à la partie quand elle est gagnée

    def changer_gagnant_grandegrille(self):

        """
           Affiche un message de fin de partie indiquant le gagnant.
        """

        fenetrefin = tk.Toplevel(self.fenetre)  # fenêtre qui recouvre la fenêtre de jeu
        fenetrefin.geometry("1920x1080")  # fenêtre à la même taille que le jeu
        fenetrefin.focus_force()  # pour la rattacher au clavier
        self.canvasfin = tk.Canvas(fenetrefin, width=1920, height=1080, bg="light blue")
        self.canvasfin.pack()
        if self.gagnant == 'X':
            self.canvasfin.create_text(500, 350, text=f"Félicitations !\n\nVous remportez la partie",
                                       font=("Times new roman", 25, "bold"), fill="black")
        else:
            self.canvasfin.create_text(500, 350, text=f"Dommage...\n\nL'IA remporte la partie",
                                       font=("Times new roman", 25, "bold"), fill="black")
        self.canvasfin.create_text(500, 500, text="Cliquez sur la touche f pour fermer la fenêtre",
                                   font=("Halvetica", 10, "bold italic"), fill="red")
        fenetrefin.bind("<Key-f>", lambda event: fenetrefin.destroy())
        self.quit_Bouton = tk.Button(self.fenetre, text="Quitter la partie", font=("Halvetica", 10, "bold italic"), command=lambda: self.fenetre.destroy(),
                                     fg="red", bg="light blue")
        self.quit_Bouton.place(x=20, y=20)



        # Mettre fin à la partie quand il y a égalité sur la grande grille:

    def findujeu_egalite(self):
        fenetrefin = tk.Toplevel(self.fenetre)  # fenêtre qui recouvre la fenêtre de jeu
        fenetrefin.geometry("1920x1080")  # fenêtre à la même taille que le jeu
        fenetrefin.focus_force()  # pour la rattacher au clavier
        self.canvasfin = tk.Canvas(fenetrefin, width=1920, height=1080, bg="light blue")
        self.canvasfin.pack()
        self.canvasfin.create_text(500, 350, text=f"Il y a égalité, personne ne remporte la partie",
                                   font=("Times new roman", 25, "bold"), fill="black")
        self.canvasfin.create_text(500, 500, text="Cliquez sur la touche f pour fermer la fenêtre",
                                   font=("Halvetica", 10, "bold italic"), fill="red")
        fenetrefin.bind("<Key-f>", lambda event: fenetrefin.destroy())
        self.label_fin = tk.Label(self.fenetre, text="Cliquez sur la touche b pour fermer la fenêtre",
                                  font=("Halvetica", 10, "bold italic"), fg="red", bg="light blue")
        self.label_fin.place(x=810, y=1010)
        self.fenetre.bind("<Key-b>", lambda event: self.fenetre.destroy())


    # ---------------------------------------------------------------------------------------------------------------------------
    # changements dans la structure et dans le graphique quand on joue

    # Dessiner un encadrment dans la grille où on doit jouer, si on y est obligé
    def dessiner_encadrement(self):
        # on dessine un encadrement dans les cas où le joueur est obligé de jouer:
        # si la case où il doit jouer n'est pas gagnée ET n'est pas pleine

        ligne = self.case[0]
        col = self.case[1]

        if self.gagnantsSousGrilles[ligne][col] == '' and self.verif_grille_pleine(self.grille[ligne][col]) == False:

            if self.case_a_jouer != None:  # si on n'est pas au 1er tour, on supprime l'ancien encadrement
                self.canvas.delete(self.case_a_jouer)

            self.case_a_jouer = self.canvas.create_rectangle(196 + col * 200, 96 + ligne * 200, 196 + col * 200 + 200,
                                                             96 + ligne * 200 + 200, fill="", outline="green", width=6)
        else:
            self.canvas.delete(self.case_a_jouer)

    # Annonce graphique du joueur dont c'est le tour
    def annoncer_joueur(self):
        self.canvas.delete(self.annonce_joueur)
        if self.joueur == 'X':
            self.annonce_joueur = self.canvas.create_text(500, 20, text="C'est à votre tour de jouer",
                                                          font=("Times new roman", 15, "bold"), fill="red")

    # Tester si le joueur peut jouer selon les règles du Ultimate Tic tac toe
    def test_jouer(self, gl, gc, l, c):
        """
        Teste si un joueur peut jouer à la position spécifiée et effectue le coup si possible.
        """

        # Le joueur peut joueur où il veut:
        # SI c'est le premier tour OU la case où il doit jouer est gagnée OU la case où il doit jouer est pleine

        if self.case == None or self.gagnantsSousGrilles[self.case[0]][self.case[1]] != '' or self.verif_grille_pleine(
                self.grille[self.case[0]][self.case[1]]) == True:
            self.jouer(gl, gc, l, c)
        else:
            if (gl, gc) == self.case:
                self.jouer(gl, gc, l, c)

    def handle_click(self, gl, gc, l, c):
        """
        Gestion du clic sur une case par le joueur humain.
        On laisse le joueur humain jouer normalement, puis on déclenche
        le coup de l'IA si la partie continue.
        """

        if self.gagnant != None or self.joueur != self.humain:
            return
        self.test_jouer(gl, gc, l, c)

        if self.gagnant == None and self.joueur == self.IA:
            self.IA_move()

    # --------------------------------------------------------------------------------------------------
    # STRATEGIE DE JEU DE L'IA

    def IA_move(self):

        gl, gc, l, c = MCTS.MCTS(
            self.grille,
            self.gagnantsSousGrilles,
            self.pokemons_places,
            self.joueur,
            self.case,
            iterations=500
        )
        self.test_jouer(gl, gc, l, c)

    def bestPokemonIA(self, pokemonAdverses):
        """
        Choisit le meilleur Pokémon contre une liste de Pokémon adverses.
        """

        if len(self.deck2) == 0:
            return None
        type1adverse = pokemonAdverses["Type 1"]
        type2adverse = pokemonAdverses["Type 2"]
        bestTypes = []
    
        types=self.matriceAdj.columns.tolist()
        for typeP in types:
            if self.matriceAdj.loc[typeP,type1adverse]>1:
                bestTypes.append(typeP)
            if isinstance(type2adverse,str):
                if self.matriceAdj.loc[typeP,type2adverse]>1:
                    bestTypes.append(typeP)

        possiblePokemons=self.deck2[(self.deck2["Type 1"].isin(bestTypes) | self.deck2["Type 2"].isin(bestTypes)) & (self.deck2["Total"]>=pokemonAdverses["Total"])]
        print(possiblePokemons)
        if len(possiblePokemons) > 0:
            return possiblePokemons.loc[possiblePokemons.index[0]]
        else:

            possiblePokemons = self.deck2[
                (self.deck2["Type 1"].isin(bestTypes) | self.deck2["Type 2"].isin(bestTypes))].sort_values(by="Total",
                                                                                                           ascending=True)
            print(possiblePokemons)
            if len(possiblePokemons) == 0:
                possiblePokemons = self.deck2[(self.deck2["Total"] >= pokemonAdverses["Total"])]
                if len(possiblePokemons) == 0:
                    idx = random.choice(self.deck2.index.tolist())
                    return self.deck2.loc[idx]
                idx = random.choice(possiblePokemons.index.tolist())
                return possiblePokemons.loc[idx]
            return possiblePokemons.loc[possiblePokemons.index[0]]

    def PokemonChoisi(self, gl=None, gc=None, l=None, c=None):
        """
        Retourne le Pokémon choisi par le joueur actuel et le retire de son deck.
        """
        if self.joueur == 'X':
            self.updateColor("X")
            if self.pokeChoisiDeck1 is None:
                return None
            self.deck1.drop(self.deck1[self.deck1["#"] == self.pokeChoisiDeck1["#"]].index, inplace=True)
            return self.pokeChoisiDeck1
        else:
            self.updateColor("O")
            if self.pokemons_places[gl][gc][l][c] != None:
                self.pokeChoisiDeck2 = self.bestPokemonIA(self.pokemons_places[gl][gc][l][c][1])
                self.deck2.drop(self.deck2[self.deck2["#"] == self.pokeChoisiDeck2["#"]].index, inplace=True)
                return self.pokeChoisiDeck2
            else:
                self.pokeChoisiDeck2 = self.pokemonChoisiRandom()
                self.deck2.drop(self.deck2[self.deck2["#"] == self.pokeChoisiDeck2["#"]].index, inplace=True)
                return self.pokeChoisiDeck2

    def pokemonChoisiRandom(self):
        """
        Retourne un Pokémon aléatoire du deck de l'IA et le retire de son deck.
        """
        if len(self.deck2) == 0:
            return None
        idx = random.choice(self.deck2.index.tolist())
        pokemon = self.deck2.loc[idx]
        self.deck2.drop(self.deck2[self.deck2["#"] == pokemon["#"]].index, inplace=True)
        return pokemon
    
    # ---------------------------------------------------------------------------------------------------------------------------
    # JOUER : coup du joueur, vérification de l'état des grilles, et changement de tour en appelant les méthodes précédentes
    def jouer(self, gl, gc, l, c):
        """
        Effectue le coup du joueur actuel à la position spécifiée.
        Gère le placement ou le combat selon la situation.
        Met à jour l'état du jeu après le coup."""
        pokemon = self.PokemonChoisi(gl, gc, l, c)
        if pokemon is None:
            return
        
        case = self.pokemons_places[gl][gc][l][c]
        self.coupsJoueurX.append((gl, gc, l, c))
        # Case vide = placement simple
        if case is None:
            self.placerPokemon(gl, gc, l, c)

        # Case occupée par l'adversaire = combat
        elif self.pokemons_places[gl][gc][l][c][0] != self.joueur and self.pokemons_places[gl][gc][l][c] != -1:
            if self.joueur == "O":
                self.initierCombat(gl, gc, l, c, pokemon, IA_turn=True)
            else:
                self.initierCombat(gl, gc, l, c, pokemon)


        # Case déjà gagnée = on ignore
        else:
            return

        # Verification après le placement/combat d'une victoire locale
        if self.verif_victoire(self.grille[gl][gc]):
            self.changer_gagnant_sousgrille(gl, gc)

        self.resetPokemonChoisi()

        # Verfication victoire grande grille
        if self.verif_victoire(self.gagnantsSousGrilles):
            self.gagnant = self.joueur
            self.changer_gagnant_grandegrille()
            return  # permet d'arrêter la fonction

        # Vérification de grille pleine dans la grande grille:

        if self.verif_grille_pleine(self.gagnantsSousGrilles):
            # le jeu est fini est personne ne gagne
            self.findujeu_egalite()
            return  # permet d'arrêter la méthode

        # Changement de tour
        self.case = (l, c)  # on retient la case qui vient d'être jouée pour obliger le suivant à y jouer

        if self.joueur == 'X':
            self.joueur = 'O'
        else:
            self.joueur = 'X'

        self.annoncer_joueur()  # annonce graphique du joueur
        self.dessiner_encadrement()  # encadrement de la sous-grille si on est obligé du joueur

    # Fonctions pour la partie Pokemon

    def placerPokemon(self, gl, gc, l, c):
        """
        Place un Pokémon dans la grille à la position spécifiée.
        Met à jour l'affichage graphique en conséquence."""

        if self.pokemons_places[gl][gc][l][c] == -1:
            return
        pokemon = self.PokemonChoisi(gl, gc, l, c)
        if pokemon is None:
            return

        self.pokemons_places[gl][gc][l][c] = (self.joueur, pokemon, pokemon["#"])
        self.grille[gl][gc][l][c] = self.joueur
        image = self.tailleImage(pathPokemon(int(pokemon["#"]), pokemon["Name"].lower()), 50, 50)
        self.boutons[(gl, gc, l, c)].configure(image=image, compound="top", bg=self.color,
                                               highlightbackground=self.color, highlightthickness=5)
        self.boutons[(gl, gc, l, c)].image = image

    def resetPokemonChoisi(self):
        """
        Réinitialise le Pokémon choisi pour le joueur actuel.
        """
        if self.joueur == 'X':
            self.pokeChoisiDeck1 = None
            self.color = None
            self.selected_label_j1.config(text="Aucun Pokémon ")
        else:
            self.pokeChoisiDeck2 = None
            self.color = None
            self.selected_label_j2.config(text="Aucun Pokémon ")

    def updateColor(self, joueur=None):
        """
        Met à jour la couleur associée au joueur actuel.
        """
        if joueur == None:
            return

        if joueur == 'X':
            self.color = "red"
        else:
            self.color = "blue"

    def initierCombat(self, gl, gc, l, c, pokemon, IA_turn=False):
        """
        Initialise un combat entre le Pokémon du joueur actuel et celui de l'adversaire.
        Met à jour l'état du jeu en fonction du résultat du combat.
        """
        pokemonIA = self.pokemons_places[gl][gc][l][c][1]
        pokemonJ = pokemon
        if IA_turn:
            pokemonIA, pokemonJ = pokemonJ, pokemonIA

        combat = PokemonJVSIA(pokemonJ, pokemonIA, self.fenetre)
        combat.fenetre.mainloop()
        gagnant_combat = combat.winner
        if gagnant_combat["#"] == pokemonIA["#"]:
            gagnant = 'O'
            self.color = "blue"
            pokemonPerdant = pokemonJ
        else:
            gagnant = 'X'
            self.color = "red"
            pokemonPerdant = pokemonIA

        self.grille[gl][gc][l][c] = gagnant
        self.updateColor(gagnant)
        self.boutons[(gl, gc, l, c)].configure(text=gagnant, image="", compound=None, bg=self.color,
                                               highlightbackground=self.color, highlightthickness=5, fg=self.color)
        self.boutons[(gl, gc, l, c)].image = None
        self.pokemons_places[gl][gc][l][c] = -1

        if gagnant == 'X':
            self.deck2.loc[len(self.deck2)] = pokemonPerdant
            self.deck2[self.deck2["#"] == pokemonPerdant["#"]]["Level"] += 1
        else:
            self.deck1.loc[len(self.deck1)] = pokemonPerdant
            self.deck1[self.deck1["#"] == pokemonPerdant["#"]]["Level"] += 1

    # ------------------------------------------------------------------------------------------------
    # CREATION DES BOUTONS

    # Création des boutons pour cliquer dans les cases de jeu
    def cases(self):
        self.boutons = {}
        for grande_ligne in range(3):
            for grande_col in range(3):
                for ligne in range(3):
                    for col in range(3):
                        self.boutons[(grande_ligne, grande_col, ligne, col)] = tk.Button(self.canvas, bg="light blue",
                                                                                         relief="flat", borderwidth=0,
                                                                                         activebackground="white",
                                                                                         command=lambda gl=grande_ligne,
                                                                                                        gc=grande_col,
                                                                                                        l=ligne,
                                                                                                        c=col: self.handle_click(
                                                                                             gl, gc, l, c))
                        self.boutons[(grande_ligne, grande_col, ligne, col)].place(
                            x=200 + 200 * grande_col + 62 * col + 8, y=100 + 200 * grande_ligne + 62 * ligne + 8,
                            width=58 - col, height=58 - ligne)

    # Afficher la fenêtre graphique
    def afficher(self):
        self.fenetre.mainloop()

