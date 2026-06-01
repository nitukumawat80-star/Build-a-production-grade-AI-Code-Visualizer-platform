import {
  AnalysisHistoryItem,
  AnalysisRequest,
  AnalysisResponse,
  DashboardSummary,
  DashboardTrend
} from "@/lib/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

export async function runAnalysis(payload: AnalysisRequest): Promise<AnalysisResponse> {
  const response = await fetch(`${API_BASE}/analysis/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Analysis failed (${response.status})`);
  }

  return response.json();
}

export async function getDashboardSummary(userId: string): Promise<DashboardSummary> {
  const response = await fetch(`${API_BASE}/dashboard/summary/${userId}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to load dashboard summary");
  }
  return response.json();
}

export async function getDashboardTrends(userId: string): Promise<DashboardTrend[]> {
  const response = await fetch(`${API_BASE}/dashboard/trends/${userId}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to load dashboard trends");
  }
  return response.json();
}

export async function getAnalysisHistory(userId: string): Promise<AnalysisHistoryItem[]> {
  const response = await fetch(`${API_BASE}/analysis/history/${userId}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error("Failed to load analysis history");
  }
  return response.json();
}

export async function createExport(analysisId: string, exportType: "mp4" | "gif" | "pdf") {
  const response = await fetch(`${API_BASE}/exports`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ analysis_id: analysisId, export_type: exportType })
  });

  if (!response.ok) {
    throw new Error("Failed to create export job");
  }
  return response.json();
}
