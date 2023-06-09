import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt 
import folium
from streamlit_folium import folium_static
import sqlite3
from datetime import datetime


################################################################# BOUTTON METTRE A JOURS ########################################################################
conn = sqlite3.connect('bdd1.db')
    
if st.button(label="Mettre à jour les données", help="Mettre à jour les données de fréquentation de la gare, les données de la méteo ainsi que les objets perdus", use_container_width=True):
    df_gare = pd.read_sql_query("SELECT * FROM gare", conn)
    df_objet_trouve = pd.read_sql_query("SELECT * FROM objet_trouve", conn)
    df_meteo = pd.read_sql_query("SELECT * FROM meteo", conn)

    st.write(":green[Les données ont été mises à jour avec succès !]", ":white_check_mark:")
    st.balloons()
    
    
############################################## Calculez entre 2019 et 2022 la somme du nombre d’objets trouvés par semaine ###########################################
    


# obtention de tout les données de objets trouvés
query = "SELECT * FROM objet_trouve"
df_objet_trouve = pd.read_sql_query(query, conn)

# Conversion de la colonne "date" au format datetime
df_objet_trouve["date"] = pd.to_datetime(df_objet_trouve["date"])

# Filtrage des données entre 2019 et 2022
df_objet_trouve = df_objet_trouve[(df_objet_trouve["date"].dt.year >= 2019) & (df_objet_trouve["date"].dt.year <= 2022)]

# Calcul de la somme du nombre d'objets trouvés par semaine
df_objet_trouve_par_sem = df_objet_trouve.groupby(pd.Grouper(key="date", freq="W-MON")).size().reset_index(name="sum")

st.header("Répartition du nombre d'objets trouvés par semaine")
# Affichage des types d'objets trouvés pour sélection
objet_types = list(df_objet_trouve["type_objet"].unique())
objet_types_selectionnes = st.multiselect("Sélectionnez les types d'objets à inclure", objet_types, default=objet_types)

# Filtrage des données pour inclure seulement les types d'objets sélectionnés
df_objet_trouve_filtre = df_objet_trouve[df_objet_trouve["type_objet"].isin(objet_types_selectionnes)]
df_objet_trouve_par_sem_filtre = df_objet_trouve_filtre.groupby(pd.Grouper(key="date", freq="W-MON")).size().reset_index(name="sum")


# Création de l'histogramme avec Plotly
fig = px.scatter(df_objet_trouve_par_sem_filtre, x="date", y="sum")

# Configuration de l'histogramme
fig.update_layout(
    xaxis_title="Semaine",
    yaxis_title="Nombre d'objets trouvés"
)

# Affichage de l'histogramme
st.plotly_chart(fig)

st.write("<br>""<br>""<br>""<br>", unsafe_allow_html=True)


################################################################### AFFICHER LA CARTE ###############################################################################

# obtention de tout les données d'objets trouvés
query_objet_trouve = "SELECT * FROM objet_trouve"
df_objet_trouve = pd.read_sql_query(query_objet_trouve, conn)

# obtention de tout les donées gare
query_gare = "SELECT * FROM gare"
df_gare = pd.read_sql_query(query_gare, conn)

st.header("Carte de Paris avec le nombre d'objets trouvés en fonction de la fréquentation de voyageur de chaque gare :")

df_objet_trouve["date"] = pd.to_datetime(df_objet_trouve["date"])

# Création d'une sélection pour trier par année
annee = st.selectbox("Tri par année", df_objet_trouve["date"].dt.year.unique())

# Création d'une sélection pour choisir de trier par types d'objets
type_objet = st.multiselect("Tri par type d'objet", df_objet_trouve["type_objet"].unique())

# Filtre les objets trouvés en fonction de l'année et du type d'objet
df_objet_trouve_filtré = df_objet_trouve[(df_objet_trouve["date"].dt.year == annee) & (df_objet_trouve["type_objet"].isin(type_objet))]

# Compte le nombre d'objets trouvés par gare
df_resultat = df_objet_trouve_filtré.groupby("nom_gare").size().reset_index(name="objets_trouves")

# Fusionne les données avec les informations de la gare (position géo + fréquentation)
df_resultat = df_resultat.merge(df_gare[["nom_gare", f"frequentation_{annee}", "latitude", "longitude"]], left_on="nom_gare", right_on="nom_gare")

# Création d'une carte centrée sur Paris
paris_carte = folium.Map(location=[48.8566, 2.3522], zoom_start=12.5)

# Ajoute un pop-up sur la carte pour chaque gare avec les informations sur les objets trouvés et la fréquentation
for index, row in df_resultat.iterrows():
    pop_up = f"{row['nom_gare']}<br>Objets trouvés: {row['objets_trouves']}<br>Fréquentation: {row[f'frequentation_{annee}']}"
    folium.Marker([row["latitude"], row["longitude"]], tooltip=pop_up).add_to(paris_carte)

folium_static(paris_carte)

st.write("<br>""<br>""<br>""<br>", unsafe_allow_html=True)

# ########################################################### Nombre d'objets trouvés en fonction de la température ####################################################


# obtention de tout les données de objets trouvés
query_objet_trouve = "SELECT * FROM objet_trouve"
df_objet_trouve = pd.read_sql_query(query_objet_trouve, conn)

# obtention de tout les données de meteo
query_meteo = "SELECT * FROM meteo"
df_meteo = pd.read_sql_query(query_meteo, conn)

# Création d'un DataFrame où on joint les deux DataFrames sur la base de la colonne date
df_merged = df_objet_trouve.merge(df_meteo, left_on='date', right_on='Date')

# Regroupe et compte le nombre d'objets trouvés par température
df_grouped = df_merged.groupby('temperature').size().reset_index(name='nombre_objets_trouves')

st.header("Nombre d'objets trouvés en fonction de la température :")

# Création d'un scatterplot avec la température sur l'axe x et objets trouvés sur l'axe y
scatterplot = alt.Chart(df_grouped).mark_circle(size=60).encode(
    x=alt.X('temperature:Q', title='Température'),
    y=alt.Y('nombre_objets_trouves:Q', title="Nombre d'objets trouvés")
)
st.altair_chart(scatterplot, use_container_width=True)

# Calcul du coefficient de corrélation
correlation = df_grouped['temperature'].corr(df_grouped['nombre_objets_trouves']).__round__(4)
st.write("D'après ce graphique, il semblerait que la température n'ait pas une grande influence sur le nombre d'objets perdus. De plus, le coefficient de corrélation de Pearson calculé n'est que de", correlation,"points.","<br>""<br>""<br>""<br>", unsafe_allow_html=True)


# #################################################### Quelle est la médiane du nombre d’objets trouvés en fonction de la saison #######################################


# obtention de tout les données de objets trouvés
query_objet_trouve = "SELECT * FROM objet_trouve"
df_objet_trouve = pd.read_sql_query(query_objet_trouve, conn)

def get_season(date: datetime) -> str:
    """
    Renvoie la saison correspondant au mois de la date passée en paramètre.

    Args:
        date (date): Objet date représentant une date.

    Returns:
        str: La saison correspondant au mois de la date passée en paramètre.
    """
    month = date.month
    if 3 <= month <= 5:
        return "printemps"
    elif 6 <= month <= 8:
        return "été"
    elif 9 <= month <= 11:
        return "automne"
    else:
        return "hiver"

df_objet_trouve["date"] = pd.to_datetime(df_objet_trouve["date"])

# Ajout d'une colonne saison
df_objet_trouve["saison"] = df_objet_trouve["date"].apply(get_season)

# Calcule de la médiane + regroupe par saison & nb d'objet trouvés
df_grouped = df_objet_trouve.groupby(["date", "saison"]).size().reset_index(name='nombre_objets_trouves')
df_median = df_grouped.groupby("saison")["nombre_objets_trouves"].median().reset_index()

st.header("Médiane journalière du nombre d'objets trouvés par saisons :")

# Création du boxplot
fig = px.box(df_grouped, x="saison", y="nombre_objets_trouves",
             color="saison", color_discrete_sequence=px.colors.qualitative.Set1)

# Personnaliser le graphique
fig.update_layout(
    xaxis_title="Saisons",
    yaxis_title="Nombre d'objets trouvés / J",
    showlegend=False,
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(
        tickmode='array',
        tickvals=df_median['saison'],
        ticktext=['Printemps', 'Été', 'Automne', 'Hiver']
    )
)

st.plotly_chart(fig)

st.write("On peut observer par ce graphique qu'il n'y a pas de lien notable entre la perte d'objets par les voyageurs et les saisons, donc on peut écarter le lien entre le froid et la perte d'objets par les voyageurs", "<br>""<br>""<br>""<br>", unsafe_allow_html=True)

# ##################################### Affichez le nombre d'objets trouvés en fonction du type de d'objet et de la saison sur un graphique ############################




# obtention de tout les données de objets trouvés
query_objet_trouve = "SELECT * FROM objet_trouve"
df_objet_trouve = pd.read_sql_query(query_objet_trouve, conn)

df_objet_trouve["date"] = pd.to_datetime(df_objet_trouve["date"])

# Ajout d'une colonne saison
df_objet_trouve["saison"] = df_objet_trouve["date"].apply(get_season)

st.header("Nombre d'objets trouvés en fonction de la saison du type d'objet ")

# Possibilté de choisir par type d'objet
selected_types = st.multiselect("Tri par types d'objet", df_objet_trouve["type_objet"].unique(), default=df_objet_trouve["type_objet"].unique())

# Possibilité de choisir une année en particulier ou le total des années
annees = list(df_objet_trouve["date"].dt.year.unique())
annees.append("Total")

# Création d'un selectbox pour choisir l'année
annee_selectionnee = st.selectbox("Tri par Année", annees)

# Filtrer en fonction de l'année
if annee_selectionnee == "Total":
    df_filtre = df_objet_trouve[df_objet_trouve["type_objet"].isin(selected_types)]
else:
    df_filtre = df_objet_trouve[(df_objet_trouve["date"].dt.year == annee_selectionnee) & df_objet_trouve["type_objet"].isin(selected_types)]

# Création d'un DF groupé par saison et type d'objet
df_grouped = df_filtre.groupby(['saison', 'type_objet']).size().reset_index(name='nombre_objets_trouves')

# Regroupper en fonction des types d'objets
df_grouped_filtered = df_grouped[df_grouped["type_objet"].isin(selected_types)]

# Création du Graphique 
fig = px.bar(df_grouped_filtered, x="saison", y="nombre_objets_trouves", color="type_objet", barmode="group")

fig.update_layout(
    xaxis_title="Saisons",
    yaxis_title="Nombre d'objets trouvés"
)

st.plotly_chart(fig)


st.write("On peut observer de par cet histogramme, qu'il y a en effet une corrélation entre le type d'objets retrouvé et la saison. Le type d'objet Bagagerie est plus retrouvé lors de la saison de l'automne avec 7647 objets suivi de la saison estivale avec 7384 objets respectivement retrouvés.", "<br>""<br>""<br>""<br>", unsafe_allow_html=True)


st.write("<br><br><h1>Conclusion :</h1>", unsafe_allow_html=True)
st.write("<br><h3>Pour conclure: d’après tout ces graphiques, la perte d’objets de tout type est variable selon les saisons; et le type 'vetements' n’est pas relié à la saison hivernale. Avec peu de différences entre les saisons.<br><br>En revanche on remarque que les voyageurs perdent plus leurs affaires de tout types et plus particulièrement de type bagagerie  pendant les saisons estivale ainsi qu'en automne, avec une frequentation élevée à la Gare Paris gare de Lyon.<br><br>Cela peut etre expliqué notamment par le départ en vacances des voyageurs souvent chargés en terme de bagages lors des ces saisons, dans la gare la plus solicitée de Paris pour voyager avec une offre dédiée aux TGV.</h3>",
         unsafe_allow_html=True, 
        )