import os
import google.generativeai as genai

apiKey = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=apiKey)

def create_embeddings(text: str):
    result = genai.embed_content(
        model="models/text-embedding-004", 
        content=text,
        task_type="semantic_similarity",
    )

    return result['embedding']

