import pandas as pd
import numpy as np
##1

df=pd.read_csv("/Users/leob/Desktop/L3 Eco-MIASHS/Algo/Projet/Partie Pokemon/Pokemon intranet.csv",sep=',',index_col="Name")
pd.DataFrame.info(df)
##2
#print(df.head(10))
##3
#print(df["Type 2"])
##4
df["Type 2"]=np.where(pd.isna(df["Type 2"]),'',df["Type 2"])
#print(df["Type 2"])
##5
df=df.drop(["#","Sp. Atk","Sp. Def"],axis=1)
#print(df.head(2))
##6
valeur=df.loc["Bulbasaur",["Type 1","Type 2"]].values
#print(valeur)
##7
ligne=df.tail(5)
colonne=df.tail(5)[df.tail(5).columns[[0,1]]]
#print(colonne)
##8
sortie=df.index[(df["Legendary"]==True) &(df["Type 1"]=='Grass')]
##9
desc=df[["Total", "HP", "Attack", "Defense"]].describe()
print(desc)
##10
maxi=df.index[df["HP"]==255]
maxim=df[df["HP"]==df["HP"].max()]
print(maxi)
print(maxim)
##11
dftri=df.sort_values(by="Speed")
#print(dftri.tail(3))
##12
print(df["Legendary"].value_counts())
##13
df["legendary"]=np.where(df["Legendary"]==True,1,0)
dftri=df.sort_values(by="legendary",ascending=False)
print(dftri)
##14
dfleg=df.where(df["legendary"]==1)
print(df[["Total","HP","Attack","Defense","Speed"]].mean())
