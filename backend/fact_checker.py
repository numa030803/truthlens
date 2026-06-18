import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_fact_checks(query: str) -> list:
    try:
        api_key = os.getenv("FACT_CHECK_API_KEY")
        url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
        params = {
            "query": query[:100],
            "key": api_key,
            "languageCode": "en"
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        results = []
        for claim in data.get("claims", [])[:3]:
            review = claim.get("claimReview", [{}])[0]
            results.append({
                "title": claim.get("text", ""),
                "url": review.get("url", ""),
                "publisher": review.get("publisher", {}).get("name", ""),
                "rating": review.get("textualRating", "")
            })
        return results
    except Exception as e:
        print("Fact check error:", e)
        return []

if __name__ == "__main__":
    results = get_fact_checks("drinking hot water cures cancer")
    print(results)
    