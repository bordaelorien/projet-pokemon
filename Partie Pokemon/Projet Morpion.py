import tkinter as tk
import deck_builder as db
import data_loader as dl
from paths import *
from tkinter import ttk
class Jeu () :

    def __init__(self):
        # GRAPHIQUE :
        self.fenetre= tk.Tk()
        self.canvas= tk.Canvas(self.fenetre, width=1920, height=1080, bg="light blue")
        self.canvas.pack()

        # STRUCTURE :
        self.grille = [[[['' for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
        
        # Statut de victoire pour chaque sous-grille (None, 'X' ou 'O')
        self.gagnants_sousgrilles = [[None for i in range(3)] for i in range(3)]

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
        
        

    def bouton_deck(self):
        bouton_deck1 = tk.Button(self.fenetre, text="Deck Joueur 1",bg="light blue", command=lambda: self.afficher_deck(True))
        bouton_deck1.place(x=900, y=100,width=200,height=30)
        self.selected_label_j1 = tk.Label(self.fenetre,text="Aucun Pokémon ",bg="light blue",fg="#2b2b2b",font=("Arial", 16, "bold"))
        self.selected_label_j1.place(x=900, y=140)
        bouton_deck2 = tk.Button(self.fenetre, text="Deck Joueur 2",bg="light blue", command=lambda: self.afficher_deck(False))
        bouton_deck2.place(x=1200, y=100,width=200,height=30)
        self.selected_label_j2 = tk.Label(self.fenetre,text="Aucun Pokémon ",bg="light blue",fg="#2b2b2b",font=("Arial", 16, "bold"))
        self.selected_label_j2.place(x=1200, y=140)
    def afficher_deck(self,bin):
        if bin:
            deck = self.deck1.copy()
            player = 1
        else:
            deck = self.deck2.copy()
            player = 2

        grouped = deck.groupby("Type 1")
        root = tk.Toplevel(self.fenetre)
        root.title("Deck Pokémon")
        root.geometry("900x900")     

        # ---- CONTENEUR GLOBAL ----
        container = tk.Frame(root)
        container.pack(fill="both", expand=True)

        # ---- CANVAS + SCROLLBAR ----
        canvas = tk.Canvas(container, bg="#2b2b2b")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # ---- FRAME SCROLLABLE ----
        scroll_frame = tk.Frame(canvas, bg="#2b2b2b")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        scroll_frame.columnconfigure(0, weight=1)
        scroll_frame.columnconfigure(1, weight=1)

        # mise à jour automatique du scrollregion
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        types = list(grouped.groups.keys())
        mid = len(types) // 2   # moitié des types
        col = 0   # on commence dans la colonne gauche
        row = 0     


        for type_name, group in grouped:
            if row >= (len(types) + 1) // 2:
                col = 1  # passer à la colonne de droite
                row = 0  # réinitialiser la ligne
            imageType= tk.PhotoImage(file=pathType(type_name.lower()))
            
            lf = tk.LabelFrame(scroll_frame, fg="white", bg="#1e1e1e",font=("Arial", 16, "bold"), padx=10, pady=10)
            
            lf.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            row += 1
            label=tk.Label(lf,image=imageType, bg="#1e1e1e")
            label.image=imageType
            label.pack()

            for _, row in group.iterrows():

                image= tk.PhotoImage(file=pathPokemon(row["#"], row["Name"].lower()))
                image=image.subsample(2,2)

                #self.deck_images.append(image) 
                btn = tk.Button(lf, text=row["Name"],compound="top",image=image,font=("Pokemon Solid", 14),bg="#3c3c3c", fg="black",command=lambda r=row: row)
                btn.image=image
                btn.pack(fill="both", pady=4)
    

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
        self.canvas.create_text(300 + 200 * grande_col, 200 + 200 * grande_ligne, text=self.joueur, font=("Arial", 100, "bold"), fill="blue")
        self.gagnants_sousgrilles[grande_ligne][grande_col]=self.joueur

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
        if self.gagnant_sous_grille == False and self.gagnants_sousgrilles[ligne][col] == None:
            if self.case_a_jouer != None:  # si on n'est pas au 1er tour, on supprime l'ancien encadrement
                self.canvas.delete(self.case_a_jouer)
            self.case_a_jouer = self.canvas.create_rectangle(196 + col * 200, 96 + ligne * 200, 196 + col * 200 + 200,
                                                                96 + ligne * 200 + 200, fill="", outline="green", width=6)
        else:
            self.canvas.delete(self.case_a_jouer)

    # Placer le joueur dans la structure et dans le graphique + vérification si gagnant :
    def gagnerCase(self,grande_ligne,grande_col,ligne,col):

        #on place le joueur dans la structure
        self.grille[grande_ligne][grande_col][ligne][col] = self.joueur

        #on place le pion graphiquement :
        self.jouer_graphiquement (grande_ligne,grande_col,ligne,col)

        #vérification de victoire locale
        if self.verif_victoire(self.grille[grande_ligne][grande_col])==True:
                self.gagnants_sousgrilles[grande_ligne][grande_col]=self.joueur
                self.changer_gagnant_sousgrille(grande_ligne,grande_col)
                self.gagnant_sous_grille=True  #booléen: est-ce que le joueur vient de gagner une sous-grille ?

        #vérification de victoire globale
        if self.verif_victoire(self.gagnants_sousgrilles):
            self.gagnant = self.joueur
            self.changer_gagnant_grandegrille()


    # Vérifier si le case est jouable selon les règles ultimate tic tac toe :
    def test_jouer(self,gl, gc, l, c):

        #Le joueur peut joueur où il veut:
        #SI c'est le premier tour OU l'autre vient de gagner OU la cas eoù il doit jouer est gagnée

        if self.case == None or self.gagnant_sous_grille==True or self.gagnants_sousgrilles[self.case[0]][self.case[1]]!=None:
            self.gagnant_sous_grille=False
            
            self.jouer(gl, gc, l, c)
        else:
            if (gl,gc)==self.case:
                self.jouer(gl, gc, l, c)
    
    def jouer(self, gl, gc, l, c):
        #si il n'y pas déjà un pokemon sur la case, je joueur en pose un
        if self.pokemons_places[gl][gc][l][c] == None:
            self.placerPokemon(gl, gc, l, c)
        #si l'adversaire a déjà mis un pokemon sur cette case, on lance un combat pour décider qui remporte la case
        elif self.pokemons_places[gl][gc][l][c][0] != self.joueur:
            self.initierCombat(gl, gc, l, c)
        #si le joueur a déjà mis un pokemon sur la case, on fait comme si il n'avait cliqué sur rien
        else:
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

    def placerPokemon(self, gl, gc, l, c, pokemon):
        #on place le pokemon dans le tableau
        self.pokemons_places[gl][gc][l][c] = (self.joueur,pokemon["#"])

        #on le place graphiquement
        image = tk.PhotoImage(file=pathPokemon(pokemon["#"], pokemon["Name"].lower()))
        image = image.subsample(11, 11)
        self.boutons[(gl, gc, l, c)].configure(image=image, compound="top" , text=f"Joueur : {self.joueur}")
        self.boutons[(gl, gc, l, c)].image = image

    def initierCombat(self, gl, gc, l, c):
        pokemon_adversaire = self.pokemons_places[gl][gc][l][c][1]
        pokemon_joueur = "bulbasaur"
        #gagnant = combat(pokemon_joueur, pokemon_adversaire)
        #la fonction 'combat' déclenche un combat pokemon et renvoie qui est le gagnant
        gagnant = self.joueur

        #si le joueur gagne le combat, il remporte la case définitivement
        if gagnant == self.joueur:
            self.gagnerCase(gl, gc, l, c)
        

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
        


fenetre= Jeu()
fenetre.dessiner_lignes()
fenetre.cases()
fenetre.afficher()