from __future__ import annotations
import re
from urllib.parse import urlparse
import tldextract

SHORTENERS = {
    "bit.ly", "t.co", "tinyurl.com", "goo.gl", "cutt.ly", "rb.gy", "is.gd", "ow.ly", "shorturl.at"
}
SUSPICIOUS_TLDS = {"zip", "mov", "top", "xyz", "click", "link", "info", "icu"}
IP_RE = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$")

def is_shortener_domain(domain: str) -> bool:
    return (domain or "").lower() in SHORTENERS

def looks_like_ip_host(host: str) -> bool:
    if not host:
        return False
    if IP_RE.match(host):
        parts = host.split(".")
        try:
            return all(0 <= int(p) <= 255 for p in parts)
        except ValueError:
            return False
    return False

def suspicious_tld(domain: str) -> bool:
    ext = tldextract.extract(domain or "")
    return (ext.suffix or "").lower() in SUSPICIOUS_TLDS

def count_dots(host: str) -> int:
    return (host or "").count(".")

def url_length(url: str) -> int:
    return len(url or "")

def has_at_symbol(url: str) -> bool:
    return "@" in (url or "")

def has_punycode(host: str) -> bool:
    h = host or ""
    return h.startswith("xn--") or "xn--" in h

def has_misleading_subdomain(host: str) -> bool:
    if not host:
        return False
    parts = host.split(".")
    if len(parts) < 3:
        return False
    brands = {"google", "microsoft", "paypal", "apple", "safaricom", "mpesa", "facebook"}
    ext = tldextract.extract(host)
    registrable = ".".join([p for p in [ext.domain, ext.suffix] if p]).lower()
    sub = ".".join(parts[:-2]).lower()
    return any(b in sub for b in brands) and registrable not in {f"{b}.com" for b in brands}

def url_to_features(url: str):
    u = url if url.startswith(("http://", "https://")) else "http://" + url
    p = urlparse(u)
    host = p.hostname or ""
    ext = tldextract.extract(host)
    domain = ".".join([x for x in [ext.domain, ext.suffix] if x])
    path = p.path or ""
    query = p.query or ""

    feats = [
        len(u),
        len(host),
        len(domain),
        len(path),
        len(query),
        host.count("."),
        int(is_shortener_domain(domain)),
        int(looks_like_ip_host(host)),
        int("https" == (p.scheme or "").lower()),
        int("@" in u),
        int(".." in u),
        int("=" in u),
        int("%" in u),
        int(has_punycode(host)),
        int(has_misleading_subdomain(host)),
        sum(ch.isdigit() for ch in u),
        sum(ch in "-_." for ch in u),
    ]
    return feats
