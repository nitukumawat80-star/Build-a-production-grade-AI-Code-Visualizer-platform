"use client";

import { motion } from "framer-motion";
import { Pause, Play, RotateCcw, SkipBack, SkipForward } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

type Step = {
  index: number;
  title: string;
  line: number;
  action: string;
  output?: string | null;
  locals?: Record<string, unknown>;
  globals?: Record<string, unknown>;
};

type Props = {
  steps: Step[];
  onStepChange?: (index: number, step: Step) => void;
};

export function TimelinePlayer({ steps, onStepChange }: Props) {
  const [current, setCurrent] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [speedMs, setSpeedMs] = useState(1100);

  useEffect(() => {
    setCurrent(0);
    setPlaying(false);
  }, [steps]);

  useEffect(() => {
    if (steps.length === 0) return;
    onStepChange?.(current, steps[current]);
  }, [current, onStepChange, steps]);

  useEffect(() => {
    if (!playing || steps.length === 0) return;
    const timer = window.setInterval(() => {
      setCurrent((prev) => {
        if (prev >= steps.length - 1) {
          setPlaying(false);
          return prev;
        }
        return prev + 1;
      });
    }, speedMs);
    return () => window.clearInterval(timer);
  }, [playing, speedMs, steps.length]);

  const step = useMemo(() => steps[current], [steps, current]);

  if (steps.length === 0) {
    return <div className="panel rounded-2xl p-6 text-sm text-slate-300">No timeline yet.</div>;
  }

  const scopeEntries = (scope?: Record<string, unknown>) =>
    Object.entries(scope || {}).slice(0, 8).map(([key, value]) => (
      <div key={key} className="rounded-lg border border-slate-800 bg-slate-900/65 px-2 py-1 text-xs">
        <span className="text-cyan-300">{key}</span>
        <span className="text-slate-400"> = </span>
        <span className="text-slate-200">{String(value)}</span>
      </div>
    ));

  return (
    <div className="panel rounded-2xl p-4 space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Dry Run Timeline</p>
          <h3 className="text-lg font-semibold text-white">
            Step {current + 1} / {steps.length}
          </h3>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => {
              setPlaying(false);
              setCurrent(0);
            }}
            className="rounded-xl border border-slate-700 p-2 text-slate-200"
            title="Reset"
          >
            <RotateCcw size={16} />
          </button>
          <button
            onClick={() => {
              setPlaying(false);
              setCurrent((p) => Math.max(0, p - 1));
            }}
            className="rounded-xl border border-slate-700 p-2 text-slate-200"
            title="Previous step"
          >
            <SkipBack size={16} />
          </button>
          <button
            onClick={() => setPlaying((p) => !p)}
            className="rounded-xl bg-pulse/20 border border-pulse/40 p-2 text-pulse"
            title={playing ? "Pause" : "Play"}
          >
            {playing ? <Pause size={16} /> : <Play size={16} />}
          </button>
          <button
            onClick={() => {
              setPlaying(false);
              setCurrent((p) => Math.min(steps.length - 1, p + 1));
            }}
            className="rounded-xl border border-slate-700 p-2 text-slate-200"
            title="Run next step"
          >
            <SkipForward size={16} />
          </button>
          <select
            value={speedMs}
            onChange={(event) => setSpeedMs(Number(event.target.value))}
            className="rounded-xl border border-slate-700 bg-slate-900/55 px-2 py-2 text-xs text-slate-200"
            title="Playback speed"
          >
            <option value={1600}>Slow</option>
            <option value={1100}>Normal</option>
            <option value={600}>Fast</option>
          </select>
        </div>
      </div>

      <input
        type="range"
        min={0}
        max={Math.max(0, steps.length - 1)}
        value={current}
        onChange={(event) => {
          setPlaying(false);
          setCurrent(Number(event.target.value));
        }}
        className="w-full accent-pulse"
      />

      <motion.div
        key={step.index}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.25 }}
        className="space-y-3 rounded-xl border border-slate-700 bg-slate-900/55 p-4"
      >
        <div>
          <p className="text-sm text-slate-300">{step.title}</p>
          <p className="mt-1 text-xl font-semibold text-white">{step.action}</p>
          <p className="mt-1 text-sm text-slate-400">Line {step.line}</p>
          {step.output ? <p className="mt-2 text-sm text-amber-300">Output: {step.output}</p> : null}
        </div>

        <div className="grid gap-3 md:grid-cols-2">
          <div>
            <p className="mb-2 text-xs uppercase tracking-wide text-slate-400">Local Variables</p>
            <div className="space-y-1">
              {scopeEntries(step.locals).length > 0 ? (
                scopeEntries(step.locals)
              ) : (
                <p className="text-xs text-slate-500">No local changes at this step.</p>
              )}
            </div>
          </div>
          <div>
            <p className="mb-2 text-xs uppercase tracking-wide text-slate-400">Global Variables</p>
            <div className="space-y-1">
              {scopeEntries(step.globals).length > 0 ? (
                scopeEntries(step.globals)
              ) : (
                <p className="text-xs text-slate-500">No global changes at this step.</p>
              )}
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
