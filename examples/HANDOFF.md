# Example HANDOFF.md

This is a sample of what a real `HANDOFF.md` looks like after a few Alpheon sessions on a project. Notes are appended in order, newest at the bottom, so the file becomes a running log of *why* the project looks the way it does.

## Handoff Note — 2026-07-10 09:12

### What changed
- **added**: `auth/session.py`
- **added**: `auth/tokens.py`
- **modified**: `app.py`

### Why
Needed real session handling before adding any user-facing features. Started
with signed cookies instead of server-side sessions to avoid adding a session
store this early — fewer moving parts while the user model is still changing.

### What was tried & rejected
Looked at using JWTs in localStorage first. Rejected — no clean way to revoke
a token before expiry, and this app needs "log out everywhere" from day one.

### What's next / open questions
Token rotation isn't implemented yet. Need to decide refresh-token lifetime
before this goes anywhere near production.

<details><summary>Change details (auto)</summary>

Recent commits:
- add signed-cookie session handling
- wip: evaluate JWT vs server session
- scaffold auth module

Diff stat:
```
 app.py             |  18 +++++++++---------
 auth/session.py     |  64 ++++++++++++++++++++++++++++++++++++++++++++++++++++
 auth/tokens.py       |  37 +++++++++++++++++++++++++++++++++
 3 files changed, 106 insertions(+), 9 deletions(-)
```
</details>

---

## Handoff Note — 2026-07-14 22:41

### What changed
- **modified**: `cache.py`
- **added**: `cache_sqlite.py`
- **deleted**: `cache_memory.py`

### Why
Needed the cache to survive process restarts — the in-memory dict was losing
all entries on every deploy, causing a cold-cache stampede. Sqlite gives us
persistence with zero infra to run.

### What was tried & rejected
Tried Redis first. Worked, but added a whole service to deploy, monitor, and
pay for just to cache ~50MB of data. Way too heavy for what we actually need.
Dropped it in favor of a single sqlite file that ships with the app.

### What's next / open questions
Need a TTL/eviction policy — right now the sqlite file just grows. Also
should benchmark read latency under load before trusting this in prod.

<details><summary>Change details (auto)</summary>

Recent commits:
- switch cache backend to sqlite
- wip: try redis for persistent cache
- add cache invalidation tests

Diff stat:
```
 cache.py           | 42 ++++++++++++++++++------------------
 cache_sqlite.py     | 58 +++++++++++++++++++++++++++++++++++++++++++++++++++
 cache_memory.py      | 31 -------------------------------
 3 files changed, 85 insertions(+), 46 deletions(-)
```
</details>

---

## Handoff Note — 2026-07-15 16:03

### What changed
- **modified**: `worker.py`
- **modified**: `requirements.txt`

### Why
Background jobs were occasionally running twice under load — two workers
picking up the same row before either marked it as claimed. Added a
`SELECT ... FOR UPDATE SKIP LOCKED` query instead of the old
"read-then-update" pattern to close the race.

### What was tried & rejected
First tried adding a Python-level lock (`threading.Lock`). Doesn't help —
the workers run as separate processes, so the lock wasn't shared and the
race was still there. Needed the fix at the database level, not the app level.

### What's next / open questions
Haven't load-tested this past 4 concurrent workers. Should confirm it holds
at the concurrency level we actually expect in production before relying on it.

<details><summary>Change details (auto)</summary>

Recent commits:
- fix double-processing race with SKIP LOCKED
- wip: try threading.Lock (reverted, doesn't work across processes)
- add worker concurrency test

Diff stat:
```
 worker.py          | 21 +++++++++++----------
 requirements.txt    |  1 +
 2 files changed, 12 insertions(+), 10 deletions(-)
```
</details>

---
