import os
import asyncio
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from schemas import AnalysisRequest, AnalysisResult, SkillGap, TailoredPoint
from pydantic_ai.models.openai import OpenAIModel

# Check API Key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set")

# Configure OpenAI (OpenRouter) via Env Vars to avoid Constructor Issues
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

# Configure the model (Switched to Llama 3.3 70B Free - More Reliable)
model = OpenAIModel('meta-llama/llama-3.3-70b-instruct:free')

# Configure the agent
agent = Agent(
    model,
    system_prompt=(
        "You are an expert Technical Recruiter and Career Coach. "
        "Your goal is to help a candidate land a job by analyzing their resume against a job description. "
        "Be critical but constructive. "
        "You must respond with a valid JSON object matching the following structure:\n"
        "{\n"
        '  "match_score": 0-100,\n'
        '  "summary": "Brief summary of the analysis",\n'
        '  "missing_keywords": ["kw1", "kw2"],\n'
        '  "tailored_suggestions": [{"original": "text", "improved": "text", "reason": "why"}],\n'
        '  "interview_questions": ["q1", "q2"]\n'
        "}\n"
        "Return ONLY the JSON. No preamble."
    ),
)

async def analyze_job_match(resume_text: str, jd_text: str) -> AnalysisResult:
    prompt = f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd_text}"
    
    # Run the agent (Text Mode)
    result = await agent.run(prompt)
    
    # DEBUG: Inspect the result object to fix the AttributeError
    print("DEBUG: Agent Run Successful.")
    print(f"DEBUG: Result Type: {type(result)}")
    print(f"DEBUG: Result Dir: {dir(result)}")
    
    # Robust extraction of text
    cleaned_json = ""
    if hasattr(result, 'data'):
        cleaned_json = result.data
    elif hasattr(result, 'output'): # Found via debugging
        cleaned_json = result.output
    elif hasattr(result, 'content'):
        cleaned_json = result.content
    elif hasattr(result, 'return_values'): 
        cleaned_json = result.return_values[0]
    else:
        # Fallback: hope the string representation is the text
        print("DEBUG: Could not find .data or .content. Using str(result).")
        cleaned_json = str(result)

    # Clean and Parse JSON manually
    cleaned_json = str(cleaned_json).strip()
    if cleaned_json.startswith("```json"):
        cleaned_json = cleaned_json.split("```json")[1].split("```")[0].strip()
    elif cleaned_json.startswith("```"):
         cleaned_json = cleaned_json.split("```")[1].split("```")[0].strip()
         
    return AnalysisResult.model_validate_json(cleaned_json)
