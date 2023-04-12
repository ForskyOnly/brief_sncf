Projet brief_sncf

Ce projet consiste à analyser les données des objets trouvés dans les gares parisiennes de la SNCF entre 2019 et 2022, en utilisant l'API open data de la SNCF et des données météorologiques récupérées sur internet. Le but est de comprendre si la température est corrélée au nombre d'objets trouvés et d'anticiper le volume d'objets perdus pour dimensionner au mieux le service en charge de leur gestion.
Étapes du projet

    Utilisation de l'API open data de la SNCF pour récupérer les données sur les objets trouvés dans les gares parisiennes entre 2019 et 2022. Stockage des données dans une BDD SQL de choix avec un schéma de base de données.

    Récupération de la liste des températures journalières sur Paris en France entre 2019 et 2022.

    Analyse visuelle des données avec Streamlit :

    Calcul du nombre d'objets trouvés par semaine et affichage sur un histogramme plotly.
    Affichage d'une carte de Paris avec le nombre d'objets trouvés en fonction de la fréquentation des voyageurs de chaque gare. Possibilité de faire varier par année et par type d'objets.

    Analyse des données en vue de la Data Science avec Streamlit :

    Affichage du nombre d'objets trouvés en fonction de la température sur un scatterplot et recherche de corrélation.
    Calcul de la médiane du nombre d'objets trouvés en fonction de la saison et recherche de corrélation.
    Affichage du nombre d'objets trouvés en fonction du type d'objet et de la saison et recherche de corrélation.

    Intégration de la conclusion globale de l'étude dans Streamlit.

    Bonus Data Ingénieur : ajout d'un bouton pour la mise à jour des données de l'application.

Technologies utilisées

    Python 3.8
    Streamlit
    Pandas
    Matplotlib
    Plotly
    SQL

Comment exécuter le code

    Cloner le repo GitHub.

    Installer les dépendances avec pip install -r requirements.txt.

    Exécuter les scripts dans l'ordre suivant :

    get_data.py pour récupérer les données de la SNCF et les stocker dans une base de données SQL.
    get_temperature.py pour récupérer les données de température et les stocker dans un fichier CSV.
    app.py pour lancer l'application Streamlit.

    Ouvrir l'application Streamlit dans le navigateur.

Auteur

Ce projet a été réalisé par un développeur indépendant.