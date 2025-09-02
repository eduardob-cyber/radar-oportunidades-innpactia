import os, csv, hashlib, json, datetime, pytz
import feedparser
from extractor import extract_dates, extract_emails

BASE_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUT_DIR, exist_ok=True)

def load_sources():
    path = os.path.join(BASE_DIR, "sources.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)["sources"]

def load_seen():
    path = os.path.join(BASE_DIR, "seen_urls.txt")
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_seen(seen):
    path = os.path.join(BASE_DIR, "seen_urls.txt")
    with open(path, "w", encoding="utf-8") as f:
        for url in sorted(seen):
            f.write(url + "\n")

def normalize_url(url):
    if not url:
        return ""
    return url.strip()

def process_rss(url):
    d = feedparser.parse(url)
    items = []
    for e in d.entries:
        link = normalize_url(getattr(e, "link", "")) or normalize_url(e.get("id", ""))
        title = getattr(e, "title", "").strip()
        summary = getattr(e, "summary", "") or getattr(e, "description", "")
        published = getattr(e, "published", "") or getattr(e, "updated", "")
        # try to extract possible deadlines/emails from summary
        dates = extract_dates(f"{title}\n{summary}")
        emails = extract_emails(f"{title}\n{summary}")
        items.append({
            "title": title,
            "link": link,
            "published": published,
            "summary": summary,
            "possible_deadlines": "; ".join(dates),
            "emails": "; ".join(set(emails)),
            "source_type": "rss",
            "source_url": url
        })
    return items

def main():
    tz = pytz.timezone("America/Bogota")
    today = datetime.datetime.now(tz).strftime("%Y%m%d")
    csv_path = os.path.join(OUT_DIR, f"convocatorias_{today}.csv")

    sources = load_sources()
    seen = load_seen()
    out_rows = []

    for s in sources:
        stype = s.get("type")
        url = s.get("url")
        if stype != "rss":
            print(f"Skipping non-RSS source for MVP: {s.get('name')}")
            continue
        try:
            items = process_rss(url)
            for it in items:
                url_key = it["link"] or (it["title"] + it["source_url"])
                if not url_key:
                    continue
                key = hashlib.sha1(url_key.encode("utf-8")).hexdigest()
                if key in seen:
                    continue
                seen.add(key)
                out_rows.append(it)
        except Exception as e:
            print(f"Error reading {url}: {e}")

    if out_rows:
        fieldnames = ["title","link","published","summary","possible_deadlines","emails","source_type","source_url"]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            for r in out_rows:
                w.writerow(r)
        print(f"Wrote {len(out_rows)} rows to {csv_path}")
    else:
        print("No new items today.")

    save_seen(seen)

if __name__ == "__main__":
    main()
