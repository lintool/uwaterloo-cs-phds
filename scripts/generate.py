"""Refresh the checked-in static catalog from phds.csv (Python standard library)."""

import csv
import re
import unicodedata
from collections import defaultdict
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TITLE = "University of Waterloo Computer Science PhDs"


def html_page(title, description, content, prefix="", script=False):
    page = f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <link rel="stylesheet" href="{prefix}assets/css/style.css">
  {f'<script src="{prefix}assets/js/catalog.js" defer></script>' if script else ''}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  {content}
  <footer><p>Source: <a href="{prefix}phds.csv">PhD records (CSV)</a>. Coverage reflects the supplied records.</p></footer>
</body>
</html>
'''
    return "\n".join(line.rstrip() for line in page.splitlines()) + "\n"


def slug(name):
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")


def label(row):
    return f'<p class="exception">{escape(row["exceptions"])}</p>' if row["exceptions"] else ""


def main():
    # The source uses Windows-1252, including accented names and punctuation.
    with (ROOT / "phds.csv").open(encoding="cp1252", newline="") as source:
        rows = [{key: " ".join(value.split()) for key, value in row.items()}
                for row in csv.DictReader(source)]
    rows.sort(key=lambda r: (-int(r["year"]), r["surname"].casefold(), r["full name"].casefold()))
    groups = defaultdict(list)
    paths = set()
    for row in rows:
        year, name = row["year"], row["full name"]
        path = f'phds/{year}/{slug(name)}.html'
        if path in paths:
            raise ValueError(f"Duplicate page path: {path}")
        paths.add(path)
        supervisors = [row[key] for key in ("supervisor", "co-supervisor", "co-supervisor2", "co-supervisor3") if row[key]]
        groups[year].append(f'''<li class="entry">
  <h3><a href="{path}">{escape(name)}</a></h3>
  <p class="thesis">{escape(row['thesis title'])}</p>
  <p class="supervisors">{'Supervisor' if len(supervisors) == 1 else 'Supervisors'}: {escape('; '.join(supervisors))}</p>
  {label(row)}
</li>''')
        fields = [("Year", year), ("Academic unit", row["unit"]), ("Surname", row["surname"]),
                  ("Supervisor", row["supervisor"])]
        fields.extend(("Co-supervisor", row[key]) for key in ("co-supervisor", "co-supervisor2", "co-supervisor3") if row[key])
        if row["exceptions"]:
            fields.append(("Exception", row["exceptions"]))
        details = "\n".join(f'<div><dt>{escape(key)}</dt><dd>{escape(value)}</dd></div>' for key, value in fields)
        content = f'''<header class="detail-header"><a href="../../index.html">{TITLE}</a></header>
<main id="main" class="detail" tabindex="-1">
  <p class="back"><a href="../../index.html#year-{year}">Back to the {year} catalog</a></p>
  <p class="eyebrow">PhD · {year}</p>
  <h1>{escape(name)}</h1>
  <h2 class="detail-thesis">{escape(row['thesis title'])}</h2>
  <dl>{details}</dl>
</main>'''
        destination = ROOT / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(html_page(f"{name} ({year}) | {TITLE}", row["thesis title"], content, "../../"), encoding="utf-8")
    years = list(groups)
    options = "\n".join(f'<option value="{year}">{year}</option>' for year in years)
    navigation = "\n".join(f'<a href="#year-{year}" data-year="{year}">{year}</a>' for year in years)
    sections = "\n".join(f'''<section class="year-group" data-year="{year}" aria-labelledby="year-{year}">
  <h2 id="year-{year}">{year} <span class="year-count">({len(entries)})</span></h2>
  <ul class="entries">{''.join(entries)}</ul>
</section>''' for year, entries in groups.items())
    content = f'''<header class="catalog-header">
  <h1>{TITLE}</h1>
  <p>{len(rows)} PhD records · {years[-1]}–{years[0]}</p>
</header>
<main id="main" tabindex="-1">
  <form id="filters" class="filters" role="search" hidden>
    <div class="search-field"><label for="query">Search the catalog</label>
      <input id="query" type="search" placeholder="Name, thesis title, or supervisor" autocomplete="off"></div>
    <div><label for="year">Year</label><select id="year"><option value="">All years</option>{options}</select></div>
    <button type="reset">Clear filters</button>
  </form>
  <noscript><p>All records are shown below. Enable JavaScript to search and filter.</p></noscript>
  <p id="result-count" class="result-count" role="status" aria-live="polite">Showing all {len(rows)} records</p>
  <div class="catalog-layout">
    <nav class="year-nav" aria-label="Browse by year"><h2>Browse by year</h2><div>{navigation}</div></nav>
    <div class="results">{sections}<p id="empty-state" hidden>No records match your search. Try another name, title, or year.</p></div>
  </div>
</main>'''
    (ROOT / "index.html").write_text(html_page(TITLE, f"Browse {len(rows)} University of Waterloo PhD records from {years[-1]} to {years[0]} by year, graduate, thesis, or supervisor.", content, script=True), encoding="utf-8")
    print(f"Wrote index.html and {len(rows)} individual pages.")


if __name__ == "__main__":
    main()
