"""Chunk every (non-excluded) PDF in data/, embed the chunks and replace the contents of rag_db.chunks.

Run from the backend folder:  python ingest/ingest_pdfs.py
"""
import hashlib
import json
import os
import re
import time
from pathlib import Path

import pymupdf
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pymongo import MongoClient

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
collection = MongoClient(os.getenv("MONGODB_URI"))["rag_db"]["chunks"]

DATA_DIR = Path("data")
CHUNK_CHARS = 800
OVERLAP_CHARS = 120
MIN_CHARS = 40
BATCH_SIZE = 10
CACHE_FILE = DATA_DIR / ".embed_cache.json"  # survives quota errors; re-runs only embed what is missing

# Files here are NOT ingested (the portfolio chatbot is public, so keep private documents out).
EXCLUDE = ()


def source_name(path):
    return re.sub(r"(\.pdf)+$", "", path.name, flags=re.I)


def split_text(text):
    """Split page text into ~CHUNK_CHARS pieces on paragraph/line boundaries, with a small overlap."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) <= CHUNK_CHARS:
        return [text] if len(text) >= MIN_CHARS else []

    pieces, current = [], ""
    for para in re.split(r"\n\s*\n|\n(?=[-•●▪\d]+[.)]?\s)", text):
        para = para.strip()
        if not para:
            continue
        # hard-split a single oversized paragraph
        while len(para) > CHUNK_CHARS:
            cut = para.rfind(". ", 0, CHUNK_CHARS)
            cut = cut + 1 if cut > CHUNK_CHARS // 2 else CHUNK_CHARS
            pieces.append(para[:cut].strip())
            para = para[cut:].strip()
        if current and len(current) + len(para) + 2 > CHUNK_CHARS:
            pieces.append(current)
            current = current[-OVERLAP_CHARS:].split(" ", 1)[-1] + "\n\n" + para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current:
        pieces.append(current)
    return [p for p in pieces if len(p) >= MIN_CHARS]


def toc_lookup(doc):
    toc = doc.get_toc()  # [level, title, page]

    def lookup(page):
        section = chapter = None
        for level, title, p in toc:
            if p > page:
                break
            section = title
            if level == 1:
                chapter = title
        return section, chapter

    return lookup


def chunk_pdf(path):
    doc = pymupdf.open(path)
    lookup = toc_lookup(doc)
    name = source_name(path)
    chunks = []
    for i, page in enumerate(doc, start=1):
        section, chapter = lookup(i)
        for text in split_text(page.get_text()):
            chunks.append(
                {
                    "text": text,
                    "source": name,
                    "page": i,
                    "printed_page": i,
                    "section": section or name,
                    "chapter": chapter or name,
                }
            )
    return chunks


def chunk_qa(path):
    """data/custom_qa.md: one chunk per 'Q: ... A: ...' block (blocks start at a line beginning with 'Q:')."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)  # allow HTML comments for instructions
    chapter = "Friends" if "friends" in path.name.lower() else "Custom Q&A"
    chunks = []
    for block in re.split(r"(?m)^(?=Q:)", text):
        block = block.strip()
        if not block.startswith("Q:") or "A:" not in block:
            continue
        question = block[2 : block.index("A:")].strip()
        chunks.append(
            {"text": block, "source": chapter, "page": 1, "printed_page": 1, "section": question, "chapter": chapter}
        )
    return chunks


def embed_batch(texts, retries=4):
    for attempt in range(retries):
        try:
            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=texts,
                config=types.EmbedContentConfig(
                    output_dimensionality=768,
                    task_type="RETRIEVAL_DOCUMENT",
                ),
            )
            return [e.values for e in result.embeddings]
        except Exception as e:
            if "PerDay" in str(e):
                raise SystemExit("Daily Gemini embedding quota is used up. Progress is cached; re-run after it resets.")
            wait = 30 * (attempt + 1)
            print(f"  Error: {e}\n  retrying in {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Embedding failed after all retries")


def main():
    chunks = []
    for pdf in sorted(DATA_DIR.glob("*.pdf")):
        if any(x in pdf.name.lower() for x in EXCLUDE):
            print(f"{pdf.name}: skipped (excluded)")
            continue
        got = chunk_pdf(pdf)
        print(f"{pdf.name}: {len(got)} chunks")
        chunks.extend(got)

    for qa in sorted(DATA_DIR.glob("*qa*.md")):
        got = chunk_qa(qa)
        print(f"{qa.name}: {len(got)} Q&A chunks")
        chunks.extend(got)

    (DATA_DIR / "chunks.json").write_text(json.dumps(chunks, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Total chunks:", len(chunks))

    # embed everything first (cached on disk) so a failure doesn't leave the DB empty
    cache = json.loads(CACHE_FILE.read_text()) if CACHE_FILE.exists() else {}
    key = lambda c: hashlib.sha1(c["text"].encode()).hexdigest()
    todo = [c for c in chunks if key(c) not in cache]
    print(f"{len(chunks) - len(todo)} cached, {len(todo)} to embed")
    for start in range(0, len(todo), BATCH_SIZE):
        batch = todo[start : start + BATCH_SIZE]
        try:
            vectors = embed_batch([c["text"] for c in batch])
        finally:
            CACHE_FILE.write_text(json.dumps(cache))
        cache.update({key(c): v for c, v in zip(batch, vectors)})
        CACHE_FILE.write_text(json.dumps(cache))
        print(f"Embedded {len(chunks) - len(todo) + start + len(batch)}/{len(chunks)}")
        time.sleep(2)

    docs = [{**c, "embedding": cache[key(c)]} for c in chunks]

    collection.delete_many({})
    collection.insert_many(docs)
    print("Total in DB:", collection.count_documents({}))


if __name__ == "__main__":
    main()
