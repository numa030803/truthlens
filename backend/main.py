from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from gemini_analyzer import analyze_news
from fact_checker import get_fact_checks
from scraper import extract_from_url

app = FastAPI(title="TruthLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

class URLInput(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"status": "TruthLens API is running ✅"}

@app.post("/analyze/text")
async def analyze_text(input: TextInput):
    if not input.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    analysis = analyze_news(input.text)
    fact_checks = get_fact_checks(input.text[:100])
    return {"analysis": analysis, "fact_checks": fact_checks}

@app.post("/analyze/url")
async def analyze_url(input: URLInput):
    text = extract_from_url(input.url)
    analysis = analyze_news(text)
    fact_checks = get_fact_checks(text[:100])
    return {"analysis": analysis, "fact_checks": fact_checks}