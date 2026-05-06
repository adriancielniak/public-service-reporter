# Public Service Reporter

Aplikacja do zgłaszania problemów dla mieszkańców gminy.

## Stack techniczny
- **Frontend**: Vue.js
- **Backend**: Python (Django + Django REST Framework)
- **Baza danych**: PostgreSQL
- **Konteneryzacja**: Docker

## Struktura projektu

```
public-service-reporter/
├── frontend/          # Aplikacja Vue.js
├── backend/           # API Python
├── docker/            # Dockerfiles i konfiguracje
├── docker-compose.yml # Orkestracja kontenerów
└── README.md          # Ten plik
```

## Szybki start

### Wymagania
- Docker i Docker Compose

### Uruchomienie całej aplikacji

```bash
docker-compose up
```

Aplikacja będzie dostępna:
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

## Zespół

- **Frontend**: [imię kolegi]
- **Backend**: [imię kolegi]
- **DevOps/Docker**: [imię kolegi]

## Notatki

Szczegóły modelu danych i endpointów API zostaną ustaleni w trakcie pracy.
