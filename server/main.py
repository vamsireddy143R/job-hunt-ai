from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import analyze_job_match
from schemas import AnalysisResult
import uvicorn
import os
import io
from pypdf import PdfReader

app = FastAPI(title="JobHunt AI API")

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "JobHunt AI Server is Running"}

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_resume(
    resume_file: UploadFile = File(None),
    resume_text: str = Form(None),
    job_description_file: UploadFile = File(None),
    job_description: str = Form(None)
):
    try:
        final_resume_text = ""
        final_jd_text = ""
        
        # Handle Resume PDF
        if resume_file:
            content = await resume_file.read()
            reader = PdfReader(io.BytesIO(content))
            for page in reader.pages:
                final_resume_text += page.extract_text() + "\n"
        elif resume_text:
            final_resume_text = resume_text
        else:
            raise HTTPException(status_code=400, detail="Please upload a PDF resume or provide text.")

        # Handle JD PDF
        if job_description_file:
            content = await job_description_file.read()
            reader = PdfReader(io.BytesIO(content))
            for page in reader.pages:
                final_jd_text += page.extract_text() + "\n"
        elif job_description:
            final_jd_text = job_description
        else:
            raise HTTPException(status_code=400, detail="Please upload a JD PDF or provide text.")

        if not final_resume_text.strip():
             raise HTTPException(status_code=400, detail="Could not extract text from the resume.")
             
        if not final_jd_text.strip():
             raise HTTPException(status_code=400, detail="Could not extract text from the job description.")

        result = await analyze_job_match(final_resume_text, final_jd_text)
        return result
    except Exception as e:
        import traceback
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("CRITICAL SERVER ERROR:")
        traceback.print_exc()
        print(f"Error Message: {str(e)}")
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
