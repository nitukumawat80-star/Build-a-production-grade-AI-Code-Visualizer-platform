"use client";

import { getAnalysisHistory, getDashboardSummary, getDashboardTrends } from "@/lib/api";
import { AnalysisHistoryItem, DashboardSummary, DashboardTrend } from "@/lib/types";
import { motion } from "framer-motion";
import Link from "next/link";
import { useEffect, useState } from "react";

const USER_ID = "de305d54-75b4-431b-adb2-eb6b9e546014";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [trends, setTrends] = useState<DashboardTrend[]>([]);
  const [history, setHistory] = useState<AnalysisHistoryItem[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const [sum, trend, userHistory] = await Promise.all([
          getDashboardSummary(USER_ID),
          getDashboardTrends(USER_ID),
          getAnalysisHistory(USER_ID)
        ]);
        setSummary(sum);
        setTrends(trend);
        setHistory(userHistory);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load analytics");
      }
    })();
  }, []);

  return (
    <main className="mx-auto min-h-screen max-w-7xl px-4 py-8 md:px-8">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-moon">Premium Analytics</p>
          <h1 className="mt-2 text-3xl font-bold text-white md:text-4xl">Growth Command Center</h1>
        </div>
        <Link href="/" className="rounded-full border border-slate-700 px-4 py-2 text-xs text-slate-300">
          Back To Visualizer
        </Link>
      </div>

      {error ? <p className="mb-4 text-sm text-rose-300">{error}</p> : null}

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {[
          { label: "Total Analyses", value: summary?.total_analyses ?? 0 },
          { label: "Avg Time Score", value: summary?.avg_time_complexity_score ?? 0 },
          { label: "Avg Space Score", value: summary?.avg_space_complexity_score ?? 0 },
          { label: "Top Language", value: summary?.top_language ?? "-" }
        ].map((item) => (
          <motion.div
            key={item.label}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            className="panel rounded-2xl p-4"
          >
            <p className="text-xs uppercase tracking-[0.2em] text-slate-400">{item.label}</p>
            <p className="mt-2 text-2xl font-bold text-white">{item.value}</p>
          </motion.div>
        ))}
      </div>

      <section className="panel mt-6 rounded-2xl p-5">
        <h2 className="text-xl font-semibold text-white">Pattern Trend by Language</h2>
        <div className="mt-4 space-y-3">
          {trends.length === 0 ? (
            <p className="text-sm text-slate-400">No trend data yet.</p>
          ) : (
            trends.map((trend) => (
              <div key={trend.bucket}>
                <div className="mb-1 flex items-center justify-between text-sm text-slate-300">
                  <span>{trend.bucket}</span>
                  <span>{trend.analyses} analyses</span>
                </div>
                <div className="h-2 w-full rounded-full bg-slate-800">
                  <div
                    className="h-2 rounded-full bg-gradient-to-r from-pulse to-moon"
                    style={{ width: `${Math.min(100, trend.analyses * 10)}%` }}
                  />
                </div>
              </div>
            ))
          )}
        </div>
      </section>

      <section className="panel mt-6 rounded-2xl p-5">
        <h2 className="text-xl font-semibold text-white">Recent User History</h2>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-sm">
            <thead>
              <tr className="text-left text-slate-400">
                <th className="py-2 pr-4">Language</th>
                <th className="py-2 pr-4">Time Complexity</th>
                <th className="py-2 pr-4">Space Complexity</th>
                <th className="py-2">Created</th>
              </tr>
            </thead>
            <tbody>
              {history.length === 0 ? (
                <tr>
                  <td colSpan={4} className="py-3 text-slate-400">
                    No analysis history yet.
                  </td>
                </tr>
              ) : (
                history.slice(0, 12).map((item) => (
                  <tr key={item.id} className="border-t border-slate-800 text-slate-200">
                    <td className="py-2 pr-4 capitalize">{item.language}</td>
                    <td className="py-2 pr-4">{item.complexity_time || "-"}</td>
                    <td className="py-2 pr-4">{item.complexity_space || "-"}</td>
                    <td className="py-2">{item.created_at || "-"}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
