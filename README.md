# Software Engineering Reviewer Registry

A public registry of researchers volunteering to review for top software engineering journals.

## Why a Registry?

Journal editors spend significant time finding qualified reviewers. This registry lets researchers proactively signal availability and expertise, making it easier for editors to find suitable reviewers for submissions.

Registered reviewers may be contacted by editors of participating journals when a submission matches their expertise.

---

## Participating Journals

- IEEE Transactions on Software Engineering (TSE)
- ACM Transactions on Software Engineering and Methodology (TOSEM)
- Empirical Software Engineering (EMSE)
- Journal of Systems and Software (JSS)
- Information and Software Technology (IST)

---

## Registration Requirements

Three profile links are mandatory. All three must be present and valid before a registration is accepted.

### Google Scholar Profile

**What is needed:** A link to your Google Scholar profile.

**Why:** Google Scholar provides a verifiable publication record. It lets editors assess your research output, citation impact, and topical expertise at a glance.

### LinkedIn Profile

**What is needed:** A link to your LinkedIn profile.

**Why:** LinkedIn provides professional identity context — institutional affiliation, career history, and (optionally) identity verification. It supplements the academic record from Google Scholar.

### ORCID Profile

**What is needed:** A link to your ORCID profile (`https://orcid.org/XXXX-XXXX-XXXX-XXXX`).

**Why:** ORCID is the standard persistent researcher identifier used by journals and publishers. It is required to unambiguously identify you across name changes and institutional moves.

---

## How to Register

**Submit a pull request** — do not send requests by email. All registrations are handled publicly via pull requests for transparency.

To register, open a pull request that adds exactly one new `.txt` file under `requests/`. Name the file after yourself, e.g. `jane-doe.txt`.

Use this exact three-line format:

```text
GoogleScholar: https://scholar.google.com/citations?user=XXXXXXXXXXXXXXX
LinkedIn: https://www.linkedin.com/in/your-profile
ORCID: https://orcid.org/0000-0000-0000-0000
```

Rules:

1. The file must contain exactly these three fields, in this order: `GoogleScholar`, `LinkedIn`, `ORCID`.
2. Each field must appear exactly once, on a single line, as `Field: value`.
3. `GoogleScholar` must be an `https://scholar.google.com/citations?user=...` URL.
4. `LinkedIn` must be an `https://www.linkedin.com/in/...` or `https://www.linkedin.com/pub/...` URL.
5. `ORCID` must be an `https://orcid.org/` URL with a valid 16-digit identifier in `XXXX-XXXX-XXXX-XXXX` format.

An automated check runs on every pull request to validate the format. Fix any reported errors before the PR can be merged.
