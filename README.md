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

## Deploy
- Backend: any Python host (Render, Railway, ...). Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Set the three env vars. Restrict `allow_origins` in `app/main.py` to your frontend domain.
- Frontend: Vercel/Netlify, build `npm run build`, output `dist`, env `VITE_API_URL=<your backend URL>`.
