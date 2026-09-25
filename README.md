# University of Waterloo Computer Science PhDs

A static academic catalog of the 510 records in `phds.csv` (1965–2016).

## Files

- `index.html`: complete catalog, newest year first and surname order within each year.
- `phds/<year>/<full-name>.html`: individual records.
- `assets/css/style.css`: shared responsive styles.
- `assets/js/catalog.js`: browser search and year filtering.
- `phds.csv`: original source, preserved in Windows-1252 encoding.
- `scripts/generate.py`: optional maintenance script for refreshing the HTML.

Serve the repository root directly with GitHub Pages. All HTML is already present;
no build, package installation, server application, or deployment workflow is required.
Relative links support both repository project URLs and custom domains. You can
also open `index.html` directly in a browser.

Search matches words across graduate names, thesis titles, and all supervisors,
ignoring case and accents. The year filter combines with the search. Without
JavaScript, all entries, year navigation, and individual pages remain available.
The seven exception records are included and labeled exactly as in the source.

## Updating records

Edit `phds.csv`, then optionally run `python3 scripts/generate.py` to refresh the
checked-in HTML. This uses only Python's standard library and is not a hosting
build step. Commit the resulting HTML alongside the CSV changes.

The generator preserves source text, apart from collapsing whitespace (including
embedded line breaks). It does not repair source spelling or missing characters.
Page URLs are derived from year and full name; changing either changes the URL.
After renaming or removing a record, review obsolete pages explicitly before
removing them. Duplicate generated paths stop generation with an error.

For local HTTP preview, run `python3 -m http.server 8000` from this directory.
