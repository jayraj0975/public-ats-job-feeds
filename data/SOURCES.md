# Seed-list sources and verification

The bundled file is a **partial discovery aid**, not a complete list of ATS
customers. Candidate identifiers were deduplicated and independently checked
on **2026-11-14**. A board was retained only when one request to the vendor's
public job-list endpoint returned a valid response with at least one listed
job. No endorsement by any source publisher, ATS vendor, or employer is
implied.

## Candidate lists used

### Open Jobs board registry

- Data: <https://raw.githubusercontent.com/elliottdehn/open-jobs/main/backend/src/boards.json>
- Repository: <https://github.com/elliottdehn/open-jobs>
- Licence: [CC0 1.0 Universal](https://raw.githubusercontent.com/elliottdehn/open-jobs/main/LICENSE)
- Use here: Greenhouse, Lever, and Ashby fallback candidates; SmartRecruiters
  candidates were counted but not verified or included.
- Changes: provider arrays were normalized, deduplicated, and filtered through
  the live checks described below.

### moonie0201 ATS Directory

- Data (pinned commit): <https://raw.githubusercontent.com/moonie0201/ats-directory/055911218e6e359ef8600f2cd875932dfdfbd90b/companies.jsonl>
- Repository/methodology: <https://github.com/moonie0201/ats-directory/tree/055911218e6e359ef8600f2cd875932dfdfbd90b>
- Licence: [CC0 1.0 Universal](https://github.com/moonie0201/ats-directory/blob/055911218e6e359ef8600f2cd875932dfdfbd90b/LICENSE)
- Use here: `status == "ok"` Greenhouse and global Lever candidates were
  prioritized before the Open Jobs candidates.
- Changes: non-matching providers/statuses and non-global Lever regions were
  excluded, then identifiers were deduplicated and live-checked.

### Deriverge companies using Ashby

- Human-readable list: <https://deriverge.com/tools/companies-using-ashby/>
- Data: <https://deriverge.com/tools/data/ats/ashby.json>
- Publisher: deriverge s.r.o.
- Licence: [Creative Commons Attribution 4.0](https://creativecommons.org/licenses/by/4.0/)
- Use here: Ashby candidates whose published snapshot reported open jobs were
  prioritized before Open Jobs candidates.
- Changes: the list was filtered, normalized, deduplicated, and independently
  live-checked. This attribution and change notice are provided under CC BY
  4.0; no endorsement is implied.

All three source files were accessed on 2026-11-14. Their publishers describe
them as public registries or downloads, and the licences above permit reuse.
Candidate-list acquisition used one request per file.

## Live verification

The original four-source verifier used an honest
`Infinityore-ATS-Seed-Verifier/1.0` user agent, disabled retries, made one
request per candidate, and was configured to stop a provider immediately on
HTTP 403 or 429. Greenhouse and Ashby were paced at no more than two requests
per second. Lever was paced at no more than one request per second to follow
its published robots crawl delay. The six later Teamtailor, Recruitee, and
Workable checks used `infinityore-public-feed-probe/0.1`, one request per
explicitly identified board, after each provider's robots policy was checked.

| ATS | Verification endpoint | Candidate count | Requests | Retained |
|---|---|---:|---:|---:|
| Greenhouse | `boards-api.greenhouse.io/v1/boards/{slug}/jobs` | 8,185 | 320 | 300 |
| Lever | `api.lever.co/v0/postings/{slug}` | 3,611 | 340 | 300 |
| Ashby | `api.ashbyhq.com/posting-api/job-board/{slug}` | 3,890 | 432 | 300 |
| SmartRecruiters | Not requested | 1,510 | 0 | 0 |
| Teamtailor | `{slug}.teamtailor.com/jobs.rss` | 2 | 2 | 2 |
| Recruitee | `{slug}.recruitee.com/api/offers/` | 2 | 2 | 2 |
| Workable | `apply.workable.com/api/v1/widget/accounts/{slug}` | 2 | 2 | 2 |

There were **1,098 live board-verification requests** and three candidate-file
downloads in the build run. No provider returned a terminal 403 or 429.

SmartRecruiters has no bundled entries. On the verification date,
<https://api.smartrecruiters.com/robots.txt> said `User-agent: *` and
`Disallow: /` (apart from a named crawler rule). The verifier therefore made
no SmartRecruiters API requests. A future refresh may add verified entries if
the policy changes or the vendor provides written permission or a suitable
public export.

Official endpoint documentation and policy references:

- Greenhouse Job Board API: <https://docs.greenhouse.io/job-board.html>
- Greenhouse API robots: <https://boards-api.greenhouse.io/robots.txt>
- Lever Postings API: <https://github.com/lever/postings-api/blob/master/README.md>
- Lever API robots: <https://api.lever.co/robots.txt>
- Ashby public job posting API: <https://developers.ashbyhq.com/docs/public-job-posting-api>
- Ashby hosted-board robots: <https://jobs.ashbyhq.com/robots.txt>
- SmartRecruiters API robots: <https://api.smartrecruiters.com/robots.txt>
- Teamtailor RSS guide: <https://support.teamtailor.com/en/articles/11171756-rss-feed-how-to-guide>
- Recruitee offers endpoint: <https://docs.recruitee.com/reference/offers>
- Workable public widget feed: `https://apply.workable.com/api/v1/widget/accounts/{slug}`

## Coverage limits

The seed covers 23,086 boards that had at least one public job on the verification
date. It can miss private, unlisted, newly created, renamed, undiscovered, or
recently reactivated boards, and any included board can later become empty or
move. It is not a customer census and freshness is not guaranteed after the
date above.
