# JobHunt AI - Resume & Interview Agent 🚀

**Student Name**: MUNAGALA CHANDRA VAMSI REDDY
**Project Link**: https://job-hunt-kg8qdo2yz-vamsireddy143rs-projects.vercel.app/
**Loom Video**: https://www.loom.com/share/0fec5d9ca0de48feb963ec3b01f1d358

## 📌 Project Overview
**JobHunt AI** is a full-stack Generative AI application designed to solve the painful "black box" problem of job hunting. It uses **Pydantic AI** to act as a personalized Career Coach.

### 💡 Problem Solved
Students and job seekers often apply to hundreds of jobs without understanding why they get rejected. They lack feedback on their resume's relevance to specific JDs and fail to prepare for technical interviews.

### ✨ Key Features
1.  **Smart Resume Scanner**: Instantly scores your resume against a target Job Description (0-100%).
2.  **Gap Analysis**: Identifies missing "Hard Skills" and keywords that ATS bots look for.
3.  **Tailored Rewrites**: Uses AI to re-write your bullet points to better match the job.
4.  **AI Mock Interview**: Generates 3-5 challenging, role-specific interview questions based on your actual gaps.

---

## 🛠️ Technical Stack
*   **Frontend**: React, Vite, TailwindCSS (Glassmorphism UI)
*   **Backend**: Python FastAPI
*   **AI Engine**: Pydantic AI (Structured Output & Validation)
*   **Model**: OpenRouter (Google Gemini 2.0 Flash / Llama 3)
*   **Deployment**: Vercel (Client) + Render (Server)

---

## 🚀 How to Run Locally

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/your-username/jobhunt-ai.git
    cd jobhunt-ai
    ```

2.  **One-Click Start (Windows)**:
    *   Double-click `start_app.bat`
    *   *Or manually:*
        *   Backend: `cd server && pip install -r requirements.txt && uvicorn main:app --reload`
        *   Frontend: `cd client && npm install && npm run dev`

3.  **Environment Variables**:
    *   Create `server/.env` and add:
        ```
        OPENROUTER_API_KEY=sk-or-your-key-here
        ```

---
