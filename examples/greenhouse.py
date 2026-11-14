# greenhouse.py — fetch one public Greenhouse board, print title/location/url
import json, urllib.request

COMPANY = "airbnb"  # any public Greenhouse board token
URL = f"https://boards-api.greenhouse.io/v1/boards/{COMPANY}/jobs?content=false"

def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "public-ats-job-feeds/1.0 (+contact)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))

def main():
    data = get_json(URL)
    for job in data.get("jobs", []):
        title = job.get("title", "").strip()
        location = (job.get("location") or {}).get("name", "")
        url = job.get("absolute_url", "")
        print(f"{title}\t{location}\t{url}")

if __name__ == "__main__":
    main()
