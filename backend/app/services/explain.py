from app.utils.rulepacks import KENYA_MPESA_RULEPACK, GENERAL_RULEPACK, find_rule_hits
from app.utils.text_normalize import normalize_text

class Explainer:
    def explain_text(self, text: str, ml_prob: float, intel: dict, level: str):
        reasons = []
        actions = []

        clean = normalize_text(text)

        hits = find_rule_hits(clean, KENYA_MPESA_RULEPACK) + find_rule_hits(clean, GENERAL_RULEPACK)
        if hits:
            hits = sorted(hits, key=lambda x: x["weight"], reverse=True)[:5]
            reasons.extend([h["reason"] for h in hits])

        if intel.get("shortener"):
            reasons.append("Shortened link detected (often used to hide destination).")
        if intel.get("reputation_hit"):
            reasons.append("Link/domain appears on a local reputation blocklist.")
        if intel.get("domain_age_days") is not None and intel["domain_age_days"] < 30:
            reasons.append(f"Domain looks newly registered ({intel['domain_age_days']} days).")

        if ml_prob >= 0.85:
            reasons.append("Message content strongly matches known phishing/scam patterns.")
        elif ml_prob >= 0.65:
            reasons.append("Message content resembles common scam language patterns.")

        reasons = list(dict.fromkeys(reasons))[:7]

        if level in ("HIGH", "CRITICAL"):
            actions = [
                "Do not click any links or call numbers in the message.",
                "Verify the request using official channels you trust.",
                "If you already clicked, change passwords and enable 2FA immediately.",
            ]
            if "M-PESA" in text.upper() or "MPESA" in text.upper():
                actions.append("For M‑Pesa related alerts, confirm via the official Safaricom/M‑Pesa app or *234#.")
        elif level == "MEDIUM":
            actions = [
                "Be cautious: verify the sender and link destination before acting.",
                "Avoid sharing OTPs, PINs, or passwords.",
            ]
        else:
            actions = ["No high-risk indicators detected, but stay alert for unexpected requests."]

        return reasons or ["No strong indicators found. Use caution with unexpected messages."], actions, []

    def explain_url(self, url: str, ml_prob: float, intel: dict, level: str):
        reasons = []
        actions = []

        if intel.get("reputation_hit"):
            reasons.append("URL/domain appears on a local reputation blocklist.")
        if intel.get("shortener"):
            reasons.append("Shortened URL detected (destination may be hidden).")
        if intel.get("has_ip"):
            reasons.append("URL uses an IP address instead of a domain (common in malicious links).")
        if intel.get("domain_age_days") is not None and intel["domain_age_days"] < 30:
            reasons.append(f"Domain looks newly registered ({intel['domain_age_days']} days).")
        if intel.get("url_length", 0) >= 80:
            reasons.append("Unusually long URL (often used to confuse users).")
        if intel.get("dot_count", 0) >= 4:
            reasons.append("Many subdomains/dots detected (can be used to mimic legitimate brands).")

        if ml_prob >= 0.85:
            reasons.append("URL features strongly match known malicious patterns.")
        elif ml_prob >= 0.65:
            reasons.append("URL structure resembles common phishing link patterns.")

        reasons = list(dict.fromkeys(reasons))[:7]

        if level in ("HIGH", "CRITICAL"):
            actions = [
                "Do not open this link.",
                "If you received it in a message, treat the message as suspicious.",
                "If you already visited it, run a malware scan and reset credentials if you entered any.",
            ]
        elif level == "MEDIUM":
            actions = [
                "Open with caution only if you can verify the sender and destination.",
                "Prefer typing the official website directly rather than clicking.",
            ]
        else:
            actions = ["No high-risk indicators detected, but verify the destination if unexpected."]

        return reasons or ["No strong indicators found."], actions
