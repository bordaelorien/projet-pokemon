import tkinter as tk
import deck_builder as db
import data_loader as dl
from paths import *
from tkinter import ttk
from PIL import Image, ImageTk
from affichageCombat import PokemonApp
import pandas as pd
class JoueurVSJoueur() :

    def __init__(self):
        # GRAPHIQUE :
        self.fenetre= tk.Tk()
        self.canvas= tk.Canvas(self.fenetre, width=1920, height=1080, bg="light blue")
        self.canvas.pack()

        # STRUCTURE :
        self.grille = [[[['' for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
        
        # Statut de victoire pour chaque sous-grille (None, 'X' ou 'O')
        self.gagnantsSousGrilles = [[None for i in range(3)] for i in range(3)]

        self.pokemons_places = [[[[None for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
        
        # Gagnant du grand morpion
        self.gagnant = None

        # Joueur actuel, initialié à X
        self.joueur = 'X'

        # Annonce graphique du joueur en cours
        self.annonce_joueur=self.canvas.create_text(500,20, text=f"C'est au joueur {self.joueur} de commencer", font=("Times new roman", 15, "bold"), fill="black")

        # VARIABLES POUR LA REGLE DU ULTIMATE TIC TAC TOE :
        #   case dans la sous-grille qui vient d'être jouée
        self.case= None    #(ligne,col)

        #   objet graphique du contour de la case à jouer
        self.case_a_jouer = None
        
        #   booléen: est-ce que le joueur vient de gagner une sous-grille?
        self.gagnant_sous_grille = False
        #Deck :
        self.deck1, self.deck2 = db.decks(dl.dfPokemon())

        # BOUTONS :
        self.bouton_deck()
        self.afficherDecks()
    
        self.pokeChoisiDeck1=None
        self.pokeChoisiDeck2=None
        self.color=None
        self.dessiner_lignes()
        self.cases()
        self.afficher()
        self.fenetre.mainloop()

        
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
    def dessiner_lignes (self): #dessin de toutes les lignes du morpion
        self.canvas.create_line(396, 100, 396, 700, width=6, fill="red")
        self.canvas.create_line(596, 100, 596, 700, width=6, fill="red")
        self.canvas.create_line(200, 296, 800, 296, width=6, fill="red")
        self.canvas.create_line(200, 496, 800, 496, width=6, fill="red")
        for ligne in range(3):
            for col in range(3):
                self.dessiner_mini_morpion(ligne,col)

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

    # Ajouter dans la sous-grille le gagnant et y détruire les boutons :
    def changer_gagnant_sousgrille(self,grande_ligne,grande_col):
        for ligne in range(3):
            for col in range(3):
                if self.boutons[(grande_ligne, grande_col, ligne, col)]:
                    self.boutons[(grande_ligne, grande_col, ligne, col)].destroy()
        self.canvas.create_rectangle(200 + 200 * grande_col, 100 + 200 * grande_ligne, 392 + 200 * grande_col,292 + 200 * grande_ligne, fill="light blue", outline="light blue", width=1)
        self.canvas.create_text(300 + 200 * grande_col, 200 + 200 * grande_ligne, text=self.joueur, font=("Arial", 100, "bold"), fill=self.color)
        self.gagnantsSousGrilles[grande_ligne][grande_col]=self.joueur

    # Mettre fin à la partie quand un joueur a gagné
    def changer_gagnant_grandegrille(self):

        #nouveau canvas par dessus la grille
        self.canvas.delete("all")
        self.canvas.create_text(500, 350, text=f"Félicitations !\n\nLe joueur {self.joueur} remporte la partie", font=("Times new roman", 25, "bold"), fill="black")
        self.canvas.create_text(500, 500, text="Cliquez sur la touche f pour fermer la fenêtre", font=("Halvetica", 10, "bold italic"), fill="red")
        self.fenetre.bind("<Key-f>", lambda event: self.fenetre.destroy())

    # Placer le pion graphiquement :
    def jouer_graphiquement(self,grande_ligne,grande_col,ligne,col):

        if self.joueur == 'X':
            
            self.canvas.create_line(200 + 200 * grande_col + 62 * col + 12, 100 + 200 * grande_ligne + 62 * ligne + 12,
                                    200 + 200 * grande_col + 62 * col + 60, 100 + 200 * grande_ligne + 62 * ligne + 60,
                                    width=3, fill="blue")
            self.canvas.create_line(200 + 200 * grande_col + 62 * col + 60, 100 + 200 * grande_ligne + 62 * ligne + 12,
                                    200 + 200 * grande_col + 62 * col + 12, 100 + 200 * grande_ligne + 62 * ligne + 60,
                                    width=3, fill="blue")
            self.boutons[(grande_ligne, grande_col, ligne, col)].destroy()

        else:
            self.canvas.create_oval(200 + 200 * grande_col + 62 * col + 12, 100 + 200 * grande_ligne + 62 * ligne + 12,
                                    200 + 200 * grande_col + 62 * col + 60, 100 + 200 * grande_ligne + 62 * ligne + 60,
                                    width=3, fill="lightblue", outline="blue")
            self.boutons[(grande_ligne, grande_col, ligne, col)].destroy()

    # Afficher le joueur dont c'est le tour
    def annoncer_joueur(self):
        self.canvas.delete(self.annonce_joueur)
        self.annonce_joueur=self.canvas.create_text(500,20, text=f"C'est au joueur {self.joueur} de jouer", font=("Times new roman", 15, "bold"), fill="black")

    # Dessiner un encadrement où le joueur doit jouer s'il y est obligé
    def dessiner_encadrement(self):
        # on dessine un encadrement dans les cas où le joueur est obligé de jouer:
        # c'est-à-dire si pas de gagnant avant et si la case où il doit jouer n'est pas déjà gagnée
        ligne=self.case[0]
        col=self.case[1]
        if self.gagnant_sous_grille == False and self.gagnantsSousGrilles[ligne][col] == None:
            if self.case_a_jouer != None:  # si on n'est pas au 1er tour, on supprime l'ancien encadrement
                self.canvas.delete(self.case_a_jouer)
            self.case_a_jouer = self.canvas.create_rectangle(196 + col * 200, 96 + ligne * 200, 196 + col * 200 + 200,
                                                                96 + ligne * 200 + 200, fill="", outline="green", width=6)
        else:
            self.canvas.delete(self.case_a_jouer)


    # Vérifier si le case est jouable selon les règles ultimate tic tac toe :
    def test_jouer(self,gl, gc, l, c):

        #Le joueur peut joueur où il veut:
        #SI c'est le premier tour OU l'autre vient de gagner OU la cas eoù il doit jouer est gagnée

        if self.case == None or self.gagnant_sous_grille==True or self.gagnantsSousGrilles[self.case[0]][self.case[1]]!=None:
            self.gagnant_sous_grille=False
            
            self.jouer(gl, gc, l, c)
        else:
            if (gl,gc)==self.case:
                self.jouer(gl, gc, l, c)
    def deckActuel(self):
        if self.joueur=='X':
            self.color="red"
            self.deck1.drop(self.deck1[self.deck1["#"] == self.pokeChoisiDeck1["#"]].index, inplace=True)
            return self.pokeChoisiDeck1
        else:
            self.color="blue"
            
            self.deck2.drop(self.deck2[self.deck2["#"] == self.pokeChoisiDeck2["#"]].index, inplace=True)
            return self.pokeChoisiDeck2
    def jouer(self, gl, gc, l, c):
        pokemon=self.deckActuel()
        if pokemon is None:
            return
        
        #si il n'y pas déjà un pokemon sur la case, je joueur en pose un
        if self.pokemons_places[gl][gc][l][c] == None:
            self.placerPokemon(gl, gc, l, c)
            
        #si l'adversaire a déjà mis un pokemon sur cette case, on lance un combat pour décider qui remporte la case
        elif self.pokemons_places[gl][gc][l][c][0] != self.joueur:
            self.initierCombat(gl, gc, l, c,pokemon)
        #si le joueur a déjà mis un pokemon sur la case, on fait comme si il n'avait cliqué sur rien
        else:
            return
        #vérification de victoire locale et globale
        if self.verifVictoire(self.grille[gl][gc])==True:
            self.changer_gagnant_sousgrille(gl,gc)
            self.gagnant_sous_grille=True 
        self.resetPokemonChoisi()
        if self.verifVictoire(self.gagnantsSousGrilles)==True:
            print("GAGNANT")
            self.changer_gagnant_grandegrille()
            return
        
        

        #on retient la case qui vient d'être jouée pour obliger le suivant à y jouer
        self.case = (l, c)

        #changement de tour
        if self.joueur=='X':
            self.joueur='O'
        else:
            self.joueur='X'

        #écrire sur la fenêtre le joueur dont c'est le tour
        self.annoncer_joueur()

        #dessin d'un encadrement graphique pour le prochain joueur:
        self.dessiner_encadrement()
    def verifVictoire(self, grille):
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
        return False

    def placerPokemon(self, gl, gc, l, c):
        if self.pokemons_places[gl][gc][l][c]==-1:
            return
        pokemon=self.deckActuel()
        print(self.color)
        if pokemon is None:
            return
        
        #on place le pokemon dans les tableaux
        self.pokemons_places[gl][gc][l][c] = (self.joueur, pokemon,pokemon["#"])
        self.grille[gl][gc][l][c] = self.joueur

        #on le place graphiquement
        image=self.tailleImage(pathPokemon(pokemon["#"], pokemon["Name"].lower()),50,50)
        self.boutons[(gl, gc, l, c)].configure(image=image, compound="top" , bg=self.color, highlightbackground=self.color, highlightthickness=5)
        self.boutons[(gl, gc, l, c)].image = image
        
    def resetPokemonChoisi(self):
        if self.joueur=='X':
            self.pokeChoisiDeck1=None
            self.color=None
            self.selected_label_j1.config(text="Aucun Pokémon ")
        else:
            self.pokeChoisiDeck2=None
            self.color=None
            self.selected_label_j2.config(text="Aucun Pokémon ")

    def initierCombat(self, gl, gc, l, c,pokemon):
        pokemonAdversaire = self.pokemons_places[gl][gc][l][c][1]
        pokemonAttaque = pokemon
        combat = PokemonApp(pokemonAttaque, pokemonAdversaire,self.fenetre)
        combat.mainloop()
        gagnant_combat = combat.winner
        if gagnant_combat["#"] == pokemonAttaque["#"]:
            self.grille[gl][gc][l][c] = self.joueur
            self.boutons[(gl, gc, l, c)].configure(text=self.joueur,image="",compound=None, bg=self.color, highlightbackground=self.color, highlightthickness=5,fg=self.color)
            self.boutons[(gl, gc, l, c)].image = None
            self.pokemons_places[gl][gc][l][c] = -1
            if self.joueur=='X':
                self.deck2.loc[len(self.deck2)] = pokemonAdversaire
                self.deck2.loc[len(self.deck2)-1, "Level"] += 1
                print(self.deck2.loc[len(self.deck2)-1])
            else:
                self.deck1.loc[len(self.deck1)] = pokemonAdversaire
                self.deck1.loc[len(self.deck1)-1, "Level"] += 1
                print(self.deck1.loc[len(self.deck1)-1])
                

        elif gagnant_combat["#"] == pokemonAdversaire["#"]:
            if self.joueur=='X':
                self.grille[gl][gc][l][c] = 'O'
                self.deck2.loc[len(self.deck2)] = pokemonAttaque
                self.deck2.loc[len(self.deck2)-1, "Level"] += 1
                self.boutons[(gl, gc, l, c)].configure(text='O',image="",compound=None, bg=self.color, highlightbackground=self.color, highlightthickness=5,fg=self.color)
                self.boutons[(gl, gc, l, c)].image = None
                self.pokemons_places[gl][gc][l][c] = -1
                
            else:
                self.grille[gl][gc][l][c] = 'X'
                self.deck1.loc[len(self.deck1)] = pokemonAttaque
                self.deck1.loc[len(self.deck1)-1, "Level"] += 1
                print(self.deck1.loc[len(self.deck1)-1])
                self.boutons[(gl, gc, l, c)].configure(text='X',image="",compound=None, bg=self.color, highlightbackground=self.color, highlightthickness=5,fg=self.color)
                self.boutons[(gl, gc, l, c)].image = None
                self.pokemons_places[gl][gc][l][c] = -1
                
    


       
        

    # Création des boutons pour cliquer dans les cases de jeu
    def cases (self):
        self.boutons = {}
        for grande_ligne in range(3):
            for grande_col in range(3):
                for ligne in range(3):
                    for col in range(3):
                        self.boutons[(grande_ligne,grande_col,ligne,col)]=tk.Button(self.canvas,bg="light blue", relief="flat", borderwidth=0, activebackground="white",command=lambda gl=grande_ligne, gc=grande_col, l=ligne, c=col: self.test_jouer(gl, gc, l, c) )
                        self.boutons[(grande_ligne,grande_col,ligne,col)].place(x=200+200*grande_col+62*col+8, y=100+200*grande_ligne+62*ligne+8, width=58-col, height=58-ligne)

    # Afficher la fenêtre graphique
    def afficher(self):
        self.fenetre.mainloop()


