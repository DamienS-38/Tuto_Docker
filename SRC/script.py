# Imports
import os
import sqlite3
import pandas as pd
from io import StringIO

# Chargement des CSV
df_produits = pd.read_csv('DATA/produits.csv', delimiter=',')
df_magasins = pd.read_csv('DATA/magasins.csv', delimiter=',')
df_ventes = pd.read_csv('DATA/ventes.csv', delimiter=',')

# Connexion à la base SQLite
db_path = os.path.join("DATA", "pme.db")

# Supprimer l'ancienne base de données si elle existe
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"Ancienne base supprimée : {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Activer les clés étrangères
cursor.execute('PRAGMA foreign_keys = ON;')

# Création des tables si elles n'existent pas
cursor.execute('''
CREATE TABLE IF NOT EXISTS Produits (
    id_produit TEXT PRIMARY KEY,
    nom TEXT,
    prix REAL,
    stock INT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Magasins (
    id_magasin TEXT PRIMARY KEY,
    ville TEXT,
    Nb_salarie INT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Ventes (
    id_vente INTEGER PRIMARY KEY AUTOINCREMENT,
    id_produit TEXT,
    id_magasin TEXT,
    date_vente TEXT,
    quantite INTEGER,
    FOREIGN KEY(id_produit) REFERENCES Produits(id_produit),
    FOREIGN KEY(id_magasin) REFERENCES Magasins(id_magasin)
    --,    UNIQUE(id_produit, id_magasin, date_vente)
)
''')

# Éviter les doublons sur Produits (Enregistrement des id_produit dans une liste)
id_produit_existant = pd.read_sql("SELECT id_produit FROM Produits", conn)['id_produit'].tolist()
df_produits = df_produits[~df_produits['id_produit'].isin(id_produit_existant)]

# Éviter les doublons sur Magasins
id_magasin_existant = pd.read_sql("SELECT id_magasin FROM Magasins", conn)['id_magasin'].tolist()
df_magasins = df_magasins[~df_magasins['id_magasin'].isin(id_magasin_existant)]

# Éviter les doublons sur Ventes (via clé composite)
#changer les types avant concaténation
df_ventes['vente_key'] = (
    df_ventes['id_produit'].astype(str) + "_" +
    df_ventes['id_magasin'].astype(str) + "_" +
    df_ventes['date_vente'].astype(str)
)

ventes_existantes = pd.read_sql("SELECT id_produit, id_magasin, date_vente FROM Ventes", conn)

ventes_existantes['vente_key'] = ventes_existantes['id_produit'] + "_" + ventes_existantes['id_magasin'] + "_" + ventes_existantes['date_vente']
df_ventes = df_ventes[~df_ventes['vente_key'].isin(ventes_existantes['vente_key'])]
df_ventes = df_ventes.drop(columns=['vente_key'])



# Insertion des données
df_produits.to_sql('Produits', con=conn, if_exists='append', index=False)
print("Insertion des produits terminée.")

df_magasins.to_sql('Magasins', conn, if_exists='append', index=False)
print("Insertion des magasins terminée.")

df_ventes.to_sql('Ventes', conn, if_exists='append', index=False)
print("Insertion des ventes terminée.")

# Finalisation
conn.commit()
conn.close()
