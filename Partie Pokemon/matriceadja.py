import pandas as pd
import numpy as np
"""
Prompt : 
dans ce CSV (Fichier pokemon) tu trouveras des types donne moi tous les liens entre ces types 
(pas d'effet, peu d'effet, effet normal, tres efficace) 
et met le moi sous la forme d'une matrice d'adjacence

"""
# Standard 18 Pokémon types in a conventional order (Attaquant/Défenseur)
types = [
    'Normal', 'Fire', 'Water', 'Grass', 'Electric', 'Ice', 'Fighting', 'Poison',
    'Ground', 'Flying', 'Psychic', 'Bug', 'Rock', 'Ghost', 'Dragon', 'Steel',
    'Fairy', 'Dark'
]

# Type chart data (Attacking Type in rows, Defending Type in columns)
type_chart_values = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0, 1, 0.5, 1, 1], # Normal
    [1, 0.5, 0.5, 2, 1, 2, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 1], # Fire
    [1, 2, 0.5, 0.5, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 0.5, 1, 1, 1], # Water
    [1, 0.5, 2, 0.5, 1, 1, 1, 0.5, 2, 0.5, 1, 0.5, 2, 1, 0.5, 0.5, 1, 1], # Grass
    [1, 1, 2, 0.5, 0.5, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0.5, 1, 1, 1], # Electric
    [1, 0.5, 0.5, 2, 1, 0.5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 0.5, 1, 1], # Ice
    [2, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 2, 0, 1, 2, 0.5, 2], # Fighting
    [1, 1, 1, 2, 1, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 0, 2, 1], # Poison
    [1, 2, 1, 0.5, 2, 1, 1, 2, 1, 0, 1, 0.5, 2, 1, 1, 2, 1, 1], # Ground
    [1, 1, 1, 2, 0.5, 2, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 0.5, 1, 1], # Flying
    [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 0.5, 1, 0], # Psychic
    [1, 0.5, 1, 2, 1, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 0.5, 0.5, 2], # Bug
    [1, 2, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 0.5, 1, 1], # Rock
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 0.5], # Ghost
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0.5, 0, 1], # Dragon
    [1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 0.5, 2, 1], # Steel
    [1, 0.5, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 1, 2, 0.5, 1, 2], # Fairy
    [1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 2, 1, 1, 2, 1, 1, 0.5, 0.5] # Dark
]

# Create the DataFrame
df_type_matrix = pd.DataFrame(type_chart_values, index=types, columns=types)

# Rename index and columns for clarity in French
df_type_matrix.index.name = "Type Attaquant"
df_type_matrix.columns.name = "Type Défenseur"

# Define the CSV file name
csv_file_name_coeffs = "matrice_efficacite_types_pokemon_coeffs.csv"

# Save the DataFrame to CSV
df_type_matrix.to_csv(csv_file_name_coeffs)

# Print the file name to signal it as an output
print(csv_file_name_coeffs)