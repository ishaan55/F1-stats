from google import genai
from google.genai import types
from dotenv import load_dotenv
import re
import json

import fastf1
fastf1.Cache.enable_cache('cache/') 

# Gemini
load_dotenv()
client = genai.Client()
def extract_gp_info(input_text: str) -> dict:
    system = f"""
    You are an assistant that extracts structured data from natural language queries about Formula 1 races.

    Given a sentence -

    Extract:
    - The **year** (as a four-digit integer, e.g., 2021).
    - The **event name**, which should be either the **city** (e.g., "Silverstone", "Monza") or **country** (e.g., "Italy", "Austria") where the race is held.

    Ensure:
    - Spelling is correct and standardized (no typos or abbreviations).
    - The year is a valid F1 season (e.g., between 2000 and the current year).
    - The output is compatible with the FastF1 API, where the event name is used to match race sessions.

    Respond **only** with a JSON object in this format (no extra explanation or text):

    {{
      "event": "Event Name", 
      "year": 2021
    }}
    """

    try:
        res = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=system
            ),
            contents=input_text
        )
        # Use regex to extract JSON from the response text
        match = re.search(r'\{[\s\S]*?\}', res.text)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print(f"[LLM Parsing Error] {e}")
        return None

# Fastf1
def analysis(year: int, event: str):
    try:
        # Load the session data
        session = fastf1.get_session(year, event, 'R')
        session.load(weather=False, telemetry=False)
        
        # top3
        top3 = session.results.iloc[:3].loc[:, ["Abbreviation", "TeamColor"]].to_dict(orient="records")
        return top3
        
    except Exception as e:
        print(f"[FastF1 Error] {e}")
        return None


if __name__ == "__main__":
    input_text = "Austria grand prix 2025"
    print(extract_gp_info(input_text))
