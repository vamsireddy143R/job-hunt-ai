# JobHunt AI - Resume & Interview Agent 🚀

**Student Name**: [Your Name]
**Project Link**: [Your Vercel URL]
**Loom Video**: [Your Loom Link]

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

## 🌐 Deployment Instructions

### 1. Backend (Render.com)
1.  Push code to GitHub.
2.  New "Web Service" -> Connect Repo.
3.  **Root Directory**: `server`
4.  **Build Command**: `pip install -r requirements.txt`
5.  **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6.  **Environment Variables**: Add `OPENROUTER_API_KEY`.

### 2. Frontend (Vercel)
1.  New Project -> Connect Repo.
2.  **Root Directory**: `client`
3.  **Build Command**: `npm run build`
4.  **Install Command**: `npm install`
5.  Deploy! 🚀
