import sqlite3 

con = sqlite3.connect("bdd.db")
curseur = con.cursor()

"""
https://sql.sh/
"""

curseur.execute("""
                CREATE TABLE IF NOT EXISTS gare (
                id_gare INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                ville TEXT NOT NULL,
                codepostal INTEGER NOT NULL,
                frequentation_2019 INTEGER NOT NULL,
                frequentation_2020 INTEGER NOT NULL,
                frequentation_2021 INTEGER NOT NULL,
                frequentation_2022 INTEGER NOT NULL
)
""")
con.commit()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS objecttrouve (
                id_object INTEGER PRIMARY KEY AUTOINCREMENT,
                id_gare INTEGER NOT NULL,
                type TEXT NOT NULL,
                nature TEXT NOT NULL,
                FOREIGN KEY (id_gare) REFERENCES gare(id_gare)
                    
)
""")
con.commit()


curseur.execute("""
                CREATE TABLE IF NOT EXISTS temperature (
                id_temperature INTEGER PRIMARY KEY AUTOINCREMENT, 
                id_gare INTEGER NOT NULL,
                date DATETIME,
                temperature INTEGER NOT NULL,
                FOREIGN KEY (id_gare) REFERENCES gare(id_gare)
                

)
""")
con.commit()





con.close()

