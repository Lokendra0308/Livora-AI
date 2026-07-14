# Livora AI — Multi-Agent AI Platform

> 🚧 Work in progress, built step by step. This README will be expanded into
> full documentation (architecture diagram, setup guide, API docs, deployment
> guide) as the final step of the build.

## Current status: Step 1 — Project Foundation ✅

- FastAPI backend skeleton with health check, structured logging, typed
  settings, and a global error-handling convention.
- React + TypeScript + Vite + TailwindCSS v4 frontend skeleton, connected to
  the backend through a dev proxy, with a typed API client.

## Quickstart (development)

**Backend**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Backend runs at http://localhost:8000 — Swagger docs at `/docs`.

**Frontend**
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at http://localhost:5173 and proxies `/api` calls to the backend.
"# nexus-ai" 
