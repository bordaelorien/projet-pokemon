# app.py
import tkinter as tk
from tkinter import StringVar,ttk

import data_loader as dl
import deck_builder as db
import deck_builder as db
import game_logic as gl
from images import *
from paths import path


class PokemonApp(tk.Toplevel):
    def __init__(self,p1,p2,fenetrePrincipale=None):
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

       # Position fixe à l'écran
        self.pokemon_left,self.pokemon_right=gl.GameLogic(self.df_attacks).premierAttaquant(p1.copy(),p2.copy())
        HPleft=self.pokemon_left["HP"]
        
        self.pokemon_right["HP"]=self.pokemon_right["HP"]

        # Logique de combat (celui qui joue)
        self.pokemon_actif = p1.copy()
        self.pokemon_passif = p2.copy()

        self.objet = {}
        self.image=[]
        ##MESSAGES :
        self.winner=None
       

        self.interfaceUtilisateur()
        self.logic.JeuCombat(self.pokemon_actif, self.pokemon_passif)

    def interfaceUtilisateur(self):
        title = tk.Label(self,text="Pokémon Battle",font=("Pokemon Solid", 32),bg=self.bg_color,fg="#FFD700",)
        title.pack(pady=10)

        self.combat_frame = tk.Frame(self, bg=self.bg_color)
        self.combat_frame.pack(fill="both", expand=True)
        self.messagePokemon=tk.Label(self.combat_frame,text=f"{self.pokemon_actif["Name"]} attaque !",bg=self.bg_color,fg=self.fg_color,font=("Arial", 16, "bold"))
        self.messagePokemon.place(x=600, y=50)
        self.affichage_pokemon_combat([self.pokemon_left, self.pokemon_right])


    def affichage_pokemon_combat(self, liste_pokemon):
        for i, pokemon in enumerate(liste_pokemon):
            deltaX = i * 900
            image = imagePokemon(str(pokemon["#"]),pokemon["Name"])
            self.image.append(image)
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

    def affichage_nom_pokemon(self, pokemon, x, y, size):
        tk.Label(self.combat_frame,text=str(pokemon["Name"]),font=("Pokemon Solid", size),bg=self.bg_color,fg=self.fg_color,).place(x=x, y=y)

    def points_vie_pokemon(self, pokemon, x, y):
        var = StringVar(value="HP: "+str(pokemon['HP']))
        self.objet["hp"+str(pokemon["#"])] = var
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
        
        self.messagePokemon.config(text=f"{defenseur['Name']} attaque !")
        
        if attaquant["Name"]!= self.pokemon_actif["Name"]:
            return
        
        if self.logic.estIlPerdant(defenseur):
            return 

        damage = self.logic.degat(attaquant, defenseur, attaque)
        
        defenseur["HP"] -= damage

        
        self.objet["hp"+str(defenseur["#"])].set(f"HP: {defenseur['HP']}")
        self.pokemon_actif, self.pokemon_passif = self.pokemon_passif, self.pokemon_actif


        if self.logic.estIlPerdant(defenseur):
            self.messagePokemon.config(text=f"{attaquant['Name']} gagne le combat !")
            if defenseur["#"]==self.pokemon_left["#"]:
                defenseur["HP"] = self.pokemon_left["HP"]
            else:
                defenseur["HP"] = self.pokemon_right["HP"]
            self.winner=attaquant
            style=ttk.Style()
            style.theme_use('clam')
            style.configure('Quit.TButton',font=("Pokemon Solid", 30),background="#FF0000",foreground="#FFFFFF")
            btnQuitter = ttk.Button(self.combat_frame, text="Quitter", style='Quit.TButton', command=self.fincombat)
            btnQuitter.place(x=700, y=500)
            

    def fincombat(self):
     
        self.objet = {}                  
        self.withdraw()   
        self.quit()

            