# 🏝️ Oasis Clermont - Dashboard Îlots de Fraîcheur

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://oasisclermont.streamlit.app/)

Application de visualisation des îlots de fraîcheur à Clermont-Ferrand, connectée en temps réel aux données météorologiques et de qualité de l'air.

![Dashboard Live](assets/dashboard_preview.png)

## 🚀 Fonctionnalités

- **Météo Temps Réel** : Température et condition actuelle via Open-Meteo API.
- **Qualité de l'Air** : Indice ATMO en direct via Open Data Clermont.
- **Carte Interactive** : Visualisation des parcs, lieux de culte, musées et passages couverts.
- **Heatmap** : Carte de chaleur identifiant les zones les plus fraîches avec légende.
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
    git clone https://github.com/nickdesi/OasisClermont.git
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

## 🌍 Sources de Données Détaillées

L'application connecte plusieurs sources en temps réel pour garantir la fraîcheur des informations :

### 1. Météo (Open-Meteo API)

- **Endpoint** : `https://api.open-meteo.com/v1/forecast`
- **Données** : Température actuelle (°C) et Codes météo (WMO).
- **Méthode** : Asynchrone (Non-bloquant).

### 2. Qualité de l'Air (Open Data Clermont / ATMO)

- **Endpoint** : `https://opendata.clermontmetropole.eu/api/records/1.0/search/`
- **Dataset** : `work_temp_ind_atmo_latest` (Flux ATMO Auvergne-Rhône-Alpes).
- **Données** : Indice global (Qualificatif) + Sous-indices (NO2, O3, PM10).

### 3. Affluence (Smart Crowd Logic)

Algorithme d'estimation réaliste interne :

- **Heure** : Pics d'affluence simulés (Midi, 17h-19h).
- **Météo** : Si T° > 30°C, forte affluence sur les musées (climatisés).

---
v2.1.0 (Live)
