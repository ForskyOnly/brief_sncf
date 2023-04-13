import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt 
import folium
from streamlit_folium import folium_static


####################################################### BOUTTON METTRE A JOURS ######################################################################################

    
if st.button(label="Mettre à jour les données", help="Mettre à jour les données de fréquentation de la gare, les données de la méteo ainsi que les objets perdus",use_container_width=True):
    df_gare = pd.read_csv("frequentations_gare.csv")
    df_objet_trouve = pd.read_csv("objets_perdus.csv")
    df_meteo = pd.read_csv("donneemeteo.csv")
    st.write(":green[Les données ont été mises à jour avec succès !]",":white_check_mark:")
    st.balloons()

    
    
    
############################################## Calculez entre 2019 et 2022 la somme du nombre d’objets trouvés par semaine ###########################################
    
# Chargement des données
df_objet_trouve = pd.read_csv("objets_perdus.csv")

# Conversion de la colonne "date" au format datetime
df_objet_trouve["Date"] = pd.to_datetime(df_objet_trouve["Date"])

# Filtrage des données entre 2019 et 2022
df_objet_trouve = df_objet_trouve[(df_objet_trouve["Date"].dt.year >= 2019) & (df_objet_trouve["Date"].dt.year <= 2022)]

# Calcul de la somme du nombre d'objets trouvés par semaine
df_objet_trouve_par_sem = df_objet_trouve.groupby(pd.Grouper(key="Date", freq="W-MON")).size().reset_index(name="sum")


st.header("Répartition du nombre d'objets trouvés par semaine")
# Affichage des types d'objets trouvés pour sélection
objet_types = list(df_objet_trouve["Type_objet"].unique())
objet_types_selectionnes = st.multiselect("Sélectionnez les types d'objets à inclure", objet_types, default=objet_types)

# Filtrage des données pour inclure seulement les types d'objets sélectionnés
df_objet_trouve_filtre = df_objet_trouve[df_objet_trouve["Type_objet"].isin(objet_types_selectionnes)]
df_objet_trouve_par_sem_filtre = df_objet_trouve_filtre.groupby(pd.Grouper(key="Date", freq="W-MON")).size().reset_index(name="sum")


# Création de l'histogramme avec Plotly
fig = px.scatter(df_objet_trouve_par_sem_filtre, x="Date", y="sum")

# Configuration de l'histogramme
fig.update_layout(
    xaxis_title="Semaine",
    yaxis_title="Nombre d'objets trouvés"
)

# Affichage de l'histogramme
st.plotly_chart(fig)

st.write("<br>""<br>""<br>""<br>", unsafe_allow_html=True)



################################################################### AFFICHER LA CARTE ###############################################################################


df_gare = pd.read_csv("frequentations_gare.csv")
df_objet_trouve = pd.read_csv("objets_perdus.csv")


st.header("Carte de Paris avec le nombre d'objets trouvés en fonction de la fréquentation de voyageur de chaque gare :")

df_objet_trouve["Date"] = pd.to_datetime(df_objet_trouve["Date"])

# Création d'une selection pour trier par année 
annee = st.selectbox("Tri par année", df_objet_trouve["Date"].dt.year.unique())

# Création d'une sélection  pour choisir de trier par types d'objets
type_objet = st.multiselect("Tri par type d'objet", df_objet_trouve["Type_objet"].unique())

# Filtre les objets trouvés en fonction de l'année et du type d'objet 
df_objet_trouve_filtré = df_objet_trouve[(df_objet_trouve["Date"].dt.year == annee) & (df_objet_trouve["Type_objet"].isin(type_objet))]

# Compte le nombre d'objets trouvés par gare
df_resultat = df_objet_trouve_filtré.groupby("Nom_gare").size().reset_index(name="objets_trouves")

# Fusionne les données avec les informations de la gare (position geo + frequentation)
df_resultat = df_resultat.merge(df_gare[["nom_gare", "frequentation_" + str(annee), "latitude", "longitude"]], left_on="Nom_gare", right_on="nom_gare")

# Creation d'une carte centré sur Paris
paris_carte= folium.Map(location=[48.8566, 2.3522], zoom_start=12.5)

# Ajoute un pop up sur la carte pourchaque gare avec les informations sur les objets trouvés et la fréquentation
for index, row in df_resultat.iterrows():
    pop_up = f"{row['Nom_gare']}<br>Objets trouvés: {row['objets_trouves']}<br>Fréquentation: {row['frequentation_' + str(annee)]}"
    folium.Marker([row["latitude"], row["longitude"]], tooltip=pop_up).add_to(paris_carte)

folium_static(paris_carte)

st.write("<br>""<br>""<br>""<br>", unsafe_allow_html=True)

########################################################### Nombre d'objets trouvés en fonction de la température ####################################################


df_meteo = pd.read_csv("donneemeteo.csv")
df_objet_trouve = pd.read_csv("objets_perdus.csv")

# modifs du nom de colonne
df_meteo = df_meteo.rename(columns={'time': 'Date'})

# creation d'un DF où on les joint 2 DF sur la base de la colonne date
df_merged = df_objet_trouve.merge(df_meteo, on='Date')

# regroupe et compte le nombre d'objets trouvés par température
df_grouped = df_merged.groupby('temperature').size().reset_index(name='nombre_objets_trouves')

st.header("Nombre d'objets trouvés en fonction de la température :")

# Création d'un scatterplot avec la température sur l'axe  x et objets trouvés sur l'axe y
scatterplot = alt.Chart(df_grouped).mark_circle(size=60).encode(
    x=alt.X('temperature:Q', title='Température'),
    y=alt.Y('nombre_objets_trouves:Q', title="Nombre d'objets trouvés")
)
st.altair_chart(scatterplot, use_container_width=True)

# Calcule du coefficient de corrélation
correlation = df_grouped['temperature'].corr(df_grouped['nombre_objets_trouves']).__round__(4)
st.write("D'après ce graphique, il semblerait que la température n'ait pas une grande influence sur le nombre d'objets perdus. De plus, le coefficient de corrélation de Pearson calculé n'est que de", correlation,"points.","<br>""<br>""<br>""<br>", unsafe_allow_html=True)



#################################################### Quelle est la médiane du nombre d’objets trouvés en fonction de la saison #######################################

# focntion pour trier les saisons

def get_season(date):
    month = date.month
    if 3 <= month <= 5:
        return "printemps"
    elif 6 <= month <= 8:
        return "été"
    elif 9 <= month <= 11:
        return "automne"
    else:
        return "hiver"

df_objet_trouve["Date"] = pd.to_datetime(df_objet_trouve["Date"])

# Ajout d'une colonne saison
df_objet_trouve["saison"] = df_objet_trouve["Date"].apply(get_season)

# Calcule de la mediane + regroupe par saison & nb d'objet trouvés
df_grouped = df_objet_trouve.groupby(["Date", "saison"]).size().reset_index(name='nombre_objets_trouves')
df_median = df_grouped.groupby("saison")["nombre_objets_trouves"].median().reset_index()

st.header("Médiane journalier du nombre d'objets trouvés par saisons :")

# Creartion du graphique
fig = px.bar(df_median, x='saison', y='nombre_objets_trouves', text='nombre_objets_trouves',
             color='saison', color_discrete_sequence=px.colors.qualitative.Set1)

# Personnaliser le graphique
fig.update_layout(
    xaxis_title="Saisons",
    yaxis_title="Médiane du nombre d'objets trouvés / J",
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



##################################### Affichez le nombre d'objets trouvés en fonction du type de d'objet et de la saison sur un graphique ############################

st.header("Nombre d'objets trouvés en fonction de la saison du type d'objet ")


# Possibilté de choisir par type d'objet
selected_types = st.multiselect("Tri par types d'objet", df_objet_trouve["Type_objet"].unique(), default=df_objet_trouve["Type_objet"].unique())

# Possibilité de choisir une année en particulier ou le total des anneés
annees = list(df_objet_trouve["Date"].dt.year.unique())
annees.append("Total")

# Creation d'un selectbox pour choisir l'année
annee_selectionnee = st.selectbox("Tri par Année", annees)

# Filtrer en fonction de l'année
if annee_selectionnee == "Total":
    df_filtre = df_objet_trouve[df_objet_trouve["Type_objet"].isin(selected_types)]
else:
    df_filtre = df_objet_trouve[(df_objet_trouve["Date"].dt.year == annee_selectionnee) & df_objet_trouve["Type_objet"].isin(selected_types)]

# Creation d'un DF groupé par saison et type d'objet
df_grouped = df_filtre.groupby(['saison', 'Type_objet']).size().reset_index(name='nombre_objets_trouves')

# Regroupper en foction des types d'objets
df_grouped_filtered = df_grouped[df_grouped["Type_objet"].isin(selected_types)]

# Creation du Graphique 
fig = px.bar(df_grouped_filtered, x="saison", y="nombre_objets_trouves", color="Type_objet", barmode="group")

fig.update_layout(
    xaxis_title="Saisons",
    yaxis_title="Nombre d'objets trouvés"
)

st.plotly_chart(fig)

st.write("On peut observer de part cet histogramme, qu'il y a en effet une corrélation entre le type d'objets retrouvé et la saison. Le type d'objet Bagagerie est plus retrouvé lors de la saison de l'automne avec 7647 objets suivi de la saison estivale avec 7384 objets respectivement retrouvés.", "<br>""<br>""<br>""<br>", unsafe_allow_html=True)


st.write("<br><br><h1>Conclusion :</h1>", unsafe_allow_html=True)
st.write("<br><h3>Pour conclure d’après tout ces graphiques, la perte d’objets de tout type est variable selon les saisons et le type vetements n’est pas relié à la saison hivernale avec peu de différences entre les saisons.<br><br>En revanche on remarque que les voyageurs perdent plus leurs affaires de tout types et plus particulièrement de type bagagerie  pendant les saisons estivale ainsi que de l’automne avec une frequentation élevée à la Gare Paris gare de Lyon.<br><br>Cela peut etre expliqué notamment par le départ en vacances des voyageurs souvent chargés en terme de bagages lors des ces saisons, dans la gare la plus solicitée de Paris pour voyager avec une offre dédiée aux TGV.</h3>",
         unsafe_allow_html=True, 
        )