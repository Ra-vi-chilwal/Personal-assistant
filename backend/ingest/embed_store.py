import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pymongo import MongoClient

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
mongo = MongoClient(os.getenv("MONGODB_URI"))
collection = mongo["rag_db"]["chunks"]

BATCH_SIZE = 50


def embed_batch(texts, retries=3):
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
            wait = 30 * (attempt + 1)
            print(f"  Error: {e}")
            print(f"  {wait}s ruk ke dobara try...")
            time.sleep(wait)

    raise Exception("Saare retries fail ho gaye")


with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("Chunks loaded:", len(chunks))

collection.delete_many({})

for start in range(0, len(chunks), BATCH_SIZE):
    batch = chunks[start:start + BATCH_SIZE]
    texts = [c["text"] for c in batch]

    vectors = embed_batch(texts)

    docs = []
    for chunk, vec in zip(batch, vectors):
        doc = dict(chunk)
        doc["embedding"] = vec
        docs.append(doc)

    collection.insert_many(docs)
    print(f"Batch {start // BATCH_SIZE + 1}: {len(docs)} chunks saved")

    time.sleep(5)

print("Total in DB:", collection.count_documents({}))