"use client";

import { DropZone } from "@/components/DropZone";
import { DryRunOutputPanel } from "@/components/DryRunOutputPanel";
import { ExportBar } from "@/components/ExportBar";
import { InsightsPanel } from "@/components/InsightsPanel";
import { MemoryAndStackPanel } from "@/components/MemoryAndStackPanel";
import { MonacoEditorPanel } from "@/components/MonacoEditorPanel";
import { PracticeLibrary } from "@/components/PracticeLibrary";
import { NarrationPanel } from "@/components/NarrationPanel";
import { TimelinePlayer } from "@/components/TimelinePlayer";
import { runAnalysis } from "@/lib/api";
import { AnalysisResponse } from "@/lib/types";
import { practiceSnippets } from "@/lib/practice-snippets";
import { motion } from "framer-motion";
import { useEffect, useState, useTransition } from "react";

const DEFAULT_PRACTICE = practiceSnippets[0];
const DEFAULT_CODE = DEFAULT_PRACTICE.code;

const DEFAULT_USER = "de305d54-75b4-431b-adb2-eb6b9e546014";

export function VisualizerShell() {
  const [language, setLanguage] = useState<"python" | "javascript" | "java" | "cpp">("python");
  const [aiProvider, setAiProvider] = useState<"local" | "gemini">("local");
  const [activePracticeId, setActivePracticeId] = useState(DEFAULT_PRACTICE.id);
  const [code, setCode] = useState(DEFAULT_CODE);
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [narrationLang, setNarrationLang] = useState<"en" | "hi">("en");
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [isPending, startTransition] = useTransition();

  useEffect(() => {
    setCurrentStepIndex(0);
  }, [result?.analysis_id]);

  const handlePracticeLoad = (snippet: (typeof practiceSnippets)[number]) => {
    startTransition(() => {
      setLanguage(snippet.language);
      setCode(snippet.code);
      setResult(null);
      setError("");
      setCurrentStepIndex(0);
      setActivePracticeId(snippet.id);
    });
  };

  const onAnalyze = async () => {
    setLoading(true);
    setError("");
    try {
      const data = await runAnalysis({
        user_id: DEFAULT_USER,
        language,
        code,
        narration_language: "both",
        optimization_level: "standard",
        ai_provider: aiProvider
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Analysis failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-7xl px-4 py-8 md:px-8">
      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.35 }}
        className="mb-8"
      >
        <p className="text-xs uppercase tracking-[0.32em] text-pulse">Startup-ready SaaS</p>
        <h1 className="mt-3 text-3xl font-bold text-white md:text-5xl">AI Code Visualizer Platform</h1>
        <p className="mt-3 max-w-3xl text-sm text-slate-300 md:text-base">
          AST-based visualization for Python, JavaScript, Java, and C++. Includes dry run, memory state,
          call stack, complexity, DSA pattern detection, and bilingual narration.
        </p>
      </motion.div>

      <PracticeLibrary
        activeId={activePracticeId}
        onLoadPractice={handlePracticeLoad}
        pending={isPending}
      />

      <div className="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-4">
          <div className="panel rounded-2xl p-4">
            <div className="flex flex-wrap items-center gap-3">
              <select
                value={language}
                onChange={(event) => setLanguage(event.target.value as typeof language)}
                className="rounded-xl border border-slate-700 bg-slate-900/50 px-3 py-2 text-sm text-white"
              >
                <option value="python">Python</option>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
              </select>
              <select
                value={aiProvider}
                onChange={(event) => setAiProvider(event.target.value as typeof aiProvider)}
                className="rounded-xl border border-slate-700 bg-slate-900/50 px-3 py-2 text-sm text-white"
                title="AI Provider"
              >
                <option value="local">Local Engine</option>
                <option value="gemini">Google Gemini</option>
              </select>
              <button
                onClick={onAnalyze}
                disabled={loading}
                className="rounded-xl bg-gradient-to-r from-pulse/80 to-emerald-400/70 px-4 py-2 text-sm font-semibold text-ink disabled:opacity-60"
              >
                {loading ? "Analyzing..." : "Analyze Code"}
              </button>
              {error ? <span className="text-xs text-rose-300">{error}</span> : null}
            </div>
          </div>

          <MonacoEditorPanel
            language={language}
            code={code}
            onChange={(value) => {
              setCode(value);
              if (value !== DEFAULT_CODE) {
                setActivePracticeId("custom");
              }
            }}
            activeLine={result?.dry_run[currentStepIndex]?.line}
          />
          <DropZone
            onCodeDrop={(content) => {
              setCode(content);
              setActivePracticeId("custom");
              setResult(null);
              setCurrentStepIndex(0);
            }}
          />
          <TimelinePlayer
            steps={result?.dry_run || []}
            onStepChange={(index) => setCurrentStepIndex(index)}
          />
        </div>

        <div className="space-y-4">
          <div className="panel rounded-2xl p-4">
            <h3 className="text-lg font-semibold text-white">AI Engine</h3>
            <p className="mt-2 text-sm text-slate-300">
              Requested: <span className="text-cyan-300">{aiProvider}</span>
            </p>
            <p className="text-sm text-slate-300">
              Used:{" "}
              <span className="text-emerald-300">{result?.ai?.used_provider || "run analysis first"}</span>
            </p>
            <p className="text-xs text-slate-500">{result?.ai?.message || "Gemini ke liye GEMINI_API_KEY set karein."}</p>
          </div>
          <NarrationPanel result={result} language={narrationLang} onLanguageChange={setNarrationLang} />
          <ExportBar result={result} />
          <DryRunOutputPanel
            steps={result?.dry_run || []}
            currentStepIndex={currentStepIndex}
            predictedOutput={result?.predicted_output || []}
          />
        </div>
      </div>

      <section className="mt-6 space-y-4">
        <MemoryAndStackPanel result={result} />
        <InsightsPanel result={result} />
      </section>
    </main>
  );
}
