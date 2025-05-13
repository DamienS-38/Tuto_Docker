import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import os

# Connexion à la base
db_path = os.path.join("DATA", "pme.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Création de la table Analyse si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS Analyse (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_analyse TEXT,
    type_analyse TEXT,
    resultat TEXT
)
""")
conn.commit()

#Récupére la date du jour
today = (datetime.now() + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')

# Initialisation d'un tableau pour stocker tous les résultats
all_results = []

# 1. Chiffre d'affaires total
query_ca_total = """
SELECT SUM(V.quantite * P.prix) AS chiffre_affaires_total
FROM Ventes V
JOIN Produits P ON V.id_produit = P.id_produit
"""
df_ca_total = pd.read_sql(query_ca_total, conn)

# Enregistrement dans la table Analyse
cursor.execute("INSERT INTO Analyse (date_analyse, type_analyse, resultat) VALUES (?, ?, ?)",
               (today, "ca_total", df_ca_total.to_json(orient="records")))
conn.commit()


# Ajouter au tableau des résultats à exporter
all_results.append({
    "date_analyse": today,
    "type_analyse": "ca_total",
    "resultat": df_ca_total.to_json(orient="records")
})

print(f"\n Chiffre d'affaires total : {df_ca_total['chiffre_affaires_total'][0]:.2f} €")




# 2. L'article le plus vendu, affiche la quantité
query_ventes_produit = """
SELECT P.nom AS Nom_produit, SUM(quantite) as Quantite_vendue
FROM Ventes V
JOIN Produits P ON V.id_produit = P.id_produit
GROUP BY V.id_produit
ORDER BY Quantite_vendue DESC
LIMIT 1
"""
df_ventes_produit = pd.read_sql(query_ventes_produit, conn)

# Enregistrer dans la table Analyse
cursor.execute("INSERT INTO Analyse (date_analyse, type_analyse, resultat) VALUES (?, ?, ?)",
               (today, "Quantité_article_plus_vendu", df_ventes_produit.to_json(orient="records")))
conn.commit()
print(f"\n L'article {df_ventes_produit['Nom_produit'][0]}, est le plus vendu avec une quantité de : {df_ventes_produit['Quantite_vendue'][0]} ")


# Ajouter au tableau des résultats à exporter
all_results.append({
    "date_analyse": today,
    "type_analyse": "Quantité_article_plus_vendu",
    "resultat": df_ventes_produit.to_json(orient="records")
})


# 3. Tableau des ventes par produit
query = """
SELECT V.id_produit AS Ref_produit, P.nom AS Nom_produit, SUM(quantite) AS Quantite_vendue
FROM Ventes V
JOIN Produits P ON V.id_produit = P.id_produit
GROUP BY V.id_produit
ORDER BY Quantite_vendue DESC
"""

df_ventes_par_produit = pd.read_sql(query, conn)

# Ajouter au tableau des résultats à exporter
all_results.append({
    "date_analyse": today,
    "type_analyse": "ventes_par_produit",
    "resultat": df_ventes_par_produit.to_json(orient="records")
})

print("\n Tableau des ventes par produit :")
print(df_ventes_par_produit.to_string(index=False))
print("\n")

# Enregistrer tous les résultats dans un seul fichier CSV
df_all_results = pd.DataFrame(all_results)
df_all_results.to_csv('analyse_resultats.csv', index=False)  # Enregistrer dans le dossier DATA


# Fermeture
conn.close()
