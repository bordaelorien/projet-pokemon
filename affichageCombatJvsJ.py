
import tkinter as tk
from tkinter import StringVar,ttk

import data_loader as dl
import game_logic as gl
from images import *
from paths import *



class PokemonJVSJ():
    def __init__(self,p1,p2,fenetrePrincipale=None):
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

       # Position fixe à l'écran
        self.pokemon_left,self.pokemon_right=p1.copy(),p2.copy()

        # Logique de combat (celui qui joue)
        self.pokemon_actif ,self.pokemon_passif =gl.GameLogic(self.df_attacks).premierAttaquant(p1.copy(),p2.copy())
        self.nameAttaquePJ1={}
        self.nameAttaquePJ2={}
        self.historique = []  # Liste des actions du combat
        self.creer_bouton_historique()


        self.HP = {}
        self.image=[]
        ##MESSAGES :
        self.winner=None
       

        self.interfaceUtilisateur()
    # ----------------------------------------------------
    # INTERFACE UTILISATEUR
    # ----------------------------------------------------
    ##Bouton historique
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
        self.messagePokemon=tk.Label(self.combat_frame,text=f"{self.pokemon_actif['Name']} attaque !",bg=self.bg_color,fg=self.fg_color,font=("Arial", 16, "bold"))
        self.messagePokemon.place(x=600, y=50)
        self.affichage_pokemon_combat([self.pokemon_left, self.pokemon_right])


    def affichage_pokemon_combat(self, liste_pokemon): 
        """
        Affiche les Pokémon en combat avec leurs informations.
        """
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
        """
        Affiche le nom du Pokémon à une position donnée.    
        """
        tk.Label(self.combat_frame,text=str(pokemon["Name"]),font=("Pokemon Solid", size),bg=self.bg_color,fg=self.fg_color,).place(x=x, y=y)

    def points_vie_pokemon(self, pokemon, x, y):
        """
        Affiche les points de vie du Pokémon à une position donnée.
        """
        var = StringVar(value="HP: "+str(pokemon['HP']))
        self.HP["hp"+str(pokemon["#"])] = var
        tk.Label(self.combat_frame,textvariable=var,font=("Pokemon Solid", 16),bg=self.bg_color,fg=self.fg_color,).place(x=x, y=y)

    def affichage_type_pokemon(self, pokemon, x, y):
        """
        Affiche les types du Pokémon à une position donnée.
        """
        self.afficher_image_type(pathType1(pokemon),x,y)

        path_type2 = pathType2(pokemon)
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
        """
        Affiche les attaques disponibles pour un Pokémon à une position donnée.
        """
        attaques = self.logic.attaques_disponibles(pokemon)
        ESP_X = 200
        for i, (nom_atk, attaque) in enumerate(attaques.iterrows()):
          
            bouton_x = x + (i % 2) * ESP_X
            bouton_y = y + (i // 2) * 50
            if pokemon["#"]==self.pokemon_left["#"]:
                self.nameAttaquePJ1[nom_atk] = attaque["Nom_Attaque"]
                tk.Button(
                    self.combat_frame,
                    text=attaque["Nom_Attaque"],
                    bg="#444444",
                    fg="black",
                    font=("Pokemon Solid", 16),
                    command=lambda atk_nom=nom_atk, atk=pokemon, defp=cible: self.faire_degats(atk, defp, atk_nom, joueur=1)
                ).place(x=bouton_x, y=bouton_y)
            else:
                self.nameAttaquePJ2[nom_atk] = attaque["Nom_Attaque"]
                tk.Button(
                    self.combat_frame,
                    text=attaque["Nom_Attaque"],
                    bg="#444444",
                    fg="black",
                    font=("Pokemon Solid", 16),
                    command=lambda atk_nom=nom_atk, atk=pokemon, defp=cible: self.faire_degats(atk, defp, atk_nom, joueur=2)
                ).place(x=bouton_x, y=bouton_y)


    # ----------------------------------------------------
    # COMBAT / DÉGÂTS
    # ----------------------------------------------------

    def faire_degats(self, attaquant, defenseur, attaque,joueur=None):
        """
        Fonction permettant d'affecter les dégats sur un Pokemon et de le mettre à jour graphiquement.
        + Gestion Historique
        + Gestion fin combat
        """
        ##Message attaque
        self.messagePokemon.config(text=f"{defenseur['Name']} attaque !")

        if attaquant["Name"]!= self.pokemon_actif["Name"]:
            return
        
        if self.logic.estIlPerdant(defenseur):
            return 

        damage = self.logic.degat(attaquant, defenseur, attaque)
        
        defenseur["HP"] -= damage
        ##Historique
        if joueur == 1:
            self.historique.append(f"{attaquant['Name']} utilise {self.nameAttaquePJ1[attaque]} → {defenseur['Name']} perd {damage} HP")
        else:
            self.historique.append(f"{attaquant['Name']} utilise {self.nameAttaquePJ2[attaque]} → {defenseur['Name']} perd {damage} HP")

        ##Mise à jour graphique
        self.HP["hp"+str(defenseur["#"])].set(f"HP: {defenseur['HP']}")
        #Changement tour
        self.pokemon_actif, self.pokemon_passif = self.pokemon_passif, self.pokemon_actif

        ##Gestion fin combat
        if self.logic.estIlPerdant(defenseur):
            self.historique.append(f"{attaquant['Name']} met K.O. {defenseur['Name']} !")
            self.messagePokemon.config(text=f"{attaquant['Name']} gagne le combat !")
            if defenseur["#"]==self.pokemon_left["#"]:
                defenseur["HP"] = self.pokemon_left["HP"]
            else:
                defenseur["HP"] = self.pokemon_right["HP"]
            self.winner=attaquant
            style=ttk.Style() # Obligation de creer un style pour mac car il ne reconnait pas les bg dans les boutons
            style.theme_use('clam')
            style.configure('Quit.TButton',font=("Pokemon Solid", 30),background="#FF0000",foreground="#FFFFFF")
            btnQuitter = ttk.Button(self.combat_frame, text="Quitter", style='Quit.TButton', command=self.fincombat)
            btnQuitter.place(x=600, y=500)
    

    def fincombat(self):
     
        self.HP = {}                  
        self.fenetre.withdraw()   
        self.fenetre.quit()

            