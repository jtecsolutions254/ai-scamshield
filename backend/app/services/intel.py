from __future__ import annotations
import re
from urllib.parse import urlparse
import httpx
import tldextract

from app.core.config import settings
from app.core.logging import logger
from app.utils.text_normalize import normalize_text
from app.utils.rulepacks import score_text_rules, KENYA_MPESA_RULEPACK
from app.utils.reputation import ReputationStore
from app.utils.url_features import (
    is_shortener_domain, looks_like_ip_host, suspicious_tld, count_dots,
    url_length, has_at_symbol, has_punycode, has_misleading_subdomain
)

URL_RE = re.compile(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', re.IGNORECASE)

class IntelLayer:
    def __init__(self):
        self.reputation = ReputationStore()

    def _extract_urls(self, text: str):
        urls = []
        for m in URL_RE.finditer(text or ""):
            u = m.group(0).strip().rstrip(").,;!")
            if u.lower().startswith("www."):
                u = "http://" + u
            urls.append(u)
        return list(dict.fromkeys(urls))

    def _domain_age_days(self, domain: str):
        try:
            with httpx.Client(timeout=settings.rdap_timeout_seconds) as client:
                r = client.get(f"https://rdap.org/domain/{domain}")
                if r.status_code != 200:
                    return None
                data = r.json()
                events = data.get("events", [])
                created = None
                for e in events:
                    if e.get("eventAction") in ("registration", "registered", "creation"):
                        created = e.get("eventDate")
                        break
                if not created:
                    return None
                from datetime import datetime, timezone
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                return max(0, int((now - dt).total_seconds() // 86400))
        except Exception as ex:
            logger.info(f"RDAP lookup failed for {domain}: {ex}")
            return None

    def inspect_text(self, text: str):
        clean = normalize_text(text)
        urls = self._extract_urls(text)

        h = score_text_rules(clean, rulepack=KENYA_MPESA_RULEPACK)

        shortener = False
        rep_hit = False
        domain_age = None
        notes = {}
        t = 0.0

        for u in urls[:3]:
            parsed = urlparse(u)
            host = parsed.hostname or ""
            ext = tldextract.extract(host)
            domain = ".".join([p for p in [ext.domain, ext.suffix] if p])
            if not domain:
                continue

            if is_shortener_domain(domain):
                shortener = True
                t += 0.25

            if self.reputation.is_bad_domain(domain) or self.reputation.is_bad_url(u):
                rep_hit = True
                t += 0.50

            if domain_age is None:
                domain_age = self._domain_age_days(domain)
                if domain_age is not None and domain_age < 30:
                    t += 0.25
                    notes["domain_age_reason"] = f"Domain looks newly registered ({domain_age} days)."

        t = min(1.0, t)
        return {
            "urls_found": urls,
            "shortener": shortener,
            "reputation_hit": rep_hit,
            "domain_age_days": domain_age,
            "redirects": [],
            "notes": notes,
            "heuristic_score": h,
            "intel_score": t,
        }

    def inspect_url(self, url: str):
        parsed = urlparse(url if url.startswith(("http://", "https://")) else "http://" + url)
        host = parsed.hostname or ""
        ext = tldextract.extract(host)
        domain = ".".join([p for p in [ext.domain, ext.suffix] if p])

        dotc = count_dots(host)
        length = url_length(url)

        score = 0.0
        if is_shortener_domain(domain):
            score += 0.25
        if looks_like_ip_host(host):
            score += 0.25
        if suspicious_tld(domain):
            score += 0.15
        if has_at_symbol(url):
            score += 0.15
        if has_punycode(host):
            score += 0.15
        if has_misleading_subdomain(host):
            score += 0.15
        if length >= 80:
            score += 0.15
        if dotc >= 4:
            score += 0.10
        score = min(1.0, score)

        rep_hit = False
        t = 0.0
        if domain and (self.reputation.is_bad_domain(domain) or self.reputation.is_bad_url(url)):
            rep_hit = True
            t += 0.6

        domain_age = None
        if domain:
            domain_age = self._domain_age_days(domain)
            if domain_age is not None and domain_age < 30:
                t += 0.25
        t = min(1.0, t)

        return {
            "shortener": is_shortener_domain(domain),
            "reputation_hit": rep_hit,
            "domain_age_days": domain_age,
            "url_length": length,
            "dot_count": dotc,
            "has_ip": looks_like_ip_host(host),
            "redirects": [],
            "notes": {"domain": domain, "host": host},
            "heuristic_score": score,
            "intel_score": t,
        }
