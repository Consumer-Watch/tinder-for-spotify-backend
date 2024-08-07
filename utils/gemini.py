import os
import google.generativeai as genai

apiKey = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=apiKey)


generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="Do not present answers in bullet points or enumaeration, separate each person into a different section and start the section title with their name. Do not use complicated words, just narrate what the person likes and how the current user can connect with them based on my music taste. list any shared artists or genres we might have to improve your answer. Let your narration be in a more personal description, as though both users should be friends. try to switch it up for each person, don't let each person be presented in the same way .",
    generation_config=generation_config,
)

def ask_gemini(json_data: any, current_user: any):
    result = model.generate_content(
        f''' 
        Given a JSON response from an API containing id, spotify_username, country, city, artists, likes (genres), name, and email, provide a detailed analysis on the following: all info of a specific user, the count of people with similar tastes, and methods to connect with individuals who share similar music preferences. Present the findings in a detailed manner as a data scientist and music expert
        Give responses that don’t contain enumeration and unnecessary information
        {json_data}

        Current User: {current_user}
        ''',
    )
    return result.text