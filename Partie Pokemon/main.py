from JvsIA import JoueurVSIA
from JvsJ import JoueurVSJoueur
import modelisation


import tkinter as tk

nbrePokemons=60

root = tk.Tk()
root.title("Ultimate Tic tac toe Pokemon")
root.geometry("1000x700")
root.resizable(width=False, height=False)

canvasmenu = tk.Canvas(root, width=1000, height=700, bg="light blue")
canvasmenu.pack()
canvasmenu.create_text(500, 50, text="Bienvenue dans Ultimate Tic tac toe Pokemon !",
                       font=("Times New Roman", 20, "bold"), fill="black")

def launch_jvsj():
    root.destroy()
    fenetre = JoueurVSJoueur(nbrePokemons)

def launch_jvsia():
    root.destroy()
    fenetre = JoueurVSIA(nbrePokemons)
def launch_modelisation():
    root.destroy()
    nbre=input("Combien de parties voulez-vous simuler ? (10 par défaut) ")
    try:
        fenetre = modelisation.IAVSIA()
        fenetre.modelisation(int(nbre))
    except:
        fenetre = modelisation.IAVSIA()
        fenetre.modelisation(10)


bouton_jvsj = tk.Button(root, text="Joueur vs Joueur", font=("Helvetica", 30, "bold"), width=20,
                        bg="light blue", fg="blue", activebackground="light blue",
                        command=launch_jvsj)
bouton_jvsj.place(x=250, y=150)

bouton_jvsia = tk.Button(root, text="Joueur vs IA", font=("Helvetica", 30, "bold"), width=20,
                         bg="light blue", fg="blue", activebackground="light blue",
                         command=launch_jvsia)
bouton_jvsia.place(x=250, y=250)

bouton_iavsia = tk.Button(root, text="IA vs aléatoire", font=("Helvetica", 30, "bold"), width=20,
                          bg="light blue", fg="blue", activebackground="light blue",
                          command=launch_modelisation) 
bouton_iavsia.place(x=250, y=350)

root.mainloop()
