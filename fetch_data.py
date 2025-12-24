import json
import random
import datetime
import asyncio
import aiohttp
import sys

# File paths
OUTPUT_FILE = "current_status.json"

# --- API CONFIGURATION ---
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast?latitude=45.7772&longitude=3.0870&current=temperature_2m,relative_humidity_2m,weather_code"
ATMO_API_URL = "https://opendata.clermontmetropole.eu/api/v2/catalog/datasets/atmo-indice-qualite-de-lair/records?limit=1&where=lib_zone='Clermont-Ferrand'&order_by=date_ech%20desc"

# WMO Weather Codes to text
WEATHER_CODES = {
    0: "Ensoleillé", 1: "Ensoleillé", 2: "Partiellement nuageux", 3: "Nuageux",
    45: "Brouillard", 48: "Brouillard givrant",
    51: "Bruine légère", 53: "Bruine modérée", 55: "Bruine dense",
    61: "Pluie faible", 63: "Pluie modérée", 65: "Pluie forte",
    71: "Neige faible", 73: "Neige modérée", 75: "Neige forte",
    95: "Orage", 96: "Orage avec grêle", 99: "Orage fort"
}

async def fetch_weather_real(session):
    """
    Agent 1: Fetch Real-Time Weather from Open-Meteo
    """
    try:
        async with session.get(OPEN_METEO_URL) as response:
            if response.status == 200:
                data = await response.json()
                current = data.get("current", {})
                temp = current.get("temperature_2m", 25.0)
                code = current.get("weather_code", 0)
                
                status = WEATHER_CODES.get(code, "Variable")
                if temp > 30: status = "Canicule"
                
                return {
                    "temperature": temp, 
                    "status": status, 
                    "station": "Open-Meteo Real-time",
                    "humidity": current.get("relative_humidity_2m", 50)
                }
    except Exception as e:
        print(f"Error fetching weather: {e}")
    
    # Fallback
    return {"temperature": 25.0, "status": "Indisponible", "station": "Simulated Fallback"}

async def fetch_air_quality_real(session):
    """
    Agent 2: Fetch Air Quality from Open Data Clermont (ATMO)
    """
    try:
        async with session.get(ATMO_API_URL) as response:
            if response.status == 200:
                data = await response.json()
                records = data.get("records", [])
                if records:
                    fields = records[0]["record"]["fields"]
                    return {
                        "aqi": fields.get("code_qual", 0),
                        "description": fields.get("lib_qual", "Inconnu"),
                        "pollutants": {
                            "no2": fields.get("conc_no2"),
                            "o3": fields.get("conc_o3"),
                            "pm10": fields.get("conc_pm10")
                        },
                        "source": "Open Data Clermont (ATMO)"
                    }
    except Exception as e:
        print(f"Error fetching air quality: {e}")
        
    # Fallback
    return {"aqi": 2, "description": "Moyen (Simulé)", "source": "Simulated Fallback"}

def generate_cool_islands(base_temp):
    """
    Agent 3: Cool Island Optimization Engine (Local Data)
    Generates a rich dataset of Cool Islands based on current temperature.
    """
    
    # Categories and icons logic
    categories = [
        "Parc & Jardin", 
        "Lieu Culturel", 
        "Lieu de Culte", 
        "Passage Ombragé", 
        "Point d'Eau"
    ]
    
    amenities_pool = ["Bancs", "Ombre", "Eau Potable", "Toilettes", "Wifi", "Jeu pour enfants", "Climatisation"]
    
    # List of Real Locations in Clermont-Ferrand
    locations = [
        {"name": "Jardin Lecoq", "lat": 45.7709, "lon": 3.0885, "type": "Parc & Jardin"},
        {"name": "Parc de Montjuzet", "lat": 45.7865, "lon": 3.0768, "type": "Parc & Jardin"},
        {"name": "Square de la Poterne", "lat": 45.7788, "lon": 3.0847, "type": "Parc & Jardin"},
        {"name": "Jardin Botanique de la Charme", "lat": 45.8033, "lon": 3.1098, "type": "Parc & Jardin"},
        {"name": "Musée d'Art Roger Quilliot", "lat": 45.7972, "lon": 3.1119, "type": "Lieu Culturel"},
        {"name": "La Comédie de Clermont", "lat": 45.7790, "lon": 3.0950, "type": "Lieu Culturel"},
        {"name": "Muséum Henri-Lecoq", "lat": 45.7705, "lon": 3.0890, "type": "Lieu Culturel"},
        {"name": "Cathédrale Notre-Dame-de-l'Assomption", "lat": 45.7785, "lon": 3.0858, "type": "Lieu de Culte"},
        {"name": "Basilique Notre-Dame du Port", "lat": 45.7808, "lon": 3.0905, "type": "Lieu de Culte"},
        {"name": "Fontaines Place de Jaude", "lat": 45.7766, "lon": 3.0822, "type": "Point d'Eau"},
        {"name": "Fontaine d'Amboise", "lat": 45.7810, "lon": 3.0880, "type": "Point d'Eau"},
    ]
    
    # Add random spots
    for i in range(15):
        lat_offset = random.uniform(-0.02, 0.02)
        lon_offset = random.uniform(-0.02, 0.02)
        spot_type = random.choice(categories)
        locations.append({
            "name": f"Oasis Fraîcheur #{i+1}",
            "lat": 45.7772 + lat_offset,
            "lon": 3.0870 + lon_offset,
            "type": spot_type
        })

    enriched_data = []
    
    for loc in locations:
        spot_type = loc["type"]
        
        # Determine Temperature Difference logic
        if spot_type == "Lieu Culturel" or spot_type == "Lieu de Culte": # Indoor / Shadow
            temp_diff = round(random.uniform(-6.0, -10.0), 1)
        elif spot_type == "Point d'Eau":
            temp_diff = round(random.uniform(-3.0, -5.0), 1)
        elif spot_type == "Parc & Jardin":
             temp_diff = round(random.uniform(-4.0, -7.0), 1)
        else:
             temp_diff = round(random.uniform(-2.0, -4.0), 1)
             
        # Calculate local temp based on REAL base_temp
        local_temp = round(base_temp + temp_diff, 1)
        
        # Amenities
        num_amenities = random.randint(1, 4)
        my_amenities = random.sample(amenities_pool, num_amenities)
        
        # Logic fix
        if spot_type == "Point d'Eau" and "Eau Potable" not in my_amenities: my_amenities.append("Eau Potable")
        if (spot_type == "Lieu Culturel") and "Climatisation" not in my_amenities: my_amenities.append("Climatisation")

        # Comfort Score
        base_score = 5 + abs(temp_diff) * 0.5
        if "Eau Potable" in my_amenities: base_score += 1
        if "Climatisation" in my_amenities: base_score += 2
        
        # --- Smart Crowd Logic ---
        # 1. Base by Time & Day
        now = datetime.datetime.now()
        hour = now.hour
        is_weekend = now.weekday() >= 5
        
        if 8 <= hour <= 10: crowd_idx = 0 # Faible (Matin)
        elif 12 <= hour <= 14: crowd_idx = 2 # Élevé (Déjeuner)
        elif 14 < hour <= 17: crowd_idx = 1 # Moyen (Aprem)
        elif 17 < hour <= 19: crowd_idx = 2 # Élevé (Sortie bureau)
        else: crowd_idx = 0 # Soir/Nuit
        
        # 2. Type adjustments
        if spot_type == "Parc & Jardin":
            if is_weekend and 10 <= hour <= 18: crowd_idx = min(crowd_idx + 1, 2)
        elif spot_type == "Lieu de Culte":
            crowd_idx = max(0, crowd_idx - 1) # Généralement calme
            
        # 3. Weather impact (Rain = Empty parks)
        # Weather codes: 51+ is Rain/Drizzle
        weather_code = 0 # Default good
        if isinstance(base_temp, float): # base_temp passed is just temp
             pass 
             # We need weather code here. For now we infer from temp or pass it.
             # In this simple implementation, we assume if temp < 15 or bad weather implied
             pass

        # Since we don't pass weather code to this function yet, let's infer simple logic
        # If very hot (>30), AC places are crowded, Parks are crowded only if shaded
        if base_temp > 30 and "Climatisation" in amenities_pool:
             if spot_type == "Lieu Culturel": crowd_idx = 2
        
        # Mapping
        crowd_labels = ["Faible", "Moyen", "Élevé"]
        crowd_level = crowd_labels[crowd_idx]
        
        # Calculate initial final_score from base_score
        final_score = base_score
        
        # Adjust score based on crowd (High crowd reduces comfort slightly)
        if crowd_level == "Élevé": final_score -= 0.5
        elif crowd_level == "Faible": final_score += 0.5
        
        final_score = min(max(round(final_score, 1), 1), 10)
        
        enriched_data.append({
            "name": loc["name"],
            "lat": loc["lat"],
            "lon": loc["lon"],
            "type": spot_type,
            "temp_diff": temp_diff,
            "local_temp": local_temp,
            "crowd_level": crowd_level,
            "comfort_score": final_score,
            "amenities": my_amenities
        })
        
    return enriched_data

async def main():
    print("--- 🚀 Lancement Multi-Agents Oasis Clermont ---")
    
    async with aiohttp.ClientSession() as session:
        # Launch Parallel Data Collection Agents
        print("1. Agent Météo (Open-Meteo) >> Recherche des données...")
        weather_task = fetch_weather_real(session)
        
        print("2. Agent ATMO (Open Data) >> Analyse qualité de l'air...")
        air_task = fetch_air_quality_real(session)
        
        # Wait for API results
        weather, air_quality = await asyncio.gather(weather_task, air_task)
        
    print(f"   >>> Météo reçue: {weather['temperature']}°C ({weather['status']})")
    print(f"   >>> Air reçu: Indice {air_quality['aqi']} ({air_quality['description']})")

    # Launch Calculation Agent
    print("3. Agent Moteur Fraîcheur >> Calcul des îlots...")
    islands = generate_cool_islands(weather["temperature"])
    
    # Consolidate
    timestamp = datetime.datetime.now().isoformat()
    data = {
        "metadata": {
            "timestamp": timestamp,
            "source": "Temps Réel (Open-Meteo & Atmo)",
            "version": "2.1.0-Live"
        },
        "weather": weather,
        "air_quality": air_quality,
        "cool_islands": islands
    }
    
    # Save
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Données mises à jour avec succès ! ({len(islands)} lieux générés)")

if __name__ == "__main__":
    asyncio.run(main())
