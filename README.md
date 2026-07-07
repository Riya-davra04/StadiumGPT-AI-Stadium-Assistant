# 🏟️ StadiumGPT - AI Smart Stadium Assistant

> **Tagline:** Making every FIFA World Cup fan's journey smarter, safer, and stress-free with Generative AI.

---

## 🚨 Detailed Problem Statement & User Persona Alignment

Attending mega-sports events like the **FIFA World Cup** inside massive stadium complexes introduces severe operational bottlenecks and friction points for fans, emergency responders, and venue operations management. Current stadium infrastructures operate in siloed data frameworks, leading to critical real-world challenges mapped below:

### 👤 Target User Personas & Pain Points
1. **The International Fan (e.g., Carlos from Brazil):** Faces severe language barriers, struggles with complex multi-tiered seating layouts, and loses 30+ minutes waiting in unmanaged food/restroom queues, missing key match moments.
2. **The Mobility-Impaired Attendee (e.g., Sarah in a wheelchair):** Encounters unexpected physical barriers (stairs, blocked ramps) due to static mapping tools that fail to provide real-time accessible route variations.
3. **The Stadium Operations Manager (e.g., Ahmed):** Lacks predictive foresight regarding crowd density spikes at gates during pre-match entries and post-match outbound transport surges, increasing crush and stampede risks.
4. **The Emergency Medic (e.g., Officer John):** Struggles to pinpoint exact micro-coordinates of a spectator facing a medical crisis inside a densely crowded zone of 80,000+ people, delaying life-saving care.

### 📉 Core Operational Friction Matrix
* **Navigation Chaos & Friction:** Massive structural designs cause disorientation. Static signage cannot dynamic-route fans away from congested turnstiles.
* **Predictive Deficiencies:** Zero live forecasting at concession stands causes parallel spikes in wait-times, threatening security safety bounds.
* **Communication Breakdown:** Traditional systems fail to translate ad-hoc critical safety instructions into 6+ global languages instantly.
* **Siloed Emergency Dispatch:** Current workflows rely on verbal relay chains rather than automated AI-triggered micro-location telemetry.
* **Post-Match Network Paralysis:** Tens of thousands exit simultaneously, causing gridlocks at metro stations and parking bays due to uncoordinated, un-load-balanced routing.

### 📊 Quantifiable Success Metrics (KPIs)
To ensure absolute problem alignment, StadiumGPT evaluates its structural efficiency against the following core benchmarks:
* **Crowd Reduction:** Target a minimum **35% reduction** in pedestrian checkpoint congestion.
* **Time Optimizations:** Save an average of **20-25 minutes per fan** during peak food stall operating hours.
* **Emergency Response Telemetry:** Achieve sub **90-second activation** for critical medical team dispatches via AI routing.
* **Inclusivity Benchmark:** Enforce **100% voice and sensory path accessibility** for international and disabled cohorts.


---

## 💡 The Solution: StadiumGPT

**StadiumGPT** breaks down these operational silos by acting as an end-to-end, multi-lingual, GenAI-powered orchestrator and real-time digital twin for stadium attendees and staff alike.

Use code with caution.┌──────────────────────────────┐│   STADIUMGPT AI ORCHESTRATOR │└──────────────┬───────────────┘┌───────────────────────┼───────────────────────┐▼                       ▼                       ▼┌─────────────────┐    ┌──────────────────┐    ┌──────────────────┐│  For Attendees  │    │  For Operations  │    │ For Security/Med │├─────────────────┤    ├──────────────────┤    ├──────────────────┤│ • Voice Wayfind │    │ • Crowd Heatmaps │    │ • Micro-Location ││ • Queue Forecast│    │ • Digital Twin   │    │   Emergency Alert││ • 6+ Languages  │    │   Simulations    │    │ • Smart Dispatch │└─────────────────┘    └──────────────────┘    └──────────────────┘
### 🎯 Challenge & Value Alignment

| FIFA Core Challenge | Critical Stadium Friction | StadiumGPT AI Solution | Expected Operational Impact |
| :--- | :--- | :--- | :--- |
| **Stadium Navigation** | Disorientation in multi-tiered seating architectures. | **AI Route Optimizer** with real-time crowd-free alternative pathfinding. | **35% Reduction** in pedestrian checkpoint congestion. |
| **Crowd Management** | Sudden bottlenecks at gates, concession stands, and restrooms. | **Real-time Heatmap generation** + Predictive ML Queue Forecasting. | **25 Min Saved** per average attendee on concession lines. |
| **Fan Safety & Medical** | Blindspots in locating localized medical emergencies instantly. | **Emergency Voice AI** + automated exact-coordinate medical team dispatch. | **Under 90 Seconds** emergency response activation. |
| **Language Barriers** | Static signage fails international multi-lingual cohorts. | **6+ Language Voice & Text AI** powered by optimized Gemini models. | **100% Inclusivity** for diverse global fan demographics. |
| **Accessibility Inclusion** | Wheelchair attendees face unexpected step/barrier blocks. | Dedicated **Wheelchair Route Mapping** + Multi-sensory UI support. | Zero-barrier navigation across the complete stadium layout. |
| **Operational Intelligence** | Management lacks foresight on post-match transport surge spikes. | **Digital Twin Simulations** integrating metro/parking capacity load data. | Optimized outbound flow preventing stampedes and station overloads. |

---

## 📁 Project Structure

```text
stadium-gpt/
├── backend/
│   ├── app/
│   │   ├── models/          # Pydantic data schemas & request validation
│   │   ├── routes/          # REST API endpoints (Auth, Navigation, Crowd, Emergency)
│   │   ├── services/        # Core business logic & Gemini AI API integrations
│   │   └── utils/           # Helper utilities, rate limiters, and security tools
│   ├── tests/               # 33+ robust passing unit and integration tests
│   └── requirements.txt     # Python backend dependencies
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable visual components (Heatmaps, Chat Interfaces)
│   │   ├── pages/           # High-level views (Dashboard, Navigator, Emergency Hub)
│   │   └── context/         # React Context for Global State & Theme management
│   └── package.json         # Frontend Node dependencies
└── docker-compose.yml       # Production-ready multi-container orchestration
```

---

## 🏗️ Deep-Dive Architecture

┌────────────────────────────────────────────────────────────────────────┐│                        Frontend UI (React.js)                          ││     • Accessible UI (High Contrast)      • Voice AI Integration        ││     • Live WebSocket Map Renderers        • Client Rate Limiting        │└───────────────────────────────────┬────────────────────────────────────┘│ Secure API Calls (HTTPS / WSS)┌───────────────────────────────────▼────────────────────────────────────┐│                        Backend Core (FastAPI)                          │├────────────────────────────────────────────────────────────────────────┤│  ┌───────────────────────┐ ┌───────────────────────┐ ┌──────────────┐  ││  │   JWT Auth & Bcrypt   │ │   AI Path Optimizer   │ │ Live Crowd  │  ││  │   Identity Guard      │ │   (Dijkstra/A* Ext)   │ │ Heatmapping  │  ││  └───────────────────────┘ └───────────────────────┘ └──────────────┘  ││  ┌───────────────────────┐ ┌───────────────────────┐ ┌──────────────┐  ││  │ Queue Wait Predictor  │ │ Emergency AI Hub      │ │ Transport    │  ││  │ (Time-Series Forecast)│ │ Coordinate Tracker    │ │ Forecast Engine│││  └───────────────────────┘ └───────────────────────┘ └──────────────┘  ││  ┌───────────────────────┐ ┌───────────────────────┐                   ││  │ Stadium Digital Twin  │ │ Multi-lingual Voice   │                   ││  │ Predictive Simulators │ │ Translation Router    │                   ││  └───────────────────────┘ └───────────────────────┘                   │├────────────────────────────────────────────────────────────────────────┤│                       Intelligent Infrastructure                       ││  ┌──────────────────────────────────────────────────────────────────┐  ││  │ • AI Layer: Google Gemini (Structured Context Inference)         │  ││  │ • Database Layer: SQLite (Relational State Storage)             │  ││  │ • Real-Time Engine: Native WebSockets (Bi-directional Broadcasts)  │  ││  └──────────────────────────────────────────────────────────────────┘  │└────────────────────────────────────────────────────────────────────────┘
---

## 🚀 Key Features Breakdown

1. **AI Route Optimizer:** Computes multi-criteria navigation paths based on current real-time walking speeds, gate status, and congestion points.
2. **Queue Predictor:** Uses chronological historical arrival data combined with live venue scans to forecast current and future wait-times at facilities.
3. **Dynamic Crowd Heatmaps:** Displays live infrastructure visual density indexes to event operators to proactively deploy marshals to overloading sectors.
4. **Incident Response System:** One-click automated voice/text hazard reports instantly ping the backend network, identifying location coordinates and dispatching medical or emergency units immediately.
5. **Universal Voice AI Support:** Allows seamless operational access to navigation instructions via voice processing across 6 major international languages.
6. **Digital Twin Core:** Simulates incoming and outgoing crowd bursts to test emergency evacuation efficiency before actual matchday events happen.

---

## 🧪 Testing Metrics & Verification

We emphasize extreme reliability for critical venue deployments through an automated testing workflow.

```bash
# Run all core application test suites
pytest tests/ -v

# Generate local test coverage matrix reports
pytest tests/ --cov=app --cov-report=html
```
* **Test Status Metrics:** `33 Passed`, `1 Skipped`, `0 Failed`
* **Target Code Coverage Matrix:** Enforced >90% coverage across core services.

---

## 🔒 Production Security Protocols

* **Cryptographic Identity Protection:** Implementation of robust JWT Access Tokens alongside standard `Bcrypt` password salt-hashing algorithms.
* **API Rate Limiting Guard:** Throttles continuous burst requests to maximum thresholds of `60 requests/minute` per unique IP state to thwart Denial of Service (DoS) attacks.
* **Strict Network Content Security:** Hardened Cross-Origin Resource Sharing (**CORS**) permissions alongside robust Content Security Policy (**CSP**) headers protecting Swagger UI OpenAPI instances against Cross-Site Scripting (XSS).
* **Deterministic Input Cleansing:** Strong parameter-level enforcement across all endpoint layers utilizing strict Pydantic parsing models.

---

## ♿ Comprehensive Accessibility Matrix

* **WAI-ARIA Conformance:** Rigorous application of explicit ARIA landmark semantics for total screen reader support.
* **Alternative Nav Paths:** Automated fallback navigation filters specialized in calculating zero-step, ramp-only wheelchair routes.
* **Low-Vision UI Assistances:** Direct system-level integrations offering native High Contrast color toggles and keyboard-only focused web interactions.

---

## 📦 Local Installation Guide

### Backend Service Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Populate your GEMINI_API_KEY value inside the generated .env
uvicorn app.main:app --reload
```

### Frontend UI Setup
```bash
cd ../frontend
npm install
npm start
```

---

## 🌐 Live System Deployments

* **Frontend Production Application UI:** [Click Here to View Live App](https://stadiumgpt-ai-stadium-assistant-1.onrender.com)
* **Backend Live Server Instance:** [Click Here to View Live Server](https://stadiumgpt-ai-stadium-assistant.onrender.com)
* **Interactive OpenAPI (Swagger UI) Documentation:** [Explore API Docs](https://stadiumgpt-ai-stadium-assistant.onrender.com/api/docs)

---

## 👨‍💻 Engineering Team
* **Lead Engineer & AI Architect:** Riya Davra ([@Riya-davra04](https://github.com))

---
## 📄 License
This application is distributed under the terms of the official **MIT License**.
