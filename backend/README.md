# Backend (Python + Django)

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
```

## Uruchomienie

```bash
python manage.py runserver 0.0.0.0:5000
```

Serwer będzie dostępny na http://localhost:5000

## Development

```bash
python manage.py runserver 0.0.0.0:5000
```

## Tworzenie nowej aplikacji

```bash
python manage.py startapp <nazwa_aplikacji>
```
