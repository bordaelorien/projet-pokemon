# main.py
from affichageCombat import PokemonApp
from selection_window import SelectionWindow
from deck_builder import decks
from data_loader import dfPokemon, dfAttaques
decks1, decks2 = decks(dfPokemon())
if __name__ == "__main__":
    print(decks1.iloc[0], decks2.iloc[0])   
    PokemonApp(decks1.iloc[0], decks2.iloc[0]).mainloop()
