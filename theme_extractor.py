import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_podcast_theme(transcript: str) -> str:
    """
    Extracts the main theme of a podcast from its transcript.

    Parameters:
    transcript (str): The transcript of the podcast.

    Returns:
    str: The main theme of the podcast.
    """
    threshold = int(len(transcript)/5)
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant that identifies the main theme of a podcast."},
            {"role": "user", "content": f"Extract the main theme of this podcast: {transcript[:threshold]}. It should be less than 5 words."}
        ]
    )
    theme = response['choices'][0]['message']['content'].strip()
    return theme