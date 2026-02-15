import React, { useEffect, useMemo, useState } from "react";
import Card from "../components/Card";
import { getJSON } from "../lib/api";
import { PieChart, Pie, Tooltip, ResponsiveContainer, Cell, BarChart, Bar, XAxis, YAxis } from "recharts";

type StatsResponse = {
  total: number;
  by_type: Record<string, number>;
  by_level: Record<string, number>;
  recent: Array<any>;
};

function toList(obj: Record<string, number>) {
  return Object.entries(obj || {}).map(([name, value]) => ({ name, value }));
}

export default function TrendsPage() {
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

  const pieLevel = useMemo(() => toList(data?.by_level || {}), [data]);
  const barType = useMemo(() => toList(data?.by_type || {}), [data]);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold">Trends</h2>
          <p className="text-sm text-slate-300 mt-1">Risk distribution and scan volume by type.</p>
        </div>
        <button className="btn-ghost" onClick={load}>Refresh</button>
      </div>

      {error ? (
        <div className="rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-200">{error}</div>
      ) : null}

      <div className="grid grid-cols-12 gap-4">
        <div className="col-span-12 lg:col-span-6">
          <Card title="Risk levels" subtitle={data ? `${data.total} total scans` : "Loading..."}>
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={pieLevel} dataKey="value" nameKey="name" innerRadius={45} outerRadius={80} paddingAngle={2}>
                    {pieLevel.map((_, idx) => (
                      <Cell key={idx} fill="rgba(56,189,248,0.85)" opacity={(idx + 1) / (pieLevel.length + 1)} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </div>

        <div className="col-span-12 lg:col-span-6">
          <Card title="Scan types" subtitle="Email vs SMS vs URL">
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={barType}>
                  <XAxis dataKey="name" />
                  <YAxis allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="value" fill="rgba(168,85,247,0.75)" radius={[10,10,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
