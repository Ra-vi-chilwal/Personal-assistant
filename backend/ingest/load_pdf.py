import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("data/chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("Chunks loaded:", len(chunks))

test_batch = chunks[:5]
texts = [c["text"] for c in test_batch]

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=texts,
    config=types.EmbedContentConfig(
        output_dimensionality=768,
        task_type="RETRIEVAL_DOCUMENT",
    ),
)

print("Embeddings received:", len(result.embeddings))