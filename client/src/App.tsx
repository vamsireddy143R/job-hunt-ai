import { useState } from 'react';
import axios from 'axios';
import { FileText, Bot, AlertTriangle, Loader2, Sparkles, BrainCircuit, Target, X, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

// Types matching Backend
interface AnalysisResult {
  match_score: number;
  summary: string;
  missing_keywords: string[];
  tailored_suggestions: { original: string; improved: string; reason: string }[];
  interview_questions: string[];
}

function App() {
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [jdFile, setJdFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AnalysisResult | null>(null);

  const handleAnalyze = async () => {
    if (!resumeFile || !jdFile) return;
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('resume_file', resumeFile);
      formData.append('job_description_file', jdFile);

      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const response = await axios.post(`${apiUrl}/analyze`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(response.data);
    } catch (error: any) {
      console.error(error);
      alert("Analysis Failed. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const clearAll = () => {
    setResumeFile(null);
    setJdFile(null);
    setResult(null);
  };

  // Radial Progress Component
  const RadialProgress = ({ score }: { score: number }) => {
    const radius = 60;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (score / 100) * circumference;

    return (
      <div className="relative flex items-center justify-center w-40 h-40">
        <svg className="w-full h-full transform -rotate-90">
          <circle cx="80" cy="80" r={radius} stroke="rgba(255,255,255,0.1)" strokeWidth="12" fill="transparent" />
          <motion.circle
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            cx="80" cy="80" r={radius}
            stroke={score > 75 ? "#10b981" : "#f59e0b"}
            strokeWidth="12"
            fill="transparent"
            strokeDasharray={circumference}
            strokeLinecap="round"
          />
        </svg>
        <div className="absolute flex flex-col items-center">
          <span className="text-4xl font-bold font-display text-white">{score}%</span>
          <span className="text-xs text-slate-400 uppercase tracking-widest mt-1">Match</span>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white font-sans selection:bg-cyan-500/30 overflow-x-hidden relative">

      {/* GLOBAL BACKGROUND */}
      <div className="fixed inset-0 z-0">
        <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-cyan-500/10 rounded-full blur-[150px] animate-pulse" style={{ animationDuration: '8s' }} />
        <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-500/10 rounded-full blur-[150px] animate-pulse" style={{ animationDuration: '10s' }} />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 py-8">

        {/* HEADER */}
        <header className="flex justify-between items-center mb-12">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-cyan-500 to-purple-600 rounded-lg">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-2xl font-bold font-display tracking-tight">JobHunt <span className="text-cyan-400">AI</span></h1>
          </div>
          <div className="flex gap-4">
            {/* Status Indicators could go here */}
          </div>
        </header>

        <main className="grid grid-cols-1 lg:grid-cols-12 gap-8">

          {/* LEFT: INPUT PANEL */}
          <div className={`lg:col-span-5 space-y-6 transition-all duration-500 ${result ? 'lg:col-span-4' : 'lg:col-span-12 lg:max-w-3xl lg:mx-auto'}`}>

            {!result && (
              <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mb-8 text-center lg:text-left">
                <h2 className="text-4xl md:text-5xl font-extrabold font-display leading-tight mb-4">
                  Crack the Code to <br />
                  <span className="bg-clip-text text-transparent bg-gradient-to-r from-cyan-400 to-purple-400">Your Dream Job.</span>
                </h2>
                <p className="text-lg text-slate-400 max-w-xl mx-auto lg:mx-0">
                  Upload your resume and the job description. Our AI will analyze the gaps and prep you to win.
                </p>
              </motion.div>
            )}

            {/* UPLOAD CARDS */}
            <div className={`grid gap-4 ${result ? 'grid-cols-1' : 'md:grid-cols-2'}`}>

              {/* Resume Upload */}
              <div
                className={`relative group p-6 rounded-2xl border transition-all duration-300 cursor-pointer overflow-hidden
                  ${resumeFile
                    ? 'bg-cyan-950/20 border-cyan-500/50 shadow-[0_0_30px_rgba(6,182,212,0.15)]'
                    : 'bg-white/5 border-white/10 hover:border-cyan-500/30 hover:bg-white/10'
                  }`}
              >
                <input type="file" accept=".pdf" onChange={(e) => e.target.files && setResumeFile(e.target.files[0])}
                  className="absolute inset-0 z-20 opacity-0 cursor-pointer" />

                <div className="relative z-10 flex flex-col items-center text-center">
                  <div className={`p-4 rounded-full mb-3 transition-colors ${resumeFile ? 'bg-cyan-500/20' : 'bg-white/10 group-hover:bg-cyan-500/10'}`}>
                    <FileText className={`w-8 h-8 ${resumeFile ? 'text-cyan-400' : 'text-slate-400 group-hover:text-cyan-300'}`} />
                  </div>
                  {resumeFile ? (
                    <div>
                      <p className="font-semibold text-cyan-100 truncate max-w-[200px]">{resumeFile.name}</p>
                      <p className="text-xs text-cyan-400 mt-1">Ready for Analysis</p>
                    </div>
                  ) : (
                    <div>
                      <p className="font-bold text-slate-200 group-hover:text-white">Upload Resume</p>
                      <p className="text-xs text-slate-500 mt-1">PDF Format Only</p>
                    </div>
                  )}
                </div>
              </div>

              {/* JD Upload */}
              <div
                className={`relative group p-6 rounded-2xl border transition-all duration-300 cursor-pointer overflow-hidden
                  ${jdFile
                    ? 'bg-purple-950/20 border-purple-500/50 shadow-[0_0_30px_rgba(147,51,234,0.15)]'
                    : 'bg-white/5 border-white/10 hover:border-purple-500/30 hover:bg-white/10'
                  }`}
              >
                <input type="file" accept=".pdf" onChange={(e) => e.target.files && setJdFile(e.target.files[0])}
                  className="absolute inset-0 z-20 opacity-0 cursor-pointer" />

                <div className="relative z-10 flex flex-col items-center text-center">
                  <div className={`p-4 rounded-full mb-3 transition-colors ${jdFile ? 'bg-purple-500/20' : 'bg-white/10 group-hover:bg-purple-500/10'}`}>
                    <Target className={`w-8 h-8 ${jdFile ? 'text-purple-400' : 'text-slate-400 group-hover:text-purple-300'}`} />
                  </div>
                  {jdFile ? (
                    <div>
                      <p className="font-semibold text-purple-100 truncate max-w-[200px]">{jdFile.name}</p>
                      <p className="text-xs text-purple-400 mt-1">Ready for Analysis</p>
                    </div>
                  ) : (
                    <div>
                      <p className="font-bold text-slate-200 group-hover:text-white">Upload Job Desc</p>
                      <p className="text-xs text-slate-500 mt-1">PDF Format Only</p>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* ANALYZE BUTTON */}
            <button
              onClick={handleAnalyze}
              disabled={loading || !resumeFile || !jdFile}
              className={`w-full py-4 rounded-xl font-bold font-display text-lg flex items-center justify-center gap-3 transition-all duration-300
                 ${loading || !resumeFile || !jdFile
                  ? 'bg-white/5 text-slate-600 cursor-not-allowed'
                  : 'bg-gradient-to-r from-cyan-600 to-purple-600 hover:shadow-[0_0_40px_rgba(147,51,234,0.3)] hover:scale-[1.02] text-white shadow-lg'
                }`}
            >
              {loading ? <Loader2 className="animate-spin" /> : <Zap className="fill-current" />}
              {loading ? 'Analyzing...' : 'Run Analysis'}
            </button>
          </div>

          {/* RIGHT: DASHBOARD (Only shows if result exists) */}
          <div className="lg:col-span-8">
            <AnimatePresence mode="wait">
              {result && (
                <motion.div
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="space-y-6"
                >

                  {/* SCORE CARD */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

                    {/* Radial Score */}
                    <div className="glass rounded-3xl p-6 flex flex-col items-center justify-center bg-white/5 border border-white/10">
                      <RadialProgress score={result.match_score} />
                    </div>

                    {/* Summary */}
                    <div className="md:col-span-2 glass rounded-3xl p-8 bg-gradient-to-br from-white/5 to-white/[0.02] border border-white/10 flex flex-col justify-center">
                      <h3 className="text-slate-400 uppercase text-xs font-bold tracking-widest mb-2">Executive Summary</h3>
                      <p className="text-lg leading-relaxed text-slate-200">
                        {result.summary}
                      </p>
                    </div>

                  </div>

                  {/* MISSING KEYWORDS */}
                  {result.missing_keywords.length > 0 && (
                    <div className="glass rounded-2xl p-6 border border-white/10">
                      <h3 className="flex items-center gap-2 text-white font-bold font-display text-lg mb-4">
                        <AlertTriangle className="w-5 h-5 text-amber-500" />
                        <span>Critical Gaps</span>
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {result.missing_keywords.map((kw, i) => (
                          <motion.span
                            key={i}
                            initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: i * 0.05 }}
                            className="px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/20 text-amber-500 text-sm font-medium"
                          >
                            {kw}
                          </motion.span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* TWO COLUMN GRID */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

                    {/* INTERVIEW QUESTIONS */}
                    <div className="glass rounded-2xl p-0 border border-white/10 overflow-hidden">
                      <div className="p-6 border-b border-white/5 bg-white/[0.02]">
                        <h3 className="flex items-center gap-2 text-white font-bold font-display text-lg">
                          <BrainCircuit className="w-5 h-5 text-purple-400" />
                          <span>Interview Challenge</span>
                        </h3>
                      </div>
                      <div className="p-4 space-y-2 max-h-[400px] overflow-y-auto custom-scrollbar">
                        {result.interview_questions.map((q, i) => (
                          <div key={i} className="group p-4 rounded-xl bg-white/5 hover:bg-white/10 transition border border-transparent hover:border-purple-500/30">
                            <div className="flex gap-3">
                              <span className="text-purple-500 font-bold font-mono text-sm opacity-50 group-hover:opacity-100">0{i + 1}</span>
                              <p className="text-sm text-slate-300 group-hover:text-white transition-colors">{q}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* IMPROVEMENTS */}
                    <div className="glass rounded-2xl p-0 border border-white/10 overflow-hidden">
                      <div className="p-6 border-b border-white/5 bg-white/[0.02]">
                        <h3 className="flex items-center gap-2 text-white font-bold font-display text-lg">
                          <Sparkles className="w-5 h-5 text-cyan-400" />
                          <span>Resume Rewrites</span>
                        </h3>
                      </div>
                      <div className="p-4 space-y-4 max-h-[400px] overflow-y-auto custom-scrollbar">
                        {result.tailored_suggestions.map((sugg, i) => (
                          <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/5">
                            <div className="mb-3 pl-3 border-l-2 border-red-500/30">
                              <p className="text-xs text-red-400/70 font-bold mb-1">ORIGINAL</p>
                              <p className="text-xs text-slate-400 line-through decoration-red-500/30">{sugg.original}</p>
                            </div>
                            <div className="pl-3 border-l-2 border-green-500">
                              <p className="text-xs text-green-400 font-bold mb-1">OPTIMIZED</p>
                              <p className="text-sm text-green-100">{sugg.improved}</p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                  </div>

                  <div className="flex justify-center pt-8">
                    <button onClick={clearAll} className="text-slate-500 hover:text-white flex items-center gap-2 transition-colors">
                      <X className="w-4 h-4" /> Reset Dashboard
                    </button>
                  </div>

                </motion.div>
              )}
            </AnimatePresence>
          </div>

        </main>
      </div>
    </div>
  );
}

export default App;
