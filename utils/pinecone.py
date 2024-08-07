import os
from typing import List
from pinecone import Pinecone

pc = Pinecone(api_key = os.getenv("PINECONE_API_KEY"))


INDEX_NAME = {
    "prod": os.getenv("PINECONE_PROD_INDEX"),
    "dev": os.getenv("PINECONE_DEV_INDEX")
}

index = pc.Index(INDEX_NAME[os.getenv("ENV")])

def push_vectors(embedding: List[float], metadata: any):
    vector_id = metadata.get('id', None)

    return index.upsert(
        vectors=[
            {
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            }
        ]
    )

def find_vectors(embedding: List[float], user_id: str):
    results = index.query(
        vector=embedding,
        top_k=3,
        include_metadata=True,
        include_values=False,
        filter={
            "id": {
                "$ne": user_id
            }
        
        }
    )
    return results