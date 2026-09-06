"""Tightened audit: only real, high-confidence credential tokens in tracked files."""

from __future__ import annotations

import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Strict full-token patterns (prefix + enough entropy to avoid binary byte noise).
PATTERNS = [
    ("github_pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("ghp_token", re.compile(r"ghp_[A-Za-z0-9]{30,}")),
    ("threads_token", re.compile(r"THAA[A-Za-z0-9_]{40,}")),
    ("instagram_token", re.compile(r"IGAA[A-Za-z0-9_]{40,}")),
    ("composio_key", re.compile(r"ck_[A-Za-z0-9_]{30,}")),
    ("notion", re.compile(r"\b(?:secret|ntn)_[A-Za-z0-9]{30,}\b")),
]

proc = subprocess.run(["git", "ls-files"], cwd=ROOT, text=True, capture_output=True, check=True)
findings = []
for rel in proc.stdout.splitlines():
    path = ROOT / rel
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        continue
    for line_no, line in enumerate(text.splitlines(), start=1):
        for label, pattern in PATTERNS:
            if pattern.search(line):
                findings.append({"path": rel, "line": line_no, "type": label})

if not findings:
    print("CLEAN: no high-confidence credential tokens in tracked files.")
else:
    print("HIGH-CONFIDENCE credential tokens found in tracked files:")
    for item in findings:
        print(f"- {item['path']}:{item['line']} [{item['type']}]")
