import re
from typing import List, Dict

GENERAL_RULEPACK = [
    {"pattern": r"\bverify( now)?\b", "weight": 0.15, "reason": "Verification pressure detected (verify now)."},
    {"pattern": r"\baccount (suspend|suspended|locked|disabled)\b", "weight": 0.20, "reason": "Threat of account restriction detected."},
    {"pattern": r"\burgent\b|\bimmediately\b|\bwithin\s?\d+\s?(hours|hrs|minutes|mins)\b", "weight": 0.15, "reason": "Urgency language detected."},
    {"pattern": r"\bpassword\b|\blogin\b|\bcredentials\b", "weight": 0.15, "reason": "Credential request cues detected."},
    {"pattern": r"\bclick\b.*\blink\b|\bopen\b.*\blink\b", "weight": 0.10, "reason": "Instruction to click/open a link detected."},
    {"pattern": r"\bconfirm\b.*\bdetails\b|\bupdate\b.*\bdetails\b", "weight": 0.12, "reason": "Request to confirm/update details detected."},
]

KENYA_MPESA_RULEPACK = [
    {"pattern": r"\bmpesa\b|\bm-pesa\b", "weight": 0.10, "reason": "M-Pesa context detected."},
    {"pattern": r"\bfuliza\b", "weight": 0.12, "reason": "Fuliza-related prompt detected."},
    {"pattern": r"\breversal\b|\breverse\b.*\btransaction\b", "weight": 0.18, "reason": "Transaction reversal lure detected."},
    {"pattern": r"\bpin\b.*\bconfirm\b|\bshare\b.*\bpin\b", "weight": 0.25, "reason": "PIN sharing cue detected (high risk)."},
    {"pattern": r"\b(you have received|umepewa|umepokea)\b.*\b(amount|ksh|kes)\b", "weight": 0.12, "reason": "Fake receipt lure detected."},
    {"pattern": r"\bagent\b.*\b(mpesa|m-pesa)\b|\bpaybill\b|\btill\b", "weight": 0.12, "reason": "Agent/Paybill/Till instruction cues detected."},
    {"pattern": r"\b(verify|thibitisha)\b.*\baccount\b|\bupdate\b.*\baccount\b", "weight": 0.12, "reason": "Account verification/update request detected."},
]

def score_text_rules(text: str, rulepack: List[Dict]) -> float:
    total = 0.0
    for r in rulepack + GENERAL_RULEPACK:
        if re.search(r["pattern"], text, flags=re.IGNORECASE):
            total += float(r["weight"])
    return min(1.0, total / 0.9)

def find_rule_hits(text: str, rulepack: List[Dict]) -> List[Dict]:
    hits = []
    for r in rulepack:
        if re.search(r["pattern"], text, flags=re.IGNORECASE):
            hits.append(r)
    return hits
