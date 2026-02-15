import React from "react";

function levelStyles(level: string) {
  switch (level) {
    case "LOW":
      return "bg-emerald-500/15 border-emerald-500/30 text-emerald-200";
    case "MEDIUM":
      return "bg-amber-500/15 border-amber-500/30 text-amber-200";
    case "HIGH":
      return "bg-orange-500/15 border-orange-500/30 text-orange-200";
    case "CRITICAL":
      return "bg-rose-500/15 border-rose-500/30 text-rose-200";
    default:
      return "bg-slate-500/15 border-slate-500/30 text-slate-200";
  }
}

export default function RiskGauge({ score, level }: { score: number; level: string }) {
  const radius = 58;
  const stroke = 10;
  const c = 2 * Math.PI * radius;
  const pct = Math.max(0, Math.min(100, score));
  const offset = c - (pct / 100) * c;

  return (
    <div className="flex items-center gap-5">
      <div className="relative">
        <svg width="140" height="140" viewBox="0 0 140 140">
          <circle cx="70" cy="70" r={radius} stroke="rgba(148,163,184,0.20)" strokeWidth={stroke} fill="transparent" />
          <circle
            cx="70"
            cy="70"
            r={radius}
            stroke="rgba(56,189,248,0.95)"
            strokeWidth={stroke}
            fill="transparent"
            strokeLinecap="round"
            strokeDasharray={c}
            strokeDashoffset={offset}
            transform="rotate(-90 70 70)"
          />
        </svg>
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <div className="text-3xl font-semibold">{pct}</div>
          <div className="text-xs text-slate-300">Risk score</div>
        </div>
      </div>

      <div className="flex-1">
        <div className="flex items-center gap-2">
          <span className={["badge", levelStyles(level)].join(" ")}>{level}</span>
          <span className="text-sm text-slate-300">0–100</span>
        </div>
        <p className="mt-2 text-sm text-slate-200/90">
          Higher scores mean stronger scam/phishing indicators from content + link intelligence.
        </p>
      </div>
    </div>
  );
}
