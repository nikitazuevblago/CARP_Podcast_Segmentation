import os
import asyncio
import os
from theme_extractor import extract_podcast_theme
from dotenv import load_dotenv
import openai
import pandas as pd
import pickle
load_dotenv()

# Set up your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")



async def classify_text(input_text, podcast_theme, model="gpt-3.5-turbo-instruct", max_retries=5, initial_delay=0.2):
    # Retry mechanism for each step in case of RateLimitError
    async def request_with_retry(prompt, max_tokens, temperature):
        for attempt in range(max_retries):
            try:
                response = await openai.ChatCompletion.acreate(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message['content'].strip()
            except openai.error.RateLimitError:
                if attempt == max_retries - 1:
                    raise  # Re-raise if max retries reached
                delay = initial_delay * (2 ** attempt)  # Exponential backoff
                print(f"Rate limit hit, retrying in {delay:.2f} seconds...")
                await asyncio.sleep(delay)

    # Step 1: Identify Clues
    clues_prompt = (
        "This is a classifier that determines whether a sentence relates to the theme of a podcast.\n"
        f"Podcast Theme: {podcast_theme}\n"
        "First, list CLUES (e.g., keywords, phrases, contextual information, semantic relations, "
        "semantic meaning, tones, references) that support the determination of whether the input sentence relates to the podcast theme.\n"
        f"Input: {input_text}\n"
        "Clues:"
    )
    clues = await request_with_retry(clues_prompt, max_tokens=100, temperature=0.7)

    # Step 2: Diagnostic Reasoning
    reasoning_prompt = (
        "Based on the input and clues, deduce the diagnostic reasoning process from premises "
        "(i.e., clues and input) that supports the determination of whether the input sentence relates to the podcast theme.\n"
        f"Podcast Theme: {podcast_theme}\n"
        f"Input: {input_text}\n"
        f"Clues: {clues}\n"
        "Reasoning:"
    )
    reasoning = await request_with_retry(reasoning_prompt, max_tokens=130, temperature=0.7)

    # Step 3: Final Classification
    classification_prompt = (
        "Considering the clues and reasoning, determine whether the sentence relates to the podcast theme. "
        "Answer with YES or NO.\n"
        f"Podcast Theme: {podcast_theme}\n"
        f"Input: {input_text}\n"
        f"Clues: {clues}\n"
        f"Reasoning: {reasoning}\n"
        "Classification:"
    )
    response_text = await request_with_retry(classification_prompt, max_tokens=10, temperature=0.0)

    # Determine final classification based on response
    try:
        response_text = response_text.lower()
        if "yes" in response_text:
            classification = 1  # Relates to the podcast theme
        elif "no" in response_text:
            classification = 0   # Does not relate to the podcast theme
        else:
            print(f"Unrecognized response: {response_text}")
            classification = None
    except Exception as e:
        print(f"Error: {e}")
        classification = None

    return {
        'input_text': input_text,
        'classification': classification,
        'clues': clues,
        'reasoning': reasoning
    }

async def classify_texts_async(input_texts, podcast_theme, model="gpt-4o-mini", max_concurrent_requests=5):
    semaphore = asyncio.Semaphore(max_concurrent_requests)  # Limit concurrent requests

    async def classify_with_semaphore(text):
        async with semaphore:  # Ensure that only a limited number of requests run concurrently
            return await classify_text(text, podcast_theme, model)

    tasks = [classify_with_semaphore(text) for text in input_texts]
    return await asyncio.gather(*tasks)
