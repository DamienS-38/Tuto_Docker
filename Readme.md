# Tuto Docker – Chargement de CSV vers SQLite avec Docker

## Objectif du projet

- Lire un ou plusieurs fichiers **CSV**.
- Générer une base **SQLite** contenant les données.
- Permettre des **requêtes SQL interactives** sur la base via Docker.

---

## Architecture (Docker)

Ce projet utilise **trois services Docker** définis dans `docker-compose.yml` :
| Service              | Description                                                        |
|----------------------|--------------------------------------------------------------------|
| **`sqlite_base`**    | Conteneur contenant la base de données SQLite.                     |
| **`csv-to-sqlite`**  | Transforme et charge les fichiers CSV dans la base de données.     |
| **`analyse`**        | Exécution d'analyses SQL sur la base de données SQLite             |

**Schéma de l'architecture** :  
![Architecture Docker](docker_architecture.png)

---

##  Arborescence du projet
```
├── DATA/
│   ├── magasins.csv              # CSV source des magasins
│   ├── produits.csv              # CSV source des produits
│   └── ventes.csv                # CSV source des ventes
│
├── SRC/
│   └── script.py                 # Script Python de transformation CSV ➜ SQLite
│
├── docker-compose.yml            # Définition des services
├── Dockerfile                    # Image Docker (Python + SQLite)
├── Readme.md                     # Documentation du projet
└── requirements.txt              # Dépendances Python
```
---

##  Fonctionnalités du script Python "script.py"
Ce script assure les étapes suivantes :
- Chargement et nettoyage des fichiers CSV
- Renommage cohérent des colonnes
- Création des tables (si elles n’existent pas) dans `pme.db`
- Insertion des données (avec vérification d’unicité pour éviter les doublons)
- Application des contraintes : clés primaires, clés étrangères, auto-incrément
---


**Schéma de la base de données SQLite "pme.db"** :  
![MCD](MCD_pme.png)

---

##  Comment exécuter l'application avec Docker
1.  **Installer Docker** si ce n’est pas déjà fait :  
    [Docker Desktop](https://www.docker.com/products/docker-desktop)

2.  **Ouvrir un terminal dans le dossier du projet**


3. **Construction des images Docker:**
```bash
docker compose build
```
4.  **Lancer le service de transformation CSV ➜ SQLite:**
Pour charger les fichiers CSV dans la base SQLite, exécute la commande suivante :
```bash
docker compose run --rm csv-to-sqlite
```

5.  **Exécuter l’analyse --> Export d'un fichier CSV 'analyse-resultats.csv' dans la racine du projet:**
Le script analyse.py permet d'extraire des indicateurs clés à partir des données de la base pme.db.
Requêtes effectuées :

    1. Chiffre d'affaires total
    
    2. Acticle le plus vendu

    3. Tableau des ventes par produit

Exécute la commande suivante pour effectuer l’analyse :
```bash
docker compose run --rm analyse
```

6.  **Pour arrêter le conteneur (à la fin de l'utilisation) :**

Une fois l'exécution terminée, tu peux arrêter tous les conteneurs Docker avec la commande suivante :
```bash
docker compose down
```

---


## Requêtes SQL dans SQLite (Pour aller plus loin)
Si tu souhaites effectuer des requêtes SQL directement dans la base de données SQLite, voici quelques étapes :

1.  **Pour construire et démarrer les conteneurs, tape :**
```bash
docker compose up --build -d
```

2.  **Vérifier que les conteneurs sont en fonctionnement :**
```bash
docker ps
```

3.  **Pour accéder à SQLite et intéragir avec la base de données, exécute :**
```bash
docker exec -it sqlite_base bash
sqlite3 /app/DATA/pme.db
```

4.  **Voici quelques commandes utiles une fois dans SQLite :**

```sql
.tables                    -- Voir les tables disponibles
.schema Ventes             -- Voir la structure de la table "Ventes"
SELECT * FROM Ventes;      -- Voir les ventes
```

Afficher le chiffre d'affaire total
```sql
SELECT SUM(V.quantite * P.prix) AS chiffre_affaires_total
FROM Ventes V
JOIN Produits P ON V.id_produit = P.id_produit;
```

5.  **Pour quitter l'interface SQLite, tape :**
```bash
.quit
```
6.  **Pour quitter le conteneur, tape:**
```bash
Exit
```
7.  **Pour arrêter les conteneurs après utilisation, tape :**
```bash
docker compose down
```  


---
## 📬 Contact
Nom : Damien S

[LinkedIn](https://www.linkedin.com/in/damien-schaeffer-45a59821b/)

---