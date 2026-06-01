import { AnalysisResponse } from "@/lib/types";

type Props = {
  result: AnalysisResponse | null;
};

export function InsightsPanel({ result }: Props) {
  if (!result) {
    return <div className="panel rounded-2xl p-6 text-sm text-slate-300">Run analysis to view insights.</div>;
  }

  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <section className="panel rounded-2xl p-4">
        <h3 className="text-lg font-semibold text-white">Complexity</h3>
        <p className="mt-2 text-sm text-slate-300">Time: {result.complexity.time}</p>
        <p className="text-sm text-slate-300">Space: {result.complexity.space}</p>
        <ul className="mt-2 list-disc pl-4 text-xs text-slate-400">
          {result.complexity.notes.map((note) => (
            <li key={note}>{note}</li>
          ))}
        </ul>
      </section>

      <section className="panel rounded-2xl p-4">
        <h3 className="text-lg font-semibold text-white">DSA Patterns</h3>
        <div className="mt-2 flex flex-wrap gap-2">
          {result.patterns.map((pattern) => (
            <span key={pattern.label} className="badge rounded-full px-3 py-1 text-xs">
              {pattern.label} ({Math.round(pattern.confidence * 100)}%)
            </span>
          ))}
        </div>
      </section>

      <section className="panel rounded-2xl p-4">
        <h3 className="text-lg font-semibold text-white">Optimization Suggestions</h3>
        <ul className="mt-2 list-disc pl-4 text-sm text-slate-300">
          {result.optimizations.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      </section>

      <section className="panel rounded-2xl p-4">
        <h3 className="text-lg font-semibold text-white">Bugs & Smells</h3>
        <ul className="mt-2 space-y-2 text-sm text-slate-300">
          {result.bug_risks.map((bug) => (
            <li key={bug.title + bug.details}>
              <strong className="text-rose-300">{bug.title}</strong>: {bug.details}
            </li>
          ))}
          {result.code_smells.map((smell) => (
            <li key={smell.title + smell.details}>
              <strong className="text-amber-300">{smell.title}</strong>: {smell.details}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
