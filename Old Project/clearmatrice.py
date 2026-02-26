import pandas as pd

# Load the CSV file
df = pd.read_csv("Pokemon intranet.csv")

# Filter out rows where the 'Name' column contains the string 'Mega'
# The tilde (~) inverts the boolean mask: it keeps rows where the condition is FALSE.
# na=False ensures that rows with missing names (if any) are not filtered out by mistake.
df_sans_mega = df[~df['Name'].str.contains('Mega', na=False)]

# Save the resulting DataFrame to a new CSV file
csv_file_name = "pokemon_sans_mega.csv"
df_sans_mega.to_csv(csv_file_name, index=False)

# Display a preview and the size comparison
print(f"Nombre total de Pokémon dans la base originale : {len(df)}")
print(f"Nombre de Pokémon après suppression des Méga-Évolutions : {len(df_sans_mega)}")
print("\nAperçu des premières lignes du nouveau DataFrame :")
print(df_sans_mega.head().to_markdown(index=False))
print(f"\nFichier CSV '{csv_file_name}' créé.")