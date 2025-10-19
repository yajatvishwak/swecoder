# FastAPI + SQLModel Starter

## Quickstart

1. Create and activate venv (already created as .venv)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install deps

```bash
pip install -r requirements.txt
```

3. Run API

```bash
uvicorn app.main:app --reload
```

4. Test

- Health: GET http://127.0.0.1:8000/health
- Items CRUD: /api/v1/items

## Configuration

- Env file: .env
- Vars: APP_NAME, DEBUG, SQLITE_DB_FILE, DATABASE_URL

If DATABASE_URL is unset, defaults to sqlite:///./app.db
