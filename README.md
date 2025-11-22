# Def Acc Hackathon

## Backend

The backend is a FastAPI server that serves the Drift Explorer API.

### Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Development

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

This starts the API server at http://localhost:8000

### API Endpoints

- `GET /api/prompts` - List all prompts (lightweight, for scatterplot)
- `GET /api/prompts/{id}` - Get full prompt details (includes rubric)
- `GET /api/clusters` - Get hierarchical cluster data
- `GET /health` - Health check

### Regenerate Mock Data

```bash
cd backend
source venv/bin/activate
python scripts/generate_mock_data.py
```

## Frontend

The frontend is a React + TypeScript app built with Vite.

### Setup

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

This starts the dev server at http://localhost:5173

### Build

```bash
npm run build
```
