FROM python:3.9-slim

# Labels pour les métadonnées
LABEL maintainer=""
LABEL version=""
LABEL description=""

#Création d'un dossier app
#A compléter

# Ajout de sqlite3 CLI
RUN apt update && apt install -y sqlite3

#Copie des sources de travail (requirements.txt) et les .csv dans le conteneur
COPY ./OuJeVeuxLeMettre /DoùCaVient
COPY requirements.txt .

#Install de requirement.txt
RUN pip install --no-cache-dir -r requirements.txt

#Lancement du script Python
#A compléter

