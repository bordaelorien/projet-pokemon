import tkinter as tk
from tkinter import ttk

import data_loader as dl
import deck_builder as db
import game_logic as gl
from affichageCombatJvsJ import PokemonApp


class SelectionWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sélection des Pokémon")
        self.geometry("1200x800")
        self.configure(bg="#2b2b2b")

        # Chargement des données
        self.df_pokemon = dl.dfPokemon()
        self.df_attacks = dl.dfAttaques()
        self.deck1, self.deck2 = db.decks(self.df_pokemon)

        # Stockage des choix
        self.pokemon_j1 = None
        self.pokemon_j2 = None
        # Affichage des sélections 
        self.selected_label_j1 = None
        self.selected_label_j2 = None


        # Interface
        self.create_ui()

    # -----------------------------------------------------
    # INTERFACE
    # -----------------------------------------------------
    def create_ui(self):
        title = tk.Label(self, text="Choisissez les Pokémons des deux joueurs",font=("Arial", 26, "bold"), fg="white", bg="#2b2b2b")
        title.pack(pady=20)

        container = tk.Frame(self, bg="#2b2b2b")
        container.pack(fill="both", expand=True)

        frame1 = tk.LabelFrame(container, text="Deck Joueur 1", fg="white",bg="#2b2b2b", font=("Arial", 18, "bold"))
        frame1.pack(side="left", fill="y", expand=True, padx=20)

        frame2 = tk.LabelFrame(container, text="Deck Joueur 2", fg="white",bg="#2b2b2b", font=("Arial", 18, "bold"))
        
        # Labels de sélection
        self.selected_label_j1 = tk.Label(frame1,text="Aucun Pokémon sélectionné",bg="#2b2b2b",fg="yellow",font=("Arial", 16, "bold"))
        self.selected_label_j1.pack(pady=10)

        self.selected_label_j2 = tk.Label(frame2,text="Aucun Pokémon sélectionné",bg="#2b2b2b",fg="yellow",font=("Arial", 16, "bold"))
        self.selected_label_j2.pack(pady=10)
        # Affichage par type
        self.create_type_sections(frame1, self.deck1, player=1)
        frame2.pack(side="right", fill="y", expand=True, padx=20)
        self.create_type_sections(frame2, self.deck2, player=2)

    # -----------------------------------------------------
    # AFFICHAGE DES TYPES + BOUTONS
    # -----------------------------------------------------
    def create_type_sections(self, frame, deck_df, player: int):

       # On crée une copie pour éviter de modifier le deck original
        deck_df = deck_df.copy()
        grouped = deck_df.groupby("Type 1")
        canvas = tk.Canvas(frame, bg="#2b2b2b")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#2b2b2b")

        scroll_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for type_name, group in grouped:
            lf = tk.LabelFrame(scroll_frame, text=type_name.capitalize(),fg="white", bg="#1e1e1e",font=("Arial", 16, "bold"), padx=10, pady=10)
            lf.pack(fill="x", pady=10)

            for _, row in group.iterrows():
                btn = tk.Button(lf, text=row["Name"],font=("Pokemon Solid", 14),bg="#3c3c3c", fg="black",command=lambda r=row, p=player: self.select_pokemon(r, p))
                btn.pack(fill="x", pady=4)

    # -----------------------------------------------------
    # SELECTION
    # -----------------------------------------------------
    def select_pokemon(self, row, player):
        if player == 1:
            self.pokemon_j1 = row
        else:
            self.pokemon_j2 = row

        print(f"P{player} → {row['Name']} sélectionné")
        
        ## Mise à jour du label de sélection
        if player == 1:
            self.selected_label_j1.config(text=f"Pokémon sélectionné : {row['Name']}")
        else:
            self.selected_label_j2.config(text=f"Pokémon sélectionné : {row['Name']}")


        if self.pokemon_j1 is not None and self.pokemon_j2 is not None:
            self.start_battle()

    # -----------------------------------------------------
    # LANCEMENT DU COMBAT
    # -----------------------------------------------------
    def start_battle(self):
        print("Lancement du combat !")
        self.destroy()

        # Ouvre la fenêtre de combat
        PokemonApp(self.pokemon_j1, self.pokemon_j2).mainloop()


# Lancement direct si standalone
if __name__ == "__main__":
    SelectionWindow().mainloop()
