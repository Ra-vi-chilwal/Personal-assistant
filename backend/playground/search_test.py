import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pymongo import MongoClient

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
collection = MongoClient(os.getenv("MONGODB_URI"))["rag_db"]["chunks"]
question = "How do I upsert records using Bulk API 2.0?"

result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question,
    config=types.EmbedContentConfig(
        output_dimensionality=768,
        task_type="RETRIEVAL_QUERY",
    ),
)
query_vector = result.embeddings[0].values

pipeline = [
    {
        "$vectorSearch": {
            "index": "vector_index",
            "path": "embedding",
            "queryVector": query_vector,
            "numCandidates": 100,
            "limit": 5,
        }
    },
    {
        "$project": {
            "_id": 0,
            "text": 1,
            "page": 1,
            "printed_page": 1,
            "section": 1,
            "score": {"$meta": "vectorSearchScore"},
        }
    },
]

results = list(collection.aggregate(pipeline))
print("Results found:", len(results))

MIN_SCORE = 0.75

good = [r for r in results if r["score"] >= MIN_SCORE]

print("Top score:", round(results[0]["score"], 4) if results else None)
print("Good results:", len(good))

if not good:
    print("\nSorry, iska jawab docs mein nahi mila.")
else:
    for r in good:
        print("\n" + "=" * 60)
        print(f"Score: {r['score']:.4f} | Section: {r['section']} | Page: {r['printed_page']}")
        print(r["text"][:200])