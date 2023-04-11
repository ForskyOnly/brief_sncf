import pandas as pd
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import folium_static





# Chargement des données
df_objet_trouve = pd.read_csv("objet_perdus.csv")

# Conversion de la colonne "date" au format datetime
df_objet_trouve["date"] = pd.to_datetime(df_objet_trouve["date"])

# Filtrage des données entre 2019 et 2022
df_objet_trouve = df_objet_trouve[(df_objet_trouve["date"].dt.year >= 2019) & (df_objet_trouve["date"].dt.year <= 2022)]

# Calcul de la somme du nombre d'objets trouvés par semaine
df_objet_trouve_par_sem = df_objet_trouve.groupby(pd.Grouper(key="date", freq="W-MON")).size().reset_index(name="sum")
#df_objet_trouve_par_sem = df_objet_trouve.groupby(df_objet_trouve["Date"].dt.reset_index(name="sum")
# Affichage des types d'objets trouvés pour sélection
objet_types = list(df_objet_trouve["type_objet"].unique())
objet_types_selectionnes = st.multiselect("Sélectionnez les types d'objets à inclure", objet_types, default=objet_types)

# Filtrage des données pour inclure seulement les types d'objets sélectionnés
df_objet_trouve_filtre = df_objet_trouve[df_objet_trouve["type_objet"].isin(objet_types_selectionnes)]
df_objet_trouve_par_sem_filtre = df_objet_trouve_filtre.groupby(pd.Grouper(key="date", freq="W-MON")).size().reset_index(name="sum")

# Affichage du tableau de données
st.write("Tableau de données", df_objet_trouve_par_sem_filtre)

# Création de l'histogramme avec Plotly
fig = px.scatter(df_objet_trouve_par_sem_filtre, x="date", y="sum")

# Configuration de l'histogramme
fig.update_layout(
    title="Répartition du nombre d'objets trouvés par semaine",
    xaxis_title="Semaine",
    yaxis_title="Nombre d'objets trouvés"
)

# Affichage de l'histogramme
st.plotly_chart(fig)

fig




################################################################### AFFICHER LA CARTE ###############################################################################


df_gare = pd.read_csv("frequentations_gare.csv")
df_objet_trouve = pd.read_csv("objet_perdus.csv")


st.header("Carte de Paris avec le nombre d'objets trouvés en fonction de la fréquentation de voyageur de chaque gare :")

# Convertion la colonne date en type datetime
df_objet_trouve["date"] = pd.to_datetime(df_objet_trouve["date"])

# Crée la possibilité de choisir une année 
annee = st.selectbox("Sélectionnez une année", df_objet_trouve["date"].dt.year.unique())

# Crée une sélection  pour choisir les types d'objets
type_objet = st.multiselect("Sélectionnez le type d'objet", df_objet_trouve["type_objet"].unique())

# Filtre les objets trouvés en fonction de l'année et du type d'objet 
df_objet_trouve_filtré = df_objet_trouve[(df_objet_trouve["date"].dt.year == annee) & (df_objet_trouve["type_objet"].isin(type_objet))]

# Compte le nombre d'objets trouvés par gare
df_resultat = df_objet_trouve_filtré.groupby("nom_gare").size().reset_index(name="objets_trouves")

# Fusionne les données avec les informations de la gare (fréquentation, latitude, longitude)
df_resultat = df_resultat.merge(df_gare[["nom_gare", "frequentation_" + str(annee), "latitude", "longitude"]], left_on="nom_gare", right_on="nom_gare")

# Crée une carte de Paris
paris_carte= folium.Map(location=[48.8566, 2.3522], zoom_start=12)

# Ajoute un pop up pour chaque gare avec les informations sur les objets trouvés et la fréquentation
for index, row in df_resultat.iterrows():
    pop_up = f"{row['nom_gare']}<br>Objets trouvés: {row['objets_trouves']}<br>Fréquentation: {row['frequentation_' + str(annee)]}"
    folium.Marker([row["latitude"], row["longitude"]], tooltip=pop_up).add_to(paris_carte)

folium_static(paris_carte)
