import { AnalysisResponse } from "@/lib/types";

type Props = {
  result: AnalysisResponse | null;
};

export function MemoryAndStackPanel({ result }: Props) {
  return (
    <div className="grid gap-4 lg:grid-cols-2">
      <section className="panel rounded-2xl p-4">
        <h3 className="text-lg font-semibold text-white">Memory Visualization</h3>
        <div className="mt-3 space-y-2 text-sm">
          {result?.memory.length ? (
            result.memory.map((cell) => (
              <div key={cell.key} className="rounded-xl border border-slate-700 bg-slate-900/45 p-3">
                <p className="font-medium text-cyan-300">{cell.key}</p>
                <p className="text-slate-300">{String(cell.value)} ({cell.value_type})</p>
                <p className="text-xs text-slate-500">~{cell.approx_bytes} bytes</p>
              </div>
            ))
          ) : (
            <p className="text-slate-400">No memory cells yet.</p>
          )}
        </div>
      </section>

      <section className="panel rounded-2xl p-4">
        <h3 className="text-lg font-semibold text-white">Function Call Stack</h3>
        <div className="mt-3 space-y-2 text-sm">
          {result?.call_stack.length ? (
            result.call_stack.map((frame, idx) => (
              <div
                key={`${frame.function}-${idx}`}
                className="rounded-xl border border-slate-700 bg-slate-900/45 p-3"
              >
                <p className="font-medium text-amber-300">{frame.function}</p>
                <p className="text-slate-300">Line {frame.line}</p>
                <p className="text-xs text-slate-500">Depth {frame.depth}</p>
              </div>
            ))
          ) : (
            <p className="text-slate-400">No frames yet.</p>
          )}
        </div>
      </section>
    </div>
  );
}
