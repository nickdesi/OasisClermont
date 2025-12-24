import streamlit as st
import json
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, HeatMap
import os
import subprocess
import datetime
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Oasis Clermont V2",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_FILE = "current_status.json"

# --- CSS PERSONNALISÉ & ASSETS ---
def local_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        /* ========== BASE STYLES ========== */
        html, body, [class*="css"], .stMarkdown, .stText, p, span, div {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
            min-height: 100vh;
        }
        
        /* ========== MODERN HEADINGS ========== */
        h1, h2, h3, .stSubheader, [data-testid="stSubheader"] {
            font-family: 'Inter', sans-serif !important;
            font-weight: 800 !important;
            letter-spacing: -0.02em !important;
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            text-shadow: none !important;
        }
        
        h1, .stTitle {
            font-size: 2.5rem !important;
            margin-bottom: 1rem !important;
        }
        
        h2, .stSubheader, [data-testid="stSubheader"] {
            font-size: 1.5rem !important;
            margin-bottom: 0.75rem !important;
        }
        
        h3 {
            font-size: 1.25rem !important;
        }
        
        /* Fix for Streamlit subheader text */
        [data-testid="stSubheader"] p,
        .stSubheader p {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            background-clip: text !important;
            font-weight: 700 !important;
            font-size: 1.4rem !important;
        }

        /* ========== GLASSMORPHISM CARDS ========== */
        .glass-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            padding: 24px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .glass-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
            border-color: rgba(255, 255, 255, 0.25);
        }

        /* ========== PREMIUM ALERT HEADER ========== */
        .alert-header {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.9) 0%, rgba(249, 115, 22, 0.9) 100%);
            backdrop-filter: blur(10px);
            padding: 20px 28px;
            border-radius: 16px;
            color: white;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3);
            animation: pulse-glow 3s ease-in-out infinite;
        }
        
        @keyframes pulse-glow {
            0%, 100% { box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3); }
            50% { box-shadow: 0 8px 48px rgba(239, 68, 68, 0.5); }
        }

        /* ========== TOP SPOTS CARDS ========== */
        .top-spot-card {
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(12px);
            padding: 16px 20px;
            border-radius: 14px;
            margin-bottom: 12px;
            border-left: 4px solid;
            border-image: linear-gradient(180deg, #38bdf8, #818cf8) 1;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
            transition: all 0.25s ease;
        }
        
        .top-spot-card:hover {
            background: rgba(255, 255, 255, 0.1);
            transform: translateX(6px);
        }
        
        .top-spot-card .spot-name {
            font-weight: 700;
            color: #f1f5f9;
            font-size: 1rem;
            margin-bottom: 4px;
        }
        
        .top-spot-card .spot-type {
            font-size: 0.85rem;
            color: #94a3b8;
        }
        
        .top-spot-card .spot-stats {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 10px;
        }
        
        .temp-badge {
            color: #38bdf8;
            font-weight: 700;
            font-size: 1.1rem;
        }
        
        .comfort-badge {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(129, 140, 248, 0.2));
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            color: #e2e8f0;
            font-weight: 600;
            border: 1px solid rgba(56, 189, 248, 0.3);
        }

        /* ========== SIDEBAR STYLING ========== */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {
            color: #e2e8f0 !important;
        }
        
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #f8fafc !important;
            -webkit-text-fill-color: #f8fafc !important;
            background: none !important;
        }
        
        /* Sidebar title */
        [data-testid="stSidebar"] .stTitle {
            font-size: 1.8rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* ========== BUTTONS ========== */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 16px rgba(59, 130, 246, 0.4) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.5) !important;
        }

        /* ========== METRICS ========== */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.06);
            backdrop-filter: blur(12px);
            padding: 16px;
            border-radius: 14px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            font-size: 0.75rem !important;
            letter-spacing: 0.05em;
        }
        
        [data-testid="stMetricValue"] {
            color: #f1f5f9 !important;
            font-weight: 800 !important;
            font-size: 1.8rem !important;
        }

        /* ========== MULTISELECT & INPUTS ========== */
        .stMultiSelect, .stSlider {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 8px;
        }
        
        .stMultiSelect [data-baseweb="tag"] {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
        }

        /* ========== INFO BOX ========== */
        .stAlert {
            background: rgba(56, 189, 248, 0.1) !important;
            border: 1px solid rgba(56, 189, 248, 0.3) !important;
            border-radius: 12px !important;
            color: #bae6fd !important;
        }

        /* ========== DIVIDERS ========== */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            margin: 20px 0;
        }

        /* ========== SECTION TITLES ========== */
        .section-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #f1f5f9;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* ========== MAP CONTAINER ========== */
        iframe {
            border-radius: 16px !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        }
        
        /* ========== CHECKBOX ========== */
        .stCheckbox label span {
            color: #e2e8f0 !important;
        }
        
        /* ========== GENERAL TEXT ========== */
        p, span, div {
            color: #cbd5e1;
        }
        
        /* ========== CAPTION ========== */
        .stCaption, [data-testid="stCaption"] {
            color: #64748b !important;
        }
    </style>
    """, unsafe_allow_html=True)

def load_data():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def refresh_data():
    with st.spinner('📡 Récupération des données satellites & capteurs...'):
        try:
            result = subprocess.run(["python3", "fetch_data.py"], capture_output=True, text=True)
            if result.returncode == 0:
                st.toast("Données mises à jour.", icon="🔄")
            else:
                st.error(f"Erreur: {result.stderr}")
        except Exception as e:
            st.error(f"Erreur script: {e}")

local_css()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏙️ Oasis Clermont Pro")
    st.caption("Outil d'Aide à la Décision - Canicule")
    st.markdown("---")
    
    # 1. Controls
    if st.button("🔄 Actualiser Temps Réel", use_container_width=True):
        refresh_data()
        st.rerun()

    st.markdown("### 🎛️ Filtres")
    
    # Load data for filters
    data = load_data()
    if data:
        all_spots = data.get("cool_islands", [])
        categories = sorted(list(set([s["type"] for s in all_spots])))
        
        selected_types = st.multiselect("Type de Lieu", categories, default=categories)
        min_comfort = st.slider("Score Confort Min.", 1, 10, 5)
        show_heatmap = st.checkbox("Afficher Carte de Chaleur", value=True)
    else:
        selected_types = []
        min_comfort = 0
        show_heatmap = False

    st.markdown("---")
    st.info("Version 2.1.0 (Live)\nDonnées Temps Réel Connectées")

# --- MAIN CONTENT ---

if not data:
    st.error("Données indisponibles. Lancez l'actualisation.")
    st.stop()

# Header Metrics
weather = data.get("weather", {})
air = data.get("air_quality", {})
temp = weather.get("temperature", 0)
aqi = air.get("aqi", 0)
metadata = data.get("metadata", {})
update_time = metadata.get("timestamp", "")[:16].replace("T", " à ")

alert_colors = {"Canicule": "#ef4444", "Ensoleillé": "#f59e0b", "Nuageux": "#64748b", "Variable": "#8b5cf6"}
bg_color = alert_colors.get(weather.get("status"), "#3b82f6")

st.markdown(f"""
<div class="alert-header" style="background-color: {bg_color}; position: relative; overflow: hidden;">
    <span style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 4px; font-size: 0.7em; font-weight: 800; letter-spacing: 1px; border: 1px solid rgba(255,255,255,0.3);">LIVE</span>
    <span>🌡️ Météo : {weather.get("status")} ({temp}°C)</span>
    <span>•</span>
    <span>💨 Qualité Air : {air.get("description")} (Indice {aqi})</span>
    <span style="font-size: 0.7em; opacity: 0.8; margin-left: 10px;">(MàJ: {update_time})</span>
</div>
""", unsafe_allow_html=True)

# Filter Data
filtered_spots = [
    s for s in all_spots 
    if s["type"] in selected_types 
    and s.get("comfort_score", 0) >= min_comfort
]

# Layout: Map (Left 70%) | Stats & List (Right 30%)
col_map, col_details = st.columns([0.7, 0.3])

with col_map:
    st.subheader(f"🗺️ Carte Interactive ({len(filtered_spots)} lieux trouvés)")
    
    # Heatmap Legend
    if show_heatmap:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.1); display: flex; align-items: center; justify-content: space-between;">
            <span style="font-size: 0.8em; font-weight: 600; color: #cbd5e1;">Intensité Fraîcheur :</span>
            <div style="flex-grow: 1; height: 8px; background: linear-gradient(90deg, lime, yellow, red); margin: 0 15px; border-radius: 4px;"></div>
            <div style="display: flex; justify-content: space-between; gap: 10px; font-size: 0.7em; color: #94a3b8;">
                <span>Modérée</span>
                <span>Élevée</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    m = folium.Map(location=[45.7772, 3.0870], zoom_start=14, tiles="OpenStreetMap")
    
    # Heatmap Layer
    if show_heatmap:
        heat_data = [[s["lat"], s["lon"], s["comfort_score"]] for s in filtered_spots]
        HeatMap(heat_data, radius=18, blur=12, max_zoom=1).add_to(m)

    # Marker Cluster
    marker_cluster = MarkerCluster().add_to(m)
    
    for spot in filtered_spots:
        # Icon Logic
        icon_map = {
            "Parc & Jardin": "tree",
            "Lieu Culturel": "book",
            "Lieu de Culte": "university", # FontAwesome name check needed, using 'university' acts as landmark
            "Passage Ombragé": "road",
            "Point d'Eau": "tint"
        }
        icon_name = icon_map.get(spot["type"], "info-sign")
        
        # Color Logic
        comfort = spot.get("comfort_score", 5)
        color = "green" if comfort >= 8 else "orange" if comfort >= 5 else "red"
        
        # Popup Content
        amenities_html = "".join([f"<span style='background:linear-gradient(135deg, #3b82f6, #8b5cf6);color:white;padding:3px 8px;border-radius:6px;font-size:0.75em;margin-right:4px;font-weight:500;'>{a}</span>" for a in spot.get("amenities", [])])
        
        html = f"""
        <div style="font-family:'Inter',sans-serif; width:280px; padding:4px;">
            <h4 style="margin:0 0 4px 0;background:linear-gradient(135deg,#38bdf8,#818cf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:700;font-size:1.1em;">{spot['name']}</h4>
            <p style="font-size:0.85em;color:#64748b;margin:0 0 10px 0;">{spot['type']}</p>
            <hr style="margin:8px 0;border:none;border-top:1px solid #e2e8f0;">
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;align-items:center;">
                <span style="font-weight:600;color:#1e293b;">Score Confort</span>
                <span style="background:linear-gradient(135deg,#38bdf8,#818cf8);color:white;padding:4px 10px;border-radius:8px;font-weight:700;">{spot['comfort_score']}/10</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="color:#64748b;">🌡️ Température locale</span>
                <span style="font-weight:600;color:#0ea5e9;">{spot.get('local_temp')}°C</span>
            </div>
            <div style="display:flex;justify-content:space-between;margin-bottom:10px;">
                <span style="color:#64748b;">👥 Affluence</span>
                <span style="font-weight:500;color:#1e293b;">{spot.get('crowd_level')}</span>
            </div>
            <div style="margin-bottom:10px;display:flex;flex-wrap:wrap;gap:4px;">{amenities_html}</div>
            <div style="background:#f0fdf4;padding:8px 12px;border-radius:8px;border-left:3px solid #22c55e;">
                <span style="font-size:0.85em;color:#166534;">❄️ <b>{spot.get('temp_diff')}°C</b> vs extérieur</span>
            </div>
        </div>
        """
        
        folium.Marker(
            location=[spot["lat"], spot["lon"]],
            popup=folium.Popup(html, max_width=260),
            tooltip=f"{spot['name']} ({spot['comfort_score']}/10)",
            icon=folium.Icon(color=color, icon=icon_name, prefix="fa")
        ).add_to(marker_cluster)

    st_folium(m, width=None, height=600)

with col_details:
    st.subheader("📊 Top Fraîcheur")
    
    # Sort by Temp Diff (Lowest first, meaning -10 is better than -2)
    top_spots = sorted(filtered_spots, key=lambda x: x.get("temp_diff", 0))[:5]
    
    for i, s in enumerate(top_spots):
        # Medal emoji for top 3
        medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"{i+1}."
        st.markdown(f"""
        <div class="top-spot-card">
            <div class="spot-name">{medal} {s['name']}</div>
            <div class="spot-type">{s['type']}</div>
            <div class="spot-stats">
                <span class="temp-badge">❄️ {s['temp_diff']}°C</span>
                <span class="comfort-badge">⭐ {s['comfort_score']}/10</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📈 Statistiques")
    avg_comfort = round(pd.DataFrame(filtered_spots)["comfort_score"].mean(), 1) if filtered_spots else 0
    
    col_a, col_b = st.columns(2)
    col_a.metric("Score Moyen", f"{avg_comfort}/10")
    col_b.metric("Lieux Ouverts", len(filtered_spots))
