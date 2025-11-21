# app.py
import tkinter as tk
from tkinter import StringVar

import data_loader as dl
import deck_builder as db
import deck_builder as db
import game_logic as gl
from images import *
from paths import path


class PokemonApp(tk.Tk):
    def __init__(self,p1,p2):
        super().__init__()
        self.title("Pokémon Battle")
        self.geometry("1600x900")
        self.bg_color = "#323232"
        self.fg_color = "#FFFFFF"
        self.configure(bg=self.bg_color)
        

        # Chargement des données
        self.df_pokemon = dl.dfPokemon()
        self.df_attacks = dl.dfAttaques()
        self.logic = gl.GameLogic(self.df_attacks)

        # État du combat
        self.pokemon_actif = p1
        self.pokemon_passif = p2

        self.objet = {}

        self.interfaceUtilisateur()
        self.logic.JeuCombat(self.pokemon_actif, self.pokemon_passif)

    # ----------------------------------------------------
    # INTERFACE UTILISATEUR
    # ----------------------------------------------------

    def interfaceUtilisateur(self):
        title = tk.Label(self,text="Pokémon Battle",font=("Pokemon Solid", 32),bg=self.bg_color,fg="#FFD700",)
        attaquant=tk.Label(self,text="Attaquant",font=("Pokemon Solid", 20),bg=self.bg_color,fg="#444A7C")
        defenseur=tk.Label(self,text="Défenseur",font=("Pokemon Solid", 20),bg=self.bg_color,fg="#B53521")
        attaquant.place(x=100, y=50)
        defenseur.place(x=1000, y=50)
        title.pack(pady=10)

        self.combat_frame = tk.Frame(self, bg=self.bg_color)
        self.combat_frame.pack(fill="both", expand=True)
        #self.texteAttaque_Defense()

        self.affichage_pokemon_combat([self.pokemon_actif, self.pokemon_passif])

    # ----------------------------------------------------
    # AFFICHAGE DES POKÉMON
    # ----------------------------------------------------

    def affichage_pokemon_combat(self, liste_pokemon):
        ##Suppression de la liste des widgets de la frame combat
        for widget in self.combat_frame.winfo_children(): 
            widget.destroy()

        for i, pokemon in enumerate(liste_pokemon):
            deltaX = i * 900
            
            image = imagePokemon(str(pokemon["#"]),pokemon["Name"])
            label_img = tk.Label(self.combat_frame,image=image)
            label_img.image = image # garder une référence pour éviter le garbage collector
            label_img.place(x=100 + deltaX, y=150)
            self.affichage_nom_pokemon(pokemon, 100 + deltaX, 50, 24)
            self.points_vie_pokemon(pokemon, 100 + deltaX, 90)
            self.affichage_type_pokemon(pokemon, 100 + deltaX, 130)

        #Affichage des attaques du pokémon 1
        self.affichage_attaques_disponibles(liste_pokemon[0], 100, 600, liste_pokemon[1])

        # Affichage des attaques du pokémon 2
        self.affichage_attaques_disponibles(liste_pokemon[1], 1000, 600, liste_pokemon[0])

    def texteAttaque_Defense(self):
        tk.Label(self.combat_frame,text="Attaquant",font=("Pokemon Solid", 20),bg=self.bg_color,fg="white",).place(x=350, y=550)
        tk.Label(self.combat_frame,text="Défenseur",font=("Pokemon Solid", 20),bg=self.bg_color,fg=self.fg_color,).place(x=1150, y=550)

    def affichage_nom_pokemon(self, pokemon, x, y, size):
        tk.Label(self.combat_frame,text=str(pokemon["Name"]),font=("Pokemon Solid", size),bg=self.bg_color,fg=self.fg_color,).place(x=x, y=y)

    def points_vie_pokemon(self, pokemon, x, y):
        var = StringVar(value="HP: "+str(pokemon['HP']))
        self.objet["hp"+str(str(pokemon["#"]))] = var
        tk.Label(self.combat_frame,textvariable=var,font=("Pokemon Solid", 16),bg=self.bg_color,fg=self.fg_color,).place(x=x, y=y)

    def affichage_type_pokemon(self, pokemon, x, y):
        self.afficher_image_type(ImageType1(pokemon),x,y)

        path_type2 = ImageType2(pokemon)
        if path_type2:
            self.afficher_image_type(path_type2, x + 144, y)
            
    def afficher_image_type(self, image_path, x, y):
        """
        Affichage image de type Pokémon à une position donnée
        """
        image = Image.open(image_path)
        tk_img = ImageTk.PhotoImage(image)
        label = tk.Label(self.combat_frame,image=tk_img,bg=self.bg_color)
        label.image = tk_img
        label.place(x=x, y=y)

    # ----------------------------------------------------
    # ATTAQUES DISPONIBLES
    # ----------------------------------------------------

    def affichage_attaques_disponibles(self, pokemon, x, y, cible):
        attaques = self.logic.attaques_disponibles(pokemon)
        ESP_X = 200
        for i, (nom_atk, attaque) in enumerate(attaques.iterrows()):
          
            bouton_x = x + (i % 2) * ESP_X
            bouton_y = y + (i // 2) * 50

            tk.Button(
                self.combat_frame,
                text=attaque["Nom_Attaque"],
                bg="#444444",
                fg="black",
                font=("Pokemon Solid", 16),
                command=lambda atk_nom=nom_atk, atk=pokemon, defp=cible: self.faire_degats(atk, defp, atk_nom)
            ).place(x=bouton_x, y=bouton_y)


    # ----------------------------------------------------
    # COMBAT / DÉGÂTS
    # ----------------------------------------------------

    def faire_degats(self, attaquant, defenseur, attaque):
        
        if attaquant["Name"]!= self.pokemon_actif["Name"]:
            return
        
        if self.logic.est_il_gagnant(defenseur):
            return self.affichage_gagnant(attaquant)

        damage = self.logic.degat(attaquant, defenseur, attaque)
        defenseur["HP"] -= damage
        print(damage)

        
        self.objet["hp"+str(defenseur["#"])].set(f"HP: {defenseur['HP']}")



        if self.logic.est_il_gagnant(defenseur):
            return self.affichage_gagnant(attaquant)
        print("Dégâts infligés :", damage)

        if attaquant["Name"] != self.pokemon_actif["Name"]:
            return

        self.pokemon_actif, self.pokemon_passif =self.pokemon_passif,self.pokemon_actif        

        self.affichage_pokemon_combat([self.pokemon_actif, self.pokemon_passif])


    # ----------------------------------------------------
    # FENÊTRE DE VICTOIRE
    # ----------------------------------------------------

    def affichage_gagnant(self, gagnant):
        popup = tk.Toplevel(self, bg=self.bg_color)

        tk.Label(popup,text=f"Victoire ! {gagnant['Name']} gagne !",font=("Pokemon Solid", 20),bg=self.bg_color,fg="#FFD700").pack(padx=20, pady=20)