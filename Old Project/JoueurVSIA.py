import tkinter as tk
import deck_builder as db
import data_loader as dl
from paths import *
from tkinter import ttk
from PIL import Image, ImageTk
from affichageCombatJvsJ import PokemonApp
import pandas as pd
from time import sleep
import random

class JoueurVSIA () :

    def __init__(self):
        # GRAPHIQUE :

        self.fenetre = tk.Tk()
        self.canvas = tk.Canvas(self.fenetre, width=1920, height=1080, bg="light blue")
        self.canvas.pack()

        # STRUCTURE :
        self.grille = [[[['' for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
        
        # Statut de victoire pour chaque sous-grille ('', 'X' ou 'O')
        self.gagnants_sousgrilles = [['' for i in range(3)] for i in range(3)]
        
        # Gagnant du grand morpion
        self.gagnant = None
        self.joueur = 'X'  # joueur qui commence
        # Mode de jeu :
        self.IA="X"
        self.joueur='O'

       


        # VARIABLES POUR LA REGLE DU ULTIMATE TIC TAC TOE :
        #   case dans la sous-grille qui vient d'être jouée
        self.case= None    #(ligne,col)

        #   objet graphique du contour de la case à jouer
        self.case_a_jouer = None
        # POKEMON :
        self.deck1,self.deck2=db.decks(dl.dfPokemon())
        # BOUTONS :
        self.bouton_deck()
        self.afficherDecks()
    
        self.pokeChoisiDeck1=None
        self.pokeChoisiDeck2=None
        self.color=None
        self.dessiner_lignes()
        self.cases()
        self.afficher()
#---------------------------------------------------------------------------------------
# PARTIE POKEMON :
    def tailleImage(self,path, sizeX,sizeY):
            try:
                image = Image.open(path)
                image = image.resize((sizeX, sizeY), Image.LANCZOS)
                return ImageTk.PhotoImage(image)
            except:
                return None
        

    def bouton_deck(self):
        label_deck=tk.Label(self.fenetre,text="Deck X",bg="light blue",fg="red",font=("Arial", 16, "bold"))
        label_deck.place(x=950, y=10)
        label_deck=tk.Label(self.fenetre,text="Deck O",bg="light blue",fg="blue",font=("Arial", 16, "bold"))
        label_deck.place(x=1250, y=10)
        self.selected_label_j1 = tk.Label(self.fenetre,text="Aucun Pokémon ",bg="light blue",fg="red",font=("Arial", 16, "bold"))
        self.selected_label_j1.place(x=900, y=60)
        self.selected_label_j2 = tk.Label(self.fenetre,text="Aucun Pokémon ",bg="light blue",fg="blue",font=("Arial", 16, "bold"))
        self.selected_label_j2.place(x=1200, y=60)
    def afficherDecks(self):
        for i in range(2):
            if i==0:
                deck=self.deck1
            else:
                deck=self.deck2
            grouped = deck.groupby("Type 1")
            j=0
            for typename,group in grouped:
                deltaY=40
                if i==0:
                    type_name=typename
                    imageType= self.tailleImage(pathType(type_name.lower()),144, 32)

                    btn = tk.Button(self.fenetre,image=imageType,font=("Arial", 16, "bold"),bg="#1e1e1e",fg="white",padx=10,pady=10,command=lambda t=type_name ,d=deck: self.afficher_pokemons_type(t, d))
                    btn.image = imageType
                    btn.place(x=900, y=100 + deltaY*j)
                    j+=1
                else:
                    type_name=typename
                    imageType= self.tailleImage(pathType(type_name.lower()), 144, 32)
                    
                    btn = tk.Button(self.fenetre,image=imageType,font=("Arial", 16, "bold"),bg="#1e1e1e",fg="white",padx=10,pady=10,command=lambda t=type_name, d=deck: self.afficher_pokemons_type(t, d))
                    btn.image = imageType
                    btn.place(x=1200, y=100 + deltaY*j)
                    j+=1

    def afficher_pokemons_type(self, type_name, deck):
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
                img_pokemon=self.tailleImage(pathPokemon(rowPokemon["#"], rowPokemon["Name"].lower()),100,100)
            except:
                img_pokemon = None
            btn = tk.Button(frame,text=rowPokemon["Name"],image=img_pokemon,compound="top",font=("Pokemon Solid", 14),bg="white",fg="#3c3c3c",padx=5,pady=5, command=lambda window=root, rowP=rowPokemon ,name=rowPokemon["Name"], player=1 if rowPokemon["Name"] in self.deck1["Name"].values else 2: (window.destroy(), self.pokemonChoisi(name, player,rowP)))
            btn.image = img_pokemon
            btn.grid(row=rowGrid, column=col, padx=10, pady=10, sticky="nsew")
            col += 1
            if col >= 3:  
                col = 0
                rowGrid += 1
    def pokemonChoisi(self, pokemonName, joueur,row=None):
        if joueur == 1:
            self.selected_label_j1.config(text=pokemonName)
            self.pokeChoisiDeck1=row
        else:
            self.selected_label_j2.config(text=pokemonName)
            self.pokeChoisiDeck2=row



#---------------------------------------------------------------------------------------
# INITIALISATION GRAPHIQUE

    # Dessiner un mini morpion
    def dessiner_mini_morpion(self,ligne,col):

        #on récupère les coordonnées graphiques haut-gauche du mini morpion
        x_coord= 200 + 200 * col
        y_coord = 100 +200 * ligne

        #verticales
        self.canvas.create_line(x_coord+67, y_coord+7, x_coord+67,y_coord+187, width=3, fill="red")
        self.canvas.create_line(x_coord+130, y_coord+7, x_coord+130, y_coord+187, width=3, fill="red")

        #horizontales
        self.canvas.create_line(x_coord+7, y_coord+67, x_coord+187,y_coord+67, width=3, fill="red")
        self.canvas.create_line(x_coord+7, y_coord+130, x_coord+187, y_coord+130, width=3, fill="red")

    # Dessiner tout le morpion
    def dessiner_lignes(self): #dessin de toutes les lignes du morpion
        
        self.canvas.create_line(396, 100, 396, 700, width=6, fill="red")
        self.canvas.create_line(596, 100, 596, 700, width=6, fill="red")
        self.canvas.create_line(200, 296, 800, 296, width=6, fill="red")
        self.canvas.create_line(200, 496, 800, 496, width=6, fill="red")
        for ligne in range(3):
            for col in range(3):
                self.dessiner_mini_morpion(ligne, col)

#----------------------------------------------------------------------------------------
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
    def verif_grille_pleine(self,grille):
        for ligne in grille:
            for col in ligne:
                if col=='':
                    return False #si un élément de la grille est vide alors elle n'est pas pleine
        return True

#--------------------------------------------------------------------------------------------------
# MISE A JOUR DES GAGNANTS ET FIN DU JEU

    # Changer le gagnant d'une sous grille dans la structure & le graphique
    def changer_gagnant_sousgrille(self,grande_ligne,grande_col):

        #on change le gagnant graphiquement
        if self.graphique==True:
            for ligne in range(3):
                for col in range(3):
                    if self.boutons[(grande_ligne, grande_col, ligne, col)]:
                        self.boutons[(grande_ligne, grande_col, ligne, col)].destroy()
            self.canvas.create_rectangle(200 + 200 * grande_col, 100 + 200 * grande_ligne, 392 + 200 * grande_col,
                                         292 + 200 * grande_ligne, fill="light blue", outline="light blue", width=1)
            self.canvas.create_text(300 + 200 * grande_col, 200 + 200 * grande_ligne, text=self.joueur,
                                    font=("Arial", 100, "bold"), fill="blue")

        #on change le gagnant dans la structure
        self.gagnants_sousgrilles[grande_ligne][grande_col]=self.joueur

    # Mettre fin à la partie quand un joueur a gagné
    def changer_gagnant_grandegrille(self):
        self.canvas.destroy()
        self.canvasfin = tk.Canvas(self.fenetre, width=1000, height=700, bg="light blue")
        self.canvasfin.pack()
        self.canvasfin.create_text(500, 350, text=f"Félicitations !\n\nLe joueur {self.joueur} remporte la partie", font=("Times new roman", 25, "bold"), fill="black")
        self.canvasfin.create_text(500, 500, text="Cliquez sur la touche f pour fermer la fenêtre", font=("Halvetica", 10, "bold italic"), fill="red")
        self.fenetre.bind("<Key-f>", lambda event: self.fenetre.destroy())
        self.fenetre.mainloop()

    # Mettre fin à la partie quand il y a égalité sur la grande grille:
    def findujeu_egalite(self):
        if self.graphique==True:
            self.canvas.destroy()
            self.canvasfin = tk.Canvas(self.fenetre, width=1000, height=700, bg="light blue")
            self.canvasfin.pack()
            self.canvasfin.create_text(500, 350, text=f"Il y a égalité, personne ne remporte la partie",
                                       font=("Times new roman", 25, "bold"), fill="black")
            self.canvasfin.create_text(500, 500, text="Cliquez sur la touche f pour fermer la fenêtre",
                                       font=("Halvetica", 10, "bold italic"), fill="red")
            self.fenetre.bind("<Key-f>", lambda event: self.fenetre.destroy())
            self.fenetre.mainloop()

#-------------------------------------------------------------------------------------------
# JOUER : changements dans la structure et dans le graphique

    # Placer le pion graphiquement :
    def jouer_graphiquement(self,grande_ligne,grande_col,ligne,col):
        if self.joueur == 'X':
            self.placerPokemon(grande_ligne,grande_col,ligne,col)
        else:
            self.canvas.create_oval(200 + 200 * grande_col + 62 * col + 12, 100 + 200 * grande_ligne + 62 * ligne + 12,
                                    200 + 200 * grande_col + 62 * col + 60, 100 + 200 * grande_ligne + 62 * ligne + 60,
                                    width=3, fill="lightblue", outline="blue")
            self.boutons[(grande_ligne, grande_col, ligne, col)].destroy()

    # Afficher le joueur dont c'est le tour dans la fenêtre
    def annoncer_joueur(self):
        self.canvas.delete(self.annonce_joueur)
        if self.joueur==self.IA:
            nom= 'IA'
        else:
            nom='Vous'
        self.annonce_joueur=self.canvas.create_text(500,20, text=f"C'est au joueur {self.joueur} ({nom}) de jouer", font=("Times new roman", 15, "bold"), fill="black")

    # Dessiner un encadrement où le joueur doit jouer s'il y est obligé
    def dessiner_encadrement(self):
        # on dessine un encadrement dans les cas où le joueur est obligé de jouer:
        # c'est-à-dire si la case où il doit jouer n'est pas gagnée OU n'est pas pleine

        ligne=self.case[0]
        col=self.case[1]

        if self.gagnants_sousgrilles[ligne][col] == '' and self.verif_grille_pleine(self.grille[ligne][col])==False:

            if self.case_a_jouer != None:  # si on n'est pas au 1er tour, on supprime l'ancien encadrement
                self.canvas.delete(self.case_a_jouer)

            self.case_a_jouer = self.canvas.create_rectangle(196 + col * 200, 96 + ligne * 200, 196 + col * 200 + 200,
                                                                 96 + ligne * 200 + 200, fill="", outline="green", width=6)
        else:
            self.canvas.delete(self.case_a_jouer)

    # Changer le tour : passer de 'X' à 'O', prenant en compte le mode de jeu
    def changer_tour(self):
        if self.joueur== self.IA :
            self.joueur = self.j
        else:
            self.joueur= self.IA
            self.ia()
#------------------------------------------------------------------------------------------------

    # Placer le joueur dans la structure, appel des méthodes précédentes:
    # - jouer graphiquement
    # - vérifications de grille pleine ou gagnée
    # - changer le tour de jeu
    def jouer (self,grande_ligne,grande_col,ligne,col):

        #on place le joueur dans la structure
        self.grille[grande_ligne][grande_col][ligne][col] = self.joueur

        #on place le pion graphiquement :
        if self.graphique == True:
            self.placerPokemon(grande_ligne,grande_col,ligne,col)
            self.jouer_graphiquement (grande_ligne,grande_col,ligne,col)

        #vérification de victoire locale
        if self.verif_victoire(self.grille[grande_ligne][grande_col])==True:
                self.gagnants_sousgrilles[grande_ligne][grande_col]=self.joueur
                self.changer_gagnant_sousgrille(grande_ligne,grande_col)

        #vérification de victoire globale
        if self.verif_victoire(self.gagnants_sousgrilles):
            self.gagnant = self.joueur
            if self.graphique==True:
                self.changer_gagnant_grandegrille()
            return True # permet à la fonction jouer() de s'arrêter, pour ne pas dessiner d'encadrement ensuite

        #vérification de grille pleine dans la grande grille:
        if self.verif_grille_pleine(self.gagnants_sousgrilles):
            #le jeu est fini est personne ne gagne
            self.findujeu_egalite()
            return True #permet à la fonction jouer() de s'arrêter, pour ne pas dessiner d'encadrement ensuite

        # on retient la case qui vient d'être jouée pour obliger le suivant à y jouer
        self.case = (ligne, col)

        # dessin d'un encadrement graphique pour le prochain joueur:
        if self.graphique==True:
            self.dessiner_encadrement()


        #changement de tour
        self.changer_tour()

        #écrire sur la fenêtre le joueur dont c'est le tour
        if self.graphique==True:
            self.annoncer_joueur()

    # Vérifier si le case est jouable selon les règles ultimate tic tac toe :
    def test_jouer(self,gl, gc, l, c):


            if self.grille[gl][gc][l][c] == '':

                # Le joueur peut joueur où il veut dans les cas suivants:
                # SI c'est le premier tour OU la case où il doit jouer est gagnée OU la case où il doit jouer est pleine
                if self.case == None  or self.gagnants_sousgrilles[self.case[0]][self.case[1]]!='' or self.verif_grille_pleine(self.grille[self.case[0]][self.case[1]])==True:
                    #il peut jouer où il veut sauf dans une grille gagnée ni une grille pleine:
                    if self.gagnants_sousgrilles[gl][gc]=='' and self.verif_grille_pleine(self.grille[gl][gc])==False:

                        self.jouer(gl, gc, l, c)
                        return True

                #sinon: il a une obligation de jeu : ne peut jouer que dans self.case

                elif (gl,gc)==self.case:
                    self.jouer(gl, gc, l, c)
                    return True

            return False

#------------------------------------------------------------------------------------------------
# CREATION DES BOUTONS DE CASES ET DEMARRAGE DES MODES DE JEU GRAPHIQUES

    # Création des boutons pour cliquer dans les cases de jeu et jeu d'IA s'il commence
    def cases(self):

        self.boutons = {}

        for grande_ligne in range(3):
                for grande_col in range(3):
                    for ligne in range(3):
                        for col in range(3):
                            self.boutons[(grande_ligne, grande_col, ligne, col)] = tk.Button(self.fenetre, bg="light blue", relief="flat",
                                                                                             borderwidth=0,activebackground="white",command=lambda gl=grande_ligne, gc=grande_col, l=ligne, c=col: self.test_jouer(gl,gc, l, c))
                            self.boutons[(grande_ligne, grande_col, ligne, col)].place(x=200 + 200 * grande_col + 62 * col + 8, y=100 + 200 * grande_ligne + 62 * ligne + 8,
                                            width=58 - col, height=58 - ligne)
        # si c'est à l'IA de commencer
        if self.joueur == self.IA:
            self.ia()

#-------------------------------------------------------------------------------------------------
# CODE DE LA STRATEGIE DE L'IA ET DE L'ALGO RANDOM


    # Random : joue aléatoirement
    def ia_random (self):

        if self.joueur == self.random:  # on vérifie que c'est bien à son tour
            if self.case==None: #si le random joue en premier

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

    def ia (self):

        if self.joueur == self.IA: # on vérifie que c'est bien son tour
            #Si on est au début de la partie on jouer au milieu
            if self.case==None:
                self.test_jouer(1, 1, 1, 1)
                self.nbcoups += 1
                return True

            #Sinon : stratégie --> Pour l'instant, l'ia joue aléatoirement

            #On essaie d'abord de jouer dans la case obligée
            else:
                gl=self.case[0]
                gc=self.case[1]
                petites_cases = [(l, c) for l in range(3) for c in range(3)] #ensemble des cases possibles
                random.shuffle(petites_cases) #on change l'orde aléatoirement
                for (l,c) in petites_cases:
                    succes=self.test_jouer(gl, gc, l, c)
                    if succes==True:
                        self.nbcoups += 1
                        return True #la fonction s'arrête: c'est à l'autre de jouer


                # Si on ne peut pas, on joue aléatoirement et partout
                grandes_cases = [(l, c) for l in range(3) for c in range(3)]  # ensemble des sous-grilles possibles
                random.shuffle(grandes_cases)  # on change l'orde aléatoirement

                for grande_grille in grandes_cases:
                    petites_cases = [(l, c) for l in range(3) for c in range(3)]  # ensemble des cases possibles
                    random.shuffle(petites_cases)  # on change l'orde aléatoirement
                    for (l, c) in petites_cases:
                        succes = self.test_jouer(grande_grille[0],grande_grille[1], l, c)
                        if succes == True:
                            self.nbcoups += 1
                            return True  # la fonction s'arrête: c'est à l'autre de jouer
        
#-------------------------------------------------------------------------------------------
# INITIALISATION DES MODES DE JEU
    # Mode joueur VS IA
    def jouer(self):
        # REMARQUE : 3 variables de joueurs:
        # self.IA : l'IA ( X ou O )
        # self.j : le joueur qui joue contre l'IA ( X ou O )
        # self.joueur : variable de la classe qui correspond au joueur actuel (change à chaque tour)


        #self.IA = random.choice(['X', 'O'])
        self.IA='X'

        if self.IA == 'X':
            self.joueur = self.IA
            self.j = 'O'  # joueur qui joue contre l'IA
            self.annonce_joueur = self.canvas.create_text(500, 20,
                                                          text=f"C'est à l'IA de commencer",
                                                          font=("Times new roman", 15, "bold"), fill="black")
        else:
            self.j = 'X'
            self.joueur = self.j
            self.annonce_joueur = self.canvas.create_text(500, 20, text=f"C'est à vous de commencer",
                                                          font=("Times new roman", 15, "bold"), fill="black")
        self.cases()

    def tailleImage(self,path, sizeX,sizeY):
        try:
            image = Image.open(path)
            image = image.resize((sizeX, sizeY), Image.LANCZOS)
            return ImageTk.PhotoImage(image)
        except:
            return None
            

    def bouton_deck(self):
        label_deck=tk.Label(self.fenetre,text="Deck X",bg="light blue",fg="red",font=("Arial", 16, "bold"))
        label_deck.place(x=950, y=10)
        label_deck=tk.Label(self.fenetre,text="Deck O",bg="light blue",fg="blue",font=("Arial", 16, "bold"))
        label_deck.place(x=1250, y=10)
        self.selected_label_j1 = tk.Label(self.fenetre,text="Aucun Pokémon ",bg="light blue",fg="red",font=("Arial", 16, "bold"))
        self.selected_label_j1.place(x=900, y=60)
        self.selected_label_j2 = tk.Label(self.fenetre,text="Aucun Pokémon ",bg="light blue",fg="blue",font=("Arial", 16, "bold"))
        self.selected_label_j2.place(x=1200, y=60)
    def afficherDecks(self):
        for i in range(2):
            if i==0:
                deck=self.deck1
            else:
                deck=self.deck2
            grouped = deck.groupby("Type 1")
            j=0
            for typename,group in grouped:
                deltaY=40
                if i==0:
                    type_name=typename
                    imageType= self.tailleImage(pathType(type_name.lower()),144, 32)

                    btn = tk.Button(self.fenetre,image=imageType,font=("Arial", 16, "bold"),bg="#1e1e1e",fg="white",padx=10,pady=10,command=lambda t=type_name ,d=deck: self.afficher_pokemons_type(t, d))
                    btn.image = imageType
                    btn.place(x=900, y=100 + deltaY*j)
                    j+=1
                else:
                    type_name=typename
                    imageType= self.tailleImage(pathType(type_name.lower()), 144, 32)
                    
                    btn = tk.Button(self.fenetre,image=imageType,font=("Arial", 16, "bold"),bg="#1e1e1e",fg="white",padx=10,pady=10,command=lambda t=type_name, d=deck: self.afficher_pokemons_type(t, d))
                    btn.image = imageType
                    btn.place(x=1200, y=100 + deltaY*j)
                    j+=1

    def afficher_pokemons_type(self, type_name, deck):
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
                img_pokemon=self.tailleImage(pathPokemon(rowPokemon["#"], rowPokemon["Name"].lower()),100,100)
            except:
                img_pokemon = None
            btn = tk.Button(frame,text=rowPokemon["Name"],image=img_pokemon,compound="top",font=("Pokemon Solid", 14),bg="white",fg="#3c3c3c",padx=5,pady=5, command=lambda window=root, rowP=rowPokemon ,name=rowPokemon["Name"], player=1 if rowPokemon["Name"] in self.deck1["Name"].values else 2: (window.destroy(), self.pokemonChoisi(name, player,rowP)))
            btn.image = img_pokemon
            btn.grid(row=rowGrid, column=col, padx=10, pady=10, sticky="nsew")
            col += 1
            if col >= 3:  
                col = 0
                rowGrid += 1
    def pokemonChoisi(self, pokemonName, joueur,row=None):
        if joueur == 1:
            self.selected_label_j1.config(text=pokemonName)
            self.pokeChoisiDeck1=row
        else:
            self.selected_label_j2.config(text=pokemonName)
            self.pokeChoisiDeck2=row
    def afficher(self):
        self.fenetre.mainloop()

#-------------------------------------------------------------------------------------------
# MENU DU JEU
    def menu(self):
        self.canvasmenu = tk.Canvas(self.fenetre, width=1000, height=700, bg="light blue")
        self.canvasmenu.pack()
        self.canvasmenu.create_text(500, 50, text=f"Bienvenue dans Ultimate Tic tac toe Pokemon !",
                                    font=("Times new roman", 20, "bold"), fill="black")

        self.bouton_jvsj = tk.Button(self.fenetre, text="Joueur vs Joueur", font=("Halvetica", 30, "bold"), width=20,
                                     bg="light blue", fg="blue", activebackground="light blue",
                                     command=lambda: self.modeJvsJ())
        self.bouton_jvsj.place(x=250, y=150)
        self.bouton_jvsia = tk.Button(self.fenetre, text="Joueur vs IA", font=("Halvetica", 30, "bold"), width=20,
                                      bg="light blue", fg="blue", activebackground="light blue",
                                      command=lambda: self.modeJvsIA())
        self.bouton_jvsia.place(x=250, y=250)
        self.bouton_iavsia = tk.Button(self.fenetre, text="IA vs aléatoire", font=("Halvetica", 30, "bold"), width=20,
                                       bg="light blue", fg="blue", activebackground="light blue",
                                       command=lambda: self.modelisation(100))
        self.bouton_iavsia.place(x=250, y=350)

        self.fenetre.mainloop()


