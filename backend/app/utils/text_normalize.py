import re

URL_RE = re.compile(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', re.IGNORECASE)
PHONE_RE = re.compile(r"(\+?\d[\d\s\-]{7,}\d)")
AMOUNT_RE = re.compile(r"(ksh\s?\d+[\d,\.]*|kes\s?\d+[\d,\.]*|\b\d+[\d,\.]*\s?(?:ksh|kes)\b)", re.IGNORECASE)
OTP_RE = re.compile(r"\b(otp|one[- ]time password|verification code|auth code)\b", re.IGNORECASE)

def normalize_text(text: str) -> str:
    if not text:
        return ""
    t = text.strip().lower()
    t = URL_RE.sub("<url>", t)
    t = PHONE_RE.sub("<phone>", t)
    t = AMOUNT_RE.sub("<amount>", t)
    t = OTP_RE.sub("<otp>", t)
    t = re.sub(r"\s+", " ", t)
    return t
