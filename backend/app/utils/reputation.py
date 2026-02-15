from pathlib import Path

class ReputationStore:
    def __init__(self):
        base = Path(__file__).resolve().parents[2]  # backend/app
        data_dir = base.parent / "data" / "reputation"
        self.bad_domains = set()
        self.bad_urls = set()
        domains_file = data_dir / "blocklist_domains.txt"
        urls_file = data_dir / "blocklist_urls.txt"

        if domains_file.exists():
            self.bad_domains = set([l.strip().lower() for l in domains_file.read_text().splitlines() if l.strip() and not l.startswith("#")])
        if urls_file.exists():
            self.bad_urls = set([l.strip() for l in urls_file.read_text().splitlines() if l.strip() and not l.startswith("#")])

    def is_bad_domain(self, domain: str) -> bool:
        return bool(domain) and domain.lower() in self.bad_domains

    def is_bad_url(self, url: str) -> bool:
        return bool(url) and url.strip() in self.bad_urls
