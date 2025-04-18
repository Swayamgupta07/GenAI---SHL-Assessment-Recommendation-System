from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

class QueryInput(BaseModel):
    query: str

class AssessmentOutput(BaseModel):
    Assessment_Name: str
    URL: str
    Remote_Testing_Support: str
    Adaptive_IRT_Support: str
    Duration: int
    Test_Type: List[str]

class RecommendResponse(BaseModel):
    recommended_assessments: List[AssessmentOutput]

@app.get("/health")
def health_check():
    return {"status": "healthy"}

def extract_valid_json(text):
    try:
        match = re.search(r'\[\s*{.*?}\s*]', text, re.DOTALL)
        if match:
            data = json.loads(match.group())
            validated = []
            for item in data:
                if all(k in item for k in [
                    "Assessment Name", "URL", "Remote Testing Support",
                    "Adaptive/IRT Support", "Duration", "Test Type"
                ]):
                    duration_match = re.search(r'\d+', str(item["Duration"]))
                    duration = int(duration_match.group()) if duration_match else 0

                    validated.append(AssessmentOutput(
                        Assessment_Name=item["Assessment Name"],
                        URL=item["URL"],
                        Remote_Testing_Support=item["Remote Testing Support"],
                        Adaptive_IRT_Support=item["Adaptive/IRT Support"],
                        Duration=duration,
                        Test_Type=item["Test Type"] if isinstance(item["Test Type"], list) else [item["Test Type"]]
                    ))
            return validated[:10]
    except Exception as e:
        print("Error extracting JSON:", e)
    return []

@app.post("/recommend", response_model=RecommendResponse)
def recommend_assessments(input: QueryInput):
    if not input.query or not input.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    prompt = (
        "You are a helpful assistant. Based on the following job description, recommend up to 10 relevant SHL assessments.\n\n"
        f"{input.query.strip()}\n\n"
        "Your response MUST be a valid JSON list. Each object in the list should have the following fields:\n"
        "- Assessment Name (string)\n"
        "- URL (valid SHL URL)\n"
        "- Remote Testing Support (Yes/No)\n"
        "- Adaptive/IRT Support (Yes/No)\n"
        "- Duration (e.g., '45 mins')\n"
        "- Test Type (list of strings)\n\n"
        "Respond ONLY with a valid JSON array in this exact format."
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        assessments = extract_valid_json(response.text)

        if not assessments:
            raise HTTPException(status_code=500, detail="No valid recommendations were generated.")
        
        return {"recommended_assessments": assessments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")
