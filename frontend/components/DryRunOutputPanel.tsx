"use client";

import { useEffect, useMemo, useState } from "react";

type Step = {
  index: number;
  output?: string | null;
};

type Props = {
  steps: Step[];
  currentStepIndex: number;
  predictedOutput: string[];
};

export function DryRunOutputPanel({ steps, currentStepIndex, predictedOutput }: Props) {
  const [displayedOutput, setDisplayedOutput] = useState("");
  const [typingDelayMs, setTypingDelayMs] = useState(20);

  const targetOutput = useMemo(() => {
    const stepOutputs = steps
      .slice(0, Math.max(0, currentStepIndex + 1))
      .map((step) => (step.output || "").trim())
      .filter((line) => line.length > 0);

    if (stepOutputs.length > 0) {
      return stepOutputs.join("\n");
    }

    if (steps.length > 0 && currentStepIndex >= steps.length - 1) {
      return predictedOutput.join("\n");
    }

    return "";
  }, [currentStepIndex, predictedOutput, steps]);

  useEffect(() => {
    if (targetOutput.length < displayedOutput.length) {
      setDisplayedOutput(targetOutput);
      return;
    }

    if (targetOutput === displayedOutput) {
      return;
    }

    const timer = window.setTimeout(() => {
      setDisplayedOutput(targetOutput.slice(0, displayedOutput.length + 1));
    }, typingDelayMs);

    return () => window.clearTimeout(timer);
  }, [displayedOutput, targetOutput, typingDelayMs]);

  return (
    <div className="panel rounded-2xl p-4">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <h3 className="text-lg font-semibold text-white">Temporary Output (Live Dry Run)</h3>
        <div className="flex items-center gap-2 text-xs text-slate-300">
          <span>Typing Speed</span>
          <input
            type="range"
            min={8}
            max={65}
            step={1}
            value={typingDelayMs}
            onChange={(event) => setTypingDelayMs(Number(event.target.value))}
            className="accent-emerald-400"
          />
          <span>{typingDelayMs}ms</span>
        </div>
      </div>

      <pre className="min-h-[120px] whitespace-pre-wrap rounded-xl border border-slate-700 bg-slate-900/60 p-3 font-mono text-sm text-emerald-300">
        {displayedOutput || "Dry run output will appear step by step here..."}
      </pre>

      <p className="mt-2 text-xs text-slate-500">
        Output is revealed gradually as each step executes. Use Play/Pause/Next/Previous in timeline.
      </p>
    </div>
  );
}
