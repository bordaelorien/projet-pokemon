import tkinter as tk

fenetre = tk.Tk()

# 1. Créer la variable de contrôle
texte_variable = tk.StringVar()

# 2. Lier le Label à cette variable avec 'textvariable'
label_dynamique = tk.Label(fenetre, textvariable=texte_variable, font=("Arial", 20))
label_dynamique.pack(pady=20)

# 3. Définir le texte initial en utilisant .set()
texte_variable.set("Bonjour !")

# 4. Fonction pour changer le texte
def changer_texte():
    texte_variable.set("Le texte a changé !")

# 5. Bouton qui appelle la fonction
bouton = tk.Button(fenetre, text="Changer", command=changer_texte)
bouton.pack()

fenetre.mainloop()