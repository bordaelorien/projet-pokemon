
    # Mode IA VS random:
    def modelisation(self,x): # x le nombre de parties

        self.modedejeu='IAvsIA'

        nbgains_ia=0    #nb de parties gagnées
        nb_egalites=0   #nb parties à égalité
        coups=[]        #tableau composé du nb de coups de l'IA à chaque partie gagnée

        # changements graphiques

        self.canvasmenu.destroy()

        self.canvasmodel = tk.Canvas(self.fenetre, width=1000, height=700, bg="light green")
        self.canvasmodel.pack()
        txt_accueil=self.canvasmodel.create_text(500, 350,
                                             text=f"Une modélisation de {x} parties est faite entre l'IA et un algorithme aléatoire",
                                     font=("Times new roman", 20, "bold"), fill="black")
        self.fenetre.update() #mette à jour la fenêtre avec le texte

        # Réalisation des x parties

        for partie in range(1,x+1):

            # Initialisation et lancement de la partie:
            jeu= Jeu(False)
            jeu.IA = random.choice(['X', 'O'])
            jeu.modedejeu='IAvsIA'
            if jeu.IA == 'X':
                jeu.joueur = jeu.IA
                jeu.random = 'O'  # robot random qui joue contre l'IA
                jeu.ia()
            else:
                jeu.random = 'X'
                jeu.joueur = jeu.random
                jeu.ia_random()
            # On garde les résultats de la partie:
            if jeu.gagnant==jeu.IA:
                nbgains_ia+=1
                coups.append(jeu.nbcoups)
            if jeu.gagnant==None:
                nb_egalites+=1

            self.fenetre.update()  # mette à jour la fenêtre avec le texte
        #Nb de coups moyens:
        if len(coups)!=0:
            moycoups = round( sum(coups) / len(coups) ,2)

        # Fenêtre d'annonce des résultats:
        self.canvasmodel.delete(txt_accueil)


        self.canvasmodel.create_text(500, 150, text=f"Une modélisation de {x} parties à été faite entre l'IA et un algorithme aléatoire",
                                   font=("Times new roman", 20, "bold"), fill="black")
        if len(coups)!=0:
            self.canvasmodel.create_text(500, 300, text=f"L'IA a gagné {nbgains_ia} parties, avec en moyenne {moycoups} coups",
                                   font=("Halvetica", 20, "bold"), fill="black")
            self.canvasmodel.create_text(500, 350,
                                         text=f"\nIl y a eu {nb_egalites} parties à égalité",font=("Halvetica", 15, "bold"), fill="black")

        else:
            self.canvasmodel.create_text(500, 300, text=f"L'IA n'a gagné aucune partie \n Il y a eu {nb_egalites} partie à égalité ",
                                         font=("Halvetica", 20, "bold "), fill="black")
        self.canvasmodel.create_text(500, 500, text=f" Cliquez sur la touche f pour fermer",
                                   font=("Halvetica", 10, "bold italic"), fill="green")
        self.fenetre.bind("<Key-f>", lambda event: self.fenetre.destroy())

