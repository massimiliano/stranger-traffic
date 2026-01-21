# 🚦 Stranger Traffic
> **Why check Google Maps in 3 seconds when you can build a Multimodal AI Agent that takes 20 seconds, burns cloud resources, and spins up a local web server to tell you exactly the same thing?**

**Stranger Traffic** is an experiment in extreme *over-engineering*. It’s a bot that uses [Datapizza AI](https://github.com/datapizza-labs/datapizza-ai) to orchestrate a complex workflow: geocoding locations, rendering interactive maps in a headless browser, taking screenshots, and performing visual analysis via openai.

## 🌟 Features
- **Agentic AI:** Reasoning capabilities to execute a multi-step workflow (Geocode -> Render -> Screenshot -> Analyze).
- **Vision Capabilities:** It doesn't read JSON traffic data (boring!). It literally *looks* at the map like a human.
- **FastAPI Server:** Serves a local HTML frontend in a background thread (because opening a local file was too easy).
- **Security First:** Secure API Key handling via dynamic script injection (no hardcoded keys in the HTML).

## 🛠️ Tech Stack

- **Python 3.9+**
- **Datapizza AI** (Agent Framework)
- **OpenAI** (Brain + Vision)
- **Playwright** (Headless Browser Automation)
- **FastAPI & Uvicorn** (Background Web Server)
- **Google Maps Platform** (Geocoding API + Maps JS API)

## 🚀 Installation

### 1. **Clone the repo:**
   ```bash
   git clone https://github.com/massimiliano/stranger-traffic.git
   cd stranger-traffic
```

### 2. **Install dependencies:**
```bash
  pip install datapizza-ai datapizza-ai-clients-openai playwright fastapi uvicorn requests python-dotenv

```

### 3. **Install Playwright browsers:**
```bash
python -m playwright install chromium

```

## 🔑 Configuration

Create a `.env` file in the project root. You will need an OpenAI Key and a Google Cloud Key.

```ini
# .env file

# OpenAI Key for the Agent logic and Vision analysis
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx

# Google Cloud Key (Must have Geocoding API & Maps JavaScript API enabled)
GOOGLE_MAPS_API_KEY=AIzaSyDxxxxxxxxxxxxxxxxx

```

> **⚠️ Google Cloud Requirements:**
> Ensure your API Key has the following APIs enabled in the Google Cloud Console:
> 1. **Maps JavaScript API** (To render the visual map)
> 2. **Geocoding API** (To convert "Colosseum" into coordinates)
> 
> 

## 🏃‍♂️ Usage

Run the main script:

```bash
python stranger_traffic.py

```

The agent will start, launch the local server, open the browser in the background, take a picture of the traffic, and describe it to you.

### Example Output

```text
👤 USER: How is the traffic at Times Square right now?

📍 [Tool] Geocoding: Times Square, NY
🌍 [Tool] Rendering Map via FastAPI...
🚦 [Tool] Waiting for traffic layer...
📸 [Tool] Screenshot captured.
🧠 [Tool] Visual Analysis with OpenAI...

----------------------------------------
🤖 AGENT:
I'm looking at the map. It's a sea of dark red lines around 7th Ave and Broadway. 
Basically, it's a parking lot. Don't even bother driving there.
----------------------------------------

```

## 📂 Project Structure

* `stranger_traffic.py`: The brain. Defines the Agent, Tools, and logic using Datapizza AI.
* `server_fastapi.py`: A minimal background web server to serve the HTML map.
* `mappa.html`: The HTML template that loads Google Maps (receives the API Key dynamically for security).
* `.env`: Where secrets live (do not commit this!).

---

*Disclaimer: This project is for educational (and entertainment) purposes. Do not use it if you are late for a meeting.*
