import time
import os
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from datapizza.agents import Agent
from datapizza.tools import tool
from datapizza.clients.openai import OpenAIClient
from datapizza.type import Media, MediaBlock, TextBlock

from server import BackgroundServer

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
MAPS_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

if not OPENAI_KEY or not MAPS_KEY:
    raise ValueError("Errore: Controlla le chiavi nel file .env")

ai_client = OpenAIClient(api_key=OPENAI_KEY, model="gpt-5.2")

server = BackgroundServer(port=8000)
server.start()

# ==========================================
# TOOLS
# ==========================================

@tool
def get_coordinates(location_name: str) -> str:
    """Ottiene le coordinate lat,lng via Google API."""
    print(f"[Tool] Geocoding: {location_name}")
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    try:
        res = requests.get(url, params={"address": location_name, "key": MAPS_KEY})
        data = res.json()
        if data['status'] == 'OK':
            loc = data['results'][0]['geometry']['location']
            return f"{loc['lat']},{loc['lng']}"
        return f"ERRORE API: {data['status']}"
    except Exception as e:
        return f"ERRORE NETWORK: {e}"

@tool
def analyze_traffic_vision(lat_lng: str) -> str:
    """
    1. Genera la mappa locale passando la API Key dinamicamente.
    2. Fa lo screenshot.
    3. Analisi del traffico.
    """
    if "," not in lat_lng: return "Errore coordinate"
    lat, lng = lat_lng.split(",")
    
    local_url = f"http://127.0.0.1:8000/map.html?lat={lat}&lng={lng}&zoom=17&key={MAPS_KEY}"
    
    screenshot_path = "evidence_traffic.png"

    # 1. SCREENSHOT
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1024, "height": 1024})
        
        print("[Tool] Rendering Mappa...")
        page.goto(local_url)
        
        print("[Tool] Attesa caricamento traffico...")
        time.sleep(4)
        
        page.screenshot(path=screenshot_path)
        browser.close()

    # 2. ANALISI VISION CON OPENAI
    try:
        print("[Tool] Analisi in corso...")
        
        image_media = Media(
            media_type="image",
            source_type="path",
            source=screenshot_path,
            extension="png"
        )

        media_block = MediaBlock(media=image_media)
        text_block = TextBlock(content="""
            Analizza questa mappa del traffico di Google Maps.
            - Linee ROSSE/SCURE: Traffico intenso.
            - Linee ARANCIONI: Rallentamenti.
            - Linee VERDI: Scorrevole. 
            - Linee BIANCHE: Sconosciute.
            Rispondi SINTETICAMENTE: C'è traffico? Dove?
        """)

        response = ai_client.invoke(
            input=[text_block, media_block],
            max_tokens=200
        )
        
        return f"REPORT VISIONE: {response.text}"

    except Exception as e:
        return f"ERRORE VISION: {e}"

# ==========================================
# AGENT
# ==========================================

system_prompt = """
Sei 'Stranger Traffic'. 
Il tuo compito è controllare il traffico usando SOLO la vista.
1. Trova le coordinate del luogo.
2. Fatti mandare lo screenshot e analizzalo.
3. Rispondi all'utente con tono sarcastico basandoti su quello che hai VISTO. Rispondi in modo simpatico, lamentandoti un po' se c'è traffico.
Note: non citare mai lo screenshot o il tool usato.
"""

agent = Agent(
    name="StrangerTraffic",
    client=ai_client,
    tools=[get_coordinates, analyze_traffic_vision],
    system_prompt=system_prompt
)

# ESECUZIONE
try:
    query = "Com'è la situazione traffico al Ispettorato Territoriale del Lavoro di Roma?"
    print(f"User: {query}\n")
    
    response = agent.run(query)
    
    print(f"Stranger Traffic:\n{response.text}")
finally:
    server.stop()