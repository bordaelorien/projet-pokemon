import tkinter as tk

app = tk.Tk()

photo = tk.PhotoImage(file = "Partie Pokemon/Photos Pokemon/Pokemons/1-bulbasaur.png")
photoimage = photo.subsample(7,7)
bouton = tk.Button(app, bg="light blue", image=photoimage, relief="flat", borderwidth=10, highlightcolor="red", activebackground="white")
bouton.place(width=40, height=40, x=100, y=100)

app.mainloop()