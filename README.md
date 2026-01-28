# Kanjakitude - MyPostman
# @author : Kanjak
# @email : kanjak.breniacs@gmail.com
# @portfolio : kanjak-b.github.io/kanjakitude
# copyright kanjakitude 2026 All right reserved

Postman-like local tool for testing REST APIs with a Python backend (FastAPI) and desktop UI (PySide6).

## Features
- HTTP methods: GET, POST, PUT, PATCH, DELETE
- URL, headers, query params, body (json/form/raw)
- Response preview: status, headers, body, timing
- Environments with variables
- Collections and history
- Auth: Bearer, Basic, API Key
- Import/export ready (JSON)

## Setup
1) Activate your venv (already created).
2) Install dependencies:

```
pip install -r requirements.txt
```

## Run backend

```
uvicorn app.backend.main:app --reload
```

## Run frontend

```
python -m app.frontend.main
```

## Notes
- The backend stores data locally in SQLite at app/backend/data/app.db.
- Secrets are masked in history; do not paste real production secrets.
