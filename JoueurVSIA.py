import tkinter as tk
import deck_builder as db
import data_loader as dl
from paths import *
from tkinter import ttk
from PIL import Image, ImageTk
from affichageCombatJvsIA import PokemonApp
import pandas as pd
import random
class JoueurVSIA() :

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
        self.humain = 'X'
        self.IA = 'O'
        self.coupsJoueurX=[]
        # Annonce graphique du joueur en cours
        self.annonce_joueur=self.canvas.create_text(500,20, text="Placer votre Pokemon pour commencer", font=("Times new roman", 15, "bold"), fill="black")

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
        self.fenetre.mainloop()

        
    def tailleImage(self,path, sizeX,sizeY):
        """
        Redimensionne une image à une taille donnée et la convertit en PhotoImage pour Tkinter."""
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
        label_deck=tk.Label(self.fenetre,text="Votre Deck",bg="light blue",fg="red",font=("Arial", 16, "bold"))
        label_deck.place(x=950, y=10)
        label_deck=tk.Label(self.fenetre,text="Deck IA",bg="light blue",fg="blue",font=("Arial", 16, "bold"))
        label_deck.place(x=1250, y=10)
        self.selected_label_j1 = tk.Label(self.fenetre,text="Aucun Pokémon ",bg="light blue",fg="red",font=("Arial", 16, "bold"))
        self.selected_label_j1.place(x=900, y=60)
        self.selected_label_j2 = tk.Label(self.fenetre,text="Aucun Pokémon ",bg="light blue",fg="blue",font=("Arial", 16, "bold"))
        self.selected_label_j2.place(x=1200, y=60)

    def afficherDecks(self):
        """
        Affiche les boutons pour chaque type de Pokémon dans les decks des joueurs.
        """
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
        """
        Met à jour le label du Pokémon sélectionné pour le joueur spécifié.
        """
        if joueur == 1:
            self.selected_label_j1.config(text=pokemonName)
            self.pokeChoisiDeck1=row
        else:
            self.selected_label_j2.config(text=pokemonName)
            self.pokeChoisiDeck2=row




    def dessiner_mini_morpion(self,ligne,col):
        """
        Dessine un mini morpion à la position spécifiée par ligne et colonne.
        """
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
    def dessiner_lignes (self): 
        """
        Dessine les lignes principales du morpion et les mini morpions."""
        self.canvas.create_line(396, 100, 396, 700, width=6, fill="red")
        self.canvas.create_line(596, 100, 596, 700, width=6, fill="red")
        self.canvas.create_line(200, 296, 800, 296, width=6, fill="red")
        self.canvas.create_line(200, 496, 800, 496, width=6, fill="red")
        for ligne in range(3):
            for col in range(3):
                self.dessiner_mini_morpion(ligne,col)


    # Regarder les alignement de pions dans une grille donnée
    def verif_victoire(self, grille):
        """
        Vérifie si le joueur actuel a gagné dans la grille donnée.
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

    # Ajouter dans la sous-grille le gagnant et y détruire les boutons :
    def changer_gagnant_sousgrille(self,grande_ligne,grande_col):
        """
        Met à jour la sous-grille gagnée par le joueur actuel et détruit les boutons correspondants.
        """
        for ligne in range(3):
            for col in range(3):
                if self.boutons[(grande_ligne, grande_col, ligne, col)]:
                    self.boutons[(grande_ligne, grande_col, ligne, col)].destroy()
        self.canvas.create_rectangle(200 + 200 * grande_col, 100 + 200 * grande_ligne, 392 + 200 * grande_col,292 + 200 * grande_ligne, fill="light blue", outline="light blue", width=1)
        self.canvas.create_text(300 + 200 * grande_col, 200 + 200 * grande_ligne, text=self.joueur, font=("Arial", 100, "bold"), fill=self.color)
        self.case= None
        self.gagnantsSousGrilles[grande_ligne][grande_col]=self.joueur

    # Mettre fin à la partie quand un joueur a gagné
    def changer_gagnant_grandegrille(self):
        """
        Affiche un message de fin de partie indiquant le gagnant.
        """

        #nouveau canvas par dessus la grille
        self.canvas.delete("all")
        self.canvas.create_text(500, 350, text=f"Félicitations !\n\nLe joueur {self.joueur} remporte la partie", font=("Times new roman", 25, "bold"), fill="black")
        self.canvas.create_text(500, 500, text="Cliquez sur la touche f pour fermer la fenêtre", font=("Halvetica", 10, "bold italic"), fill="red")
        self.fenetre.bind("<Key-f>", lambda event: self.fenetre.destroy())


    def verif_grille_pleine(self, grille):
        lignes=len(grille)
        col=len(grille[1])
        for ligne in range(lignes):
            for c in range(col):
                if grille[ligne][c]=='':
                    return False

        return True
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

    def annoncer_joueur(self):
        self.canvas.delete(self.annonce_joueur)
        if self.joueur=='X':
            self.annonce_joueur=self.canvas.create_text(500,20, text="C'est à votre tour de jouer", font=("Times new roman", 15, "bold"), fill="red")
        

 
    # TESTER SI UN JOUEUR PEUT JOUER ET JOUER EFFECTIVEMENT
    def test_jouer(self,gl, gc, l, c):
        """
        Teste si un joueur peut jouer à la position spécifiée et effectue le coup si possible.
        """

        if self.case == None or self.gagnant_sous_grille==True or self.gagnantsSousGrilles[self.case[0]][self.case[1]]!=None:
            self.gagnant_sous_grille=False
            
            self.jouer(gl, gc, l, c)
        else:
            if (gl,gc)==self.case:
                self.jouer(gl, gc, l, c)
    
    def handle_click(self, gl, gc, l, c):
        """
        Gestion du clic sur une case par le joueur humain.
        On laisse le joueur humain jouer normalement, puis on déclenche
        le coup de l'IA si la partie continue.
        """
        # On ignore les clics si la partie est finie ou si ce n'est pas le tour de l'humain
        if self.gagnant!= None or self.joueur != self.humain:
            return
        self.test_jouer(gl, gc, l, c)
        # Après le tour du joueur, si la partie n'est pas finie et que c'est à l'IA de jouer, on lance IA_move
        if self.gagnant == None and self.joueur == self.IA:
            self.IA_move()

    def IA_move(self):
        """
        Pour l'instant aleatoire
        """
        if self.gagnant is not None or self.joueur != self.IA:
            return

        if len(self.deck2) == 0:
            return

        # Sélection d'un Pokémon aléatoire pour l'IA
        idx = random.choice(self.deck2.index.tolist())
        self.pokeChoisiDeck2 = self.deck2.loc[idx]
        self.updateColor("O")

        # Construction de la liste des coups possibles
        coups_possibles = []

        # Détermination des sous-grilles autorisées
        if self.case== None or self.gagnant_sous_grille or self.gagnantsSousGrilles[self.case[0]][self.case[1]] != None:
            # IA peut jouer dans n'importe quelle sous-grille non gagnée
            sous_grilles = [(gl, gc) for gl in range(3) for gc in range(3)
                            if self.gagnantsSousGrilles[gl][gc] == None]
        else:
            # IA obligée de jouer dans la sous-grille self.case si elle n'est pas déjà gagnée
            if self.gagnantsSousGrilles[self.case[0]][self.case[1]] == None:
                sous_grilles = [self.case]
            else:
                sous_grilles = []

        # Pour chaque sous-grille autorisée, on regarde les cases encore disponibles
        for gl, gc in sous_grilles:
            for l in range(3):
                for c in range(3):
                    # On ne joue pas sur une case déjà résolue (valeur -1)
                    if self.pokemons_places[gl][gc][l][c] != -1 and self.grille[gl][gc][l][c] == '' and (gl, gc, l, c) not in self.coupsJoueurX:
                        coups_possibles.append((gl, gc, l, c))

        
        if not coups_possibles:
            return

        gl, gc, l, c = random.choice(coups_possibles)
        self.test_jouer(gl, gc, l, c)

    def PokemonChoisi(self):
        """
        Retourne le Pokémon choisi par le joueur actuel et le retire de son deck.
        """
        if self.joueur == 'X':
            # Joueur X (Humain)
            self.updateColor("X")
            if self.pokeChoisiDeck1 is None:
                return None
            self.deck1.drop(self.deck1[self.deck1["#"] == self.pokeChoisiDeck1["#"]].index, inplace=True)
            return self.pokeChoisiDeck1
        else:
            # Joueur O (IA)
            self.updateColor("O")
            # Si aucun Pokémon n'a encore été choisi pour l'IA, on en prend un aléatoirement
            if self.pokeChoisiDeck2 is None:
                if len(self.deck2) == 0:
                    return None
                idx = random.choice(self.deck2.index.tolist())
                self.pokeChoisiDeck2 = self.deck2.loc[idx]
            if self.pokeChoisiDeck2 is None:
                return None
            self.deck2.drop(self.deck2[self.deck2["#"] == self.pokeChoisiDeck2["#"]].index, inplace=True)
            return self.pokeChoisiDeck2

    def jouer(self, gl, gc, l, c):
        pokemon = self.PokemonChoisi()
        if pokemon is None:
            return
        
        case = self.pokemons_places[gl][gc][l][c]
        self.coupsJoueurX.append((gl, gc, l, c))
        #Case vide = placement simple
        if case is None:
            self.placerPokemon(gl, gc, l, c)

        #Case occupée par l'adversaire = combat
        elif self.pokemons_places[gl][gc][l][c][0] != self.joueur and self.pokemons_places[gl][gc][l][c] != -1:
            if self.joueur=="O":
                self.initierCombat(gl, gc, l, c, pokemon,IA_turn=True)
            else:
                self.initierCombat(gl, gc, l, c, pokemon)

        #Case déjà gagnée = on ignore
        else:
            return

        # Verifications après le placement/combat
        if self.verif_victoire(self.grille[gl][gc]):
            self.changer_gagnant_sousgrille(gl, gc)
            self.gagnant_sous_grille = True

        self.resetPokemonChoisi()

        # Verfication victoire grande grille
        if self.verifVictoire(self.gagnantsSousGrilles):
            self.changer_gagnant_grandegrille()
            return

        # Tour suivant
        self.case = (l, c)
        if self.joueur == 'X':
            self.joueur = 'O'
        else:
            self.joueur = 'X'
        self.annoncer_joueur()
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
        pokemon=self.PokemonChoisi()
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
    def updateColor(self,joueur=None):
        if joueur == None:
            return
        
        if joueur=='X':
            self.color="red"
        else:
            self.color="blue"
    def initierCombat(self, gl, gc, l, c,pokemon,IA_turn=False):
        pokemonIA = self.pokemons_places[gl][gc][l][c][1]
        pokemonJ = pokemon
        if IA_turn:
            pokemonIA, pokemonJ = pokemonJ, pokemonIA

        combat = PokemonApp(pokemonJ, pokemonIA,self.fenetre)
        combat.mainloop()
        gagnant_combat = combat.winner
        print(gagnant_combat["Name"],pokemonIA["Name"])
        if gagnant_combat["#"] == pokemonIA["#"]:
            gagnant='O'
            self.color="blue"
            pokemonPerdant = pokemonJ
        else:
            gagnant = 'X'
            self.color="red"
            pokemonPerdant = pokemonIA
        
        self.grille[gl][gc][l][c] = gagnant
        print("Gagnant du combat :", gagnant)
        self.updateColor(gagnant)
        self.boutons[(gl, gc, l, c)].configure(text=gagnant,image="",compound=None, bg=self.color, highlightbackground=self.color, highlightthickness=5,fg=self.color)
        self.boutons[(gl, gc, l, c)].image = None
        self.pokemons_places[gl][gc][l][c] = -1

        if gagnant=='X':
            self.deck2.loc[len(self.deck2)] = pokemonPerdant
            self.deck2.loc[len(self.deck2)-1, "Level"] += 1
        else:
            self.deck1.loc[len(self.deck1)] = pokemonPerdant
            self.deck1.loc[len(self.deck1)-1, "Level"] += 1

                
                
    

    # Création des boutons pour cliquer dans les cases de jeu
    def cases (self):
        self.boutons = {}
        for grande_ligne in range(3):
            for grande_col in range(3):
                for ligne in range(3):
                    for col in range(3):
                        self.boutons[(grande_ligne,grande_col,ligne,col)]=tk.Button(self.canvas,bg="light blue", relief="flat", borderwidth=0, activebackground="white",command=lambda gl=grande_ligne, gc=grande_col, l=ligne, c=col: self.handle_click(gl, gc, l, c) )
                        self.boutons[(grande_ligne,grande_col,ligne,col)].place(x=200+200*grande_col+62*col+8,y=100+200*grande_ligne+62*ligne+8, width=58-col, height=58-ligne)

    # Afficher la fenêtre graphique
    def afficher(self):
        self.fenetre.mainloop()
