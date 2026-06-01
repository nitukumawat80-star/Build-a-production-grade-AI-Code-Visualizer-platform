export type AnalysisRequest = {
  user_id: string;
  language: "python" | "javascript" | "js" | "java" | "cpp" | "c++";
  code: string;
  narration_language: "en" | "hi" | "both";
  optimization_level: "standard" | "aggressive";
};

export type AnalysisResponse = {
  analysis_id: string;
  user_id: string;
  language: string;
  ast_summary: Record<string, unknown>;
  dry_run: Array<{
    index: number;
    title: string;
    line: number;
    action: string;
    locals: Record<string, unknown>;
    globals: Record<string, unknown>;
    output?: string | null;
  }>;
  memory: Array<{
    key: string;
    value: unknown;
    value_type: string;
    approx_bytes: number;
  }>;
  call_stack: Array<{
    function: string;
    line: number;
    depth: number;
    locals?: Record<string, unknown>;
  }>;
  predicted_output: string[];
  complexity: {
    time: string;
    space: string;
    notes: string[];
  };
  patterns: Array<{
    label: string;
    confidence: number;
    evidence: string;
  }>;
  optimizations: string[];
  code_smells: Array<{ title: string; severity: string; details: string }>;
  bug_risks: Array<{ title: string; severity: string; details: string }>;
  narration: {
    en: string;
    hi: string;
  };
};

export type DashboardSummary = {
  total_analyses: number;
  avg_time_complexity_score: number;
  avg_space_complexity_score: number;
  top_language: string;
  monthly_growth_percent: number;
};

export type DashboardTrend = {
  bucket: string;
  analyses: number;
  avg_complexity_score: number;
};

export type AnalysisHistoryItem = {
  id: string;
  user_id: string;
  language: string;
  complexity_time?: string | null;
  complexity_space?: string | null;
  created_at?: string | null;
};
