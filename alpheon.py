#!/usr/bin/env python3
"""
Alpheon — remembers WHY your project is the way it is.

Proof of concept (v0.1). No account, no database, no cloud.
At the end of a coding session, Alpheon looks at what changed in your git repo
and generates a human-readable "Handoff Note" capturing what changed, WHY,
what was tried & rejected, and what's next — appended to HANDOFF.md.

The note is DRAFTED for you to review before it's saved (human-in-the-loop),
so bad/hallucinated reasoning never silently becomes "truth."

Usage:
    python alpheon.py                # summarize uncommitted changes in current repo
    python alpheon.py --since HEAD~1 # summarize changes since a given commit
    python alpheon.py --note "tried Redis, too heavy, used sqlite"  # add your own why

This PoC produces the STRUCTURE and captures your rationale. In the real product,
an LLM fills in the 'why' automatically by reading the diff + session transcript.
Here we keep it dependency-free and deterministic so it runs anywhere instantly.
"""
import argparse
import datetime
import subprocess
import sys
import os
import textwrap


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout.strip()
    except FileNotFoundError:
        return ""


def in_git_repo():
    return run(["git", "rev-parse", "--is-inside-work-tree"]) == "true"


def changed_files(since):
    if since:
        out = run(["git", "diff", "--name-status", since])
    else:
        # staged + unstaged
        out = run(["git", "diff", "--name-status", "HEAD"])
    files = []
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) >= 2:
            status, path = parts[0], parts[-1]
            label = {"A": "added", "M": "modified", "D": "deleted", "R": "renamed"}.get(status[0], "changed")
            files.append((label, path))
    return files


def diff_stat(since):
    if since:
        return run(["git", "diff", "--stat", since])
    return run(["git", "diff", "--stat", "HEAD"])


def recent_commits(n=3):
    return run(["git", "log", f"-{n}", "--pretty=format:- %s"])


def build_note(files, stat, commits, user_note):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    if files:
        changed = "\n".join(f"- **{label}**: `{path}`" for label, path in files)
    else:
        changed = "- (no uncommitted changes detected — run after editing, or use --since)"

    why = user_note.strip() if user_note else "_[review & fill in: WHY were these changes made? What problem did they solve?]_"
    rejected = "_[review & fill in: what did you try that DIDN'T work, so nobody repeats it?]_"
    nxt = "_[review & fill in: what's the next step / open question?]_"

    note = f"""
## Handoff Note — {now}

### What changed
{changed}

### Why
{why}

### What was tried & rejected
{rejected}

### What's next / open questions
{nxt}

<details><summary>Change details (auto)</summary>

Recent commits:
{commits or "- (none)"}

Diff stat:
```
{stat or "(none)"}
```
</details>

---
"""
    return note


def main():
    ap = argparse.ArgumentParser(description="Alpheon — remember the WHY.")
    ap.add_argument("--since", help="git ref to diff against (e.g. HEAD~1)", default=None)
    ap.add_argument("--note", help="your one-line 'why' for this session", default="")
    ap.add_argument("--yes", action="store_true", help="save without confirmation")
    args = ap.parse_args()

    if not in_git_repo():
        print("Alpheon: not inside a git repo. cd into your project first.")
        sys.exit(1)

    files = changed_files(args.since)
    stat = diff_stat(args.since)
    commits = recent_commits()
    note = build_note(files, stat, commits, args.note)

    print("=" * 60)
    print("ALPHEON — draft handoff note (review before saving):")
    print("=" * 60)
    print(note)

    if not args.yes:
        ans = input("Append this to HANDOFF.md? [y/N] ").strip().lower()
        if ans != "y":
            print("Discarded. Nothing saved.")
            return

    with open("HANDOFF.md", "a", encoding="utf-8") as f:
        if os.path.getsize("HANDOFF.md") == 0 if os.path.exists("HANDOFF.md") else True:
            pass
        f.write(note)
    print("Saved to HANDOFF.md ✔  The 'why' is now recoverable.")


if __name__ == "__main__":
    main()
