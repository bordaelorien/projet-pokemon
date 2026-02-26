
import tkinter as tk
from tkinter import StringVar, ttk
from PIL import Image, ImageTk

import data_loader as dl
import game_logic as gl
from images import *
from paths import *

class PokemonJVSIA():
    def __init__(self, p1, p2, fenetrePrincipale=None):
        try:
            self.fenetre=tk.Toplevel(fenetrePrincipale)
        except:
            self.fenetre=tk.Tk()
        
        self.fenetre.title("Pokémon Battle")
        self.fenetre.geometry("1600x900")
        self.bg_color = "#323232"
        self.fg_color = "#FFFFFF"
        self.fenetre.configure(bg=self.bg_color)

        # Chargement des données
        self.df_pokemon = dl.dfPokemon()
        self.df_attacks = dl.dfAttaques()
        self.logic = gl.GameLogic(self.df_attacks)
        # Déterminer premier attaquant
        self.pJoueur, self.pIA = p1.copy(), p2.copy()
        # Tour actif
        self.pokemon_actif,self.pokemon_passif=self.logic.premierAttaquant(self.pJoueur.copy(),self.pIA.copy())
        self.nameAttaquePJ={}
        self.nameAttaquePIA={}
        self.historique = []  # Liste des actions du combat
        self.creer_bouton_historique()

        # Interface
        self.HP = {}
        self.image = []
        self.winner = None

        self.interfaceUtilisateur()
    

        # Si l'IA commence
        if self.pokemon_actif["#"] == self.pIA["#"]:
            self.tour_IA(self.pIA, self.pJoueur)

        

    # ----------------------------------------------------
    # INTERFACE
    # ----------------------------------------------------
    # BOUTON HISTORIQUE
    def creer_bouton_historique(self):
        """
        Crée le bouton qui ouvre l'historique du combat.
        """
        btn = tk.Button(
            self.fenetre,
            text="Historique",
            bg="#FFD700",    
            fg="#0033CC",    
            font=("Pokemon Solid", 18),
            command=self.afficher_historique
        )
        btn.place(x=20, y=20)
    def afficher_historique(self):
        """
        Ouvre une fenêtre affichant tout l'historique du combat.
        """
        top = tk.Toplevel(self.fenetre)
        top.title("Historique du combat")
        top.geometry("500x600")
        top.configure(bg="#323232")

        tk.Label(
            top,
            text="Historique du combat",
            font=("Pokemon Solid", 24),
            fg="#FFD700",
            bg="#323232"
        ).pack(pady=10)

        # Zone scrollable
        cadre = tk.Frame(top, bg="#323232")
        cadre.pack(fill="both", expand=True)

        canvas = tk.Canvas(cadre, bg="#323232", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(cadre, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        frame_interior = tk.Frame(canvas, bg="#323232")
        canvas.create_window((0, 0), window=frame_interior, anchor="nw")

        # Remplir avec l'historique
        for action in self.historique:
            tk.Label(
                frame_interior,
                text=action,
                fg="#FFFFFF",
                bg="#323232",
                font=("Arial", 14)
            ).pack(anchor="w", padx=10, pady=5)

        frame_interior.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


    def interfaceUtilisateur(self):
        """
         Configure l'interface utilisateur pour le combat.
        """
        title = tk.Label(self.fenetre,text="Pokémon Battle",font=("Pokemon Solid", 32),bg=self.bg_color,fg="#FFD700",)
        title.pack(pady=10)
        self.combat_frame = tk.Frame(self.fenetre, bg=self.bg_color)
        self.combat_frame.pack(fill="both", expand=True)

        self.messagePokemon = tk.Label(self.combat_frame,text=f"{self.pokemon_actif['Name']} attaque !",bg=self.bg_color,fg=self.fg_color,font=("Arial", 16, "bold"))
        self.messagePokemon.place(x=600, y=50)

        self.affichage_pokemon_combat([self.pJoueur, self.pIA])

    def affichage_pokemon_combat(self, liste_pokemon):
        """
        Affiche les Pokémon en combat avec leurs informations.
        """
        for i, pokemon in enumerate(liste_pokemon):
            deltaX = i * 900
            image = imagePokemon(str(pokemon["#"]), pokemon["Name"])
            self.image.append(image)

            label_img = tk.Label(self.combat_frame, image=image, bg=self.bg_color)
            label_img.image = image
            label_img.place(x=100 + deltaX, y=150)

            self.affichage_nom_pokemon(pokemon, 100 + deltaX, 50, 24)
            self.points_vie_pokemon(pokemon, 100 + deltaX, 90)
            self.affichage_type_pokemon(pokemon, 100 + deltaX, 130)

        self.affichage_attaques_disponibles(liste_pokemon[0], 100, 600, liste_pokemon[1])

        # Attaques IA 
        self.affichage_attaques_disponibles(liste_pokemon[1], 1000, 600, liste_pokemon[0])

    def affichage_nom_pokemon(self, pokemon, x, y, size):
        """
        Affiche le nom du Pokémon à une position donnée.
        """
        tk.Label(self.combat_frame,text=str(pokemon["Name"]),font=("Pokemon Solid", size),bg=self.bg_color,fg=self.fg_color).place(x=x, y=y)

    def points_vie_pokemon(self, pokemon, x, y):
        """
        Affiche les points de vie du Pokémon à une position donnée."""
        var = StringVar(value="HP: " + str(pokemon["HP"]))
        self.HP["hp" + str(pokemon["#"])] = var
        tk.Label(self.combat_frame,textvariable=var,font=("Pokemon Solid", 16),bg=self.bg_color,fg=self.fg_color).place(x=x, y=y)

    def affichage_type_pokemon(self, pokemon, x, y):
        """
        Affiche les types du Pokémon à une position donnée.
        """
        self.afficher_image_type(pathType1(pokemon), x, y)

        path_type2 = pathType2(pokemon)
        if path_type2:
            self.afficher_image_type(path_type2, x + 144, y)

    def afficher_image_type(self, image_path, x, y):
        """
        Affiche une image de type Pokémon à une position donnée.
        """
        image = Image.open(image_path)
        tk_img = ImageTk.PhotoImage(image)

        label = tk.Label(self.combat_frame, image=tk_img, bg=self.bg_color)
        label.image = tk_img
        label.place(x=x, y=y)


    def affichage_attaques_disponibles(self, pokemon, x, y, cible):
        """
        Affiche les attaques disponibles pour un Pokémon à une position donnée.
        """
        attaques = self.logic.attaques_disponibles(pokemon)
        ESP_X = 200

        IA_turn = (pokemon["#"] == self.pIA["#"])

        for i, (nom_atk, attaque) in enumerate(attaques.iterrows()):
            if IA_turn:
                self.nameAttaquePIA[nom_atk]=attaque["Nom_Attaque"]
            else:
                self.nameAttaquePJ[nom_atk]=attaque["Nom_Attaque"]

            bouton_x = x + (i % 2) * ESP_X
            bouton_y = y + (i // 2) * 50

            tk.Button(
                self.combat_frame,
                text=attaque["Nom_Attaque"],
                bg="#444444",
                fg="black",
                font=("Pokemon Solid", 16),
                state="disabled" if IA_turn else "normal",
                command=lambda atk_nom=nom_atk, atk=pokemon, defp=cible: self.faire_degats(atk, defp, atk_nom)).place(x=bouton_x, y=bouton_y)


    def tour_IA(self, ia_pokemon, pokeDefenseur):
        """
        Gère le tour de l'IA en choisissant et en exécutant une attaque.
        """
        attaques = self.logic.attaques_disponibles(ia_pokemon)

        meilleur_atk = None
        meilleur_deg = -1

        for nom_atk, attaque in attaques.iterrows():
            deg = self.logic.degat(ia_pokemon, pokeDefenseur.copy(), nom_atk)
            print(deg, nom_atk)
            if deg > meilleur_deg:
                meilleur_deg = deg
                meilleur_atk = nom_atk

        self.faire_degats(ia_pokemon, pokeDefenseur, meilleur_atk, IA_turn=True)

    # ----------------------------------------------------
    # COMBAT / DÉGÂTS
    # ----------------------------------------------------

    def faire_degats(self, attaquant, defenseur, attaque, IA_turn=False):
        """
        Gère l'exécution d'une attaque et met à jour l'état du combat.
        """

        if not IA_turn:
            self.messagePokemon.config(text=f"{attaquant['Name']} attaque avec {self.nameAttaquePJ[attaque]} !")

        if attaquant["Name"] != self.pokemon_actif["Name"]:
            return

        if self.logic.estIlPerdant(defenseur):
            return

        damage = self.logic.degat(attaquant, defenseur, attaque)
        print(damage)
        defenseur["HP"] -= damage
        self.historique.append(f"{attaquant['Name']} utilise {self.nameAttaquePJ[attaque] if not IA_turn else self.nameAttaquePIA[attaque]} → {defenseur['Name']} perd {damage} HP")


        # Mise à jour graphique
        self.HP["hp" + str(defenseur["#"])].set(f"HP: {defenseur['HP']}")

        # Changement de tour
        self.pokemon_actif, self.pokemon_passif = self.pokemon_passif,self.pokemon_actif

        # KO 
        if self.logic.estIlPerdant(defenseur):
            self.historique.append(f"{attaquant['Name']} met K.O. {defenseur['Name']} !")

            self.messagePokemon.config(text=f"{attaquant['Name']} a gagné le combat !")

            # Reset HP
            if defenseur["#"] == self.pJoueur["#"]:
                defenseur["HP"] = self.pJoueur["HP"]
            else:
                defenseur["HP"] = self.pIA["HP"]

            self.winner = attaquant

            # Bouton quitter
            style = ttk.Style() # Obligation de creer un style pour mac car il ne reconnait pas les bg dans les boutons
            style.theme_use("clam")
            style.configure("Quit.TButton",font=("Pokemon Solid", 30),background="#FF0000",foreground="#FFFFFF")
            btnQuitter = ttk.Button(self.combat_frame,text="Quitter",style="Quit.TButton",command=self.fincombat)
            btnQuitter.place(x=600, y=500)
            return

        # Tour IA
        if self.pokemon_actif["#"] == self.pIA["#"]:
            self.tour_IA(self.pIA, self.pJoueur)

    def fincombat(self):
        self.HP = {}
        self.fenetre.withdraw()
        self.fenetre.quit()
