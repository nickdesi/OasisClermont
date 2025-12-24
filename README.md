# 🏝️ Oasis Clermont - Dashboard Îlots de Fraîcheur

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://oasisclermont.streamlit.app/)

Application de visualisation des îlots de fraîcheur à Clermont-Ferrand, connectée en temps réel aux données météorologiques et de qualité de l'air.

![Dashboard Live](https://github.com/user-attachments/assets/placeholder)

## 🚀 Fonctionnalités

- **Météo Temps Réel** : Température et condition actuelle via Open-Meteo API.
- **Qualité de l'Air** : Indice ATMO en direct via Open Data Clermont.
- **Carte Interactive** : Visualisation des parcs, lieux de culte, musées et passages couverts.
- **Heatmap** : Carte de chaleur identifiant les zones les plus fraîches.
- **Smart Crowd** : Estimation intelligente de l'affluence en fonction de l'heure et de la météo.
- **Top Fraîcheur** : Classement des meilleurs spots pour se rafraîchir.

## 🛠️ Stack Technique

- **Python 3.9+**
- **Streamlit** (Interface Web)
- **Folium** (Cartographie)
- **AsyncIO & Aiohttp** (Agents de données asynchrones)
- **Pandas** (Traitement de données)

## 📦 Installation

1. Cloner le dépôt :

    ```bash
    git clone https://github.com/votre-username/OasisClermont.git
    cd OasisClermont
    ```

2. Créer un environnement virtuel :

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Installer les dépendances :

    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Lancement

```bash
streamlit run app.py
```

## 🌍 Données

- **Météo** : [Open-Meteo](https://open-meteo.com/)
- **Air** : [ATMO Auvergne-Rhône-Alpes](https://www.atmo-auvergnerhonealpes.fr/)

---
v2.1.0 (Live)
