from datetime import datetime

import json
from openai import OpenAI
import os
from typing import Dict, Any

async def markdown_to_json(markdown_content: str):
    """
    Convert markdown content to JSON using Claude 3.5 API
    
    Args:
        markdown_content (str): The markdown content to convert
        
    Returns:
        Result: Contains the extracted Vacancy data and status information
    """
    try:
        # Initialize the Anthropic client
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
        )



        # Prepare the prompt
        prompt = """Extract a list of items from the text into a JSON array with 'title', 'startDate', 'endDate', 'eventType', 'urlToEvent' and 'description' fields. 
        make sure that the date is in the format ISO 8601 YYYY-MM-DDTHH:MM:SSZ. and that the url to the event is a real url.
        Provide the output in valid JSON format matching this structure:
        [{
            "title": "Charlie & The Welfare",
            "description": "Rock",
            "startDate": "2025-01-26T00:00:00Z",
            "endDate": "2025-01-26T23:59:59Z",
            "eventType": "Music",
            "urlToEvent": "https://cafelievense.nl/charlie-the-welfare/"
        },
        {
            "title": "Jamsessie",
            "description": "Jam session",
            "startDate": "2025-01-29T20:30:00Z",
            "endDate": "2025-01-29T23:59:59Z",
            "eventType": "Jam",
            "urlToEvent": "https://cafelievense.nl/jamsessie-3/"
        }]
        
        Here's the content to analyze:
        
        """ + markdown_content


        message = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o",
        )

        # Extract the JSON response - updated to handle the new response format
        response_content = message.choices[0].message.content


        # Find the JSON content between ```json and ``` markers
        json_start = response_content.find('```json\n') + 7  # Skip past ```json\n
        json_end = response_content.find('```', json_start)
        json_str = response_content[json_start:json_end].strip()
        
        # Parse the JSON
        data = json.loads(json_str)

        return data

    except Exception as e:
        print(f"Error in markdown_to_json: {e}")
        return None

