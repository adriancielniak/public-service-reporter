# Public Service Reporter

🏛️ About Public Service Reporter (PSR)Public Service Reporter (PSR) is an open-source, full-stack municipal management platform designed to bridge the gap between local citizens and community officials. The application automates the detection, reporting, and systematic monitoring of infrastructural issues, safety hazards, and public utility failures within public spaces.  By providing an intuitive spatial reporting system for residents and a robust management dashboard for local authorities, PSR digitizes municipal workflows, making community maintenance transparent, efficient, and data-driven.

🎯 Purpose & ObjectivesTraditional methods of reporting civic issues (such as phone calls or physical paperwork) often lead to delayed response times, lost data, and lack of transparency for citizens. PSR was developed to solve these friction points by achieving the following goals:Empower Citizens: Give residents an effortless, instant way to report localized problems with exact geographical pinning right from their devices.Optimize Municipal Workflow: Provide municipal workers with an automated queue system to track, triage, and update the status of infrastructure repairs.  Increase Transparency: Keep the public informed about community issues, preventing duplicate reports and building trust through clear visual updates on resolution progress.Support Data-Driven Decisions: Aggregate spatial and categorical data so city planners can easily identify recurring problematic zones or infrastructure trends.

The ecosystem is built with absolute decoupled scalability in mind:

📱 VUE 3 FRONTEND SPA                               🔒 DJANGO REST FRAMEWORK API
+---------------------------+                      +-------------------------------+
|     Leaflet Map Layer     |                      |    Custom AbstractUser Model  |
|    (User GPS Location)    |                      |  (standard / worker / admin)  |
+-------------+-------------+                      +---------------+---------------+
              |                                                    |
   Interacts  |                                                    | Evaluates User
   With State |                                                    | Roles
              v                                                    v
+-------------+-------------+  Secure HTTP Requests  +---------------+---------------+
|    Centralized Axios      |=====================>|  Custom RBAC Permission Layer |
|  & Reactive State Refs    |  (DRF Token Auth)    |   (IsOwner & IsAdmin Rules)   |
+---------------------------+                      +-------------------------------+

## Tech Stack
- **Frontend**: Vue.js
- **Backend**: Python (Django + Django REST Framework)
- **Baza danych**: PostgreSQL
- **Konteneryzacja**: Docker

## Project Structure

```
public-service-reporter/
├── frontend/          # Aplikacja Vue.js
├── backend/           # API Python
├── docker/            # Dockerfiles i konfiguracje
├── docker-compose.yml # Orkestracja kontenerów
└── README.md          # Ten plik
```

## Quick Start

### Wymagania
- Docker i Docker Compose

### Launching the app

```bash
docker-compose up
```

Application will be accessible:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:5000
- **Baza danych**: localhost:5432

## Development

### Frontend (Vue.js)
```bash
cd frontend
npm install
npm run serve
```

### Backend (Python)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # lub venv\Scripts\activate na Windows
pip install -r requirements.txt
python app.py
```

## Team

- **Frontend**: [imię kolegi]
- **Backend**: [imię kolegi]
- **DevOps/Docker**: [imię kolegi]

## Notes ???

Szczegóły modelu danych i endpointów API zostaną ustaleni w trakcie pracy.
