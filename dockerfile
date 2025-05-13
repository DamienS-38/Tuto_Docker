FROM python:3.9-slim

# Labels pour les métadonnées
LABEL maintainer="Damien"
LABEL version="1.0"
LABEL description="Tuto_docker"

#Création d'un dossier app
WORKDIR /app

# Ajout de sqlite3 CLI
RUN apt update && apt install -y sqlite3

#Copie des sources de travail (requirements.txt) et les .csv dans le conteneur
COPY ./SRC /SRC
COPY ./DATA /DATA
COPY requirements.txt .

#Install de requirement.txt
RUN pip install --no-cache-dir -r requirements.txt

#Lancement du script Python
CMD ["python", "SRC/script.py"]

