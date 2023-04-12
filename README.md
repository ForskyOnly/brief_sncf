
# Brief Find in translation

## Context du projet

Le projet consiste à analyser les données des objets trouvés dans les gares parisiennes de la SNCF entre 2019 et 2022, en utilisant l'API open data de la SNCF et des données météorologiques récupérées sur internet. Le but est de comprendre si la température est corrélée au nombre d'objets trouvés et d'anticiper le volume d'objets perdus pour dimensionner au mieux le service en charge de leur gestion.


## Description du projet 

Ce projet a été réalisé lors de la formation Dev IA Microsoft by Simplon HDF.
Ce projet utilise l'API Open data de SNCF pour récupérer les informations de frequentations des gares parisiennes ainsi que les objets perdus dans ces gares. Il comprend également une visualisation de ces informations à l'aide de la bibliothèque Folium et une interface Web construite avec Streamlit.

## Fonctionnalités

#### Récupération des données :

1. Utilisation de l'API open data de la SNCF pour récupérer les données sur les objets trouvés ainsi que la frequentation dans les gares parisiennes entre 2019 et 2022.
2. Récupération des données météorologiques de Paris entre 2019 et 2022
3. Stockage des données dans une BDD SQL avec un schéma de base de données.
4. Créaion de fichier csv pour les données récoltès.

#### Analyse visuelle des données avec Streamlit :

5. Calcul du nombre d'objets trouvés par semaine et affichage sur un histogramme
6. Affichage d'une carte de Paris avec le nombre d'objets trouvés en fonction de la fréquentation des voyageurs de chaque gare. Possibilité de faire varier par année et par type d'objets.

#### Analyse des données en vue de la Data Science avec Streamlit :

7. Affichage du nombre d'objets trouvés en fonction de la température sur un scatterplot et recherche de corrélation.
8. Calcul de la médiane du nombre d'objets trouvés en fonction de la saison et recherche de corrélation.
9. Affichage du nombre d'objets trouvés en fonction du type d'objet et de la saison et recherche de corrélation.

## Installation

1. Clonez [ce dépôt.](https://github.com/ForskyOnly/brief_sncf)
2. Installez les dépendances avec `pip install`.


## bibliothèque utilisées

- streamlit 
- pandas as pd
- plotly.express 
- altair   
- folium
- streamlit_folium 
- sqlite3
- requests
- datetime

## Utilisation

- Exécutez tout les notebooks `.ipynb` pour récupérer les informations.
- Exécutez `streamlit run main.py` pour lancer l'interface Web Streamlit.

## Contributeurs

Ce projet a été réalisé par [Amine](https://github.com/amineelbb) et [Rubic](https://github.com/ForskyOnly)



## License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
