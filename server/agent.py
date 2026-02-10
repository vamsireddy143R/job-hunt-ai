import os
import asyncio
import re
from pydantic_ai import Agent
from dotenv import load_dotenv
from schemas import AnalysisResult
from pydantic_ai.models.gemini import GeminiModel

# Load environment variables
load_dotenv()

# Check API Key
api_key = os.getenv("OPENROUTER_API_KEY") # We keep the env var name for compatibility, but it holds the Google Key now
if not api_key:
    raise ValueError("API Key is missing. Please check OPENROUTER_API_KEY in Render.")

import google.generativeai as genai

# Configure GenAI Native Client
genai.configure(api_key=api_key)

SYSTEM_PROMPT = (
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
)

def get_best_model_name():
    """Dynamically find the best available Gemini model to avoid 404s."""
    print("DEBUG: Listing available Google Models...")
    try:
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        print(f"DEBUG: Found models: {available_models}")
        
        # Priority List
        priorities = [
            'models/gemini-1.5-flash',
            'models/gemini-1.5-flash-001',
            'models/gemini-1.5-pro',
            'models/gemini-1.5-pro-001',
            'models/gemini-pro',
            'models/gemini-1.0-pro'
        ]
        
        for p in priorities:
            if p in available_models:
                print(f"DEBUG: Selected specific model: {p}")
                return p # Return full 'models/...' string which is safer
        
        # Fallback: any gemini model
        for m in available_models:
            if 'gemini' in m:
                print(f"DEBUG: Selected fallback model: {m}")
                return m
                
        return 'gemini-1.5-flash' # Absolute fallback

    except Exception as e:
        print(f"DEBUG: Model listing failed ({e}). Defaulting to gemini-1.5-flash")
        return 'gemini-1.5-flash'

async def analyze_job_match(resume_text: str, jd_text: str) -> AnalysisResult:
    prompt = f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd_text}"
    
    # 1. auto-detect model
    model_name = get_best_model_name()
    # Strip 'models/' prefix if pydantic-ai adds it automatically (it often does)
    # But genai.list_models returns 'models/foo'. Pydantic usually expects just 'foo' or 'models/foo'.
    # Let's try passing the clean name.
    clean_model_name = model_name.replace('models/', '')
    
    print(f"DEBUG: Initializing Agent with {clean_model_name}...")
    
    try:
        # Set GEMINI_API_KEY environment variable for pydantic-ai
        os.environ["GEMINI_API_KEY"] = api_key
        model = GeminiModel(clean_model_name)
        agent = Agent(model, system_prompt=SYSTEM_PROMPT)
        
        # Run Agent
        result = await agent.run(prompt)
        print("DEBUG: Agent Run Successful.")
        return parse_result(result)
        
    except Exception as e:
        print(f"CRITICAL: Agent failed. Error: {str(e)}")
        raise e

def parse_result(result):
    """Helper to safely extract JSON from Agent result"""
    cleaned_json = ""
    if hasattr(result, 'data'):
        cleaned_json = result.data
    elif hasattr(result, 'output'):
        cleaned_json = result.output
    elif hasattr(result, 'content'):
        cleaned_json = result.content
    elif hasattr(result, 'return_values') and result.return_values: 
        cleaned_json = result.return_values[0]
    else:
        cleaned_json = str(result)

    cleaned_json = str(cleaned_json).strip()
    
    # Remove DeepSeek <think> tags if present
    cleaned_json = re.sub(r'<think>.*?</think>', '', cleaned_json, flags=re.DOTALL).strip()

    # Parse Markdown Code Blocks
    if cleaned_json.startswith("```json"):
        cleaned_json = cleaned_json.split("```json")[1].split("```")[0].strip()
    elif cleaned_json.startswith("```"):
         cleaned_json = cleaned_json.split("```")[1].split("```")[0].strip()
         
    return AnalysisResult.model_validate_json(cleaned_json)
