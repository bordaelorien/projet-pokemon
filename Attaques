import pandas as pd
"""
Prompt: 
cree un df avec 4 attaques de chaque type de pokemon dans la df avec leur stat pour effectuer les calculs de degat
dans ce cas la rajoute 4 attaques de chaque type dans un nouveau df avec la puissance de cette attaque
rajoute une colonne dans ce tableau avec les attaque faisant perdre des hp a l'attaquant et leur pv perdu 
(si cela depend des hp du pokemon attaquant tu peux ne rajouter que coefficient)
"""
# Load the previously created attack list CSV
try:
    df_attaques = pd.read_csv("pokemon_liste_attaques_par_type.csv")
except FileNotFoundError:
    # Fallback in case the file doesn't exist in this session (though it should)
    # This data is identical to the output of the previous step
    attack_data = [
        ('Normal', 'Ultralaser', 150), ('Normal', 'Plaquage', 85), ('Normal', 'Vive-Attaque', 40), ('Normal', 'Coupe', 50),
        ('Fire', 'Déflagration', 110), ('Fire', 'Lance-Flammes', 90), ('Fire', 'Roue de Feu', 60), ('Fire', 'Flammèche', 40),
        ('Water', 'Hydrocanon', 110), ('Water', 'Surf', 90), ('Water', 'Vibraqua', 60), ('Water', 'Pistolet à O', 40),
        ('Grass', 'Lance-Soleil', 120), ('Grass', 'Lame-Feuille', 90), ('Grass', 'Canon Graine', 80), ('Grass', 'Fouet Lianes', 45),
        ('Electric', 'Fatal-Foudre', 110), ('Electric', 'Tonnerre', 90), ('Electric', 'Rayon Chargé', 50), ('Electric', 'Éclair', 40),
        ('Ice', 'Blizzard', 110), ('Ice', 'Laser Glace', 90), ('Ice', 'Vent Glace', 55), ('Ice', 'Éclats Glace', 40),
        ('Fighting', 'Close Combat', 120), ('Fighting', 'Stratopercut', 85), ('Fighting', 'Casse-Brique', 75), ('Fighting', 'Mach Punch', 40),
        ('Poison', 'Détricanon', 120), ('Poison', 'Cradovague', 95), ('Poison', 'Bombe Beurk', 90), ('Poison', 'Direct Toxik', 80),
        ('Ground', 'Séisme', 100), ('Ground', 'Tunnel', 80), ('Ground', 'Piétisol', 60), ('Ground', 'Tir de Boue', 55),
        ('Flying', 'Rapace', 120), ('Flying', 'Lame d\'Air', 75), ('Flying', 'Aéropique', 60), ('Flying', 'Tornade', 40),
        ('Psychic', 'Prescience', 120), ('Psychic', 'Choc Psy', 100), ('Psychic', 'Psyko', 90), ('Psychic', 'Choc Mental', 50),
        ('Bug', 'Mégacorne', 120), ('Bug', 'Bourdon', 90), ('Bug', 'Plaie-Croix', 80), ('Bug', 'Piqûre', 60),
        ('Rock', 'Lame de Roc', 100), ('Rock', 'Éboulement', 75), ('Rock', 'Tomberoche', 60), ('Rock', 'Jet-Pierres', 50),
        ('Ghost', 'Revenant', 120), ('Ghost', 'Ball\'Ombre', 80), ('Ghost', 'Griffe Ombre', 70), ('Ghost', 'Châtiment', 65),
        ('Dragon', 'Draco Météor', 130), ('Dragon', 'Colère', 120), ('Dragon', 'Draco-Choc', 85), ('Dragon', 'Draco-Souffle', 60),
        ('Steel', 'Poing Météor', 90), ('Steel', 'Tête de Fer', 80), ('Steel', 'Luminocanon', 80), ('Steel', 'Pisto-Poing', 40),
        ('Fairy', 'Pouvoir Lunaire', 95), ('Fairy', 'Câlinerie', 90), ('Fairy', 'Éclat Magique', 80), ('Fairy', 'Vent Féérique', 40),
        ('Dark', 'Tricherie', 95), ('Dark', 'Mâchouille', 80), ('Dark', 'Vibrobscur', 80), ('Dark', 'Coup Bas', 70)
    ]
    df_attaques = pd.DataFrame(attack_data, columns=['Type', 'Nom_Attaque', 'Puissance'])

# Define the recoil effects for the attacks in this specific list
# Note: Most recoil attacks (Damoclès, Boutefeu, etc.) were not in this sample.
# 'Rapace' (Brave Bird) is the only one.
# 'Close Combat' and 'Draco Meteor' lower stats, but don't cause HP loss (recoil).
recoil_map = {
    'Rapace': '1/3 des dégâts infligés'
    # 'Damoclès': '1/3 des dégâts infligés' (Not in list)
    # 'Bélier': '1/4 des dégâts infligés' (Not in list)
    # 'Boutefeu': '1/3 des dégâts infligés' (Not in list)
    # 'Électacle': '1/3 des dégâts infligés' (Not in list)
}

# Create the new column by mapping the dictionary
df_attaques['Recul_PV_Perdus'] = df_attaques['Nom_Attaque'].map(recoil_map)

# Fill non-recoil attacks with 'Aucun'
df_attaques['Recul_PV_Perdus'] = df_attaques['Recul_PV_Perdus'].fillna('Aucun')

# Define the new CSV file name
new_csv_name = "pokemon_attaques_avec_recul.csv"

# Save the updated DataFrame to the new CSV
df_attaques.to_csv(new_csv_name, index=False)

print(f"Fichier CSV '{new_csv_name}' créé.")
print("\nAperçu du DataFrame mis à jour (extrait du type Vol) :")
print(df_attaques[df_attaques['Type'] == 'Flying'].to_markdown(index=False))