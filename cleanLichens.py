import os
import pandas as pd
import seaborn as sns
import numpy
import matplotlib as plt
import matplotlib.pyplot as plt
import requests
import sys
import os
import io
import tkinter as tk
from tkinter import filedialog
from pandas import DataFrame
# Import des données depuis l'API TelaBotanica en CSV

url = "https://api.tela-botanica.org/service:cel:CelWidgetExport/export?pays=FR%2CFX%2CGF%2CPF%2CTF&programme=tb_lichensgo&standard=1&debut=0&limite=20000&format=csv&colonnes=standardexport,auteur,avance,etendu,standard"
source = requests.get(url).content
df = pd.read_csv(io.StringIO(source.decode('utf-8')))

df_copy = df.copy()

# Colonne avec les valeurs manquantes
"""
@:param : un Dataframe
        : détermine le nombre de valeurs manquantes pour chaque colonnes
"""


def missing_cols(df):
    '''prints out columns with its amount of missing values'''
    total = 0
    for col in df.columns:
        missing_vals = df[col].isnull().sum()
        total += missing_vals
        if missing_vals != 0:
            print(f"{col} => {df[col].isnull().sum()}")

    if total == 0:
        print("no missing values left")


# Pourcentage des valeurs manquantes
"""
@:param : un Dataframe
        : détermine le nombre de valeurs manquantes pour chaque colonnes en pourcentage
        
"""


def donnee_manquantes(df):
    '''prints out columns with missing values with its %'''
    for col in df_copy.columns:
        pct = df[col].isna().mean() * 100
        if (pct != 0):
            print('{} => {}%'.format(col, round(pct, 2)))


"""
@:param : Dataframe
retourne une carte de chaleur des valeurs null et non null  
"""
def carteChaleur(df):
    fig, ax = plt.subplots(figsize=(25, 8))
    cols = df_copy.columns[:]
    colours = ['#000099', '#ffff00']  # specify the colours - yellow is missing. blue is not missing.
    sns.heatmap(df[cols].isnull(), cmap=sns.color_palette(colours))

# Supression des colonnes non nécessaires


colonnes_a_sup = ["Lieu-dit", "Milieu", "Notes", "Lien vers l'observation sur IdentiPlante",
                  "Image(s)","Cohérence entre la localité et les coordonnées GPS",
                  "Précision de la localisation","Station", "Abondance",
                  "Phénologie", "Observateur", "Structure de l'observateur",
                  "Déterminateur","Source bibliographique", "ext:altitude-releve",
                  "ext:circonference", "ext:face-ombre", "ext:com-arbres",
                  "ext:latitude-arbres","ext:longitude-arbres", "ext:altitude-arbres",
                  "Nom retenu", "Numéro nomenclatural nom retenu","Certitude", "Source de la saisie",
                  "Mots Clés", "Indicateur de fiabilité", "Score IdentiPlante",
                  "Abondance", "Phénologie", "Transmis",
                  "Présence d'un échantillon d'herbier", "Date Transmission"]

df_copy.drop(colonnes_a_sup, axis=1, inplace=True)

# Correction du type des diffents champs

df_copy["Identifiant Commune" ] = df_copy['Identifiant Commune'].astype(str)


# Traitement des valeurs manquantes dans le dataFrame.
df_copy.Famille = df_copy["Famille"].fillna("Null")
df_copy["Référentiel taxonomique"] = df_copy["Référentiel taxonomique"].fillna("Inconnu")
df_copy["Identifiant Commune"] = df_copy["Identifiant Commune"].fillna("Inconnu").astype(str)
df_copy["Identifiant"] = df_copy["Identifiant"].astype(str)
df_copy["Numéro nomenclatural"] = df_copy["Numéro nomenclatural"].fillna("Inconnu").astype(str)
df_copy["Espèce"] = df_copy["Espèce"].fillna("Null")
df_copy["Floutage (niveau de localisation diffusé)"] = df_copy["Floutage (niveau de localisation diffusé)"].fillna("Null")
df_copy["ext:loc-sur-tronc"] = df_copy["ext:loc-sur-tronc"].fillna("Null").astype(str)
df_copy["ext:loc-sur-tronc"] = df_copy["ext:loc-sur-tronc"].str.split(";")


########################################################################################################################################################

root = tk.Tk()
canvas1 = tk.Canvas(root, width=300, height=300, bg='lightsteelblue2', relief='raised')
canvas1.pack()

def exportCSV():
    global df

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv(export_file_path, index=False, header=True)


saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white',
                             font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=saveAsButton_CSV)

root.mainloop()