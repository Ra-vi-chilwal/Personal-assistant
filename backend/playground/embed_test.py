import os 
from dotenv import load_dotenv
from google import genai
from google.genai import types        
import numpy as np       # NEW (upar imports ke saath)
load_dotenv()


api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)


sentences = [
    "How to insert records in bulk?",
    "Bulk data loading in Salesforce",
    "How to make biryani?",
]

result = client.models.embed_content(
    model = 'gemini-embedding-001',
    contents=sentences,
    config=types.EmbedContentConfig(output_dimensionality=768),
)

vector = result.embeddings[0]
print("Total vectors:",vector, len(result.embeddings))
for i, emb in enumerate(result.embeddings):
    print(sentences[i], "->", len(emb.values), "numbers")  
