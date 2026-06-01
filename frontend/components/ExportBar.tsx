"use client";

import { createExport } from "@/lib/api";
import { AnalysisResponse } from "@/lib/types";
import { useState } from "react";

type Props = {
  result: AnalysisResponse | null;
};

export function ExportBar({ result }: Props) {
  const [status, setStatus] = useState<string>("");

  const handleExport = async (format: "mp4" | "gif" | "pdf") => {
    if (!result) return;
    setStatus(`Creating ${format.toUpperCase()} job...`);
    try {
      const job = await createExport(result.analysis_id, format);
      setStatus(`${format.toUpperCase()} job queued: ${job.id}`);
    } catch (error) {
      setStatus(`Export failed: ${error instanceof Error ? error.message : "unknown error"}`);
    }
  };

  return (
    <div className="panel rounded-2xl p-4">
      <div className="flex flex-wrap items-center gap-3">
        <button
          onClick={() => handleExport("mp4")}
          className="rounded-xl border border-slate-600 px-3 py-2 text-sm text-slate-200 hover:border-pulse/70"
        >
          Export MP4
        </button>
        <button
          onClick={() => handleExport("gif")}
          className="rounded-xl border border-slate-600 px-3 py-2 text-sm text-slate-200 hover:border-pulse/70"
        >
          Export GIF
        </button>
        <button
          onClick={() => handleExport("pdf")}
          className="rounded-xl border border-slate-600 px-3 py-2 text-sm text-slate-200 hover:border-pulse/70"
        >
          Export PDF
        </button>
      </div>
      {status ? <p className="mt-2 text-xs text-slate-400">{status}</p> : null}
    </div>
  );
}
