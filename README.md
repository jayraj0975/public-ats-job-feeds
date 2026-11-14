# public-ats-job-feeds

A plain, practical guide to the **public, unauthenticated job-posting feeds** that many companies expose through their applicant tracking system (ATS) — the endpoints a company's own "Careers" page calls to render its open roles. No login, no API key, no applicant data. If a board is public, so is the JSON or XML behind it.

This repo is documentation and two small examples, not a scraper framework. It covers nine systems: Greenhouse, Lever, Ashby, Breezy, Personio, BambooHR, Teamtailor, Recruitee, and Workable. Every endpoint pattern below was called successfully against real public boards on 14 November 2026. Vendors change these feeds without notice, and nothing here is a promise of completeness, freshness or uptime.

**SmartRecruiters is deliberately excluded** from this guide. Its API `robots.txt` (`https://api.smartrecruiters.com/robots.txt`) said `User-agent: * / Disallow: /` as of 2026-11-14, so we do not document or hit it here. Do not add it back without checking the current policy or getting written permission.

## 1. What this is

Public job-board feeds are the read-only endpoints a company's careers page calls to list open roles: a JSON array of titles, locations, and apply links. They are open by design so that job aggregators and careers widgets can display them. This repo documents the endpoint shape for nine common ATS vendors, the fields each returns, what each is known to limit, and a minimal copy-paste example so you can fetch one board and look at it. It also points at a hosted, pay-per-result version for people who don't want to run code. Everything here is read-only and about **published job metadata** — no candidate records, no recruiter contacts, no forms.

## 2. Endpoint table

| System | Public endpoint pattern | Format | Fields you get (top level) | Known limits |
|---|---|---|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/{companyId}/jobs?content=false` | JSON | `id`, `title`, `location.name`, `absolute_url`, `updated_at`, `metadata` | `content=true` returns full HTML descriptions; keep it off for listings. `companyId` is the board token (letters, numbers, dots, underscores, hyphens). |
| Lever | `https://api.lever.co/v0/postings/{companyId}?mode=json` | JSON | `id`, `text` (title), `categories.location`, `categories.team`, `hostedUrl`, `createdAt`, `updatedAt` | `mode=json` is required; default HTML mode is not machine-friendly. Published crawl delay is about 1 request/sec (`https://api.lever.co/robots.txt`). |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/{companyId}` | JSON | `jobs[].id`, `title`, `location`, `department`, `team`, `employmentType`, `isRemote`, `publishedAt`, `jobUrl`, `applyUrl` | Response is `{apiVersion, jobs: [...]}`, not a bare array. Use the public board slug. Pay data only appears when the company publishes it. |
| Breezy | `https://{companyId}.breezy.hr/json` | JSON | `id`, `name` (title), `department`, `location`, `type`, `published_date`, `url` | Per-tenant subdomain; the `/json` suffix is the machine-readable variant of the careers page. |
| Personio | `https://{companyId}.jobs.personio.de/xml` (some tenants use `.com`) | XML | per position: id, name, office, department, employment type, creation date | XML only. Per-tenant subdomain. Text may contain non-ASCII characters: parse the raw bytes, not a decoded guess. |
| BambooHR | `https://{companyId}.bamboohr.com/careers/list` | JSON | `result[].id`, `jobOpeningName`, `departmentLabel`, `employmentStatusLabel`, `location`, `atsLocation` | Returned under a `result` key. Posting dates need the per-job detail call (`/careers/{id}/detail`). |
| Teamtailor | `https://{companyId}.teamtailor.com/jobs.rss` | RSS (XML) | `item.title`, `item.link`, `item.pubDate`, `item.description` | RSS feed; pagination and description length are tenant-set. `companyId` is a DNS-style label. |
| Recruitee | `https://{companyId}.recruitee.com/api/offers/` | JSON | `offers[].id`, `offers[].title`, `offers[].location`, `offers[].department`, `offers[].created_at`, `offers[].careers_url` | Per-tenant subdomain; wrapped in `offers[]`. Recruitee's own docs say unauthenticated Careers Site API calls will return HTTP 401 starting **10 February 2027** — verify before then. |
| Workable | `https://apply.workable.com/api/v1/widget/accounts/{companyId}` | JSON | `jobs[].shortcode`, `title`, `department`, `employment_type`, `location`, `published_on`, `url` | This is the feed behind Workable's embeddable careers widget. Large accounts return thousands of rows in one response. |

Fetch one board by hand and look at the response before you build on a row: vendors change these feeds without notice.

## 3. Two 25-line examples, no dependencies

Python 3 standard library only (`urllib`, `json`). Each example fetches one board and prints title, location, and application URL. Change `COMPANY` to any public board slug. Keep requests to about one per second.

```python
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
```

```python
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
```

Both scripts read only; neither logs in, stores cookies, or posts anything. If a board returns 404 or an empty array, that slug is not public — try another.

## 4. Rules of the road

- **Public data only.** Fetch only endpoints that a company's own careers page already calls. If it needs a login, a cookie, or an API key, it is not in scope.
- **No applicant data, ever.** These feeds list open roles. They do not touch candidate records, application forms, recruiter emails, phone numbers, or demographics. Don't enrich listings with any of that.
- **Be polite.** About one request per second per host. Read each host's `robots.txt` first. On HTTP 429 or 403, stop that provider, back off, and don't hammer retries.
- **Set an honest user agent** with a way to reach you; don't spoof a browser.
- **No circumventing controls.** No CAPTCHA solving, no auth bypass, no scraping behind WAFs.
- **SmartRecruiters is out of scope here** because its API `robots.txt` disallows generic automated access (`Disallow: /` for `User-agent: *` as of 2026-11-14). Add it only with a policy change or written permission.
- **Respect each vendor's terms.** If a vendor's terms say no automated collection, don't ship a script against it — email them instead.
- **Don't spam.** Job listings are not a contact list. Using this data to mass-email recruiters or post to social media violates the spirit and usually the letter of the terms.

## 5. Normalised schema

Deduplicate and unify across vendors using this shape. Field names are `snake_case` plain JSON. Any field a vendor does not expose is `null` — never invent it.

| Field | Type | Meaning |
|---|---|---|
| `source` | string | One of `greenhouse`, `lever`, `ashby`, `breezy`, `personio`, `bamboohr`, `teamtailor`, `recruitee`, `workable`. |
| `companyId` | string | Board slug or tenant subdomain as used in the URL (e.g. `airbnb`, `spotify`, `bunq`). |
| `jobId` | string | Vendor's own job ID for that board. Stable only within the board; combine with `source`+`companyId` for a global key. |
| `title` | string | Role title as published. |
| `department` | string \| null | Team or department, when exposed. |
| `location` | string \| null | Human-readable location; do not parse into structured fields unless the vendor already did. |
| `employmentType` | string \| null | Full-time / part-time / contract, when published. |
| `postedAt` | string \| null | ISO 8601 (UTC) posted date, only if the vendor exposes it. |
| `updatedAt` | string \| null | ISO 8601 (UTC) last-updated date, only if the vendor exposes it. |
| `applyUrl` | string | Public apply URL from the listing. Must be `https`. |

A minimal record:

```json
{
  "source": "greenhouse",
  "companyId": "airbnb",
  "jobId": "4129031",
  "title": "Software Engineer",
  "department": null,
  "location": "Remote - US",
  "employmentType": null,
  "postedAt": null,
  "updatedAt": "2026-11-10T18:22:00Z",
  "applyUrl": "https://boards.greenhouse.io/airbnb/jobs/4129031"
}
```

If you deduplicate, dedupe on `source` + `companyId` + `jobId`, not on title (two openings share a title all the time).

## 6. Don't want to run it yourself?

If wiring nine vendors for one-off pulls is not worth your afternoon, there are hosted, pay-per-result actors on the Apify Store by **jayraj0975**:

| Actor | Link |
|---|---|
| Greenhouse jobs | https://apify.com/jayraj0975/greenhouse-jobs |
| Lever jobs | https://apify.com/jayraj0975/lever-jobs |
| More | https://apify.com/jayraj0975 |

Pricing is about **$1 per 1,000 results** (pay-per-event; only deduplicated rows written to the dataset count). There is no tie-in here — the examples in section 3 remain the zero-cost path and are enough to get started.

## 7. Seed list note

The file `data/seed_slugs.json` carries a **906-board verified list** first built on **2026-11-14**: 300 Greenhouse, 300 Lever, 300 Ashby boards that had at least one public job on that date, plus 2 each for Teamtailor, Recruitee, and Workable; 0 for SmartRecruiters. Boards were deduplicated and live-checked with one request per candidate under an honest user agent; Greenhouse and Ashby were paced at ≤2 req/s, Lever at ≤1 req/s to honour its published crawl delay. The list is a **discovery aid, not a census**, and will age as boards open, close, renames, or move. It is built from these sources — credit them exactly as they appear in `data/SOURCES.md`:

- **Open Jobs board registry** — https://github.com/elliottdehn/open-jobs — Licence: [CC0 1.0 Universal](https://raw.githubusercontent.com/elliottdehn/open-jobs/main/LICENSE). Used for Greenhouse, Lever, and Ashby fallback candidates. Provider arrays normalized, deduplicated, filtered through live checks.
- **moonie0201 ATS Directory** (pinned commit `055911218e6e359ef8600f2cd875932dfdfbd90b`) — https://github.com/moonie0201/ats-directory — Licence: [CC0 1.0 Universal](https://github.com/moonie0201/ats-directory/blob/055911218e6e359ef8600f2cd875932dfdfbd90b/LICENSE). Used for `status == "ok"` Greenhouse and global Lever candidates.
- **Deriverge companies using Ashby** — https://deriverge.com/tools/companies-using-ashby/ (data: https://deriverge.com/tools/data/ats/ashby.json), publisher deriverge s.r.o. — Licence: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/). Used for Ashby candidates with open jobs; filtered, normalized, deduplicated, and independently live-checked. This attribution and change notice are provided under CC BY 4.0; no endorsement is implied.

SmartRecruiters has zero entries because its API `robots.txt` disallowed generic automated access on the verification date. No SmartRecruiters request was made. See `data/SOURCES.md` for the exact licence text, verification table, and coverage limits.

## 8. Licence

Code in this repository is released under the **MIT Licence** (see `LICENSE`). The seed data carries the upstream licences listed in section 7; redistributing the seed requires preserving those notices exactly. No licence is granted for any vendor endpoint — those remain governed by each vendor's terms and `robots.txt`.
