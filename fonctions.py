from urllib.request import urlopen
import pandas as pd
import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt
import requests
import seaborn as sns
import io
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk


"""
def telecharger():

    try: 
        os.makedirs('DonnéeBrut')
    except OSError:
        if not os.path.isdir('DonnéeBrut'):
            Raise
"""
# import requests
#Telechargement de données
url = "https://api.tela-botanica.org/service:cel:CelWidgetExport/export?pays=FR%2CFX%2CGF%2CPF%2CTF&programme=tb_lichensgo&standard=1&debut=0&limite=20000&format=csv&colonnes=standardexport,auteur,avance,etendu,standard"
result = requests.get(url).content
df = pd.read_csv(io.StringIO(result.decode('utf-8')))
#df.to_csv("DonnéeBrut/Lichen.csv")
df_copy = df.copy()


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

df_copy["Id_site"] = df_copy["ext:latitude-releve"].astype(str) + df_copy["ext:longitude-releve"].astype(str)

    # Suppression des colonnes non nécessaires

colonnes_a_sup = ["Lieu-dit", "Milieu", "Notes", "Lien vers l'observation sur IdentiPlante", "Image(s)", "Cohérence entre la localité et les coordonnées GPS", "Précision de la localisation",
                  "Station", "Abondance", "Phénologie", "Observateur", "Structure de l'observateur","Déterminateur","Source bibliographique", "ext:altitude-releve",
                  "ext:face-ombre", "ext:com-arbres","ext:latitude-arbres","ext:longitude-arbres","ext:altitude-arbres", "Nom retenu", "Numéro nomenclatural nom retenu",
                  "Certitude",  "Transmis", "Source de la saisie", "Mots Clés","Indicateur de fiabilité",  "Score IdentiPlante", "Abondance", "Phénologie",
                  "Présence d'un échantillon d'herbier" ,"Date Transmission"]

df_copy.drop(colonnes_a_sup, axis = 1, inplace = True)

    #convertir la colonne Identifiant commune en str. 
df_copy["Identifiant Commune" ] = df_copy['Identifiant Commune'].astype(str)
df_copy["Identifiant" ] = df_copy['Identifiant'].astype(str)
df_copy["Numéro nomenclatural" ] = df_copy['Numéro nomenclatural'].astype(str)
df_copy["Détermination validée sur IdentiPlante" ] = df_copy['Détermination validée sur IdentiPlante'].astype(str)

#Creation du repertoire d'enregistrement des tables en sortie
"""
    try: 
        os.makedirs('OutPut')
    except OSError:
        if not os.path.isdir('OutPut'):
            Raise
"""
# Traitement des valeurs manquantes dans le dataFrame.
# df_copy.Famille = df_copy["Famille"].fillna("Null")
df_copy["Référentiel taxonomique"] = df_copy["Référentiel taxonomique"].fillna("Inconnu")
df_copy["Identifiant Commune"] = df_copy["Identifiant Commune"].fillna("Inconnu").astype(str)
df_copy["Identifiant"] = df_copy["Identifiant"].astype(str)
df_copy["Numéro nomenclatural"] = df_copy["Numéro nomenclatural"].fillna("Inconnu").astype(str)
df_copy["Espèce"] = df_copy["Espèce"].fillna("Null")
df_copy["Floutage (niveau de localisation diffusé)"] = df_copy["Floutage (niveau de localisation diffusé)"].fillna("Null")
df_copy["ext:loc-sur-tronc"] = df_copy["ext:loc-sur-tronc"].str.split(";")
df_copy['ext:circonference'] = df_copy['ext:circonference'].replace(np.nan, 0)
df_copy["ext:loc-sur-tronc"] = df_copy["ext:loc-sur-tronc"].fillna("Null").astype(str)


    #Sélectionner les arbres et les exporter vers une tables uniques =====================================
#Sélectionner les arbres et les exporter vers une tables uniques
filtr_arbre_saisi =  df_copy[df_copy['ext:latitude-releve'].notnull()]
arbre_saisi = pd.DataFrame(filtr_arbre_saisi[["Identifiant","Id_site","Latitude","Longitude","Espèce","Famille","ext:num_arbre","ext:circonference"]])
arbre_saisi.rename(columns = {'Espèce':'Espece_arbre',
                              'Identifiant' : 'Id_arbre'}, inplace = True)

#arbre_saisi.to_csv("table_arbre.csv", index=False)

    #Séléctionner les lichens==================================== 
filtr_lichens_saisi = df_copy[df_copy['ext:id_obs_arbre'].notnull()]
lichens_saisi = pd.DataFrame(filtr_lichens_saisi[["Identifiant","Espèce","ext:id_obs_arbre"]])


lichens_saisi.rename(columns = {'Espèce' : 'Espece_lichens','Identifiant' : 'Id_lichens','ext:id_obs_arbre':'Id_arbre'}, inplace=True)
lichens_saisi['Id_arbre'] = lichens_saisi['Id_arbre'].replace(np.nan,0)
lichens_saisi['Id_arbre'] = lichens_saisi['Id_arbre'].astype(int)
lichens_saisi['Id_arbre'] = lichens_saisi['Id_arbre'].astype(str)

    #Séléctionner des sites======================================
filtr_site_saisi =  df_copy[df_copy['ext:latitude-releve'].notnull()]
table_site = filtr_site_saisi[["Id_site", "ext:latitude-releve","ext:longitude-releve", "ext:rue", "Commune", "Pays"]]
table_site = table_site.drop_duplicates()
#table_site.to_csv("table_site.csv",index=False)

#Séléctionner des elements de la table Quadrat ======================================

filtre_quadrat_saisi = df_copy[df_copy['ext:id_obs_arbre'].notnull()]
table_quadrat = pd.DataFrame(filtre_quadrat_saisi[["Identifiant","ext:loc-sur-tronc","Date"]])
table_quadrat.rename(columns={'Identifiant':'Id_lichens','ext:loc-sur-tronc' : 'Location_lichens_sur_arbre','Date':'Date_Observation'},inplace=True)
table_quadrat["Id_arbre"] = lichens_saisi["Id_arbre"]
table_quadrat = table_quadrat.reindex(columns = ['Id_lichens','Id_arbre','Location_lichens_sur_arbre','Date_Observation'])
table_quadrat = table_quadrat.reset_index()
table_quadrat.rename(columns = {'index': 'Id_quadrat'},inplace=True)
table_quadrat.Id_quadrat = np.arange(1, len(table_quadrat)+1)

#Ajout de l'Id quadra à la table Lichen==================================================================
lichens_saisi["Id_quadrat"] = table_quadrat["Id_quadrat"]

#Séléctionner des elements de la table Completude=================================================================
filtr_completude_saisi =  df_copy[df_copy['ext:latitude-releve'].notnull()]
table_completude = pd.DataFrame(filtr_completude_saisi[["Id_site","Identifiant", "ext:latitude-releve","ext:longitude-releve","ext:num_arbre", "ext:rue", "Commune", "Pays"]])
table_completude.rename(columns={'Identifiant':'Id_arbre',"ext:latitude-releve":"Latitude_site","ext:longitude-releve":"Longitude_site","ext:num_arbre":"Num_arbre","ext:rue":"Rue"},inplace=True)

    #========================Extraction des tables=============================
"""
arbre_saisi.to_csv("table_arbre.csv", index=False)
lichens_saisi.to_csv("table_lichens.csv",index=False)
table_site.to_csv("table_site.csv", index=False)
table_quadrat.to_csv("table_quadrat.csv", index=False)
table_completude.to_csv("table_completude.csv", index=False)
"""
"""
    lichens_saisi.to_csv("OutPut/table_lichens.csv",index=False)
"""
root = tk.Tk()
canvas1 = tk.Canvas(root, width=900, height=650, bg='lightsteelblue2', relief='raised')
canvas1.pack()

def exportCSV():
    global df

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='clean_data', title='Export Données Lichens Go !')
    df_copy.to_csv(export_file_path, index=False, header=True)

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='table_arbre_saisi', title='Export Données Lichens Go !')
    arbre_saisi.to_csv(export_file_path, index=False, header=True)

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='table_lichens_saisi', title='Export Données Lichens Go !')
    lichens_saisi.to_csv(export_file_path, index=False, header=True)

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='table_quadrat', title='Export Données Lichens Go !')
    table_quadrat.to_csv(export_file_path, index=False, header=True)

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='table_completude', title='Export Données Lichens Go !')
    table_completude.to_csv(export_file_path, index=False, header=True)

    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv', initialfile='table_site', title='Export Données Lichens Go !')
    table_site.to_csv(export_file_path, index=False, header=True)


saveAsButton_CSV = tk.Button(text='Exporter les tables dans un dossier',  command=exportCSV, bg='green', fg='white',
                             font=('helvetica', 12, 'bold'))
canvas1.create_window(450, 450, window=saveAsButton_CSV)

URL = "https://www.open-sciences-participatives.org/uploads/img/program/logo_progam/5c095adeace69_Logo-LichensGo-jaune_RVB.jpg"
u = urlopen(URL)
raw_data = u.read()
u.close()
photo = ImageTk.PhotoImage(data=raw_data) # <-----




# Display image
canvas1.create_image(0, 0, image=photo, anchor="nw")

root.mainloop()

