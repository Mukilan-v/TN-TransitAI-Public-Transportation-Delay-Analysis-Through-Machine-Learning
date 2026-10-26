# 🚌 Tamil Nadu Smart Transport AI (TransitAI)

A futuristic, high-performance Intelligent Transit & Fleet Optimization Platform tailored specifically for the Tamil Nadu State Transport Corporation (TNSTC) highway road network and commercial fleet operations across all 38 Tamil Nadu districts.

---

## 🌟 Key Features

### 1. 🗺️ AI Highway Route Graph & Distance Matrix (All 38 Districts)
- Complete highway road graph linking all 38 Tamil Nadu districts (from Chennai and Kanchipuram to Madurai, Coimbatore, and Kanyakumari).
- Dijkstra-based shortest highway pathfinder with dynamic transit hubs, milestones, and travel duration estimations.

### 2. 🧠 Machine Learning Arrival Delay Predictor
- Predicts highway arrival delays in minutes with high accuracy based on:
  - Rush hour traffic surges (Peak Morning / Evening windows).
  - Weekend holiday congestion patterns.
  - Weather penalties (Rain, Fog, Storm).
  - High-altitude ghat road transit (Nilgiris / Ooty & Kodaikanal).

### 3. 🛰️ GPS Live Radar & Fleet Telemetry Cockpit
- Real-time vehicle monitoring simulation with interactive gauges:
  - Speedometer (0–120 km/h) & Odometer tracking.
  - Real-time engine health and coolant telemetry.
  - Highway milestone progression along NH 45 (GST Road), NH 44, and NH 544.
  - Dynamic micro-climate road surface sensor.

### 4. 🌦️ Automated Satellite Weather Monitoring
- Live satellite weather integration with dynamic road condition analysis (Dry Asphalt, Wet Road, Foggy Ghat Hazard).

### 5. 🎨 6-Theme Multi-Color Palette Switcher
- Instant visual theme switching with persistent localStorage:
  1. **☀️ Spendorio Sunset Bright**: Ultra-crisp modern daylight glass styling.
  2. **🌌 Cosmic Cyber Violet**: Neon violet glass with glowing gradients.
  3. **🌿 Nilgiris Emerald Eco**: Forest emerald & alpine teal eco-transit.
  4. **🌊 Marina Bay Ocean**: Deep maritime azure inspired by the Bay of Bengal.
  5. **👑 Royal Amber Highway**: Luxury golden night expressway coach aesthetic.
  6. **🔮 Cyberpunk Synthwave**: Pulsing synthwave neon magenta & laser cyan.

### 6. 🕒 Live Digital Transit Clock
- Live synchronized 24-hour / 12-hour clock with active green pulsing beacon and Indian Standard Time (IST) formatting.

### 7. 🚌 Animated Highway Track & Moving Express Bus
- Cruising SETC Super Express coach with animated road markings, spinning alloy wheels, amber LED route destination board (`CHENNAI ➔ MADURAI`), twin headlight beams, and interactive dual-tone air horn audio blast via Web Audio API.

### 8. 🔒 Secure Authentication & Background Account Engine
- Strict username and password verification (rejects incorrect credentials).
- Live real-time username & email availability verification on signup.
- 2-Step verified password recovery via registered email (no public exposure of credentials).
- Completely client-side and standalone: runs 100% in your browser without requiring server installations.

---

## 🚀 Quick Start (Zero Setup Required)

1. **Option A: Direct Browser Launch (Recommended)**
   - Double-click `index.html` to open it in any modern browser (Chrome, Edge, Firefox, Safari).
   - Everything runs instantly client-side!

2. **Option B: Run with Python HTTP Server**
   ```bash
   python -m http.server 8000
   ```
   Open `http://localhost:8000` in your web browser.

3. **Option C: Flask Backend (Optional)**
   ```bash
   cd tn_transport_ai
   pip install flask pandas scikit-learn
   python app.py
   ```

---

## 📁 Repository Structure

```
├── index.html                   # Complete Standalone Single-File Web Application
├── README.md                    # Project Documentation
├── .gitignore                   # Git Ignore Configuration
├── run.bat                      # One-click Windows starter
├── run.py                       # Python runner script
└── tn_transport_ai/             # Flask Backend & Machine Learning Engine
    ├── app.py                   # Flask REST API Server
    ├── fleet_engine.py          # Real-time Fleet Simulation & Dispatch Engine
    ├── route_engine.py          # Highway Routing & Dijkstra Algorithm
    ├── weather_engine.py        # Weather Sourcing & Road Condition Logic
    ├── traffic_engine.py        # Rush Hour & Congestion Multipliers
    ├── train_model.py           # ML Model Training Pipeline
    ├── data/                    # Tamil Nadu District Coordinates & CSV Datasets
    ├── models/                  # Trained Machine Learning Model (.pkl)
    ├── templates/               # Jinja2 HTML Templates
    └── static/                  # CSS, Icons, PWA Manifest, and Images
```

---

## 👥 Authors & Credits
- **Developer**: Mukilan V
- **Framework**: Tamil Nadu Smart Transport AI • TransitAI System
- **License**: MIT
