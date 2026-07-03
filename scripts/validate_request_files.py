#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, parse_qs

REQUIRED_FIELDS = ("GoogleScholar", "LinkedIn", "ORCID")

ORCID_RE = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")


def validate_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def validate_google_scholar(value: str) -> bool:
    if not validate_https_url(value):
        return False
    parsed = urlparse(value)
    if parsed.netloc not in {"scholar.google.com"}:
        return False
    if parsed.path != "/citations":
        return False
    qs = parse_qs(parsed.query)
    return bool(qs.get("user"))


def validate_linkedin(value: str) -> bool:
    if not validate_https_url(value):
        return False
    parsed = urlparse(value)
    if parsed.netloc not in {"www.linkedin.com", "linkedin.com"}:
        return False
    return parsed.path.startswith("/in/") or parsed.path.startswith("/pub/")


def validate_orcid(value: str) -> bool:
    if not validate_https_url(value):
        return False
    parsed = urlparse(value)
    if parsed.netloc not in {"orcid.org", "www.orcid.org"}:
        return False
    identifier = parsed.path.strip("/")
    return bool(ORCID_RE.fullmatch(identifier))


def parse_request_file(path: Path) -> list[str]:
    errors: list[str] = []
    lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]

    if len(lines) != len(REQUIRED_FIELDS):
        errors.append(
            f"must contain exactly {len(REQUIRED_FIELDS)} non-empty lines in the documented format"
        )

    fields: dict[str, str] = {}
    seen_names: list[str] = []

    for index, line in enumerate(lines, start=1):
        if ":" not in line:
            errors.append(f"line {index}: expected 'Field: value'")
            continue

        name, value = line.split(":", 1)
        name = name.strip()
        value = value.strip()
        seen_names.append(name)

        if name not in REQUIRED_FIELDS:
            errors.append(f"line {index}: unknown field '{name}'")
            continue
        if name in fields:
            errors.append(f"line {index}: duplicate field '{name}'")
            continue
        if not value:
            errors.append(f"line {index}: field '{name}' must not be empty")
            continue

        fields[name] = value

    if seen_names and tuple(seen_names) != REQUIRED_FIELDS:
        errors.append(
            "fields must appear exactly once and in this order: GoogleScholar, LinkedIn, ORCID"
        )

    for field in REQUIRED_FIELDS:
        if field not in fields:
            errors.append(f"missing field '{field}'")

    scholar = fields.get("GoogleScholar")
    if scholar and not validate_google_scholar(scholar):
        errors.append(
            "GoogleScholar must be an https://scholar.google.com/citations?user=... URL"
        )

    linkedin = fields.get("LinkedIn")
    if linkedin and not validate_linkedin(linkedin):
        errors.append(
            "LinkedIn must be an https://www.linkedin.com/in/... or https://www.linkedin.com/pub/... URL"
        )

    orcid = fields.get("ORCID")
    if orcid and not validate_orcid(orcid):
        errors.append(
            "ORCID must be an https://orcid.org/XXXX-XXXX-XXXX-XXXX URL with a valid 16-character identifier"
        )

    return errors


def iter_request_files(paths: list[str]) -> list[Path]:
    if paths:
        return [Path(path) for path in paths]
    return sorted(Path("requests").glob("*.txt"))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate reviewer registration request files under requests/."
    )
    parser.add_argument("paths", nargs="*", help="Specific request files to validate.")
    args = parser.parse_args()

    paths = iter_request_files(args.paths)
    if not paths:
        print("No request files found.", file=sys.stderr)
        return 1

    has_errors = False
    for path in paths:
        errors = parse_request_file(path)
        if not errors:
            print(f"OK: {path}")
            continue

        has_errors = True
        print(f"ERROR: {path}")
        for error in errors:
            print(f"  - {error}")

    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
