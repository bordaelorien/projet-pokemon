import JoueurVSJoueur
import JoueurVSIA
import JoueurVSIA


import tkinter as tk



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
    # call the function/class from the module
    fenetre = JoueurVSJoueur.JoueurVSJoueur()

def launch_jvsia():
    root.destroy()
    fenetre = JoueurVSIA.JoueurVSIA()

def launch_iavsia():
    root.destroy()
    # reuse JoueurVSIA as placeholder for IA vs IA; replace with proper module/function if available
    fenetre = JoueurVSIA.JoueurVSIA()

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
                          command=launch_iavsia)  # or another script for IA vs IA
bouton_iavsia.place(x=250, y=350)

root.mainloop()
