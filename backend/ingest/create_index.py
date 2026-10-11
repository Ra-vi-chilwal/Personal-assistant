import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.operations import SearchIndexModel

load_dotenv()
mongo = MongoClient(os.getenv("MONGODB_URI"))
collection = mongo["rag_db"]["chunks"]

index_model = SearchIndexModel(
    name="vector_index",
    type="vectorSearch",
    definition={
        "fields": [
            {
                "type": "vector",
                "path": "embedding",
                "numDimensions": 768,
                "similarity": "cosine",
            },
            {
                "type": "filter",
                "path": "chapter",
            },
        ]
    },
)

collection.create_search_index(model=index_model)
print("Index create request bhej di. Build hone mein 1-2 minute lagenge.")