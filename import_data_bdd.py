import requests
import sqlite3
from dateutil.parser import parse
import csv

def creer_base_donnees():
    """
        Crée la base de données SQLite pour stocker les données de la gare, les objets trouvés et la météo.

        Returns:
            conn (sqlite3.Connection): La connexion à la base de données.
    """
    conn = sqlite3.connect("bdd1.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gare (
            id_gare INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_gare TEXT NOT NULL,
            frequentation_2019 INTEGER,
            frequentation_2020 INTEGER,
            frequentation_2021 INTEGER,
            frequentation_2022 INTEGER,
            latitude REAL,
            longitude REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS objet_trouve (
            id_objet INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_gare TEXT NOT NULL,
            type_objet TEXT NOT NULL,
            nature_objet TEXT NOT NULL,
            date TEXT NOT NULL,
            FOREIGN KEY (nom_gare) REFERENCES gare(nom_gare)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meteo (
            id_meteo INTEGER PRIMARY KEY AUTOINCREMENT,
            Date TEXT NOT NULL,
            temperature REAL NOT NULL
        )
    """)

    conn.commit()

    return conn




urls =  ["https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2019&refine.gc_obo_gare_origine_r_name=Paris+Gare+de+Lyon","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2019&refine.gc_obo_gare_origine_r_name=Paris+Montparnasse","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2019&refine.gc_obo_gare_origine_r_name=Paris+Gare+du+Nord","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2019&refine.gc_obo_gare_origine_r_name=Paris+Saint-Lazare","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2019&refine.gc_obo_gare_origine_r_name=Paris+Est","https://ressources.data.sncf.com//api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2019&refine.gc_obo_gare_origine_r_name=Paris+Bercy","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2019&refine.gc_obo_gare_origine_r_name=Paris+Austerlitz","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.gc_obo_gare_origine_r_name=Paris+Austerlitz&refine.gc_obo_date_heure_restitution_c=2020","https://ressources.data.sncf.com//api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2020&refine.gc_obo_gare_origine_r_name=Paris+Bercy","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2020&refine.gc_obo_gare_origine_r_name=Paris+Est","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2020&refine.gc_obo_gare_origine_r_name=Paris+Saint-Lazare","https://ressources.data.sncf.com//api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2020&refine.gc_obo_gare_origine_r_name=Paris+Gare+du+Nord","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2020&refine.gc_obo_gare_origine_r_name=Paris+Montparnasse","https://ressources.data.sncf.com//api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2020&refine.gc_obo_gare_origine_r_name=Paris+Gare+de+Lyon","https://ressources.data.sncf.com//api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2021&refine.gc_obo_gare_origine_r_name=Paris+Montparnasse","https://ressources.data.sncf.com//api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2021&refine.gc_obo_gare_origine_r_name=Paris+Gare+de+Lyon","https://ressources.data.sncf.com//api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2021&refine.gc_obo_gare_origine_r_name=Paris+Saint-Lazare","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2021&refine.gc_obo_gare_origine_r_name=Paris+Gare+du+Nord","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2021&refine.gc_obo_gare_origine_r_name=Paris+Est","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2021&refine.gc_obo_gare_origine_r_name=Paris+Austerlitz","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2021&refine.gc_obo_gare_origine_r_name=Paris+Bercy","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2022&refine.gc_obo_gare_origine_r_name=Paris+Gare+de+Lyon","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2022&refine.gc_obo_gare_origine_r_name=Paris+Montparnasse","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2022&refine.gc_obo_gare_origine_r_name=Paris+Saint-Lazare","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2022&refine.gc_obo_gare_origine_r_name=Paris+Gare+du+Nord","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2022&refine.gc_obo_gare_origine_r_name=Paris+Est","https://ressources.data.sncf.com//api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2022&refine.gc_obo_gare_origine_r_name=Paris+Austerlitz","https://ressources.data.sncf.com/api/records/1.0/search/?dataset=objets-trouves-restitution&q=paris&sort=date&facet=date&facet=gc_obo_date_heure_restitution_c&facet=gc_obo_gare_origine_r_name&facet=gc_obo_nature_c&facet=gc_obo_type_c&facet=gc_obo_nom_recordtype_sc_c&refine.date=2022&refine.gc_obo_gare_origine_r_name=Paris+Bercy"]

def importer_donnees_gares(urls: list[str], conn: sqlite3.Connection) -> None:
    """
    Importe les données de fréquentation des gares à partir d'une liste d'URLs.

    Args:
        urls (List[str]): Liste d'URLs à partir desquelles importer les données de fréquentation.
        conn (sqlite3.Connection): Connexion à la base de données pour effectuer les opérations d'insertion.

    Returns:
        None.
    """
    cursor = conn.cursor()
    rows = 50

    for url in urls:
        start = 0
        total_records = None

        while total_records is None or start < total_records:
            response = requests.get(url, params={"rows": rows, "start": start})

            if response.status_code == 200:
                response_json = response.json()
                records = response_json["records"]
                total_records = response_json["nhits"]

                for record in records:
                    date = parse(record["fields"]["date"])
                    formatted_date = date.strftime("%Y-%m-%d")
                    objet_trouve = (
                        record["fields"]["gc_obo_gare_origine_r_name"],
                        record["fields"]["gc_obo_type_c"],
                        record["fields"]["gc_obo_nature_c"],
                        formatted_date
                    )
                    cursor.execute("""
                        INSERT INTO objet_trouve (nom_gare, type_objet, nature_objet, date)
                        VALUES (?, ?, ?, ?)
                    """, objet_trouve)

                start += rows
                conn.commit()

            else:
                print(response.status_code)
                break
            



coordonnees = {
    "Paris Austerlitz": (48.840609, 2.366563),
    "Paris Bercy": (48.840889, 2.381641),
    "Paris Est": (48.876576, 2.359084),
    "Paris Gare de Lyon": (48.844512, 2.373522),
    "Paris Gare du Nord": (48.880931, 2.355158),
    "Paris Montparnasse": (48.840847, 2.319543),
    "Paris Saint-Lazare": (48.876141, 2.326190)
}


def importer_frequentation_gares(url: str, conn: sqlite3.Connection)-> None:
    """
    Importe la fréquentation des gares depuis l'API située à l'URL donnée et les insère dans la base de données
    passée en paramètre.

    Args:
        url (str): URL de l'API contenant les données de fréquentation des gares.
        conn (sqlite3.Connection): Connexion à la base de données dans laquelle insérer les données.

    Returns:
        None
    """
    response = requests.get(url)
    data = response.json()

    cursor = conn.cursor()

    if "records" in data:
        for index, record in enumerate(data["records"]):
            if index > 0:
                gare_info = {
                    "nom_gare": record["fields"]["nom_gare"],
                    "frequentation_2019": record["fields"]["total_voyageurs_2019"],
                    "frequentation_2020": record["fields"]["total_voyageurs_2020"],
                    "frequentation_2021": record["fields"]["total_voyageurs_2021"],
                }

                if gare_info["nom_gare"] == "Paris Bercy Bourgogne - Pays d'Auvergne":
                    gare_info["nom_gare"] = "Paris Bercy"

                if gare_info["nom_gare"] in coordonnees:
                    gare_info["latitude"], gare_info["longitude"] = coordonnees[gare_info["nom_gare"]]

                frequentation_moyenne = (gare_info["frequentation_2019"] + gare_info["frequentation_2020"] + gare_info["frequentation_2021"]) // 3
                gare_info["frequentation_2022"] = frequentation_moyenne

                cursor.execute("""
                    INSERT OR IGNORE INTO gare (nom_gare, frequentation_2019, frequentation_2020, frequentation_2021, frequentation_2022, latitude, longitude)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (gare_info["nom_gare"], gare_info["frequentation_2019"], gare_info["frequentation_2020"], gare_info["frequentation_2021"], gare_info["frequentation_2022"], gare_info["latitude"], gare_info["longitude"]))

    conn.commit()
    
    

def importer_donnees_meteo(csv_path: str, conn: sqlite3.Connection) -> None:
    """
    Importe les données de température depuis un fichier CSV et les insère dans la base de données passée en paramètre.

    Args:
        csv_path (str): Chemin vers le fichier CSV contenant les données de température.
        conn (sqlite3.Connection): Connexion à la base de données dans laquelle insérer les données.

    Returns:
        None
    """
    cursor = conn.cursor()

    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  

        for row in reader:
            date, temperature = row
            cursor.execute("""
                INSERT INTO meteo (date, temperature)
                VALUES (?, ?)
            """, (date, temperature))

    conn.commit()

url_frequentation = "https://ressources.data.sncf.com/api/records/1.0/search/?dataset=frequentation-gares&q=paris&sort=nom_gare&facet=nom_gare&facet=code_postal&facet=segmentation_drg"
conn = creer_base_donnees()
csv_path = "donneemeteo.csv"  


importer_donnees_gares(urls, conn)
importer_frequentation_gares(url_frequentation, conn)
importer_donnees_meteo(csv_path, conn)
conn.close()

