import os
import asyncio
from pydantic_ai import Agent
from dotenv import load_dotenv
from schemas import AnalysisResult
from pydantic_ai.models.openai import OpenAIModel

# Load environment variables
load_dotenv()

# Check API Key
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set")

# Configure OpenAI (OpenRouter) via Env Vars
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_BASE_URL"] = "https://openrouter.ai/api/v1"

import re

# MULTI-MODEL FALLBACK LIST
# Switching to DeepSeek & Qwen (Newest Free Providers) to avoid Llama 402/429 blocks
MODELS_TO_TRY = [
    'deepseek/deepseek-r1-distill-llama-70b:free', # High Intelligence, Free
    'qwen/qwen-2.5-72b-instruct:free',            # Very Stable, Free
    'meta-llama/llama-3.1-8b-instruct:free',       # Old Reliable Backup
]

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

async def analyze_job_match(resume_text: str, jd_text: str) -> AnalysisResult:
    prompt = f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd_text}"
    last_exception = None

    print(f"DEBUG: Starting Analysis. Models available: {len(MODELS_TO_TRY)}")

    for model_name in MODELS_TO_TRY:
        print(f"DEBUG: Trying Model -> {model_name} ...")
        try:
            # Initialize Agent with specific model
            model = OpenAIModel(model_name)
            agent = Agent(model, system_prompt=SYSTEM_PROMPT)
            
            # Run Agent
            result = await agent.run(prompt)
            
            # If we get here, it worked!
            print(f"DEBUG: Success with {model_name}!")
            return parse_result(result)
            
        except Exception as e:
            print(f"DEBUG: Failed with {model_name}. Error: {str(e)}")
            last_exception = e
            # Wait a bit before hitting the next one
            await asyncio.sleep(1)
            # Continue to next model loop...

    # If all fail
    print("CRITICAL: All models failed.")
    raise last_exception or Exception("All AI models failed to respond.")

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
