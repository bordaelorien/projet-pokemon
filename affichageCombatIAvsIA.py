
from game_logic import GameLogic
from data_loader import dfAttaques

def combatIAvsIA(p1, p2):
    """
    Simule un combat automatique entre deux Pokémon.

    """

    # --- On clone pour éviter de modifier les originaux ---
    A = p1.copy()
    B = p2.copy()

    # HP initiaux
    A_hp = int(A["HP"])
    B_hp = int(B["HP"])
    logic= GameLogic(df_attacks=dfAttaques())

    # Combat jusqu'à la mort d'un des deux
    while A_hp > 0 and B_hp > 0:
        atkA = best_Attack(A, B, logic)  
        dmgA = GameLogic.degat(logic, A, B, atkA)
        B_hp -= dmgA
        if B_hp <= 0:
            return A   
        atkB = best_Attack(B, A, logic)
        dmgB = GameLogic.degat(logic, B, A, atkB)
        A_hp -= dmgB
        if A_hp <= 0:
            return B   
        

def best_Attack(attacker, defender,logic):
    """
    Choisit la meilleure attaque pour le Pokémon attaquant contre le défenseur.
    """
    
    attaques = GameLogic.attaques_disponibles(logic, attacker)

    meilleur_atk = None
    meilleur_deg = -1

    for nom_atk, attaque in attaques.iterrows():
        deg = GameLogic.degat(logic, attacker, defender.copy(), nom_atk)
        if deg > meilleur_deg:
            meilleur_deg = deg
            meilleur_atk = nom_atk
    return meilleur_atk
