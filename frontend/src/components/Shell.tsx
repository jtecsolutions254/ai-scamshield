import React from "react";
import { NavLink } from "react-router-dom";

const NavItem = ({ to, label, icon }: { to: string; label: string; icon: string }) => (
  <NavLink
    to={to}
    className={({ isActive }) =>
      [
        "flex items-center gap-3 rounded-xl px-3 py-2 transition border",
        isActive
          ? "bg-slate-900/70 border-sky-500/30 shadow-glow"
          : "bg-slate-900/30 border-slate-800 hover:bg-slate-900/50",
      ].join(" ")
    }
  >
    <span className="text-lg">{icon}</span>
    <span className="font-medium">{label}</span>
  </NavLink>
);

export default function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen gradient-bg">
      <div className="mx-auto max-w-7xl px-4 py-6">
        <header className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-2xl bg-sky-500/20 border border-sky-500/30 flex items-center justify-center shadow-glow">
              <span className="text-xl">🛡</span>
            </div>
            <div>
              <h1 className="text-xl font-semibold tracking-tight">AI ScamShield</h1>
              <p className="text-sm text-slate-300/90">Phishing • Scam SMS • Malicious URL Detection</p>
            </div>
          </div>
          <a className="btn-ghost" href="/docs" target="_blank" rel="noreferrer">
            API Docs
          </a>
        </header>

        <div className="mt-6 grid grid-cols-12 gap-4">
          <aside className="col-span-12 md:col-span-3 lg:col-span-2">
            <div className="glass rounded-2xl p-3">
              <nav className="flex flex-col gap-2">
                <NavItem to="/" label="Analyze" icon="🔎" />
                <NavItem to="/history" label="History" icon="🗂️" />
                <NavItem to="/trends" label="Trends" icon="📈" />
              </nav>
              <div className="mt-4 rounded-xl bg-slate-900/40 border border-slate-800 p-3 text-xs text-slate-300">
                <div className="font-semibold text-slate-100">Tip</div>
                Paste an M‑Pesa scam SMS or suspicious URL to test. You’ll get a risk score + reasons.
              </div>
            </div>
          </aside>

          <main className="col-span-12 md:col-span-9 lg:col-span-10">
            <div className="glass rounded-2xl p-5">{children}</div>
            <footer className="mt-4 text-xs text-slate-400">
              Defense‑in‑depth: ML + Kenya‑focused heuristics + threat‑intel signals.
            </footer>
          </main>
        </div>
      </div>
    </div>
  );
}
