import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données d'objets trouvés et de température
df_objet_trouve = pd.read_csv("objet_perdus.csv")
df_temperature = pd.read_csv("donneemeteo.csv")

# Conversion de la colonne "date" au format datetime
df_objet_trouve["date"] = pd.to_datetime(df_objet_trouve["date"])

df_temperature["date"] = pd.to_datetime(df_objet_trouve["date"])




# Jointure des données d'objets trouvés et de température par date
#df_fusion = pd.merge(df_objet_trouve, df_temperature, on="date")

# Affichage du scatterplot avec le nombre d'objets trouvés en fonction de la température
plt.scatter(df_objet_trouve["nombre_objet"], df_temperature["temperature"], alpha=0.5)
plt.xlabel("Température (°C)")
plt.ylabel("Nombre d'objets trouvés")
plt.title("Corrélation entre le nombre d'objets trouvés et la température")
plt.show()

# Calcul du coefficient de corrélation entre le nombre d'objets trouvés et la température
#corr = df_temperature["temperature"].corr(df_objet_trouve["nombre_objet"])
#print("Coefficient de corrélation :", corr)