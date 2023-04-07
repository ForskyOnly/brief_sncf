
import streamlit as st
import pandas as pd
import plotly.express as px



# Chargement des données
df_objet_trouve = pd.read_csv("objet_perdus.csv")

# Conversion de la colonne "date" au format datetime
df_objet_trouve["Date"] = pd.to_datetime(df_objet_trouve["Date"])

# Filtrage des données entre 2019 et 2022
df_objet_trouve = df_objet_trouve[(df_objet_trouve["Date"].dt.year >= 2019) & (df_objet_trouve["Date"].dt.year <= 2022)]

# Calcul de la somme du nombre d'objets trouvés par semaine
df_objet_trouve_par_sem = df_objet_trouve.groupby(pd.Grouper(key="Date", freq="W-MON")).size().reset_index(name="sum")
#df_objet_trouve_par_sem = df_objet_trouve.groupby(df_objet_trouve["Date"].dt.reset_index(name="sum")
# Affichage des types d'objets trouvés pour sélection
objet_types = list(df_objet_trouve["Type_objet"].unique())
objet_types_selectionnes = st.multiselect("Sélectionnez les types d'objets à inclure", objet_types, default=objet_types)

# Filtrage des données pour inclure seulement les types d'objets sélectionnés
df_objet_trouve_filtre = df_objet_trouve[df_objet_trouve["Type_objet"].isin(objet_types_selectionnes)]
df_objet_trouve_par_sem_filtre = df_objet_trouve_filtre.groupby(pd.Grouper(key="Date", freq="W-MON")).size().reset_index(name="sum")

# Affichage du tableau de données
st.write("Tableau de données", df_objet_trouve_par_sem_filtre)

# Création de l'histogramme avec Plotly
fig = px.scatter(df_objet_trouve_par_sem_filtre, x="Date", y="sum")

# Configuration de l'histogramme
fig.update_layout(
    title="Répartition du nombre d'objets trouvés par semaine",
    xaxis_title="Semaine",
    yaxis_title="Nombre d'objets trouvés"
)

# Affichage de l'histogramme
st.plotly_chart(fig)

fig