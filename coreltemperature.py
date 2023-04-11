import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données d'objets trouvés et de température
df_objet_trouve = pd.read_csv("objet_perdus.csv")
df_temperature = pd.read_csv("donneemeteo.csv")

# Conversion de la colonne "date" au format datetime
df_objet_trouve["date"] = pd.to_datetime(df_objet_trouve["date"])



# Jointure des données d'objets trouvés et de température par date
df_fusion = pd.merge(df_objet_trouve, df_temperature, on="time")

# Affichage du scatterplot avec le nombre d'objets trouvés en fonction de la température
plt.scatter(df_fusion["temperature"], df_fusion["nombre_objet"], alpha=0.5)
plt.xlabel("Température (°C)")
plt.ylabel("Nombre d'objets trouvés")
plt.title("Corrélation entre le nombre d'objets trouvés et la température")

# Calcul du coefficient de corrélation entre le nombre d'objets trouvés et la température
corr = df_fusion["temperature"].corr(df_fusion["nombre"])
print("Coefficient de corrélation :", corr)