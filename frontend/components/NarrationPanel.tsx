import { AnalysisResponse } from "@/lib/types";

type Props = {
  result: AnalysisResponse | null;
  language: "en" | "hi";
  onLanguageChange: (lang: "en" | "hi") => void;
};

export function NarrationPanel({ result, language, onLanguageChange }: Props) {
  return (
    <div className="panel rounded-2xl p-4">
      <div className="flex items-center justify-between gap-3">
        <h3 className="text-lg font-semibold text-white">AI Narration</h3>
        <div className="flex gap-2">
          <button
            onClick={() => onLanguageChange("en")}
            className={`rounded-full px-3 py-1 text-xs ${
              language === "en"
                ? "bg-pulse/30 text-pulse border border-pulse/40"
                : "border border-slate-700 text-slate-300"
            }`}
          >
            English
          </button>
          <button
            onClick={() => onLanguageChange("hi")}
            className={`rounded-full px-3 py-1 text-xs ${
              language === "hi"
                ? "bg-amber-500/20 text-amber-300 border border-amber-400/30"
                : "border border-slate-700 text-slate-300"
            }`}
          >
            Hindi
          </button>
        </div>
      </div>
      <p className="mt-3 text-sm leading-relaxed text-slate-300">
        {result ? result.narration[language] : "Narration will appear after analysis."}
      </p>
    </div>
  );
}
