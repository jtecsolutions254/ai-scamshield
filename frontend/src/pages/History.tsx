import React, { useEffect, useState } from "react";
import Card from "../components/Card";
import { getJSON } from "../lib/api";

type StatsResponse = {
  total: number;
  by_type: Record<string, number>;
  by_level: Record<string, number>;
  recent: Array<{ id: string; type: string; risk_score: number; risk_level: string; created_at: string; excerpt: string }>;
};

export default function HistoryPage() {
  const [data, setData] = useState<StatsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    setError(null);
    try {
      const s = await getJSON<StatsResponse>("/api/v1/stats");
      setData(s);
    } catch (e: any) {
      setError(e?.message || "Failed to load");
    }
  }

  useEffect(() => { load(); }, []);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold">History</h2>
          <p className="text-sm text-slate-300 mt-1">Latest analyses saved in PostgreSQL.</p>
        </div>
        <button className="btn-ghost" onClick={load}>Refresh</button>
      </div>

      {error ? (
        <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-200">{error}</div>
      ) : null}

      <Card title="Recent scans" subtitle={data ? `${data.total} total scans` : "Loading..."}>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="text-slate-400">
              <tr>
                <th className="text-left py-2">Time</th>
                <th className="text-left py-2">Type</th>
                <th className="text-left py-2">Risk</th>
                <th className="text-left py-2">Excerpt</th>
              </tr>
            </thead>
            <tbody>
              {(data?.recent || []).map((r) => (
                <tr key={r.id} className="border-t border-slate-800">
                  <td className="py-2 pr-3 text-slate-300">{new Date(r.created_at).toLocaleString()}</td>
                  <td className="py-2 pr-3"><span className="badge bg-slate-900/40 border-slate-800">{r.type.toUpperCase()}</span></td>
                  <td className="py-2 pr-3"><span className="badge bg-sky-500/10 border-sky-500/20 text-sky-200">{r.risk_level} • {r.risk_score}</span></td>
                  <td className="py-2 text-slate-300">{r.excerpt}</td>
                </tr>
              ))}
              {!data?.recent?.length ? (
                <tr><td className="py-3 text-slate-400" colSpan={4}>No scans yet. Go to Analyze and run one.</td></tr>
              ) : null}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
