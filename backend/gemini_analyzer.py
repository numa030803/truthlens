from google import genai
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_news(text):
    prompt = f"""
    You are TruthLens, an expert fact-checking AI.
    Analyze this news content for credibility:
    "{text}"
    Respond ONLY in this exact JSON, no extra text:
    {{
        "verdict": "Real or Fake or Unverified",
        "score": 0,
        "reasoning": "your reasoning here",
        "red_flags": ["flag1"],
        "positive_signals": ["signal1"],
        "category": "Politics/Health/Science/Finance/Other"
    }}
    """
    try:
        response = client.models.generate_content(
           model="gemini-2.5-flash",
            contents=prompt
        )
        raw = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(raw)
    except Exception as e:
        print("ERROR:", e)
        return {
            "verdict": "Unverified",
            "score": 50,
            "reasoning": "Could not analyze.",
            "red_flags": [],
            "positive_signals": [],
            "category": "Other"
        }

if __name__ == "__main__":
    result = analyze_news("Drinking hot water cures cancer instantly")
    print(result)