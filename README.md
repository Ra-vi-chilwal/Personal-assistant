# Personal Assistant: portfolio with RAG chatbot

React (Vite) portfolio in `frontend/` + FastAPI RAG chatbot in `backend/` (Gemini embeddings, MongoDB Atlas vector search, Groq LLM).

## Run locally
```
cd backend
python -m venv venv && venv\Scripts\pip install -r requirements.txt
copy .env.example .env      # fill in GEMINI_API_KEY, GROQ_API_KEY, MONGODB_URI
venv\Scripts\python -m uvicorn app.main:app --reload --port 8000

cd frontend
npm install
npm run dev
```

## Feed the chatbot
Put PDFs (and `*qa*.md` files with `Q:` / `A:` blocks) in `backend/data/` (git-ignored, keep private files out of the repo), then:
```
cd backend
venv\Scripts\python ingest\ingest_pdfs.py
```
Create the Atlas vector index once with `ingest/create_index.py`.

## Deploy (one service on Render)
FastAPI serves the built React site (`frontend/dist`, committed) and the `/chat` API from one URL.

1. After changing the frontend: `cd frontend && npm run build`, then commit `frontend/dist`.
2. Render -> New -> Blueprint -> pick this repo (uses `render.yaml`).
3. Set env vars `GEMINI_API_KEY`, `GROQ_API_KEY`, `MONGODB_URI`.
4. MongoDB Atlas -> Network Access: allow Render to connect (e.g. `0.0.0.0/0`).
5. Free plan sleeps when idle; ping `/health` every ~10 min (UptimeRobot) to keep it awake.

Local dev: backend on :8000, `npm run dev` on :5173 (Vite proxies `/chat` to the backend).
