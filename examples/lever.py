# lever.py — fetch one public Lever board, print title/location/url
import json, urllib.request

COMPANY = "spotify"  # any public Lever board slug
URL = f"https://api.lever.co/v0/postings/{COMPANY}?mode=json"

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "public-ats-job-feeds/1.0 (+contact)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def main():
    data = get_json(URL)
    for job in data:
        title = job.get("text", "").strip()
        categories = job.get("categories") or {}
        location = categories.get("location", "")
        url = job.get("hostedUrl", "")
        print(f"{title}\t{location}\t{url}")

if __name__ == "__main__":
    main()
