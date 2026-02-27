# app.py
import tkinter as tk
from tkinter import StringVar, ttk
from PIL import Image, ImageTk

import data_loader as dl
import deck_builder as db
import game_logic as gl
from images import *
from paths import path
from time import sleep


class PokemonApp(tk.Toplevel):
    def __init__(self, p1, p2, fenetrePrincipale=None):
        super().__init__(fenetrePrincipale)
        self.title("Pokémon Battle")
        self.geometry("1600x900")
        self.bg_color = "#323232"
        self.fg_color = "#FFFFFF"
        self.configure(bg=self.bg_color)

        # Chargement des données
        self.df_pokemon = dl.dfPokemon()
        self.df_attacks = dl.dfAttaques()
        self.logic = gl.GameLogic(self.df_attacks)
        self.pJ, self.pIA = p1, p2
        # Déterminer premier attaquant
        self.pokemon_left, self.pokemon_right = self.pJ, self.pIA
        hp_left = self.pokemon_left["HP"]
        # Tour actif
        self.pokemon_actif,self.pokemon_passif=self.logic.premierAttaquant(self.pokemon_left.copy(),self.pokemon_right.copy())

        # Interface
        self.objet = {}
        self.image = []
        self.winner = None

        self.interfaceUtilisateur()
        self.logic.JeuCombat(self.pokemon_actif, self.pokemon_passif)

        # Si l'IA commence
        if self.pokemon_actif["#"] == self.pIA["#"]:
            sleep(1)
            self.tour_IA(self.pokemon_right, self.pokemon_left)

    # ----------------------------------------------------
    # INTERFACE
    # ----------------------------------------------------

    def interfaceUtilisateur(self):
        title = tk.Label(self,text="Pokémon Battle",font=("Pokemon Solid", 32),bg=self.bg_color,fg="#FFD700",)
        title.pack(pady=10)
        self.combat_frame = tk.Frame(self, bg=self.bg_color)
        self.combat_frame.pack(fill="both", expand=True)

        self.messagePokemon = tk.Label(self.combat_frame,text=f"{self.pokemon_actif['Name']} attaque !",bg=self.bg_color,fg=self.fg_color,font=("Arial", 16, "bold"))
        self.messagePokemon.place(x=600, y=50)

        self.affichage_pokemon_combat([self.pokemon_left, self.pokemon_right])

    def affichage_pokemon_combat(self, liste_pokemon):
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
        tk.Label(self.combat_frame,text=str(pokemon["Name"]),font=("Pokemon Solid", size),bg=self.bg_color,fg=self.fg_color).place(x=x, y=y)

    def points_vie_pokemon(self, pokemon, x, y):
        var = StringVar(value="HP: " + str(pokemon["HP"]))
        self.objet["hp" + str(pokemon["#"])] = var
        tk.Label(self.combat_frame,textvariable=var,font=("Pokemon Solid", 16),bg=self.bg_color,fg=self.fg_color).place(x=x, y=y)

    def affichage_type_pokemon(self, pokemon, x, y):
        self.afficher_image_type(ImageType1(pokemon), x, y)

        path_type2 = ImageType2(pokemon)
        if path_type2:
            self.afficher_image_type(path_type2, x + 144, y)

    def afficher_image_type(self, image_path, x, y):
        image = Image.open(image_path)
        tk_img = ImageTk.PhotoImage(image)

        label = tk.Label(self.combat_frame, image=tk_img, bg=self.bg_color)
        label.image = tk_img
        label.place(x=x, y=y)

    # ----------------------------------------------------
    # ATTAQUES DISPONIBLES
    # ----------------------------------------------------

    def affichage_attaques_disponibles(self, pokemon, x, y, cible):
        attaques = self.logic.attaques_disponibles(pokemon)
        ESP_X = 200

        IA_turn = (pokemon["#"] == self.pokemon_right["#"])

        for i, (nom_atk, attaque) in enumerate(attaques.iterrows()):
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

    # ----------------------------------------------------
    # IA : CHOISIR L'ATTAQUE OPTIMALE
    # ----------------------------------------------------

    def tour_IA(self, ia_pokemon, pokeDefenseur):
        attaques = self.logic.attaques_disponibles(ia_pokemon)

        meilleur_atk = None
        meilleur_deg = -1

        for nom_atk, attaque in attaques.iterrows():
            deg = self.logic.degat(ia_pokemon, pokeDefenseur.copy(), nom_atk)
            if deg > meilleur_deg:
                meilleur_deg = deg
                meilleur_atk = nom_atk

        self.faire_degats(ia_pokemon, pokeDefenseur, meilleur_atk, IA_turn=True)

    # ----------------------------------------------------
    # COMBAT / DÉGÂTS
    # ----------------------------------------------------

    def faire_degats(self, attaquant, defenseur, attaque, IA_turn=False):

        if not IA_turn:
            self.messagePokemon.config(text=f"{attaquant['Name']} attaque avec {attaque} !")

        if attaquant["Name"] != self.pokemon_actif["Name"]:
            return

        if self.logic.estIlPerdant(defenseur):
            return

        damage = self.logic.degat(attaquant, defenseur, attaque)
        defenseur["HP"] -= damage

        # Mise à jour graphique
        self.objet["hp" + str(defenseur["#"])].set(f"HP: {defenseur['HP']}")

        # Changement de tour
        self.pokemon_actif, self.pokemon_passif = self.pokemon_passif,self.pokemon_actif

        # KO ?
        if self.logic.estIlPerdant(defenseur):

            self.messagePokemon.config(text=f"{attaquant['Name']} a gagné le combat !")

            # Reset HP
            if defenseur["#"] == self.pokemon_left["#"]:
                defenseur["HP"] = self.pokemon_left["HP"]
            else:
                defenseur["HP"] = self.pokemon_right["HP"]

            self.winner = attaquant

            # Bouton quitter
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("Quit.TButton",font=("Pokemon Solid", 30),background="#FF0000",foreground="#FFFFFF")
            btnQuitter = ttk.Button(self.combat_frame,text="Quitter",style="Quit.TButton",command=self.fincombat)
            btnQuitter.place(x=700, y=500)
            return

        # SI LE PROCHAIN JOUEUR EST L'IA → JOUER AUTOMATIQUEMENT
        if self.pokemon_actif["#"] == self.pokemon_right["#"]:
            self.tour_IA(self.pokemon_right, self.pokemon_left)
            

    def fincombat(self):
        self.objet = {}
        self.withdraw()
        self.quit()
