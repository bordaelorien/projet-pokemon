
import pandas as pd


def decks(df, deck_size = 60):
    fracPokemon=df.sample(deck_size*2).sort_values(by="Total",ascending=False)
    dfByType = {Type: sous_df for Type, sous_df in fracPokemon.groupby('Type 1')}

    compteur = 0
    ltemp = []
    ltemp2 = []

    for type_name in dfByType:
        df_type = dfByType[type_name].copy()
        if compteur % 2 == 0:
            ltemp.append(df_type.iloc[::2])
            ltemp2.append(df_type.drop(df_type.iloc[::2].index))
        else:
            ltemp2.append(df_type.iloc[::2])
            ltemp.append(df_type.drop(df_type.iloc[::2].index))
        compteur += 1

    deck1 = pd.concat(ltemp)
    deck2 = pd.concat(ltemp2)

    if len(deck1) < deck_size:
        diff = deck_size - len(deck1)
        supplement = deck2.sample(diff)
        deck1 = pd.concat([deck1, supplement])
        deck2 = deck2.drop(supplement.index)
    elif len(deck2) < deck_size:
        diff = deck_size - len(deck2)
        supplement = deck1.sample(diff)
        deck2 = pd.concat([deck2, supplement])
        deck1 = deck1.drop(supplement.index)

    deck1["Level"] = 1
    deck2["Level"] = 1

    return deck1, deck2

