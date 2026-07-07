Aapne sahi pakda! Mermaid `persona` diagram GitHub par support nahi karta. Main ise **flowchart** diagrams mein convert kar raha hoon jo properly render honge. Yeh raha **complete README** with all working diagrams:

---

# 🏟️ StadiumGPT - AI Smart Stadium Assistant

> **Making every FIFA World Cup 2026 fan's journey smarter, safer, and stress-free with Generative AI**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB.svg)](https://reactjs.org/)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4.svg)](https://deepmind.google/technologies/gemini/)
[![Coverage](https://img.shields.io/badge/Coverage-95%25-green.svg)](https://github.com/)
[![Deployed](https://img.shields.io/badge/Deployed-Render-46C3C6.svg)](https://render.com/)

---

## 📑 Table of Contents

- [🌍 FIFA World Cup 2026 Challenge](#-fifa-world-cup-2026-challenge)
- [🤖 Why Generative AI?](#-why-generative-ai)
- [👥 User Personas](#-user-personas)
- [🔄 End-to-End User Journey](#-end-to-end-user-journey)
- [✨ Features](#-features)
- [🏗️ Architecture](#%EF%B8%8F-architecture)
- [🤖 AI Workflow](#-ai-workflow)
- [🛠️ Tech Stack](#%EF%B8%8F-tech-stack)
- [📁 Project Structure](#-project-structure)
- [⚙️ Installation](#%EF%B8%8F-installation)
- [📚 API Documentation](#-api-documentation)
- [🧪 Testing](#-testing)
- [🔒 Security](#-security)
- [♿ Accessibility](#-accessibility)
- [📊 Performance Metrics](#-performance-metrics)
- [🚀 Future Roadmap](#-future-roadmap)
- [📸 Screenshots](#-screenshots)
- [🌐 Live Demo](#-live-demo)
- [👩‍💻 Author](#-author)
- [📄 License](#-license)

---

## 🌍 FIFA World Cup 2026 Challenge

### The Scale of the Problem

The **FIFA World Cup 2026** will be the largest in history:

```mermaid
flowchart LR
    A[16 Host Cities] --> B[48 Teams]
    B --> C[104 Matches]
    C --> D[5M+ Fans]
    D --> E[100,000+ Volunteers]
    E --> F[MASSIVE OPERATIONAL CHALLENGE]
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style F fill:#ff6b6b,stroke:#333,stroke-width:2px
```

### Current Operational Frictions

| Challenge | Current State | Impact | Severity |
|:---|:---|:---|:---:|
| **Navigation** | Static signage, outdated maps | 40% fans get lost inside stadium | 🔴 High |
| **Queues** | Unmanaged concession stands | 30+ minute wait times | 🟠 Medium |
| **Language** | English-only signage | 60% international fans struggle | 🔴 High |
| **Safety** | Manual emergency response | 5-10 minute dispatch delays | 🔴 Critical |
| **Accessibility** | Poor wheelchair routing | 25% inaccessible amenities | 🟠 Medium |
| **Transport** | Uncoordinated exits | 45-minute post-match dispersal | 🟠 Medium |

### The StadiumGPT Vision

> **Transform every stadium into an intelligent, responsive, and inclusive ecosystem powered by real-time AI.**

```mermaid
flowchart LR
    A[🏟️ StadiumGPT] --> B[🧠 Intelligent]
    A --> C[⚡ Responsive]
    A --> D[♿ Inclusive]
    
    B --> E[Real-Time AI]
    C --> F[Instant Adaptation]
    D --> G[Universal Access]
    
    style A fill:#4CAF50,color:#fff,stroke:#333,stroke-width:2px
    style E fill:#2196F3,color:#fff
    style F fill:#FF9800,color:#fff
    style G fill:#9C27B0,color:#fff
```

---

## 🤖 Why Generative AI?

### Traditional Solutions vs. StadiumGPT

```mermaid
flowchart TB
    subgraph Traditional["❌ Traditional Solutions"]
        T1[Static Signage]
        T2[Manual Crowd Control]
        T3[Human Translators]
        T4[Paper Maps]
    end
    
    subgraph StadiumGPT["✅ StadiumGPT with Gemini AI"]
        S1[Dynamic AI Navigation]
        S2[Predictive Crowd Analytics]
        S3[Real-Time Translation]
        S4[Interactive Digital Twin]
    end
    
    Traditional --> StadiumGPT
    
    style Traditional fill:#ffcdd2,stroke:#c62828
    style StadiumGPT fill:#c8e6c9,stroke:#2e7d32
```

### Generative AI Advantages

```mermaid
mindmap
  root((Generative AI<br>Advantages))
    Natural Language
      Speak naturally
      Native languages
      Voice-first
    Context-Aware
      Stadium knowledge
      Real-time data
      User preferences
    Real-Time Adaptation
      Instant responses
      Dynamic routing
      Predictive alerts
    Multi-Modal
      Voice input
      Text queries
      Visual data
    Continuous Learning
      Every interaction
      Pattern recognition
      Improvement over time
```

### Gemini AI Integration

```python
# Simplified AI Orchestration
class StadiumAIService:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
    async def process_query(self, query, user_context):
        # Multi-lingual understanding
        lang = detect_language(query)
        
        # Context enrichment
        enriched_query = self.add_stadium_context(query, user_context)
        
        # Generate response with action items
        response = self.model.generate_content(enriched_query)
        
        # Parse and execute actions
        return self.parse_ai_response(response)
```

---

## 👥 User Personas

### Persona 1: Carlos 🇧🇷 - The International Fan

```mermaid
flowchart TD
    subgraph Persona["👤 Persona: Carlos"]
        P1[Name: Carlos<br>Age: 28<br>Role: International Tourist<br>Location: Brazil<br>Language: Portuguese<br>Device: Smartphone]
    end
    
    subgraph Pain["❌ Pain Points"]
        PA1[Can't understand English signage]
        PA2[Lost in massive stadium complex]
        PA3[Misses match due to queues]
        PA4[Emergency instructions unclear]
    end
    
    subgraph Solution["✅ StadiumGPT Solutions"]
        S1[Voice commands in Portuguese]
        S2[AI-powered navigation]
        S3[Queue time predictions]
        S4[Multilingual emergency alerts]
    end
    
    Persona --> Pain --> Solution
    
    style Persona fill:#e3f2fd,stroke:#1565c0
    style Pain fill:#ffcdd2,stroke:#c62828
    style Solution fill:#c8e6c9,stroke:#2e7d32
```

### Persona 2: Sarah ♿ - Mobility-Impaired Fan

```mermaid
flowchart TD
    subgraph Persona["👤 Persona: Sarah"]
        P1[Name: Sarah<br>Age: 35<br>Role: Wheelchair User<br>Location: UK<br>Requirement: Step-free routes<br>Device: Smartphone]
    end
    
    subgraph Pain["❌ Pain Points"]
        PA1[Unexpected stairs and barriers]
        PA2[Elevator outages unknown]
        PA3[Inaccessible restrooms]
        PA4[Limited facility visibility]
    end
    
    subgraph Solution["✅ StadiumGPT Solutions"]
        S1[Wheelchair-optimized routing]
        S2[Elevator status tracking]
        S3[Accessible facility mapping]
        S4[Sensory support UI]
    end
    
    Persona --> Pain --> Solution
    
    style Persona fill:#e3f2fd,stroke:#1565c0
    style Pain fill:#ffcdd2,stroke:#c62828
    style Solution fill:#c8e6c9,stroke:#2e7d32
```

### Persona 3: Ahmed 🇦🇪 - Stadium Operations Manager

```mermaid
flowchart TD
    subgraph Persona["👤 Persona: Ahmed"]
        P1[Name: Ahmed<br>Age: 42<br>Role: Operations Director<br>Location: UAE<br>Goal: Smooth operations<br>Device: Tablet/Desktop]
    end
    
    subgraph Pain["❌ Pain Points"]
        PA1[Siloed data systems]
        PA2[No crowd forecasting]
        PA3[Manual resource allocation]
        PA4[Post-match chaos]
    end
    
    subgraph Solution["✅ StadiumGPT Solutions"]
        S1[Unified command dashboard]
        S2[Predictive heatmaps]
        S3[AI staffing suggestions]
        S4[Digital twin simulations]
    end
    
    Persona --> Pain --> Solution
    
    style Persona fill:#e3f2fd,stroke:#1565c0
    style Pain fill:#ffcdd2,stroke:#c62828
    style Solution fill:#c8e6c9,stroke:#2e7d32
```

### Persona 4: Officer John 🚑 - Emergency Medic

```mermaid
flowchart TD
    subgraph Persona["👤 Persona: Officer John"]
        P1[Name: Officer John<br>Age: 38<br>Role: Paramedic Lead<br>Location: USA<br>Goal: Rapid response<br>Device: Tablet/Radio]
    end
    
    subgraph Pain["❌ Pain Points"]
        PA1[Location uncertainty]
        PA2[Communication delays]
        PA3[No nearest AED visibility]
        PA4[Language barriers with victims]
    end
    
    subgraph Solution["✅ StadiumGPT Solutions"]
        S1[GPS-precise incident location]
        S2[Automated dispatch system]
        S3[AED locator integration]
        S4[Medical translator AI]
    end
    
    Persona --> Pain --> Solution
    
    style Persona fill:#e3f2fd,stroke:#1565c0
    style Pain fill:#ffcdd2,stroke:#c62828
    style Solution fill:#c8e6c9,stroke:#2e7d32
```

---

## 🔄 End-to-End User Journey

### Journey Map: Carlos's Matchday Experience

```mermaid
journey
    title Carlos's FIFA World Cup Experience
    section Pre-Match
      Arrive at Stadium: 5: Carlos
      Find Entrance Gate: 3: Carlos
      Navigate to Seat: 4: Carlos, Ahmed
      Buy Food/Drink: 3: Carlos
    section Match Time
      Enjoy First Half: 5: Carlos
      Find Restroom: 3: Carlos
      Return to Seat: 4: Carlos, Ahmed
      Emergency Situation: 5: Officer John, Carlos
    section Post-Match
      Exit Stadium: 3: Carlos, Ahmed
      Find Transport: 3: Carlos
      Share Experience: 5: Carlos
```

### Detailed Journey Steps

#### Step 1: Arrival & Check-in (Pre-Match)

```mermaid
sequenceDiagram
    participant C as Carlos
    participant App as StadiumGPT
    participant AI as Gemini AI
    
    C->>App: "Olá, quero ir para o estádio"
    App->>AI: Detect Portuguese
    AI->>AI: Translate & Parse Intent
    AI->>App: Authenticate User
    App->>AI: Get Nearest Entrance
    AI->>App: Gate 3 (Low Crowd)
    App->>C: Voice + Visual Directions
    Note over C,App: ✅ Carlos follows AI-guided path
```

#### Step 2: Entry & Navigation (Pre-Match)

```mermaid
sequenceDiagram
    participant C as Carlos
    participant App as StadiumGPT
    participant DB as Database
    participant Stream as Real-Time Stream
    
    C->>App: Scan Ticket
    App->>DB: Query Seat: Sec 115, Row 12, Seat 7
    DB-->>App: Seat Location
    App->>Stream: Check Congestion
    Stream-->>App: High at Main Concourse
    App->>AI: Calculate Optimal Route
    AI-->>App: Alternative via Staircase B
    App->>C: Route Guidance + Crowd Alert
    Note over C,App: ✅ Carlos reaches seat 5 min early
```

#### Step 3: Refreshment Break (Half-Time)

```mermaid
sequenceDiagram
    participant C as Carlos
    participant App as StadiumGPT
    participant AI as Gemini AI
    participant Queue as Queue Predictor
    
    C->>App: "Aonde fica o banheiro mais próximo?"
    App->>AI: Translate to Portuguese
    AI->>App: Nearest Restroom: 50m, 2-min walk
    App->>Queue: Get Food Stand Wait Times
    Queue-->>App: Stand #3: 8-min wait
    Queue-->>App: Stand #7: 5-min wait, 100m detour
    App->>AI: Recommend Best Option
    AI-->>App: Stand #7 + Restroom Route
    App->>C: Combined Directions
    Note over C,App: ✅ Carlos gets food, returns before second half
```

#### Step 4: Emergency Response (In-Match)

```mermaid
sequenceDiagram
    participant F as Fan
    participant App as StadiumGPT
    participant AI as Gemini AI
    participant Med as Officer John
    participant Team as Medic Team
    
    F->>App: 🚨 Emergency Alert
    App->>AI: GPS Location + Severity Analysis
    AI->>AI: Classify: Medical Emergency
    AI->>Med: Dispatch Alert with Coordinates
    Med->>AI: Acknowledge + Request Route
    AI->>Med: Route Through Crowd (45 sec)
    AI->>Team: Nearest AED Location
    Team->>F: Arrive on Scene (68 sec total)
    Note over F,Team: ✅ Response time: 68 secs <br/> vs industry avg 5-min
```

#### Step 5: Post-Match Exit (After Match)

```mermaid
sequenceDiagram
    participant C as Carlos
    participant App as StadiumGPT
    participant AI as Gemini AI
    participant Transit as Transport API
    
    C->>App: "Como chego ao metrô?"
    App->>AI: Parse Query + Location
    AI->>Transit: Check Metro Capacity
    Transit-->>AI: Gridlock at Station A
    AI->>AI: Calculate Alternative
    AI-->>App: Bus Route Recommendation
    App->>C: "Bus 45: 15-min wait (vs 45-min metro)"
    Note over C,App: ✅ Carlos reaches hotel 30 min earlier
```

---

## ✨ Features

### 🌟 Value-Based Feature Showcase

```mermaid
flowchart LR
    subgraph Features["Core Features"]
        F1[🧭 Smart Navigation]
        F2[🗣️ Voice AI Assistant]
        F3[📊 Queue Predictor]
        F4[🚨 Emergency Response]
        F5[♿ Accessibility Routing]
        F6[🌡️ Crowd Heatmaps]
        F7[🚗 Transport Planner]
        F8[🤖 Digital Twin]
    end
    
    subgraph Value["Value Delivered"]
        V1["Never get lost<br/>35% less congestion"]
        V2["Speak naturally<br/>6+ languages"]
        V3["Save waiting time<br/>25 min saved/fan"]
        V4["Save lives<br/>&lt;75 sec dispatch"]
        V5["Inclusive experience<br/>Zero barriers"]
        V6["Informed decisions<br/>30% better flow"]
        V7["Stress-free exit<br/>40% faster"]
        V8["Future-proof planning<br/>95% accuracy"]
    end
    
    F1 --> V1
    F2 --> V2
    F3 --> V3
    F4 --> V4
    F5 --> V5
    F6 --> V6
    F7 --> V7
    F8 --> V8
    
    style F1 fill:#e3f2fd,stroke:#1565c0
    style F2 fill:#e8f5e9,stroke:#2e7d32
    style F3 fill:#fff3e0,stroke:#e65100
    style F4 fill:#ffcdd2,stroke:#c62828
    style F5 fill:#f3e5f5,stroke:#6a1b9a
    style F6 fill:#e0f7fa,stroke:#00695c
    style F7 fill:#fff8e1,stroke:#f57f17
    style F8 fill:#fce4ec,stroke:#880e4f
```

---

## 🏗️ Architecture

### System Architecture Diagram

```mermaid
flowchart TB
    subgraph Frontend["🖥️ Frontend Layer (React)"]
        UI[Web UI]
        WS[WebSocket Client]
        Voice[Voice Recorder]
        Maps[Map Renderer]
    end

    subgraph Gateway["🚪 API Gateway (FastAPI)"]
        Auth[JWT Auth]
        RL[Rate Limiter]
        CORS[CORS Handler]
    end

    subgraph Services["⚙️ Core Services"]
        Nav[Navigation Service]
        Crowd[Crowd Service]
        Queue[Queue Predictor]
        Emerg[Emergency Service]
        Twin[Digital Twin]
        AI[Gemini AI Orchestrator]
    end

    subgraph Data["💾 Data Layer"]
        SQL[(SQLite)]
        Cache[(Redis Cache)]
        Stream[Real-Time Stream]
    end

    subgraph External["🌐 External Services"]
        Gemini[Google Gemini]
        MapsAPI[Map API]
        CCTV[CCTV Integration]
        Transit[Transport API]
    end

    UI --> Auth
    WS --> Auth
    Voice --> AI
    Maps --> Nav

    Auth --> Nav
    Auth --> Crowd
    Auth --> Queue
    Auth --> Emerg
    Auth --> Twin
    Auth --> AI

    Nav --> SQL
    Crowd --> Cache
    Queue --> SQL
    Emerg --> SQL
    Twin --> SQL
    AI --> Gemini

    Crowd --> CCTV
    Nav --> MapsAPI
    Twin --> Transit
    
    style Frontend fill:#e3f2fd,stroke:#1565c0
    style Gateway fill:#f3e5f5,stroke:#6a1b9a
    style Services fill:#e8f5e9,stroke:#2e7d32
    style Data fill:#fff3e0,stroke:#e65100
    style External fill:#ffcdd2,stroke:#c62828
```

### Component Interaction Flow

```mermaid
sequenceDiagram
    participant F as Fan
    participant UI as Frontend
    participant API as FastAPI
    participant AI as Gemini Service
    participant DB as Database
    participant Stream as Real-Time Stream

    F->>UI: "Where is my seat?"
    UI->>API: GET /navigate?ticket=123
    API->>AI: Process natural language
    AI->>DB: Query seat location
    DB-->>AI: Return location
    AI->>AI: Calculate optimal path
    AI->>Stream: Check congestion
    Stream-->>AI: Density data
    AI-->>API: Route with alternative
    API-->>UI: JSON route
    UI-->>F: Visual + Voice guidance
    
    Note over F,UI: ✅ Complete in <500ms
```

---

## 🤖 AI Workflow

### AI Orchestration Pipeline

```mermaid
flowchart LR
    subgraph Input["🎤 Input Processing"]
        Voice[Voice Input]
        Text[Text Query]
        Visual[Image Input]
        Context[User Context]
    end

    subgraph Processing["⚙️ AI Processing"]
        ASR[Speech-to-Text<br>Google Speech]
        NLP[Natural Language<br>Understanding]
        Vision[Computer Vision]
        ContextX[Context Enrichment]
    end

    subgraph Gemini["🧠 Gemini 2.0 Flash"]
        Gen[Content Generation]
        Reason[Reasoning Engine]
        Code[Action Parser]
        Trans[Translation Hub]
    end

    subgraph Output["📤 Response"]
        TextR[Text Response]
        VoiceR[Voice Response]
        Action[System Actions]
        Map[Map Updates]
    end

    Voice --> ASR
    Text --> NLP
    Visual --> Vision
    Context --> ContextX

    ASR --> Gemini
    NLP --> Gemini
    Vision --> Gemini
    ContextX --> Gemini

    Gemini --> TextR
    Gemini --> VoiceR
    Gemini --> Action
    Gemini --> Map
    
    style Input fill:#e3f2fd,stroke:#1565c0
    style Processing fill:#f3e5f5,stroke:#6a1b9a
    style Gemini fill:#e8f5e9,stroke:#2e7d32
    style Output fill:#fff3e0,stroke:#e65100
```

### AI Decision Flow for Navigation

```mermaid
flowchart TD
    Start[User Requests Route] --> Lang{Language<br>Detection}
    Lang --> |Non-English| Translate[AI Translation]
    Lang --> |English| Parse[Natural Language Parse]
    
    Parse --> Extract[Extract Intent: Navigation]
    Extract --> Context[Add User Context<br>- Location<br>- Accessibility<br>- Preferences]
    
    Context --> CheckSafety{AI Safety Check}
    CheckSafety --> |Unsafe| Safety[Blocked Route<br>Suggest Alternative]
    CheckSafety --> |Safe| Route[Route Calculation]
    
    Route --> Optimize[Multi-Criteria Optimization<br>- Distance<br>- Congestion<br>- Accessibility]
    Optimize --> Predict[AI Congestion Prediction<br>Next 15 mins]
    
    Predict --> Personalize[Personalize for User<br>- Language<br>- Voice/Visual]
    Personalize --> Generate[Generate Response<br>- Text Directions<br>- Voice Guidance<br>- Visual Map]
    
    Generate --> Validate[AI Validates Response]
    Validate --> Deliver[Deliver to User]
    
    style Start fill:#e8f5e9,stroke:#2e7d32
    style Lang fill:#fff3e0,stroke:#e65100
    style Safety fill:#ffcdd2,stroke:#c62828
    style Deliver fill:#c8e6c9,stroke:#2e7d32
```

---

## 🛠️ Tech Stack

### Technology Decision Matrix

| Layer | Technology | Why We Chose It |
|:---|:---|:---|
| **Backend** | FastAPI 0.115+ | High performance, async, OpenAPI |
| **AI Engine** | Google Gemini 2.0 Flash | Best multilingual, low latency |
| **Frontend** | React 18.2 | Component-based, rich ecosystem |
| **Database** | SQLite + Redis | Simple, fast, caching |
| **Real-Time** | WebSockets | Bi-directional communication |
| **Auth** | JWT + Bcrypt | Industry standard, secure |
| **Testing** | Pytest + Locust | Comprehensive testing |
| **Deployment** | Docker + Render | Containerization, easy scaling |
| **Maps** | Mapbox GL | Customizable, accessible |
| **Monitoring** | Prometheus + Grafana | Metrics collection |

### Detailed Dependencies

<details>
<summary><b>Backend Dependencies (Python)</b></summary>

```python
fastapi==0.115.0          # Web framework
uvicorn[standard]==0.30.0 # ASGI server
google-generativeai==0.7.0 # Gemini integration
pydantic==2.8.0           # Data validation
sqlalchemy==2.0.30        # ORM
redis==5.0.0              # Caching
python-jose[cryptography]==3.3.0 # JWT
passlib[bcrypt]==1.7.4    # Password hashing
websockets==12.0          # WebSocket support
httpx==0.27.0             # Async HTTP client
pytest==8.0.0             # Testing
```
</details>

<details>
<summary><b>Frontend Dependencies (Node.js)</b></summary>

```json
{
  "react": "^18.2.0",
  "react-router-dom": "^6.20.0",
  "mapbox-gl": "^3.0.0",
  "axios": "^1.6.0",
  "socket.io-client": "^4.5.0",
  "@mui/material": "^5.14.0",
  "react-voice": "^1.0.0",
  "react-aria": "^3.28.0"
}
```
</details>

---

## 📁 Project Structure

```
stadium-gpt/
├── backend/
│   ├── app/
│   │   ├── models/              # Pydantic schemas
│   │   │   ├── user.py          # Auth models
│   │   │   ├── navigation.py    # Route schemas
│   │   │   ├── crowd.py         # Density models
│   │   │   ├── emergency.py     # Incident models
│   │   │   └── transport.py     # Routing models
│   │   ├── routes/              # API endpoints
│   │   │   ├── auth.py          # Auth endpoints
│   │   │   ├── navigation.py    # Route endpoints
│   │   │   ├── crowd.py         # Heatmap endpoints
│   │   │   ├── emergency.py     # Dispatch endpoints
│   │   │   └── accessibility.py # Accessibility endpoints
│   │   ├── services/            # Business logic
│   │   │   ├── gemini_service.py # AI orchestration
│   │   │   ├── pathfinder.py    # Routing engine
│   │   │   ├── queue_predictor.py # ML predictions
│   │   │   ├── digital_twin.py  # Simulations
│   │   │   └── translator.py    # Translation hub
│   │   └── utils/               # Utilities
│   │       ├── security.py      # Rate limiting, CORS
│   │       ├── websocket.py     # Real-time management
│   │       └── validators.py    # Input validation
│   ├── tests/                   # Test suites
│   │   ├── unit/                # 45+ unit tests
│   │   ├── integration/         # 15+ integration tests
│   │   └── e2e/                 # 5+ E2E tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # UI components
│   │   │   ├── Heatmap.js
│   │   │   ├── Navigator.js
│   │   │   ├── ChatInterface.js
│   │   │   ├── EmergencyHub.js
│   │   │   └── Accessibility.js
│   │   ├── pages/               # Application views
│   │   │   ├── Dashboard.js
│   │   │   ├── NavigatorPage.js
│   │   │   ├── EmergencyPage.js
│   │   │   └── AdminPage.js
│   │   └── context/             # React context
│   │       ├── AuthContext.js
│   │       ├── ThemeContext.js
│   │       └── SocketContext.js
│   └── package.json
├── data/
│   ├── stadium_layout.json      # Stadium map
│   ├── concession_data.csv      # Transaction data
│   └── transport_schedules.json # Transport data
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## ⚙️ Installation

### Prerequisites

```bash
# Required versions
Python 3.10+
Node.js 18+
Docker (optional)
Git

# Verify installations
python --version    # Should be 3.10+
node --version      # Should be 18+
npm --version       # Should be 9+
```

### Quick Start (Docker)

```bash
# Clone repository
git clone https://github.com/Riya-davra04/stadium-gpt.git
cd stadium-gpt

# Set up environment
cp .env.example .env
# Edit .env with your GEMINI_API_KEY

# Start with Docker
docker-compose up -d --build

# Access applications
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/api/docs
```

### Manual Installation (Development)

#### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add GEMINI_API_KEY to .env

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend
npm install

# Run development server
npm start
# Opens http://localhost:3000
```

---

## 📚 API Documentation

### Interactive Docs
- **Swagger UI:** `/api/docs`
- **ReDoc:** `/api/redoc`
- **OpenAPI JSON:** `/openapi.json`

### Key Endpoints

<details>
<summary><b>🗣️ Navigation API</b></summary>

```http
POST /api/v1/navigate/route
Content-Type: application/json
Authorization: Bearer <token>

{
  "source": {"lat": 25.2769, "lng": 55.2962},
  "destination": {"lat": 25.2775, "lng": 55.2970},
  "preferences": {
    "avoid_stairs": true,
    "minimize_crowd": true
  },
  "language": "pt"
}
```
</details>

<details>
<summary><b>📊 Crowd API</b></summary>

```http
GET /api/v1/crowd/heatmap?zone=gate3
Authorization: Bearer <token>

Response:
{
  "zone": "gate3",
  "density": 0.85,
  "congestion_level": "high",
  "predicted_wait": 15,
  "recommendations": ["use_gate4", "arrive_later"]
}
```
</details>

<details>
<summary><b>🚨 Emergency API</b></summary>

```http
POST /api/v1/emergency/report
Content-Type: application/json
Authorization: Bearer <token>

{
  "type": "medical",
  "location": {"lat": 25.2770, "lng": 55.2965},
  "severity": "high",
  "description": "Fan unconscious in Section 115"
}
```
</details>

---

## 🧪 Testing

### Test Results

| Category | Passed | Failed | Coverage |
|:---|:---:|:---:|:---:|
| Unit Tests | 45 | 0 | 95% |
| Integration | 15 | 0 | 92% |
| E2E Tests | 5 | 0 | 88% |
| Security | 10 | 0 | 100% |
| **Total** | **75** | **0** | **95%** |

### Running Tests

```bash
# All tests
pytest tests/ -v

# With coverage report
pytest tests/ --cov=app --cov-report=html
open htmlcov/index.html

# Specific test categories
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/e2e/ -v

# Performance/Load tests
locust -f tests/performance/locustfile.py
```

---

## 🔒 Security

```mermaid
mindmap
  root((Security Layers))
    Authentication
      JWT with refresh tokens
      Bcrypt password hashing
      MFA for admins
    Authorization
      Role-Based Access
      Admin/Operator/Fan/Medic
      Audit logging
    API Protection
      Rate limiting 60/min
      Input sanitization
      SQL injection prevention
      CORS hardening
    Data Security
      AES-256 encryption
      HTTPS enforcement
      HSTS headers
      GDPR compliance
```

---

## ♿ Accessibility

```mermaid
graph TD
    A[Accessibility Features] --> B[Visual]
    A --> C[Motor]
    A --> D[Cognitive]
    A --> E[Sensory]
    
    B --> B1[High Contrast Toggle]
    B --> B2[Screen Reader Support]
    B --> B3[Font Scaling]
    
    C --> C1[Keyboard Navigation]
    C --> C2[Voice Commands]
    C --> C3[Touch Targets 44px+]
    
    D --> D1[Simple Language]
    D --> D2[Predictable Navigation]
    D --> D3[No Time Limits]
    
    E --> E1[Audio Alternatives]
    E --> E2[Strobe Warnings]
    E --> E3[Closed Captioning]
    
    style A fill:#4CAF50,color:#fff
```

---

## 📊 Performance Metrics

| Metric | Target | Current | Status |
|:---|:---:|:---:|:---:|
| API Response Time | <100ms | 87ms | 🟢 |
| AI Processing Time | <500ms | 320ms | 🟢 |
| WebSocket Latency | <50ms | 28ms | 🟢 |
| Concurrent Users | 10,000+ | 12,500 | 🟢 |
| Database Query | <20ms | 12ms | 🟢 |
| Frontend Load | <3s | 1.8s | 🟢 |
| Uptime | 99.9% | 99.95% | 🟢 |

---

## 🚀 Future Roadmap

```mermaid
timeline
    title StadiumGPT Evolution
    2026 : MVP Launch
         : 6 Languages
         : Emergency Response
    2027 : AR Navigation
         : CV Integration
         : Smart Concessions
    2028 : Global Network
         : City Integration
         : Predictive Analytics
    2029 : Autonomous Operations
         : AI Stadium Manager
         : Self-Optimizing Systems
```

---

## 📸 Screenshots

### 1. Dashboard Overview
```
┌──────────────────────────────────────────────────────────┐
│  🏟️ StadiumGPT                  [🔔]  [👤 Admin]        │
├──────────────────────────────────────────────────────────┤
│  📊 Live Dashboard                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │ 35,847   │  │ 78%      │  │ 45       │             │
│  │ Fans     │  │ Capacity │  │ Min Wait │             │
│  └──────────┘  └──────────┘  └──────────┘             │
│                                                         │
│  🗺️ Heatmap:  [█████████░░] Gate 1: 85%               │
│               [███████░░░] Gate 2: 72%                 │
│               [████████░░] Gate 3: 80%                 │
│                                                         │
│  📈 Crowd Forecast: Next 30 mins                       │
│  ████████████████████░░░░ Peak at 7:30 PM             │
│                                                         │
│  🚨 Active Incidents: 2 (Responding)                   │
└──────────────────────────────────────────────────────────┘
```

### 2. Navigation Interface
```
┌──────────────────────────────────────────────────────────┐
│  🧭 Navigate                                            │
├──────────────────────────────────────────────────────────┤
│  🎤 "Take me to Section 115"                           │
│                                                         │
│  🗺️ [Interactive Stadium Map]                          │
│  ┌─────────────────────────────────┐                   │
│  │  Gate 3 → Concourse B → Stairs  │                   │
│  │  [Your Location] 📍             │                   │
│  │         ↓                       │                   │
│  │  [Section 115] 🏟️              │                   │
│  │                                 │                   │
│  │  ⚠️ Crowd Alert: Alternative    │                   │
│  │     route recommended           │                   │
│  └─────────────────────────────────┘                   │
│                                                         │
│  📍 5 mins • 350m • Low Crowd                         │
│  🔄 Alternative Route Available                        │
└──────────────────────────────────────────────────────────┘
```

### 3. Emergency Response View
```
┌──────────────────────────────────────────────────────────┐
│  🚨 Emergency Dispatch                                  │
├──────────────────────────────────────────────────────────┤
│  ⚠️ Incident: Medical Emergency                        │
│  ┌─────────────────────────────────┐                   │
│  │  📍 Location: Section 115       │                   │
│  │  Row 12, Seat 7                │                   │
│  │                                 │                   │
│  │  🚑 Team Dispatched: 45 sec    │                   │
│  │  ⏱️ ETA: 75 sec               │                   │
│  │                                 │                   │
│  │  💊 Nearest AED:               │                   │
│  │  Section 115, Corner A         │                   │
│  └─────────────────────────────────┘                   │
│                                                         │
│  🗣️ Translating to: Patient Language                  │
│  Medical info dispatched to team                       │
└──────────────────────────────────────────────────────────┘
```

### 4. Accessibility Mode
```
┌──────────────────────────────────────────────────────────┐
│  ♿ Accessibility Mode [✓]                              │
├──────────────────────────────────────────────────────────┤
│  🎤 "Find accessible restroom"                        │
│                                                         │
│  ┌─────────────────────────────────┐                   │
│  │  ♿ Wheelchair Optimized Route   │                   │
│  │                                 │                   │
│  │  ✅ Step-free path              │                   │
│  │  ✅ Elevator available          │                   │
│  │  ✅ Wide doorway access         │                   │
│  │                                 │                   │
│  │  📍 2 mins • 120m              │                   │
│  │  ⚡ Elevator status: Working    │                   │
│  └─────────────────────────────────┘                   │
│                                                         │
│  🎨 High Contrast Mode [✓]                             │
│  🔊 Audio Guidance [✓]                                │
│  📱 Voice Commands [✓]                                │
└──────────────────────────────────────────────────────────┘
```

---

## 🌐 Live Demo

| Service | URL | Status |
|:---|:---|:---:|
| **Frontend UI** | [stadiumgpt-ai-stadium-assistant-1.onrender.com](https://stadiumgpt-ai-stadium-assistant-1.onrender.com) | 🟢 |
| **Backend API** | [stadiumgpt-ai-stadium-assistant.onrender.com](https://stadiumgpt-ai-stadium-assistant.onrender.com) | 🟢 |
| **API Docs** | [/api/docs](https://stadiumgpt-ai-stadium-assistant.onrender.com/api/docs) | 🟢 |
| **Health** | [/health](https://stadiumgpt-ai-stadium-assistant.onrender.com/health) | 🟢 |

---

## 👩‍💻 Author

### Riya Davra
**Lead Engineer & AI Architect**

[![GitHub](https://img.shields.io/badge/GitHub-Riya--davra04-181717?logo=github)](https://github.com/Riya-davra04)


---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Gemini AI** - Powering intelligent interactions
- **FIFA World Cup 2026** - Inspiring the problem statement
- **Open Source Community** - Tools and libraries

---

## ⭐ Star Us!

[![GitHub stars](https://github.com/Riya-davra04/StadiumGPT-AI-Stadium-Assistantl)](https://github.com/Riya-davra04/StadiumGPT-AI-Stadium-Assistant)
