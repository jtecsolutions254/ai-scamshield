import React, { useMemo, useState } from "react";
import Card from "../components/Card";
import RiskGauge from "../components/RiskGauge";
import { postJSON } from "../lib/api";

type AnalyzeMode = "email" | "sms" | "url";

type AnalyzeResponse = {
  type: string;
  risk_score: number;
  risk_level: string;
  ml: { prob_phish: number; confidence: number; model_version: string };
  intel: {
    urls_found: string[];
    shortener: boolean;
    domain_age_days?: number | null;
    reputation_hit: boolean;
    redirects: string[];
    notes: Record<string, any>;
  };
  reasons: string[];
  recommended_actions: string[];
  analysis_id: string;
};

const sampleSMS =
  "M-PESA: Your account will be locked. Verify now at http://example-login-secure.com/verify to avoid suspension.";
const sampleEmail =
  "Subject: Account Verification Required\nFrom: Support <support@secure-mail.example>\n\nDear customer, your account will be suspended within 24 hours. Verify now: http://bit.ly/abc";
const sampleURL = "http://paypal.com.verify-user.security-update.xyz/login";

export default function AnalyzePage() {
  const [mode, setMode] = useState<AnalyzeMode>("sms");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalyzeResponse | null>(null);

  const [smsText, setSmsText] = useState(sampleSMS);
  const [emailBody, setEmailBody] = useState(sampleEmail);
  const [url, setUrl] = useState(sampleURL);

  const endpoint = useMemo(() => {
    if (mode === "email") return "/api/v1/analyze-email";
    if (mode === "sms") return "/api/v1/analyze-sms";
    return "/api/v1/analyze-url";
  }, [mode]);

  async function analyze() {
    setError(null);
    setLoading(true);
    setResult(null);
    try {
      let payload: any = {};
      if (mode === "sms") payload = { text: smsText };
      if (mode === "email") payload = { body: emailBody };
      if (mode === "url") payload = { url };
      const res = await postJSON<AnalyzeResponse>(endpoint, payload);
      setResult(res);
    } catch (e: any) {
      setError(e?.message || "Analysis failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h2 className="text-xl font-semibold">Analyze suspicious content</h2>
          <p className="text-sm text-slate-300 mt-1">
            Choose Email, SMS, or URL. Get a risk score, reasons, and recommended actions.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button className={mode === "email" ? "btn-primary" : "btn-ghost"} onClick={() => setMode("email")}>
            Email
          </button>
          <button className={mode === "sms" ? "btn-primary" : "btn-ghost"} onClick={() => setMode("sms")}>
            SMS
          </button>
          <button className={mode === "url" ? "btn-primary" : "btn-ghost"} onClick={() => setMode("url")}>
            URL
          </button>
        </div>
      </div>

      <div className="grid grid-cols-12 gap-4">
        <div className="col-span-12 lg:col-span-6">
          <Card
            title="Input"
            subtitle="Paste the suspicious content below."
            right={
              <button className="btn-primary" onClick={analyze} disabled={loading}>
                {loading ? "Analyzing..." : "Analyze"}
              </button>
            }
          >
            {mode === "sms" ? (
              <div className="space-y-2">
                <textarea className="input h-44" value={smsText} onChange={(e) => setSmsText(e.target.value)} placeholder="Paste SMS here..." />
                <div className="text-xs text-slate-400">Tip: include the full message including any links or phone numbers.</div>
              </div>
            ) : null}

            {mode === "email" ? (
              <div className="space-y-2">
                <textarea className="input h-44" value={emailBody} onChange={(e) => setEmailBody(e.target.value)} placeholder="Paste email text here..." />
                <div className="text-xs text-slate-400">For better accuracy, include subject/from lines and the message body.</div>
              </div>
            ) : null}

            {mode === "url" ? (
              <div className="space-y-2">
                <input className="input" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="Paste URL" />
                <div className="text-xs text-slate-400">The system inspects URL structure + reputation + (optional) domain age.</div>
              </div>
            ) : null}

            {error ? (
              <div className="mt-3 rounded-xl border border-rose-500/30 bg-rose-500/10 p-3 text-sm text-rose-200">{error}</div>
            ) : null}
          </Card>
        </div>

        <div className="col-span-12 lg:col-span-6">
          <Card title="Result" subtitle={result ? `Analysis ID: ${result.analysis_id}` : "Run an analysis to see results."}>
            {result ? (
              <div className="space-y-4">
                <RiskGauge score={result.risk_score} level={result.risk_level} />

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-3">
                    <div className="text-xs text-slate-400">ML Probability</div>
                    <div className="text-lg font-semibold">{(result.ml.prob_phish * 100).toFixed(1)}%</div>
                    <div className="text-xs text-slate-400 mt-1">Confidence: {(result.ml.confidence * 100).toFixed(1)}%</div>
                    <div className="text-xs text-slate-500 mt-1">Model: {result.ml.model_version}</div>
                  </div>
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-3">
                    <div className="text-xs text-slate-400">Link intelligence</div>
                    <div className="text-sm mt-2 space-y-1 text-slate-200">
                      <div>Shortener: <span className="text-slate-100 font-semibold">{String(result.intel.shortener)}</span></div>
                      <div>Reputation hit: <span className="text-slate-100 font-semibold">{String(result.intel.reputation_hit)}</span></div>
                      <div>
                        Domain age:{" "}
                        <span className="text-slate-100 font-semibold">
                          {result.intel.domain_age_days === null || result.intel.domain_age_days === undefined ? "Unknown" : `${result.intel.domain_age_days} days`}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-3">
                    <div className="text-sm font-semibold">Why it was flagged</div>
                    <ul className="mt-2 list-disc pl-5 text-sm text-slate-200 space-y-1">
                      {result.reasons.map((r, i) => (<li key={i}>{r}</li>))}
                    </ul>
                  </div>
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-3">
                    <div className="text-sm font-semibold">Recommended actions</div>
                    <ul className="mt-2 list-disc pl-5 text-sm text-slate-200 space-y-1">
                      {result.recommended_actions.map((a, i) => (<li key={i}>{a}</li>))}
                    </ul>
                  </div>
                </div>

                {result.intel.urls_found?.length ? (
                  <div className="rounded-2xl border border-slate-800 bg-slate-900/30 p-3">
                    <div className="text-sm font-semibold">URLs found</div>
                    <div className="mt-2 flex flex-col gap-2">
                      {result.intel.urls_found.map((u, i) => (
                        <div key={i} className="text-xs rounded-xl border border-slate-800 bg-slate-950/40 px-3 py-2 break-all">{u}</div>
                      ))}
                    </div>
                  </div>
                ) : null}
              </div>
            ) : (
              <div className="text-sm text-slate-300">
                No result yet. Paste content and click <span className="text-slate-100 font-semibold">Analyze</span>.
              </div>
            )}
          </Card>
        </div>
      </div>
    </div>
  );
}
