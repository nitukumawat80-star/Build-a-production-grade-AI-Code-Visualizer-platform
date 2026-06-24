"use client";

import { practiceSnippets, PracticeSnippet } from "@/lib/practice-snippets";

type Props = {
  activeId: string;
  onLoadPractice: (snippet: PracticeSnippet) => void;
  pending?: boolean;
};

export function PracticeLibrary({ activeId, onLoadPractice, pending = false }: Props) {
  return (
    <section className="panel rounded-2xl p-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs uppercase tracking-[0.25em] text-slate-400">Practice Library</p>
          <h2 className="text-xl font-semibold text-white">Load a clean dry run example</h2>
        </div>
        <p className="text-xs text-slate-500">Pick a snippet and watch the timeline light up.</p>
      </div>

      <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        {practiceSnippets.map((snippet) => {
          const isActive = snippet.id === activeId;

          return (
            <article
              key={snippet.id}
              className={`rounded-2xl border p-4 transition ${
                isActive
                  ? "border-pulse/60 bg-pulse/10 shadow-[0_0_0_1px_rgba(0,217,192,0.2)]"
                  : "border-slate-700 bg-slate-900/55 hover:border-slate-500"
              }`}
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <p className="text-xs uppercase tracking-[0.18em] text-slate-500">{snippet.concept}</p>
                  <h3 className="mt-1 text-lg font-semibold text-white">{snippet.title}</h3>
                </div>
                {isActive ? (
                  <span className="rounded-full border border-pulse/40 bg-pulse/15 px-2 py-1 text-[10px] uppercase tracking-[0.2em] text-pulse">
                    Active
                  </span>
                ) : null}
              </div>

              <p className="mt-3 text-sm text-slate-300">{snippet.description}</p>
              <p className="mt-2 text-xs text-slate-400">{snippet.dryRunFocus}</p>
              <p className="mt-2 text-xs text-emerald-300">Expected output: {snippet.expectedOutput}</p>

              <button
                onClick={() => onLoadPractice(snippet)}
                disabled={pending && !isActive}
                className="mt-4 w-full rounded-xl bg-gradient-to-r from-pulse/80 to-emerald-400/70 px-3 py-2 text-sm font-semibold text-ink disabled:opacity-60"
              >
                {isActive ? "Loaded" : `Load ${snippet.title}`}
              </button>
            </article>
          );
        })}
      </div>
    </section>
  );
}
